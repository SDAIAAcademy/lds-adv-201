# /// script
# requires-python = ">=3.11"
# dependencies = ["openpyxl>=3.1"]
# ///
"""Generate every file the labs use, into labs/files/ (and labs/files/capstone/ for the capstone case).

    uv run labs/_tools/prepare_files.py

Deterministic: a fixed seed gives the same files on every run, so every participant, every reference value and
the answer key agree. Every organisation, person, number and rule is fictional; ID and mobile numbers have the
shape of real ones and are not real.
"""
from __future__ import annotations

import csv
import math
import random
import shutil
import sys
from datetime import date, timedelta
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

TOOLS = Path(__file__).resolve().parent
LABS = TOOLS.parent
OUT = LABS / "files"
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(LABS / "spike"))
import content_a as A  # noqa: E402
import content_day3 as D3  # noqa: E402
import content_b as B  # noqa: E402
import jawab as J  # noqa: E402

SEED = 2027
HEAD = Font(bold=True, color="FFFFFF")
FILL = PatternFill("solid", fgColor="0F766E")
INPUT = PatternFill("solid", fgColor="FFF7E6")


# ------------------------------------------------------------------ helpers


def write_csv(path: Path, header: list[str], rows: list[list]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def sheet(wb: Workbook, title: str, header: list[str], rows: list[list], widths=None, first=False, rtl=True):
    ws = wb.active if first else wb.create_sheet()
    ws.title = title
    ws.sheet_view.rightToLeft = rtl
    ws.append(header)
    for c in ws[1]:
        c.font, c.fill = HEAD, FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append(r)
    for i, wdt in enumerate(widths or [18] * len(header), start=1):
        ws.column_dimensions[get_column_letter(i)].width = wdt
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    return ws


def lognormal(rng: random.Random, median: float, sigma: float) -> float:
    return median * math.exp(rng.gauss(0, sigma))


# ------------------------------------------------------------------ enquiry logs (day 1)


def enquiry_logs(rng: random.Random, start: date, days: int, cats, subjects, prefix: str, base_weekday: int,
                 base_weekend: int, dup_dates: list[date], en_share=0.18, targeted_weeks=6):
    rows = []
    n = 0
    shares = [c[2] for c in cats]
    for d in range(days):
        day = start + timedelta(days=d)
        weekend = day.weekday() in (4, 5)  # Friday and Saturday
        volume = base_weekend if weekend else base_weekday
        if day.weekday() == 6:  # Sunday, the heaviest day
            volume = int(volume * 1.35)
        volume = int(volume * (1 + 0.002 * d) * rng.uniform(0.92, 1.08))
        week = d // 7
        for _ in range(volume):
            n += 1
            key, _, _, median, repeat = rng.choices(cats, weights=shares)[0]
            lang = "en" if rng.random() < en_share else "ar"
            channel = rng.choices(["web_form", "app_chat", "email"], weights=[45, 35, 20])[0]
            minutes = lognormal(rng, median * (1.25 if lang == "en" else 1.0), 0.45)
            status = "closed"
            if rng.random() < 0.018:
                minutes = rng.uniform(480, 1500)
                status = "auto_closed"
            frh = lognormal(rng, 9.0 if channel == "email" else 4.5, 0.6) * (1.6 if day.weekday() == 6 else 1.0)
            rep = rng.random() < repeat * (1.3 if lang == "en" else 1.0)
            qa_type, qa = "none", ""
            if week < targeted_weeks:
                escalated = key == "complaint_followup" or rep
                if escalated and rng.random() < 0.09:
                    qa_type = "targeted"
            elif rng.random() < 0.02:
                qa_type = "random"
            if qa_type != "none":
                p_wrong = 0.13 if qa_type == "targeted" else 0.045
                p_incomplete = 0.09 if qa_type == "targeted" else 0.03
                if key in ("renew_licence", "minor_works", "signage", "waste", "parks"):
                    p_wrong *= 1.5  # stale fees after the circular
                if lang == "en":
                    p_incomplete *= 1.6
                u = rng.random()
                qa = "wrong_info" if u < p_wrong else ("incomplete" if u < p_wrong + p_incomplete else "correct")
            subj = rng.choice([s for s in subjects[key] if (lang == "en") == s.isascii()] or subjects[key])
            rows.append([f"{prefix}{n:06d}", day.isoformat(), channel, lang, key, subj, f"AG{rng.randint(1, 42):02d}",
                         round(minutes, 1), status, round(frh, 1), "yes" if rep else "no", qa_type, qa])
    dups = [r for r in rows if date.fromisoformat(r[1]) in dup_dates]
    out = rows + [list(r) for r in dups]
    out.sort(key=lambda r: (r[1], r[0]))
    return out


def baseline(rows: list[list], period_days: int) -> dict:
    """The reference baseline: duplicates removed, auto-closed excluded from handling time, random QA only."""
    seen, clean = set(), []
    for r in rows:
        if r[0] in seen:
            continue
        seen.add(r[0])
        clean.append(r)
    out = {}
    for key in sorted({r[4] for r in clean}):
        sub = [r for r in clean if r[4] == key]
        mins = sorted(r[7] for r in sub if r[8] == "closed")
        qa = [r for r in sub if r[11] == "random"]
        out[key] = {
            "count": len(sub),
            "monthly": len(sub) / period_days * 30.4,
            "median": pct(mins, 50), "p90": pct(mins, 90), "mean": sum(mins) / len(mins),
            "qa_n": len(qa), "error_rate": sum(r[12] != "correct" for r in qa) / len(qa) if qa else 0.0,
            "repeat_rate": sum(r[10] == "yes" for r in sub) / len(sub),
        }
    return {"rows_raw": len(rows), "rows_clean": len(clean), "by_category": out}


def pct(sorted_values: list[float], p: float) -> float:
    """Percentile by linear interpolation (the method of spreadsheet PERCENTILE and of Python's default)."""
    k = (len(sorted_values) - 1) * p / 100
    f = math.floor(k)
    c = min(f + 1, len(sorted_values) - 1)
    return sorted_values[f] + (sorted_values[c] - sorted_values[f]) * (k - f)


# ------------------------------------------------------------------ knowledge base (day 1 and 2)


def knowledge_base(base: Path, articles, titles, classification, owner, licence) -> None:
    kb = base / "kb"
    if kb.exists():
        shutil.rmtree(kb)
    rows = []
    for aid, cat, coll, src, reviewed, ar, en in articles:
        body = f"# {aid} · {titles[aid]}\n\n## ar\n{ar}\n"
        if en:
            body += f"\n## en\n{en}\n"
        write_text(kb / f"{aid}.txt", body)
        rows.append([aid, titles[aid], cat, coll, classification[coll], src, licence[src], owner[coll], reviewed,
                     "current", "yes" if en else "no"])
    write_csv(base / "kb_index.csv",
              ["article_id", "title", "category", "collection", "classification", "source", "licence_note", "owner",
               "last_reviewed", "status", "has_en"], rows)


# ------------------------------------------------------------------ case A


def case_a() -> dict:
    rng = random.Random(SEED)
    start = date(2026, 6, 28)
    rows = enquiry_logs(rng, start, 91, A.CATEGORIES, A.SUBJECTS, "E", 205, 55,
                        [date(2026, 8, 16), date(2026, 8, 17)])
    write_csv(OUT / "enquiries.csv",
              ["enquiry_id", "received_date", "channel", "language", "category", "subject", "agent_id",
               "handling_minutes", "status", "first_response_hours", "repeat_within_7d", "qa_sample_type",
               "qa_result"], rows)
    base = baseline(rows, 91)
    write_text(OUT / "request_memo.txt", A.REQUEST_MEMO)
    write_text(OUT / "interview_notes.txt", A.INTERVIEWS)
    write_text(OUT / "data_dictionary.txt", A.DATA_DICTIONARY)

    in_scope = {"renew_licence", "new_licence", "minor_works", "signage", "waste", "payments", "parks", "violations"}
    ref_rows = []
    names = {c[0]: c[1] for c in A.CATEGORIES}
    for key, v in base["by_category"].items():
        ref_rows.append([key, names[key], v["count"], round(v["monthly"]), round(v["median"], 1), round(v["p90"], 1),
                         round(v["mean"], 2), v["qa_n"], round(v["error_rate"], 3), round(v["repeat_rate"], 3),
                         "yes" if key in in_scope else "no"])
    write_csv(OUT / "baseline_reference.csv",
              ["category", "category_ar", "enquiries_91_days", "monthly_volume", "median_handling_min",
               "p90_handling_min", "mean_handling_min", "random_qa_sample", "error_rate", "repeat_rate",
               "kb_category"], ref_rows)

    wb = Workbook()
    sheet(wb, "تكاليف الموظفين", ["البند", "القيمة", "الوحدة"], [list(r) for r in A.STAFF_COSTS], [48, 14, 10], first=True)
    for r in range(2, len(A.STAFF_COSTS) + 2):
        wb.active.cell(r, 2).number_format = "#,##0"
    wb.save(OUT / "staff_costs.xlsx")

    knowledge_base(OUT, A.ARTICLES, A.ARTICLE_TITLES, A.CLASSIFICATION, A.OWNER, A.LICENCE)
    write_csv(OUT / "questions.csv", ["qid", "lang", "category", "question", "answerable", "gold_fact", "gold_articles"],
              [list(q) for q in A.QUESTIONS])
    write_csv(OUT / "access_matrix.csv", A.ACCESS_COLUMNS, [list(r) for r in A.ACCESS])
    return base, rows


IN_SCOPE = ["renew_licence", "new_licence", "minor_works", "signage", "waste", "payments", "parks", "violations"]
STALE = ["A01", "A09", "A14", "A18", "A26"]
SUPERSEDED = ["A11"]
ADAPTED = {"label": "adapted", "exclude_articles": STALE + SUPERSEDED, "respect_permissions": True,
           "chunking": "paragraph", "min_score": 0.25}


def fake_id(rng):
    return "1" + "".join(str(rng.randint(0, 9)) for _ in range(9))


def fake_mobile(rng):
    return "05" + "".join(str(rng.randint(0, 9)) for _ in range(8))


def day2_files() -> dict:
    """Case files, sources, the readiness scorecard to start from, the findings of lab 1.4 as a fallback."""
    rng = random.Random(SEED + 2)
    folder = OUT / "case_files"
    if folder.exists():
        shutil.rmtree(folder)
    counts = []
    for i, (cat, msg, reply, extra) in enumerate(D3.CASE_TOPICS, start=1):
        name = f"{rng.choice(D3.FIRST)} {rng.choice(D3.LAST)}"
        nid, mob = fake_id(rng), fake_mobile(rng)
        district = rng.choice(D3.DISTRICTS)
        plot = rng.randint(100, 999)
        lines = [f"ملف الحالة C{i:02d} · الفئة: {cat} · بيانات اصطناعية للتدريب",
                 f"المستفيد: {name}", f"رقم الهوية: {nid}", f"الجوال: {mob}",
                 f"العنوان: {district}، قطعة {plot}", "", f"رسالة المستفيد: {msg}"]
        fields = {"name": 1, "national_id": 1, "mobile": 1, "address": 1, "health": 0, "child": 0, "bank": 0}
        if extra == "iban":
            lines.append("رقم الآيبان: SA" + "".join(str(rng.randint(0, 9)) for _ in range(22)))
            fields["bank"] = 1
        if extra == "health":
            fields["health"] = 1
        if extra == "child":
            lines.append(f"اسم الطالبة: {rng.choice(D3.FIRST[1::2])} (11 سنة)")
            fields["child"] = 1
        lines += ["", f"رد الموظف: {reply}"]
        write_text(folder / f"C{i:02d}.txt", "\n".join(lines))
        counts.append([f"C{i:02d}", cat] + list(fields.values()))
    write_csv(OUT / "sources.csv", ["source", "description", "content", "kept_by"], [list(r) for r in D3.SOURCES])

    blank = Workbook()
    ws = sheet(blank, "البطاقة", ["المعيار", "الاسم", "السؤال", "الدرجة (0 إلى 3)", "الدليل", "صاحب الفجوة"],
               [[c[0], c[1], c[2], "", "", ""] for c in D3.CRITERIA], [16, 16, 40, 12, 60, 22], first=True)
    sheet(blank, "مقياس الدرجات", ["الدرجة", "المعنى"], [list(x) for x in D3.SCORE_SCALE], [10, 70])
    blank.save(OUT / "scorecard_blank.xlsx")

    wb = Workbook()
    rows = [[c[0], c[1], c[2], "", "", ""] for c in D3.CRITERIA]
    ref = {
        "coverage": (1, "الفئات الثماني التي تجيب عنها المقالات تمثل 71.4% من الطلب؛ لا مقالات تجيب عن الحفر والبيع المتجول ومتابعة حالة البلاغات (28.6%)؛ 23 مقالًا من 48 لها نسخة إنجليزية",
                     "مؤيد الصاعدي"),
        "quality": (0, "خمس مقالات رسوم متقادمة بعد التعميم 14 لعام 2026 (A01 وA09 وA14 وA18 وA26)، ومقالان متعارضان في مدة رخصة الترميم (A11 وA12)",
                    "مؤيد الصاعدي"),
        "rights": (1, "ست مقالات من حزمة المورد مرخصة داخل منصته فقط (A15 وA20 وA23 وA28 وA41 وA42): تصلح لخيار الشراء من المورد، ولا تصلح للبناء أو الشراكة دون إعادة كتابة",
                   "بتول النجراني"),
    }
    for r in rows:
        if r[0] in ref:
            r[3], r[4], r[5] = ref[r[0]]
    ws = sheet(wb, "البطاقة", ["المعيار", "الاسم", "السؤال", "الدرجة (0 إلى 3)", "الدليل", "صاحب الفجوة"], rows,
               [16, 16, 40, 12, 60, 22], first=True)
    for r in range(5, 8):
        for c in (4, 5, 6):
            ws.cell(r, c).fill = INPUT
    sheet(wb, "مقياس الدرجات", ["الدرجة", "المعنى"], [list(x) for x in D3.SCORE_SCALE], [10, 70])
    wb.save(OUT / "scorecard_start.xlsx")

    findings = [[a, "stale", "رسوم قبل التعميم 14 لعام 2026"] for a in STALE]
    findings += [["A11", "superseded", "مدة قديمة يناقضها A12"]]
    findings += [[a, "vendor_rights", "ترخيص داخل منصة المورد فقط"] for a in ("A15", "A20", "A23", "A28", "A41", "A42")]
    findings += [[a, "restricted", "لا يقرؤه دور الموظف"] for a in ("A33", "A34", "A36")]
    write_csv(OUT / "kb_findings_reference.csv", ["article_id", "finding", "note"], findings)
    return {"case_fields": counts}


def spike_files() -> dict:
    """The supplied run log of the starter prototype (labs 2.3 and 2.4 start from it)."""
    rows, fig = J.run({}, write=False)
    write_csv(OUT / "results_starter.csv", list(rows[0].keys()), [list(r.values()) for r in rows])
    rows2, fig2 = J.run(ADAPTED, write=False)
    return {"starter": fig, "adapted": fig2, "flips": J.compare(rows, rows2)}


def day3_files(rows: list[list], spike: dict) -> dict:
    write_text(OUT / "risk_levels.txt", D3.RISK_LEVELS)
    write_csv(OUT / "use_case_variants.csv", ["variant", "description"], [list(v) for v in D3.VARIANTS])
    write_csv(OUT / "candidate_risks.csv", ["risk", "description"], [list(r) for r in D3.CANDIDATE_RISKS])
    write_csv(OUT / "vendor_dataflows.csv", ["option", "name", "what_leaves", "hosted"], [list(r) for r in D3.DATAFLOWS])

    wb = Workbook()
    sheet(wb, "ورقة الفحص", ["#", "الخطر", "الاحتمالية (1 إلى 3)", "الأثر (1 إلى 3)", "الضابط", "المسؤول",
                             "موعد التحقق"], [[i, "", "", "", "", "", ""] for i in range(1, 6)], [5, 40, 12, 12, 45, 26, 16],
          first=True)
    sheet(wb, "المسؤولون", ["المسؤول"], [[o] for o in D3.OWNERS], [50])
    sheet(wb, "البوابة", ["الخيار", "أساس نظامي للبيانات", "فحص التصنيف", "إشراف بشري على ما يمس الأفراد",
                          "يعبر البوابة؟", "شرط العبور"], [[o[0], "", "", "", "", ""] for o in D3.DATAFLOWS],
          [8, 22, 16, 26, 14, 40])
    wb.save(OUT / "screening_start.xlsx")

    seen, clean = set(), []
    for r in rows:
        if r[0] not in seen:
            seen.add(r[0])
            clean.append(r)
    scope = [r for r in clean if r[4] in IN_SCOPE]
    closed = [r[7] for r in scope if r[8] == "closed"]
    facts = {
        "in_scope_annual": round(len(scope) / 91 * 365),
        "mean_handling": round(sum(closed) / len(closed), 2),
        "ar_share": round(sum(r[3] == "ar" for r in scope) / len(scope), 3),
        "accuracy": round(spike["adapted"]["accuracy"], 3),
        "accuracy_low": round(spike["adapted"]["wilson_low"], 3),
    }
    cost_workbook(OUT / "cost_sheets.xlsx", facts, formulas=False)
    cost_workbook(OUT / "tco_reference.xlsx", facts, formulas=True)
    return facts


def cost_workbook(path: Path, facts: dict, formulas: bool, mod=D3) -> None:
    """cost_sheets.xlsx: the inputs. tco_reference.xlsx: the same inputs plus the model as formulas."""
    wb = Workbook()
    arows = [[key, label, facts.get(key, value)] for key, label, value in mod.ASSUMPTIONS]
    ws = sheet(wb, "الافتراضات", ["المفتاح", "الافتراض", "القيمة"], arows, [20, 60, 14], first=True)
    names = {}
    for i, (key, _, _) in enumerate(mod.ASSUMPTIONS, start=2):
        names[key] = f"'الافتراضات'!$C${i}"
        ws.cell(i, 3).fill = INPUT
    if formulas:
        ws.append(["cost_per_minute", "تكلفة دقيقة عمل الموظف (ريال)", f"={names['loaded_cost']}/({names['hours']}*60)"])
        names["cost_min"] = f"'الافتراضات'!$C${ws.max_row}"
    for opt, spec in mod.OPTIONS.items():
        rows = [[name, kind, amount, quoted] for name, kind, amount, quoted in spec["items"]]
        sheet(wb, f"الخيار {opt}", ["البند", "النوع", "المبلغ (ريال)", "في عرض السعر"], rows, [52, 20, 16, 14])
    sheet(wb, "بنود غائبة", ["المفتاح", "البند", "النوع", "المبلغ (ريال)", "الخيارات"],
          [list(m) for m in mod.MISSING], [16, 60, 18, 14, 12])
    sheet(wb, "أنواع البنود", ["النوع", "المعنى"], [
        ["one_off", "مرة واحدة في بداية المشروع"], ["annual", "كل سنة"],
        ["per_agent_year", "لكل موظف في السنة"], ["per_drafted_answer", "لكل مسودة إجابة يصوغها المساعد"]], [22, 50])
    if formulas:
        tco_sheet(wb, names, mod)
    wb.save(path)


def tco_sheet(wb: Workbook, n: dict, mod=D3) -> None:
    """The reference model in formulas: years 0 to 3 per option, then 36 months of cumulative net value."""
    ws = wb.create_sheet("النموذج")
    ws.sheet_view.rightToLeft = True
    ws.append(["الخيار", "البند", "السنة 0", "السنة 1", "السنة 2", "السنة 3", "المجموع"])
    for c in ws[1]:
        c.font, c.fill = HEAD, FILL
    vol = lambda y: f"{n['in_scope_annual']}*(1+{n['growth']})^{y}"
    adopt = lambda y: n['adoption_y1'] if y == 1 else n['adoption_y2']
    h, m, acc, s, r = n['mean_handling'], n['cost_min'], n['accuracy'], n['saving_when_usable'], n['review_minutes']
    out = {}
    for opt, spec in mod.OPTIONS.items():
        share = "1" if "en" in spec["benefit"]["languages"] else n['ar_share']
        extra = [(k, a) for key, _, k, a, opts in mod.MISSING if opt in opts.split()]
        items = [(k, a) for _, k, a, _ in spec["items"]] + extra
        one_off = sum(a for k, a in items if k == "one_off")
        annual = sum(a for k, a in items if k == "annual")
        per_agent = sum(a for k, a in items if k == "per_agent_year")
        per_draft = sum(a for k, a in items if k == "per_drafted_answer")
        cost_row = ws.max_row + 1
        cells = [f"={one_off}"]
        for y in (1, 2, 3):
            parts = [str(annual), f"{per_agent}*{n['agents']}"]
            if per_draft:
                parts.append(f"{per_draft}*{vol(y)}*{adopt(y)}*{share}")
            cells.append("=" + "+".join(parts))
        ws.append([opt, "التكلفة"] + cells + [f"=SUM(C{cost_row}:F{cost_row})"])
        ben_row = ws.max_row + 1
        bcells = ["=0"]
        for y in (1, 2, 3):
            if spec["benefit"]["ai"]:
                bcells.append(f"={vol(y)}*{share}*{adopt(y)}*({acc}*{s}*{h}-{r})*{m}")
            else:
                bcells.append(f"={vol(y)}*({n['a_handling_cut']}+{n['a_deflection']})*{h}*{m}")
        ws.append([opt, "المنافع"] + bcells + [f"=SUM(C{ben_row}:F{ben_row})"])
        net_row = ws.max_row + 1
        ws.append([opt, "صافي القيمة"] + [f"={col}{ben_row}-{col}{cost_row}" for col in "CDEFG"])
        out[opt] = net_row
    ws.column_dimensions["B"].width = 16
    for col in "CDEFG":
        ws.column_dimensions[col].width = 14
    for row in ws.iter_rows(min_row=2, min_col=3, max_col=7):
        for c in row:
            c.number_format = "#,##0"

    mo = wb.create_sheet("الأشهر")
    mo.sheet_view.rightToLeft = True
    mo.append(["الشهر"] + [f"الصافي التراكمي {o}" for o in mod.OPTIONS])
    for c in mo[1]:
        c.font, c.fill = HEAD, FILL
    mo.append([0] + [f"='النموذج'!C{out[o]}" for o in mod.OPTIONS])
    for t in range(1, 37):
        col_year = "DEF"[(t - 1) // 12]
        rowv = [t]
        for j, o in enumerate(mod.OPTIONS, start=2):
            rowv.append(f"={get_column_letter(j)}{t + 1}+'النموذج'!{col_year}{out[o]}/12")
        mo.append(rowv)
    mo.append([])
    mo.append(["نقطة التعادل (الشهر)"] + [
        f'=IF(COUNTIF({get_column_letter(j)}2:{get_column_letter(j)}38,"<0")>36,"لا تعادل خلال 36 شهرًا",'
        f'COUNTIF({get_column_letter(j)}2:{get_column_letter(j)}38,"<0"))' for j in range(2, 6)])
    for row in mo.iter_rows(min_row=2, min_col=2, max_col=5, max_row=38):
        for c in row:
            c.number_format = "#,##0"
    for j in range(1, 6):
        mo.column_dimensions[get_column_letter(j)].width = 22


CAP = OUT / "capstone"
ADAPTED_B = {"case": "objections", "label": "adapted", "role": "officer", "exclude_articles": ["B03", "B19"],
             "respect_permissions": True, "chunking": "paragraph", "min_score": 0.25}


def case_b() -> dict:
    """The capstone pack: an unseen second use case of the same agency."""
    rng = random.Random(SEED + 7)
    start = date(2026, 1, 4)
    rows = enquiry_logs(rng, start, 182, B.CATEGORIES, B.SUBJECTS, "O", 22, 4,
                        [date(2026, 3, 1)], en_share=0.12, targeted_weeks=0)
    out = []
    for r in rows:
        day = date.fromisoformat(r[1])
        # planted: signage objections were not carried over to the new platform for four weeks
        if r[4] == "signage_violation" and date(2026, 4, 12) <= day < date(2026, 5, 10):
            continue
        r = list(r)
        r[9] = max(1, round(lognormal(rng, 18, 0.4)))  # days to decision
        out.append(r)
    write_csv(CAP / "objections.csv",
              ["objection_id", "received_date", "channel", "language", "category", "subject", "officer_id",
               "drafting_minutes", "status", "days_to_decision", "appealed", "qa_sample_type", "qa_result"], out)
    write_text(CAP / "request_memo.txt", B.REQUEST_MEMO)
    write_text(CAP / "interview_notes.txt", B.INTERVIEWS)
    write_text(CAP / "data_dictionary.txt", B.DATA_DICTIONARY)
    knowledge_base(CAP, B.ARTICLES, B.TITLES, B.CLASSIFICATION, B.OWNER, B.LICENCE)
    write_csv(CAP / "access_matrix.csv", B.ACCESS_COLUMNS, [list(r) for r in B.ACCESS])
    write_csv(CAP / "questions.csv", ["qid", "lang", "category", "question", "answerable", "gold_fact", "gold_articles"],
              [list(q) for q in B.QUESTIONS])

    crng = random.Random(SEED + 8)
    folder = CAP / "case_files"
    if folder.exists():
        shutil.rmtree(folder)
    for i, (cat, msg, extra) in enumerate(B.CASE_TOPICS, start=1):
        lines = [f"ملف الاعتراض K{i:02d} · المخالفة: {cat} · بيانات اصطناعية للتدريب",
                 f"المعترض: {crng.choice(D3.FIRST)} {crng.choice(D3.LAST)}", f"رقم الهوية: {fake_id(crng)}",
                 f"الجوال: {fake_mobile(crng)}", f"رقم المخالفة: V{crng.randint(10000, 99999)}", "",
                 f"نص الاعتراض: {msg}"]
        if extra == "third_party":
            lines.append(f"بيانات الجار: {crng.choice(D3.FIRST)} {crng.choice(D3.LAST)}، رقم الهوية {fake_id(crng)}، العمر 74 سنة")
        if extra == "iban":
            lines.append("رقم الآيبان: SA" + "".join(str(crng.randint(0, 9)) for _ in range(22)))
        write_text(folder / f"K{i:02d}.txt", "\n".join(lines))

    wb = Workbook()
    sheet(wb, "تكاليف الموظفين", ["البند", "القيمة", "الوحدة"], [list(r) for r in B.STAFF_COSTS], [48, 14, 10], first=True)
    wb.save(CAP / "staff_costs.xlsx")

    seen, clean = set(), []
    for r in out:
        if r[0] not in seen:
            seen.add(r[0])
            clean.append(r)
    closed = [r[7] for r in clean if r[8] == "closed"]
    facts = {"in_scope_annual": round(len(clean) / 182 * 365), "mean_handling": round(sum(closed) / len(closed), 2),
             "ar_share": round(sum(r[3] == "ar" for r in clean) / len(clean), 3)}
    cost_workbook(CAP / "cost_sheets.xlsx", facts, formulas=False, mod=B)
    starter = J.run({"case": "objections", "role": "officer"}, write=False)[1]
    adapted = J.run(ADAPTED_B, write=False)[1]
    return {"rows": len(out), "clean": len(clean), "facts": facts, "starter": starter, "adapted": adapted}


def demo_files() -> None:
    """A parallel example for the slides, never used by a lab: the walk-in counter of the agency's head office."""
    rng = random.Random(SEED + 11)
    rows, n = [], 0
    for d in range(28):
        day = date(2026, 3, 1) + timedelta(days=d)
        if day.weekday() in (4, 5):
            continue
        for _ in range(rng.randint(40, 55)):
            n += 1
            service = rng.choices(["licence", "permit", "payment"], weights=[5, 3, 2])[0]
            minutes = lognormal(rng, {"licence": 12, "permit": 16, "payment": 6}[service], 0.4)
            status = "served"
            if rng.random() < 0.025:
                minutes, status = rng.uniform(300, 600), "ticket_not_closed"
            rows.append([f"V{n:05d}", day.isoformat(), service, round(minutes, 1), status])
    rows += [list(r) for r in rows if r[1] == "2026-03-10"]
    rows.sort(key=lambda r: (r[1], r[0]))
    write_csv(OUT / "examples" / "counter_visits.csv", ["visit_id", "visit_date", "service", "service_minutes", "status"], rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    demo_files()
    base, rows = case_a()
    print("case A rows:", base["rows_raw"], "clean:", base["rows_clean"])
    for k, v in base["by_category"].items():
        print(f"  {k:20s} {v['count']:6d} med {v['median']:5.1f} p90 {v['p90']:6.1f} mean {v['mean']:5.2f} "
              f"qa {v['qa_n']:3d} err {v['error_rate']:.3f} rep {v['repeat_rate']:.3f}")
    day2_files()
    spike = spike_files()
    print("spike starter", round(spike["starter"]["accuracy"], 3), "adapted", round(spike["adapted"]["accuracy"], 3),
          "flips", spike["flips"])
    facts = day3_files(rows, spike)
    print("cost facts", facts)
    cb = case_b()
    print("capstone rows", cb["rows"], "clean", cb["clean"], cb["facts"])
    print("capstone starter", round(cb["starter"]["accuracy"], 3), cb["starter"]["outcomes"])
    print("capstone adapted", round(cb["adapted"]["accuracy"], 3), cb["adapted"]["outcomes"])


if __name__ == "__main__":
    main()
