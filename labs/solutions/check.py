# /// script
# requires-python = ">=3.11"
# dependencies = ["openpyxl>=3.1"]
# ///
"""Run the reference solution of every lab against the course files and check what it finds.

    uv run labs/solutions/check.py              # every lab
    uv run labs/solutions/check.py 1.2 2.4      # some labs
    uv run labs/solutions/check.py demo         # the parallel examples the slides use before each lab

What runs for real: every computation on the files (baseline, coverage, stale articles, personal data, permissions,
the retrieval of the prototype, the grading, the intervals, the costs, break-even and sensitivity). What runs
against a stand-in: the drafting step of the prototype, done by an extractive answerer (labs/spike/jawab.py)
because no model key is used here. The steps a participant writes in words (a decision question, a risk level,
a recommendation) have their reference answers in the lab pages' trainer blocks and in answer_key.md.
Nothing is written to disk.
"""
from __future__ import annotations

import csv
import math
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
LABS = HERE.parent
FILES = LABS / "files"
sys.path.insert(0, str(LABS / "spike"))
sys.path.insert(0, str(HERE))
import jawab as J  # noqa: E402
import costmodel as CM  # noqa: E402

KB_CATEGORIES = ["renew_licence", "new_licence", "minor_works", "signage", "waste", "payments", "parks", "violations"]
STALE = ["A01", "A09", "A14", "A18", "A26"]
ADAPTED = {"label": "adapted", "exclude_articles": STALE + ["A11"], "respect_permissions": True,
           "chunking": "paragraph", "min_score": 0.25}
THRESHOLD = {"accuracy": 0.80, "lower_bound": 0.65, "leaks": 0}
LABS_RUN = {}


def lab(lab_id):
    def wrap(fn):
        LABS_RUN[lab_id] = fn
        return fn
    return wrap


def read(path: Path) -> list[dict]:
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def pct(values: list[float], p: float) -> float:
    v = sorted(values)
    k = (len(v) - 1) * p / 100
    f = math.floor(k)
    c = min(f + 1, len(v) - 1)
    return v[f] + (v[c] - v[f]) * (k - f)


def dedupe(rows: list[dict], key: str) -> list[dict]:
    seen, out = set(), []
    for r in rows:
        if r[key] not in seen:
            seen.add(r[key])
            out.append(r)
    return out


def ok(cond, msg):
    if not cond:
        raise AssertionError(msg)


# ------------------------------------------------------------------ day 1


@lab("1.1")
def lab_1_1():
    memo = (FILES / "request_memo.txt").read_text(encoding="utf-8")
    notes = (FILES / "interview_notes.txt").read_text(encoding="utf-8")
    dictionary = (FILES / "data_dictionary.txt").read_text(encoding="utf-8")
    ok("روبوت محادثة" in memo and "لجنة التوجيه" in memo, "the memo names the solution and the committee")
    ok("24 شهرًا" in notes, "the finance rule is in the interviews")
    measures = {
        "حجم الاستفسارات لكل فئة": "category, received_date",
        "زمن المعالجة": "handling_minutes, status",
        "نسبة الخطأ": "qa_sample_type, qa_result",
        "تكرار التواصل": "repeat_within_7d",
        "زمن أول رد": "first_response_hours",
        "رضا السكان": "غير متاح في السجل",
    }
    for m, f in measures.items():
        for field in [x.strip() for x in f.split(",") if x.strip().isascii()]:
            ok(field in dictionary, f"{field} is in the data dictionary")
    print("decision: whether to fund an AI drafting assistant for written enquiries, which option, at what cost, "
          "decided by the steering committee at its next meeting; owner: the deputy CEO for resident services")
    print("measures and fields:", "; ".join(f"{m}: {f}" for m, f in measures.items()))


def baseline_rows():
    raw = read(FILES / "enquiries.csv")
    clean = dedupe(raw, "enquiry_id")
    return raw, clean


