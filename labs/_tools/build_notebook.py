# /// script
# requires-python = ">=3.11"
# ///
"""Write the spike notebook twice from the cells below:

    labs/spike/jawab_spike.ipynb       for participants: the second run starts from the starter settings
    labs/solutions/jawab_spike.ipynb   the reference: the second run with the adapted settings of lab 2.4

    uv run labs/_tools/build_notebook.py
"""
from __future__ import annotations

import json
from pathlib import Path

LABS = Path(__file__).resolve().parents[1]

MD, CODE = "markdown", "code"

SETUP = '''# الإعداد: يعمل في Colab وفي JupyterLab وعلى حاسوب محمول دون تثبيت أي مكتبة
import os, sys
from pathlib import Path

if "google.colab" in sys.modules:
    if not Path("lds-adv-201").exists():
        os.system("git clone -q https://github.com/SDAIAAcademy/lds-adv-201")
    os.chdir("lds-adv-201/labs/spike")
else:
    here = Path.cwd()
    for p in [here, *here.parents]:
        if (p / "labs" / "spike" / "jawab.py").exists():
            os.chdir(p / "labs" / "spike")
            break
        if (p / "jawab.py").exists():
            os.chdir(p)
            break
sys.path.insert(0, str(Path.cwd()))
import jawab as J
print("المجلد:", Path.cwd().name, "· النموذج:", os.environ.get("LLM_MODEL") or "البديل الاستخراجي (لا نموذج لغوي)")'''

MODEL = '''# اختياري: نموذج لغوي عبر واجهة محادثة غير مرتبطة بمقدم خدمة بعينه
# في Colab أضف المفاتيح في لوحة Secrets، ثم أزل علامة التعليق من الأسطر الأربعة التالية:
# from google.colab import userdata
# os.environ["LLM_BASE_URL"] = "https://openrouter.ai/api/v1"
# os.environ["LLM_MODEL"] = "google/gemma-4-31b-it:free"
# os.environ["LLM_API_KEY"] = userdata.get("LLM_API_KEY")
print("نموذج لغوي" if J.using_model() else "البديل الاستخراجي: لا مفتاح، فكل رقم هنا رقم الاسترجاع والإعدادات وحدها")'''

STARTER_RUN = '''CASE = "enquiries"     # المشروع الختامي: "objections"
ROLE = "agent"         # المشروع الختامي: "officer"

starter = dict(J.STARTER, case=CASE, role=ROLE, label=f"{CASE}_starter")
# المشروع الختامي: دقائق المراجعة وتكلفة الدقيقة من ملاحظات المقابلات وورقة التكاليف في حزمة الحالة
# starter["review_minutes"] = ...
# starter["sar_per_minute"] = ...
rows_starter, fig_starter = J.run(starter)
J.show(fig_starter)
print("سجل التشغيل:", f"runs/{starter['label']}.csv", "و", f"runs/{starter['label']}.json")'''

REVIEW = '''# خمس إجابات تراجعها بيدك قبل أن تثق بالتصحيح الآلي
import csv
labels = {q["qid"]: q for q in J.read_csv(J.CASES[CASE] / "questions.csv")}
for r in rows_starter[:5]:
    print(r["qid"], "|", r["question"])
    print("   الإجابة:", r["answer"])
# احكم على الإجابات الخمس في جدولك أولًا، ثم شغّل الخلية التالية لترى الوسم وحكم التصحيح الآلي'''

REVEAL = '''# الوسم وحكم التصحيح الآلي للإجابات الخمس
for r in rows_starter[:5]:
    q = labels[r["qid"]]
    print(r["qid"], "· المتوقع:", q["gold_fact"] or "امتناع", "من", q["gold_articles"] or "لا مصدر", "· التصحيح الآلي:", r["outcome"])'''

ADAPT_PARTICIPANT = '''# التكييف (المختبر 2.4): غيّر الإعدادات ثم شغّل الخلية. لا تغيّر الأسئلة ولا التصحيح.
adapted = dict(starter, label=f"{CASE}_adapted")
adapted["exclude_articles"] = []          # مقالات تستبعدها: المتقادمة والمتعارضة التي وجدتها في المختبر 1.4
adapted["respect_permissions"] = False    # True: يقرأ الاسترجاع ما يحق للدور فقط
adapted["chunking"] = "article"           # "article" أو "paragraph"
adapted["min_score"] = 0.0                # عتبة الامتناع: تحتها يمتنع النموذج ويحيل إلى المختص

rows_adapted, fig_adapted = J.run(adapted)
J.show(fig_adapted)'''

