"""The cost model of labs 3.3 and 3.4, written in Python so the workbook's formulas can be checked against it.

It reads only the input sheets of a cost workbook (assumptions, the four option sheets, the missing items), never
the formula sheets.
"""
from __future__ import annotations

from openpyxl import load_workbook

OPTIONS = ["A", "B", "C", "D"]


def read_inputs(path) -> dict:
    wb = load_workbook(path, data_only=False)
    a = {r[0]: r[2] for r in wb["الافتراضات"].iter_rows(min_row=2, values_only=True) if r[0] and r[0] != "cost_per_minute"}
    opts = {}
    for o in OPTIONS:
        opts[o] = [(r[0], r[1], float(r[2])) for r in wb[f"الخيار {o}"].iter_rows(min_row=2, values_only=True) if r[0]]
    missing = [(r[0], r[2], float(r[3]), r[4].split()) for r in wb["بنود غائبة"].iter_rows(min_row=2, values_only=True) if r[0]]
    return {"a": a, "options": opts, "missing": missing}


BENEFIT = {"A": {"ai": False, "share": "all"},
           "B": {"ai": True, "share": "all"}, "C": {"ai": True, "share": "all"}, "D": {"ai": True, "share": "ar"}}


def model(inp: dict, volume_factor=1.0, accuracy=None, token_price_factor=1.0, include_missing=True,
          realisation=1.0) -> dict:
    a = inp["a"]
    m = a["loaded_cost"] / (a["hours"] * 60)
    h = a["mean_handling"]
    acc = a["accuracy"] if accuracy is None else accuracy
    out = {}
    for o in OPTIONS:
        items = [(k, amt) for _, k, amt in inp["options"][o]]
        if include_missing:
            items += [(k, amt) for _, k, amt, opts in inp["missing"] if o in opts]
        share = a["ar_share"] if BENEFIT[o]["share"] == "ar" else 1.0
        one_off = sum(x for k, x in items if k == "one_off")
        years = []
        for y in (1, 2, 3):
            vol = a["in_scope_annual"] * volume_factor * (1 + a["growth"]) ** y
            adopt = a["adoption_y1"] if y == 1 else a["adoption_y2"]
            cost = sum(x for k, x in items if k == "annual") + sum(x for k, x in items if k == "per_agent_year") * a["agents"]
            per_draft = sum(x for k, x in items if k == "per_drafted_answer")
            if o == "C":
                per_draft *= token_price_factor
            cost += per_draft * vol * adopt * share
            if BENEFIT[o]["ai"]:
                ben = vol * share * adopt * (acc * a["saving_when_usable"] * h - a["review_minutes"]) * m
            else:
                ben = vol * (a["a_handling_cut"] + a["a_deflection"]) * h * m
            years.append((cost, ben * realisation))
        net = -one_off + sum(b - c for c, b in years)
        cum, be = -one_off, None
        if cum >= 0:
            be = 0
        for t in range(1, 37):
            c, b = years[(t - 1) // 12]
            cum += (b - c) / 12
            if be is None and cum >= 0:
                be = t
        out[o] = {"one_off": one_off, "cost": [c for c, _ in years], "benefit": [b for _, b in years],
                  "tco3": one_off + sum(c for c, _ in years), "net3": net, "break_even_month": be}
    return out