@lab("1.2")
def lab_1_2():
    raw, clean = baseline_rows()
    print(f"rows {len(raw)}, after removing duplicates {len(clean)} ({len(raw) - len(clean)} duplicates)")
    closed = [float(r["handling_minutes"]) for r in clean if r["status"] == "closed"]
    allm = [float(r["handling_minutes"]) for r in clean]
    auto = sum(r["status"] == "auto_closed" for r in clean)
    print(f"auto-closed {auto}; handling minutes, closed only: median {statistics.median(closed):.1f}, "
          f"p90 {pct(closed, 90):.1f}, mean {statistics.mean(closed):.2f}; with auto-closed: mean {statistics.mean(allm):.2f}")
    rnd = [r for r in clean if r["qa_sample_type"] == "random"]
    tgt = [r for r in clean if r["qa_sample_type"] == "targeted"]
    err = lambda rs: sum(r["qa_result"] != "correct" for r in rs) / len(rs)
    print(f"QA error rate: random sample {err(rnd):.3f} (n={len(rnd)}), targeted sample {err(tgt):.3f} (n={len(tgt)}), "
          f"both mixed {err(rnd + tgt):.3f}")
    lo, hi = J.wilson(sum(r["qa_result"] != "correct" for r in rnd), len(rnd))
    print(f"  random-sample error rate 95% interval {lo:.3f} to {hi:.3f}")
    print(f"repeat contact within 7 days: {sum(r['repeat_within_7d'] == 'yes' for r in clean) / len(clean):.3f}")
    ref = {r["category"]: r for r in read(FILES / "baseline_reference.csv")}
    by = defaultdict(list)
    for r in clean:
        by[r["category"]].append(r)
    total = len(clean)
    for cat in sorted(by, key=lambda c: -len(by[c])):
        rs = by[cat]
        mins = [float(r["handling_minutes"]) for r in rs if r["status"] == "closed"]
        monthly = len(rs) / 91 * 30.4
        med, p90 = statistics.median(mins), pct(mins, 90)
        ok(round(monthly) == int(ref[cat]["monthly_volume"]), f"{cat} monthly volume")
        ok(abs(med - float(ref[cat]["median_handling_min"])) < 0.051, f"{cat} median")
        ok(abs(p90 - float(ref[cat]["p90_handling_min"])) < 0.051, f"{cat} p90")
        print(f"  {cat:20s} share {len(rs) / total:5.1%} monthly {monthly:6.0f} median {med:5.1f} p90 {p90:5.1f}")
    ok(len(raw) - len(clean) > 0 and auto > 0, "the planted duplicates and auto-closed rows are there")
    ok(err(tgt) > 2 * err(rnd), "the targeted sample inflates the error rate")


@lab("1.3")
def lab_1_3():
    ref = read(FILES / "baseline_reference.csv")
    costs = {r[0]: r[1] for r in _xlsx_rows(FILES / "staff_costs.xlsx")}
    per_min = costs["التكلفة السنوية المحمَّلة للموظف"] / (costs["ساعات العمل المنتجة للموظف في السنة"] * 60)
    scope = [r for r in ref if r["kb_category"] == "yes"]
    annual = sum(int(r["enquiries_91_days"]) for r in scope) / 91 * 365
    minutes = sum(int(r["enquiries_91_days"]) * float(r["mean_handling_min"]) for r in scope) / 91 * 365
    ceiling = minutes * per_min
    print(f"cost per minute {per_min:.4f} SAR; in-scope enquiries a year {annual:,.0f}; "
          f"handling minutes a year {minutes:,.0f}")
    print(f"value ceiling (all handling time of in-scope enquiries) {ceiling:,.0f} SAR a year; "
          f"at a 30% cut {0.3 * ceiling:,.0f} SAR a year")
    share = sum(int(r["enquiries_91_days"]) for r in scope) / sum(int(r["enquiries_91_days"]) for r in ref)
    print(f"in-scope share of demand {share:.1%}")
    print("reference threshold: accuracy at least 80%, the lower bound of its 95% interval at least 65%, "
          "no permission leak; stop if the lower bound is still under 50% after one adaptation round or a leak cannot be closed by settings")
    ok(abs(per_min - 2.1429) < 0.001, "cost per minute")


def _xlsx_rows(path):
    from openpyxl import load_workbook
    ws = load_workbook(path).worksheets[0]
    return [r for r in ws.iter_rows(min_row=2, values_only=True) if r[0]]