ADAPT_SOLUTION = '''# التكييف (المختبر 2.4): الإعدادات المرجعية
adapted = dict(starter, label=f"{CASE}_adapted")
adapted["exclude_articles"] = ["A01", "A09", "A14", "A18", "A26", "A11"] if CASE == "enquiries" else ["B03", "B19"]
adapted["respect_permissions"] = True
adapted["chunking"] = "paragraph"
adapted["min_score"] = 0.25

rows_adapted, fig_adapted = J.run(adapted)
J.show(fig_adapted)
if CASE == "enquiries":
    assert fig_adapted["correct"] == 23, fig_adapted["correct"]'''

COMPARE = '''# مقارنة مزدوجة: السؤال نفسه في التشغيلين
flips = J.compare(rows_starter, rows_adapted)
print("تحسّن:", flips["fixed"])
print("ساء:", flips["broken"])
print("صحيح في الاثنين:", flips["both_right"], "· خطأ في الاثنين:", flips["both_wrong"])'''

DECIDE = '''# القرار مقابل العتبة التي كتبتها قبل التجربة (المختبر 1.3). غيّر الأرقام إلى عتبتك.
THRESHOLD = {"accuracy": 0.80, "lower_bound": 0.65}
f = fig_adapted
meets = (f["accuracy"] >= THRESHOLD["accuracy"] and f["wilson_low"] >= THRESHOLD["lower_bound"]
         and f["outcomes"].get("permission_leak", 0) == 0)
print(f"الدقة {f['accuracy']:.1%} · الحد الأدنى {f['wilson_low']:.1%} · تسريب الصلاحيات {f['outcomes'].get('permission_leak', 0)}")
print("يستوفي العتبة" if meets else "لا يستوفي العتبة: إعادة عمل أو توقف، بحسب أسباب الإخفاق")'''


def cells(solution: bool):
    return [
        (MD, "# دفتر التجربة: النموذج الأولي «جواب»\n\n"
             "مقرر LDS-ADV-201 · المختبران 2.2 و2.4 والمشروع الختامي.\n\n"
             "يسترجع «جواب» أقرب مقاطع قاعدة المعرفة لكل سؤال من فهرس متجهات في الذاكرة، ثم يصوغ مسودة إجابة، "
             "ثم يصحّحها مقابل الوسم، ويكتب سجل تشغيل في `runs/`. كل رقم في جدول نتائجك يعود إلى سجل تشغيل.\n\n"
             "بلا مفتاح يصوغ المسودة **بديل استخراجي**: ينسخ أقرب جملة في المقطع الأول ويستشهد به. لا يترجم ولا يعيد الصياغة، "
             "فيُظهر أثر الاسترجاع والإعدادات وحدها. قل في جدولك أيهما أنتج الأرقام."),
        (CODE, SETUP),
        (MD, "## 1 · النموذج\n\nاختياري. الأرقام في الشرائح وفي مفتاح المدرّب من البديل الاستخراجي. "
             "النماذج المجانية لها حدود للطلبات في الدقيقة واليوم، والدفتر يحفظ كل رد في `cache/` فلا تتكرر الطلبات."),
        (CODE, MODEL),
        (MD, "## 2 · التشغيل المبدئي (المختبر 2.2)\n\nالإعدادات كما سُلّمت: لا استبعاد، ولا احترام للصلاحيات، ولا امتناع."),
        (CODE, STARTER_RUN),
        (MD, "## 3 · راجع بيدك\n\nاقرأ الإجابات الخمس، واحكم عليها بمعيار الإجابة الصحيحة في ميثاقك قبل أن تنظر إلى حكم التصحيح الآلي."),
        (CODE, REVIEW),
        (CODE, REVEAL),
        (MD, "## 4 · التكييف وإعادة القياس (المختبر 2.4)\n\nغيّر ثلاثة إعدادات على الأقل، وشغّل على الأسئلة الثلاثين نفسها."),
        (CODE, ADAPT_SOLUTION if solution else ADAPT_PARTICIPANT),
        (CODE, COMPARE),
        (CODE, DECIDE),
        (MD, "## 5 · ما تحمله معك\n\nملفا التشغيلين في `runs/`: انسخ أرقامهما إلى جدول النتائج، وأرفق الملفين بدراسة الجدوى."),
    ]


def notebook(solution: bool) -> dict:
    out = []
    for kind, src in cells(solution):
        lines = src.splitlines(keepends=True)
        cell = {"cell_type": kind, "metadata": {}, "source": lines}
        if kind == CODE:
            cell.update({"execution_count": None, "outputs": []})
        out.append(cell)
    return {"cells": out, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                       "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}


def main():
    for path, sol in ((LABS / "spike" / "jawab_spike.ipynb", False), (LABS / "solutions" / "jawab_spike.ipynb", True)):
        path.write_text(json.dumps(notebook(sol), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("wrote", path.relative_to(LABS))


if __name__ == "__main__":
    main()
