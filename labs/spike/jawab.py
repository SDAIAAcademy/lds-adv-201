"""Jawab (جواب): the retrieval-grounded prototype of the feasibility spike.

Standard library only, so it runs in Colab, in JupyterLab and on a laptop processor without any install.

What it does, for each labelled question:
  1. retrieves the closest knowledge-base passages from an in-memory vector index (TF-IDF vectors of character
     n-grams: no model to download, no key);
  2. drafts an answer from them, either with a language model behind a provider-neutral chat API
     (LLM_BASE_URL, LLM_API_KEY, LLM_MODEL in the environment) or, when no key is set, with the stand-in:
     an extractive answerer that copies the sentence of the top passage closest to the question and cites it;
  3. grades the draft against the label: the expected fact, the sources allowed to support it, or a decline;
  4. writes a run log (one row per question, plus the settings) so every figure of the spike can be recomputed.

The stand-in is not a language model. It never translates and never paraphrases, so it shows what retrieval
and the settings do; it cannot show what a model adds or breaks. Say which one produced a figure.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
import unicodedata
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
LABS = HERE.parent
FILES = LABS / "files"
RUNS = HERE / "runs"
CACHE = HERE / "cache"

CASES = {
    "enquiries": FILES,
    "objections": FILES / "capstone",
}

STARTER = {
    "case": "enquiries",
    "label": "starter",
    "top_k": 3,
    "chunking": "article",
    "exclude_articles": [],
    "respect_permissions": False,
    "role": "agent",
    "prefer_newest": False,
    "min_score": 0.0,
    "price_in_usd_per_m": 0.20,
    "price_out_usd_per_m": 0.40,
    "usd_to_sar": 3.75,
    "chars_per_token": 3.0,
    "review_minutes": 1.0,
    "sar_per_minute": 2.14,
}

DECLINE_AR = "لا أجد في المصادر المتاحة إجابة عن هذا السؤال، وأحيله إلى المختص."
DECLINE_EN = "I cannot find this in the available sources; I am passing it to a specialist."

# ------------------------------------------------------------------ text


def norm(text: str) -> str:
    """Arabic and English text as compared here: forms folded, marks removed, digits Western, lower case."""
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789"))
    text = re.sub(r"[ً-ْـ]", "", text)
    for a, b in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ة", "ه"), ("ى", "ي")):
        text = text.replace(a, b)
    text = re.sub(r"(?<=\d),(?=\d{3})", "", text)
    return re.sub(r"\s+", " ", text.lower()).strip()


def grams(text: str) -> Counter:
    t = " " + re.sub(r"[^\w ]", " ", norm(text)) + " "
    t = re.sub(r" +", " ", t)
    out = Counter()
    for n in (3, 4):
        for i in range(len(t) - n + 1):
            g = t[i:i + n]
            if g.strip():
                out[g] += 1
    return out


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!؟?])\s+|\n+", text.strip())
    return [p.strip() for p in parts if len(p.strip()) > 3]


def lang_of(text: str) -> str:
    return "ar" if re.search(r"[؀-ۿ]", text) else "en"


# ------------------------------------------------------------------ knowledge base


def read_csv(path: Path) -> list[dict]:
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load_kb(case: str) -> tuple[list[dict], dict]:
    """Passages (one per article and language) and the article index."""
    base = CASES[case]
    index = {r["article_id"]: r for r in read_csv(base / "kb_index.csv")}
    passages = []
    for aid, meta in index.items():
        raw = (base / "kb" / f"{aid}.txt").read_text(encoding="utf-8")
        blocks = re.split(r"^## (ar|en)\s*$", raw, flags=re.M)
        for i in range(1, len(blocks), 2):
            body = blocks[i + 1].strip()
            passages.append({"article_id": aid, "lang": blocks[i], "text": body, "meta": meta})
    return passages, index


def chunk(passages: list[dict], how: str) -> list[dict]:
    """article: one passage per article and language. paragraph: one passage per paragraph of an article."""
    if how == "article":
        return passages
    out = []
    for p in passages:
        for para in [x.strip() for x in p["text"].split("\n") if x.strip()]:
            out.append({**p, "text": para})
    return out


def load_access(case: str) -> dict:
    """role -> set of collections the role may read."""
    out = {}
    for r in read_csv(CASES[case] / "access_matrix.csv"):
        out[r["role"]] = {k for k, v in r.items() if k != "role" and v.strip().upper() == "R"}
    return out


class Index:
    """An in-memory vector index: TF-IDF weights of character n-grams, cosine similarity."""

    def __init__(self, passages: list[dict]):
        self.passages = passages
        tfs = [grams(p["text"]) for p in passages]
        df = Counter()
        for tf in tfs:
            df.update(tf.keys())
        n = len(passages)
        self.idf = {g: math.log((1 + n) / (1 + d)) + 1 for g, d in df.items()}
        self.vecs = [self._weigh(tf) for tf in tfs]

    def _weigh(self, tf: Counter) -> dict:
        v = {g: (1 + math.log(c)) * self.idf.get(g, 0.0) for g, c in tf.items()}
        norm_ = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {g: x / norm_ for g, x in v.items()}

    def search(self, query: str, allowed=None) -> list[tuple[float, dict]]:
        q = self._weigh(grams(query))
        hits = []
        for p, v in zip(self.passages, self.vecs):
            if allowed is not None and not allowed(p):
                continue
            s = sum(w * v.get(g, 0.0) for g, w in q.items())
            hits.append((round(s, 4), p))
        hits.sort(key=lambda h: (-h[0], h[1]["article_id"], h[1]["lang"]))
        return hits


# ------------------------------------------------------------------ the prototype


def retrieve(index: Index, question: str, s: dict, access: dict) -> list[tuple[float, dict]]:
    excluded = set(s["exclude_articles"])
    readable = access.get(s["role"], set())

    def allowed(p):
        if p["article_id"] in excluded:
            return False
        if s["respect_permissions"] and p["meta"]["collection"] not in readable:
            return False
        return True

    hits = index.search(question, allowed)[: s["top_k"]]
    if s["prefer_newest"] and hits:
        top = hits[0][0]
        near = [h for h in hits if h[0] >= 0.8 * top]
        newest = max(near, key=lambda h: (h[1]["meta"]["last_reviewed"], h[0]))
        hits = [newest] + [h for h in hits if h is not newest]
    return hits


def draft_standin(question: str, hits, s: dict) -> tuple[str, list[str]]:
    lang = lang_of(question)
    if not hits or hits[0][0] < s["min_score"]:
        return (DECLINE_AR if lang == "ar" else DECLINE_EN), []
    passage = hits[0][1]
    qv = grams(question)
    best, best_s = "", -1.0
    for sent in sentences(passage["text"]):
        sv = grams(sent)
        overlap = sum(min(c, sv[g]) for g, c in qv.items())
        score = overlap / (1 + 0.15 * len(sent))
        if score > best_s:
            best, best_s = sent, score
    return f"{best} [{passage['article_id']}]", [passage["article_id"]]


SYSTEM = (
    "You draft answers for municipal contact-centre agents. Answer only from the passages given, in the "
    "language of the question, in one or two sentences, and cite the article id in square brackets, for "
    "example [A12]. If the passages do not contain the answer, reply exactly with: "
    f"{DECLINE_AR} (for an Arabic question) or {DECLINE_EN} (for an English question)."
)


def build_prompt(question: str, hits) -> str:
    blocks = [f"[{p['article_id']}] {p['text']}" for _, p in hits]
    return "Passages:\n" + "\n\n".join(blocks) + f"\n\nQuestion: {question}"


def draft_model(question: str, hits, s: dict) -> tuple[str, list[str], dict]:
    base = os.environ["LLM_BASE_URL"].rstrip("/")
    model = os.environ["LLM_MODEL"]
    lang = lang_of(question)
    if not hits or hits[0][0] < s["min_score"]:
        return (DECLINE_AR if lang == "ar" else DECLINE_EN), [], {}
    body = {
        "model": model,
        "temperature": 0,
        "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": build_prompt(question, hits)}],
    }
    key = hashlib.sha256(json.dumps(body, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:20]
    CACHE.mkdir(parents=True, exist_ok=True)
    cached = CACHE / f"{key}.json"
    if cached.exists():
        data = json.loads(cached.read_text(encoding="utf-8"))
    else:
        req = urllib.request.Request(
            base + "/chat/completions",
            data=json.dumps(body).encode(),
            headers={"Authorization": f"Bearer {os.environ.get('LLM_API_KEY', '')}", "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120) as r:
            data = json.loads(r.read().decode())
        cached.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    text = data["choices"][0]["message"]["content"].strip()
    cites = re.findall(r"\[([A-Z]\d{2})\]", text)
    return text, cites, data.get("usage", {})


def using_model() -> bool:
    return bool(os.environ.get("LLM_BASE_URL") and os.environ.get("LLM_MODEL"))


# ------------------------------------------------------------------ grading and figures


def is_decline(text: str) -> bool:
    t = norm(text)
    return norm(DECLINE_AR)[:25] in t or norm(DECLINE_EN)[:25] in t


def grade(q: dict, text: str, cites: list[str], index: dict, s: dict, access: dict) -> str:
    """One outcome per question. Correct: correct, correct_decline. Failures: the rest.

    The order of the tests is the order of severity: an answer that leaks a restricted source is a leak even
    when its fact is right."""
    answerable = q["answerable"] == "yes"
    if is_decline(text):
        return "declined_answerable" if answerable else "correct_decline"
    if not answerable:
        return "unsupported"
    readable = access.get(s["role"], set())
    if any(index[c]["collection"] not in readable for c in cites if c in index):
        return "permission_leak"
    if lang_of(re.sub(r"\[[A-Z]\d{2}\]", "", text)) != q["lang"]:
        return "wrong_language"
    gold_sources = set(q["gold_articles"].split())
    if not set(cites) & gold_sources:
        return "wrong_source"
    facts = [f for f in q["gold_fact"].split("|") if f]
    if not any(norm(f) in norm(text) for f in facts):
        return "wrong_fact"
    return "correct"


CORRECT = {"correct", "correct_decline"}
GROUNDING = {"unsupported", "wrong_source", "permission_leak"}


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def figures(rows: list[dict], s: dict) -> dict:
    n = len(rows)
    k = sum(r["outcome"] in CORRECT for r in rows)
    lo, hi = wilson(k, n)
    by_lang = {}
    for lang in ("ar", "en"):
        sub = [r for r in rows if r["lang"] == lang]
        kk = sum(r["outcome"] in CORRECT for r in sub)
        by_lang[lang] = {"n": len(sub), "correct": kk, "accuracy": kk / len(sub) if sub else 0.0}
    answered = [r for r in rows if r["outcome"] not in ("correct_decline", "declined_answerable")]
    grounding = sum(r["outcome"] in GROUNDING for r in rows)
    model_sar = sum(float(r["cost_usd"]) for r in rows) * s["usd_to_sar"]
    review_sar = n * s["review_minutes"] * s["sar_per_minute"]
    return {
        "n": n, "correct": k, "accuracy": k / n, "wilson_low": lo, "wilson_high": hi,
        "by_lang": by_lang, "answered": len(answered), "grounding_failures": grounding,
        "grounding_rate": grounding / n, "outcomes": dict(Counter(r["outcome"] for r in rows)),
        "model_cost_sar": model_sar, "review_cost_sar": review_sar,
        "cost_per_correct_sar": (model_sar + review_sar) / k if k else float("inf"),
    }


def compare(a: list[dict], b: list[dict]) -> dict:
    """Paired comparison of two runs on the same questions: which questions flipped."""
    ra = {r["qid"]: r["outcome"] in CORRECT for r in a}
    rb = {r["qid"]: r["outcome"] in CORRECT for r in b}
    fixed = sorted(q for q in ra if not ra[q] and rb.get(q))
    broken = sorted(q for q in ra if ra[q] and not rb.get(q))
    return {"fixed": fixed, "broken": broken, "both_right": sum(ra[q] and rb.get(q, False) for q in ra),
            "both_wrong": sum((not ra[q]) and not rb.get(q, False) for q in ra)}


def run(settings: dict | None = None, write: bool = True) -> tuple[list[dict], dict]:
    s = dict(STARTER)
    s.update(settings or {})
    passages, index_meta = load_kb(s["case"])
    access = load_access(s["case"])
    index = Index(chunk(passages, s["chunking"]))
    questions = read_csv(CASES[s["case"]] / "questions.csv")
    model = os.environ.get("LLM_MODEL", "") if using_model() else "stand-in (extractive, no language model)"
    rows = []
    for q in questions:
        hits = retrieve(index, q["question"], s, access)
        usage = {}
        if using_model():
            text, cites, usage = draft_model(q["question"], hits, s)
        else:
            text, cites = draft_standin(q["question"], hits, s)
        prompt_chars = len(SYSTEM) + len(build_prompt(q["question"], hits))
        t_in = usage.get("prompt_tokens") or round(prompt_chars / s["chars_per_token"])
        t_out = usage.get("completion_tokens") or round(len(text) / s["chars_per_token"])
        cost = t_in * s["price_in_usd_per_m"] / 1e6 + t_out * s["price_out_usd_per_m"] / 1e6
        rows.append({
            "qid": q["qid"], "lang": q["lang"], "category": q["category"], "question": q["question"],
            "answer": text, "cited": " ".join(cites),
            "top_article": hits[0][1]["article_id"] if hits else "", "top_score": f"{hits[0][0]:.3f}" if hits else "",
            "tokens_in": t_in, "tokens_out": t_out, "cost_usd": f"{cost:.8f}",
            "outcome": grade(q, text, cites, index_meta, s, access),
        })
    fig = figures(rows, s)
    if write:
        RUNS.mkdir(parents=True, exist_ok=True)
        with open(RUNS / f"{s['label']}.csv", "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        log = {"settings": s, "model": model, "figures": fig}
        (RUNS / f"{s['label']}.json").write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    return rows, fig


def show(fig: dict) -> None:
    pct = lambda x: f"{100 * x:.1f}%"
    print(f"صحيح {fig['correct']} من {fig['n']}: {pct(fig['accuracy'])} · "
          f"فترة ثقة ويلسون 95% من {pct(fig['wilson_low'])} إلى {pct(fig['wilson_high'])}")
    for lang, v in fig["by_lang"].items():
        print(f"  {lang}: {v['correct']} من {v['n']}")
    print(f"إخفاقات الاستناد: {fig['grounding_failures']} من {fig['n']}")
    print("النتائج:", "، ".join(f"{k} {v}" for k, v in sorted(fig["outcomes"].items())))
    print(f"التكلفة لكل إجابة صحيحة: {fig['cost_per_correct_sar']:.2f} ريال "
          f"(النموذج {fig['model_cost_sar']:.4f} ريال، المراجعة {fig['review_cost_sar']:.2f} ريال)")