@lab("1.4")
def lab_1_4():
    _, clean = baseline_rows()
    index = read(FILES / "kb_index.csv")
    demand = Counter(r["category"] for r in clean)
    covered = sum(demand[c] for c in KB_CATEGORIES) / len(clean)
    print(f"demand in categories the articles answer: {covered:.1%}; not covered: "
          + ", ".join(f"{c} {demand[c] / len(clean):.1%}" for c in ("excavation", "street_vending", "complaint_followup", "other")))
    en = sum(r["has_en"] == "yes" for r in index)
    en_cov = Counter(r["category"] for r in index if r["has_en"] == "yes" and r["collection"] == "kb_public")
    print(f"articles with an English version: {en} of {len(index)}")
    # stale: an article that states a fee the circular A48 has changed
    circ = (FILES / "kb" / "A48.txt").read_text(encoding="utf-8").split("## en")[0]
    keys = {"تجديد رخصة النشاط التجاري": None, "رخصة الترميم": None, "اللوحة الإعلانية": None, "حاوية النفايات": None,
            "قاعة الحديقة": None}
    for line in circ.splitlines():
        for k in keys:
            if k in line:
                keys[k] = re.search(r"(\d[\d,]*) ريال", line).group(1)
    stale = []
    for r in index:
        if r["article_id"] == "A48":
            continue
        text = (FILES / "kb" / f"{r['article_id']}.txt").read_text(encoding="utf-8").split("## en")[0]
        for k, new in keys.items():
            m = re.search(r"(\d[\d,]*) ريال", text)
            if k in text and m and ("رسوم" in text or "إيجار" in text) and m.group(1) != new and "غرامة" not in text:
                stale.append(r["article_id"])
    print("stale fee articles:", stale)
    ok(sorted(set(stale)) == STALE, f"stale articles {stale}")
    vendor = [r["article_id"] for r in index if r["source"] == "vendor"]
    print("vendor-pack articles (licence inside the vendor's platform only):", vendor)
    print("conflict: A11 (10 business days, reviewed 2024-09-30) against A12 (5 business days, reviewed 2026-04-18)")
    print("reference scores: coverage 1, quality 0 (blocking until the fees are fixed), rights of use 1")


# ------------------------------------------------------------------ day 2


@lab("2.1")
def lab_2_1():
    pd = Counter()
    files = sorted((FILES / "case_files").glob("C*.txt"))
    per_file = {}
    for f in files:
        t = f.read_text(encoding="utf-8")
        found = {
            "national_id": len(re.findall(r"\b1\d{9}\b", t)),
            "mobile": len(re.findall(r"\b05\d{8}\b", t)),
            "iban": len(re.findall(r"\bSA\d{22}\b", t)),
            "health": int(bool(re.search(r"إعاقة|علاج|المستشفى", t))),
            "child": int(bool(re.search(r"\(\d{1,2} سنة\)", t))),
        }
        pd.update(found)
        per_file[f.stem] = found
    print(f"case files {len(files)}: national IDs {pd['national_id']}, mobiles {pd['mobile']}, IBANs {pd['iban']}, "
          f"health data in {pd['health']} files, a child's data in {pd['child']} file(s)")
    print("sensitive data (health):", [k for k, v in per_file.items() if v["health"]],
          "child:", [k for k, v in per_file.items() if v["child"]], "bank:", [k for k, v in per_file.items() if v["iban"]])
    access = J.load_access("enquiries")
    extra = sorted(access["svc-jawab"] - access["agent"])
    print("the service account reads, beyond the agent role:", extra)
    ok(extra == ["enforcement_notes", "enquiry_logs", "kb_supervisor"], "permission gap")
    ok(pd["national_id"] == 20 and pd["health"] == 2 and pd["child"] == 1 and pd["iban"] == 1, "planted personal data")
    print("reference classification: kb_public Public; kb_supervisor, enforcement_notes, case_files, vendor_pack Restricted")
    print("reference scores: classification 2, personal data 1 (the spike needs no case file: synthetic articles only), "
          "permissions 0 (blocking: retrieval must filter by the asking agent's role)")


@lab("2.2")
def lab_2_2():
    qs = read(FILES / "questions.csv")
    langs = Counter(q["lang"] for q in qs)
    unans = sum(q["answerable"] == "no" for q in qs)
    print(f"questions {len(qs)}: Arabic {langs['ar']}, English {langs['en']}, unanswerable {unans}")
    _, clean = baseline_rows()
    en_share = sum(r["language"] == "en" for r in clean) / len(clean)
    print(f"English share of demand {en_share:.1%} against {langs['en'] / len(qs):.1%} of the questions")
    rows, fig = J.run({}, write=False)
    J.show(fig)
    ok(fig["correct"] == 15, f"starter correct {fig['correct']}")


@lab("2.3")
def lab_2_3():
    rows = read(FILES / "results_starter.csv")
    s = dict(J.STARTER)
    fig = J.figures(rows, s)
    J.show(fig)
    z = 1.96
    p = fig["accuracy"]
    need = math.ceil(z * z * p * (1 - p) / 0.08 ** 2)
    print(f"questions needed for a half-width of 8 points at {p:.0%}: {need}")
    ok(fig["correct"] == 15 and round(fig["wilson_low"], 3) == 0.332, "starter figures")


@lab("2.4")
def lab_2_4():
    starter = read(FILES / "results_starter.csv")
    index = {r["article_id"]: r for r in read(FILES / "kb_index.csv")}
    qs = {q["qid"]: q for q in read(FILES / "questions.csv")}
    kinds = Counter()
    for r in starter:
        if r["outcome"] in J.CORRECT:
            continue
        top = r["cited"]
        q = qs[r["qid"]]
        if r["outcome"] == "permission_leak":
            kinds["permission"] += 1
        elif r["outcome"] == "unsupported":
            kinds["answered without a source (should decline)"] += 1
        elif top in STALE or top == "A11":
            kinds["stale or superseded source"] += 1
        elif q["lang"] == "en" and all(index[g]["has_en"] == "no" for g in q["gold_articles"].split()):
            kinds["language: no English article"] += 1
        else:
            kinds["retrieval miss"] += 1
    print("starter failures by cause:", dict(kinds))
    rows_a, fig_a = J.run({}, write=False)
    rows_b, fig_b = J.run(ADAPTED, write=False)
    J.show(fig_b)
    flips = J.compare(rows_a, rows_b)
    print("paired comparison:", flips)
    meets = (fig_b["accuracy"] >= THRESHOLD["accuracy"] and fig_b["wilson_low"] >= THRESHOLD["lower_bound"]
             and fig_b["outcomes"].get("permission_leak", 0) == 0)
    print("decision against the threshold of lab 1.3:", "go" if meets else "rework")
    ok(fig_b["correct"] == 23 and not meets, "adapted figures and decision")


# ------------------------------------------------------------------ day 3


@lab("3.1")
def lab_3_1():
    v = read(FILES / "use_case_variants.csv")
    ok(len(v) == 6, "six variants")
    ref = {"V1": "limited", "V2": "limited (residents see it directly: transparency and a way to a person)",
           "V3": "high (decides on a person's money: a person decides, conformity assessment before and after)",
           "V4": "unacceptable (social scoring of residents): does not proceed", "V5": "little or no risk",
           "V6": "high (ranks people for enforcement)"}
    for k, x in ref.items():
        print(f"  {k}: {x}")


@lab("3.2")
def lab_3_2():
    flows = read(FILES / "vendor_dataflows.csv")
    out = [f["option"] for f in flows if "خارج المملكة" in f["hosted"]]
    print("options whose data leave the Kingdom by default:", out)
    ok(out == ["B"], "only option B")
    print("reference five risks: R01 stale fee (likelihood x impact 3 x 2 = 6), R02 restricted criteria in a draft (2 x 3 = 6), "
          "R03 personal data abroad (option B: 4 x 3 = 12, high), R05 over-reliance (3 x 2 = 6), R04 English service (3 x 2 = 6); scales 1 to 4 as in the national AI risk management framework")
    print("gate: B passes only with in-Kingdom hosting (+720 SAR per seat a year) and a transfer assessment; "
          "A, C, D pass with conditions (C: personal data removed before the model; all: a person sends every reply)")


@lab("3.3")
def lab_3_3():
    inp = CM.read_inputs(FILES / "cost_sheets.xlsx")
    quote = CM.model(inp, include_missing=False)
    full = CM.model(inp)
    for o in CM.OPTIONS:
        print(f"  {o}: 3-year TCO quote only {quote[o]['tco3']:,.0f}, with the missing items {full[o]['tco3']:,.0f}; "
              f"benefits {sum(full[o]['benefit']):,.0f}; net {full[o]['net3']:,.0f}")
    order = sorted(CM.OPTIONS, key=lambda o: -full[o]["net3"])
    print("ranking by 3-year net value:", order)
    ok(order[0] == "A" and full["B"]["net3"] < 0, "ranking")


@lab("3.4")
def lab_3_4():
    inp = CM.read_inputs(FILES / "cost_sheets.xlsx")
    base = CM.model(inp)
    runs = {"base": base, "volume -20%": CM.model(inp, 0.8), "volume +20%": CM.model(inp, 1.2),
            "accuracy at the lower bound": CM.model(inp, accuracy=inp["a"]["accuracy_low"]),
            "token price x3": CM.model(inp, token_price_factor=3)}
    for name, r in runs.items():
        print(f"  {name:28s} " + "  ".join(
            f"{o}: net {r[o]['net3']:>9,.0f} BE {r[o]['break_even_month'] or '-'}" for o in CM.OPTIONS))
    best_ai = max(["B", "C", "D"], key=lambda o: base[o]["net3"])
    lo, hi = 0.5, 1.0
    for _ in range(50):
        mid = (lo + hi) / 2
        r = CM.model(inp, accuracy=mid)
        if r[best_ai]["net3"] < r["A"]["net3"]:
            lo = mid
        else:
            hi = mid
    print(f"best AI option {best_ai}; it matches A on 3-year net value at an accuracy of {hi:.3f}")
    ok(base["A"]["break_even_month"] <= 24, "A within the 24-month rule")


# ------------------------------------------------------------------ the capstone pack and the slides


@lab("capstone")
def lab_capstone():
    cap = FILES / "capstone"
    raw = read(cap / "objections.csv")
    clean = dedupe(raw, "objection_id")
    closed = [float(r["drafting_minutes"]) for r in clean if r["status"] == "closed"]
    print(f"objections {len(raw)}, after removing duplicates {len(clean)}; drafting minutes median "
          f"{statistics.median(closed):.1f}, mean {statistics.mean(closed):.2f}")
    weeks = Counter((r["category"], (int(r["received_date"][5:7]))) for r in clean if r["category"] == "signage_violation")
    print("signage objections by month (the migration gap):", dict(sorted((m, n) for (_, m), n in weeks.items())))
    rnd = [r for r in clean if r["qa_sample_type"] == "random"]
    print(f"random QA error rate {sum(r['qa_result'] != 'correct' for r in rnd) / len(rnd):.3f} (n={len(rnd)})")
    # review minutes and the cost of a minute come from the capstone pack: 4 minutes, 240,000 / (1,540 x 60)
    base = {"case": "objections", "role": "officer", "review_minutes": 4.0, "sar_per_minute": 240000 / (1540 * 60)}
    figs = {}
    for label, s in (("starter", base),
                     ("adapted", dict(base, exclude_articles=["B03", "B19"], respect_permissions=True,
                                      chunking="paragraph", min_score=0.25))):
        rows, figs[label] = J.run(dict(J.STARTER, **s), write=False)
        print(label, end=": ")
        J.show(figs[label])
    ok(figs["adapted"]["correct"] == 22, "capstone adapted figures")
    inp = CM.read_inputs(cap / "cost_sheets.xlsx")
    inp["a"]["accuracy"] = round(figs["adapted"]["accuracy"], 3)
    inp["a"]["accuracy_low"] = round(figs["adapted"]["wilson_low"], 3)
    r = CM.model(inp)
    for o in CM.OPTIONS:
        print(f"  {o}: 3-year TCO {r[o]['tco3']:,.0f}, net {r[o]['net3']:,.0f}, break-even {r[o]['break_even_month']}")


@lab("demo")
def demo():
    rows = read(FILES / "examples" / "counter_visits.csv")
    clean = dedupe(rows, "visit_id")
    served = [float(r["service_minutes"]) for r in clean if r["status"] == "served"]
    allm = [float(r["service_minutes"]) for r in clean]
    print(f"counter visits {len(rows)}, unique {len(clean)}; minutes served only: median {statistics.median(served):.1f} "
          f"mean {statistics.mean(served):.1f}; with unclosed tickets: mean {statistics.mean(allm):.1f}, "
          f"median {statistics.median(allm):.1f}")
    for k, n in ((18, 25), (90, 125), (9, 10)):
        lo, hi = J.wilson(k, n)
        print(f"Wilson 95%: {k}/{n} = {k / n:.0%}, interval {lo:.1%} to {hi:.1%}")
    # an inspection-report summariser: a parallel costing example
    reports, minutes_saved, per_min = 6000, 6.0, 2.5
    print(f"inspection summaries: {reports} reports x {minutes_saved} minutes x {per_min} SAR = "
          f"{reports * minutes_saved * per_min:,.0f} SAR a year")


def main(argv):
    wanted = argv or list(LABS_RUN)
    failed = 0
    for lab_id in wanted:
        print(f"\n== {lab_id}")
        try:
            LABS_RUN[lab_id]()
            print("PASS")
        except AssertionError as e:
            failed += 1
            print("FAIL:", e)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
