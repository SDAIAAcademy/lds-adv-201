"""Texts of the capstone case: replies to residents' objections against municipal violation fines.

The same fictional agency (Al-Hadaba Municipal Services Agency), a second use case the participant has not seen.
Every name, number and rule is fictional and synthetic.
"""

CATEGORIES = [
    # key, Arabic name, share, median drafting minutes, probability of an appeal after the reply
    ("shop_hygiene", "نظافة المحلات الغذائية", 0.24, 24.0, 0.10),
    ("signage_violation", "اللوحات المخالفة", 0.18, 18.0, 0.07),
    ("building_violation", "مخالفات البناء", 0.16, 38.0, 0.18),
    ("pavement_occupation", "إشغال الأرصفة", 0.14, 16.0, 0.06),
    ("waste_dumping", "رمي المخلفات", 0.12, 20.0, 0.09),
    ("licence_expired", "ممارسة نشاط برخصة منتهية", 0.16, 15.0, 0.05),
]

SUBJECTS = {
    "shop_hygiene": ["اعتراض على مخالفة نظافة", "المخالفة غير صحيحة", "Hygiene fine objection"],
    "signage_violation": ["اعتراض على مخالفة لوحة", "اللوحة مرخصة", "Sign fine objection"],
    "building_violation": ["اعتراض على مخالفة بناء", "الأعمال مرخصة", "Building fine objection"],
    "pavement_occupation": ["اعتراض على مخالفة إشغال", "Pavement fine objection"],
    "waste_dumping": ["اعتراض على مخالفة مخلفات", "لست صاحب المخلفات"],
    "licence_expired": ["اعتراض على مخالفة رخصة", "جددت الرخصة قبل المخالفة", "Expired licence fine"],
}

ARTICLES = [
    ("B01", "shop_hygiene", "reg_public", "agency", "2026-02-01",
     "غرامة مخالفة نظافة المحل الغذائي في المرة الأولى 1,000 ريال، وتتضاعف عند التكرار خلال سنة.", None),
    ("B02", "signage_violation", "reg_public", "agency", "2026-02-01",
     "غرامة اللوحة غير المرخصة 500 ريال، وتُزال اللوحة إذا لم تُرخص خلال 30 يومًا.", None),
    ("B03", "building_violation", "reg_public", "agency", "2025-06-15",
     "غرامة البناء دون رخصة 5,000 ريال للمخالفة البسيطة.", None),
    ("B04", "pavement_occupation", "reg_public", "agency", "2026-02-01",
     "غرامة إشغال الرصيف دون تصريح 300 ريال عن كل يوم يثبته المراقب.", None),
    ("B05", "waste_dumping", "reg_public", "agency", "2026-02-01",
     "غرامة رمي المخلفات في غير أماكنها 2,000 ريال، ويُلزم المخالف بالإزالة.", None),
    ("B06", "licence_expired", "reg_public", "agency", "2026-02-01",
     "غرامة ممارسة النشاط برخصة منتهية 800 ريال، وتسقط إذا ثبت أن التجديد سبق تاريخ المخالفة.", None),
    ("B07", "general", "reg_public", "agency", "2026-02-01",
     "يُقبل الاعتراض إذا قدم المعترض دليلًا على خطأ في هوية المخالف أو تاريخ المخالفة أو وصفها.",
     "An objection is accepted if the objector proves an error in the identity of the offender, the date or the description of the violation."),
    ("B08", "general", "reg_public", "agency", "2026-02-01",
     "يُقدَّم الاعتراض خلال 30 يومًا من تاريخ الإشعار، ولا يُنظر فيما يُقدَّم بعدها.",
     "An objection is filed within 30 days of the notice; later objections are not considered."),
    ("B09", "general", "reg_public", "agency", "2026-02-01",
     "يُبت في الاعتراض خلال 20 يوم عمل، ويُبلَّغ المعترض بالقرار وأسبابه كتابةً.",
     "An objection is decided within 20 business days and the objector is told the decision and its reasons in writing."),
    ("B10", "general", "reg_public", "agency", "2026-02-01",
     "يحق لمن رُفض اعتراضه التظلم أمام لجنة المراجعة خلال 15 يومًا من إبلاغه.",
     "An objector whose objection is rejected may appeal to the review committee within 15 days of being told."),
    ("B11", "general", "reg_public", "agency", "2026-02-01",
     "يُعلَّق سداد الغرامة حتى البت في الاعتراض.", "Payment of the fine is suspended until the objection is decided."),
    ("B12", "shop_hygiene", "reg_public", "agency", "2026-02-01",
     "يكفي في اعتراض النظافة تقرير زيارة لاحقة يثبت إزالة المخالفة، ولا يُسقط الغرامة إلا خطأ في الضبط.", None),
    ("B13", "building_violation", "reg_public", "agency", "2026-02-01",
     "إذا كانت الأعمال مشمولة برخصة ترميم سارية وقت الضبط سقطت مخالفة البناء.", None),
    ("B14", "waste_dumping", "reg_public", "agency", "2026-02-01",
     "يُقبل اعتراض رمي المخلفات إذا لم تثبت الصور أو المحضر صلة المعترض بالمخلفات.", None),
    ("B15", "signage_violation", "reg_public", "agency", "2026-02-01",
     "تسقط مخالفة اللوحة إذا قدّم المعترض تصريحًا ساريًا وقت الضبط.", None),
    ("B16", "pavement_occupation", "reg_public", "agency", "2026-02-01",
     "يُخفَّض أيام إشغال الرصيف إلى ما يثبته المحضر بالتاريخ.", None),
    ("B17", "general", "reg_public", "agency", "2026-02-01",
     "يكتب رد الاعتراض بلغة واضحة ويذكر المادة التي استند إليها القرار.", None),
    ("B18", "general", "reg_public", "agency", "2026-02-01",
     "لا يجوز أن يتضمن الرد بيانات شخص آخر غير المعترض.", None),
    ("B19", "general", "reg_public", "agency", "2024-11-01",
     "يُبت في الاعتراض خلال 30 يوم عمل.", None),
    ("B20", "general", "legal_internal", "agency", "2026-03-10",
     "توجيه داخلي للتسوية: يُقبل اعتراض المحلات الصغيرة في المرة الأولى إذا كانت الغرامة أقل من 1,000 ريال. لا يُذكر هذا التوجيه في الردود.", None),
    ("B21", "general", "legal_internal", "agency", "2026-03-10",
     "مستهدف الرقابة للربع: خفض نسبة الاعتراضات المقبولة إلى 20%.", None),
    ("B22", "general", "vendor_templates", "vendor", "2025-12-01",
     "قالب رد الاعتراض: التحية، ورقم المخالفة، والقرار، والأسباب، وحق التظلم، والختام.", None),
    ("B23", "general", "reg_public", "agency", "2026-02-01",
     "إذا قُبل الاعتراض أُلغيت الغرامة وأُعيد ما سُدد منها خلال 14 يومًا.", None),
    ("B24", "building_violation", "reg_public", "agency", "2026-05-20",
     "تعديل لائحة المخالفات لعام 2026: أصبحت غرامة البناء دون رخصة 7,500 ريال للمخالفة البسيطة.", None),
]

TITLES = {
    "B01": "غرامة النظافة", "B02": "غرامة اللوحة", "B03": "غرامة البناء", "B04": "غرامة إشغال الرصيف",
    "B05": "غرامة المخلفات", "B06": "غرامة الرخصة المنتهية", "B07": "أسباب قبول الاعتراض", "B08": "مهلة الاعتراض",
    "B09": "مدة البت", "B10": "التظلم", "B11": "تعليق السداد", "B12": "اعتراض النظافة", "B13": "اعتراض البناء",
    "B14": "اعتراض المخلفات", "B15": "اعتراض اللوحة", "B16": "اعتراض الإشغال", "B17": "صياغة الرد",
    "B18": "بيانات الآخرين", "B19": "مدة البت (قديم)", "B20": "توجيه التسوية الداخلي", "B21": "مستهدف الرقابة",
    "B22": "قالب الرد", "B23": "إعادة المبالغ", "B24": "تعديل اللائحة 2026",
}

CLASSIFICATION = {"reg_public": "عام", "legal_internal": "مقيد", "vendor_templates": "مقيد"}
OWNER = {"reg_public": "الإدارة القانونية", "legal_internal": "الإدارة القانونية", "vendor_templates": "مورد نظام المراسلات"}
LICENCE = {"agency": "محتوى من إعداد الهيئة", "vendor": "مرخص للاستخدام داخل نظام المراسلات فقط"}

ACCESS_COLUMNS = ["role", "reg_public", "legal_internal", "vendor_templates", "case_files"]
ACCESS = [
    ("officer", "R", "-", "R", "R"),
    ("legal_advisor", "R", "R", "R", "R"),
    ("svc-jawab", "R", "R", "R", "R"),
]

QUESTIONS = [
    ("q01", "ar", "shop_hygiene", "كم غرامة مخالفة نظافة المحل الغذائي في المرة الأولى؟", "yes", "1000", "B01"),
    ("q02", "ar", "signage_violation", "متى تُزال اللوحة غير المرخصة؟", "yes", "30 يوم", "B02"),
    ("q03", "ar", "building_violation", "كم غرامة البناء دون رخصة للمخالفة البسيطة؟", "yes", "7500", "B24"),
    ("q04", "ar", "pavement_occupation", "كيف تُحسب غرامة إشغال الرصيف؟", "yes", "300", "B04"),
    ("q05", "ar", "waste_dumping", "كم غرامة رمي المخلفات في غير أماكنها؟", "yes", "2000", "B05"),
    ("q06", "ar", "licence_expired", "متى تسقط غرامة ممارسة النشاط برخصة منتهية؟", "yes", "سبق تاريخ المخالفة", "B06"),
    ("q07", "ar", "general", "ما أسباب قبول الاعتراض على المخالفة؟", "yes", "هوية المخالف", "B07"),
    ("q08", "ar", "general", "ما مهلة تقديم الاعتراض على المخالفة؟", "yes", "30 يوم", "B08"),
    ("q09", "ar", "general", "في كم يومًا يُبت في الاعتراض؟", "yes", "20 يوم عمل", "B09"),
    ("q10", "ar", "general", "هل يحق للمعترض التظلم إذا رُفض اعتراضه؟", "yes", "لجنة المراجعة", "B10"),
    ("q11", "ar", "general", "هل يسدد المعترض الغرامة قبل البت في اعتراضه؟", "yes", "يعلق", "B11"),
    ("q12", "ar", "shop_hygiene", "هل يسقط تقرير الزيارة اللاحقة مخالفة النظافة؟", "yes", "خطا في الضبط", "B12"),
    ("q13", "ar", "building_violation", "متى تسقط مخالفة البناء إذا كانت الأعمال ترميمًا؟", "yes", "رخصة ترميم سارية", "B13"),
    ("q14", "ar", "waste_dumping", "متى يُقبل الاعتراض على مخالفة رمي المخلفات؟", "yes", "صله المعترض", "B14"),
    ("q15", "ar", "signage_violation", "ما الذي يُسقط مخالفة اللوحة؟", "yes", "تصريحا ساريا", "B15"),
    ("q16", "ar", "general", "هل نقبل اعتراض محل صغير في مخالفته الأولى إذا كانت الغرامة قليلة؟", "yes", "هويه المخالف", "B07"),
    ("q17", "ar", "general", "ما نسبة الاعتراضات التي تقبلها الهيئة عادة؟", "no", "", ""),
    ("q18", "ar", "general", "هل يمكن تقسيط الغرامة بعد رفض الاعتراض؟", "no", "", ""),
    ("q19", "ar", "general", "متى تُعاد الغرامة المسددة إذا قُبل الاعتراض؟", "yes", "14 يوم", "B23"),
    ("q20", "ar", "general", "ما الذي يجب أن يذكره رد الاعتراض؟", "yes", "الماده", "B17"),
    ("q21", "ar", "general", "هل أذكر في الرد بيانات جار المعترض الذي شهد المخالفة؟", "yes", "شخص اخر", "B18"),
    ("q22", "ar", "general", "هل يُطلب من المعترض حضور جلسة استماع؟", "no", "", ""),
    ("q23", "en", "general", "How long does the objector have to file an objection?", "yes", "30 days", "B08"),
    ("q24", "en", "general", "How long does the agency take to decide an objection?", "yes", "20 business days", "B09"),
    ("q25", "en", "general", "Can a rejected objector appeal?", "yes", "review committee", "B10"),
    ("q26", "en", "general", "Must the fine be paid while the objection is pending?", "yes", "suspended", "B11"),
    ("q27", "en", "building_violation", "What is the fine for minor building work without a permit?", "yes", "7,500|7500", "B24"),
    ("q28", "en", "general", "On what grounds is an objection accepted?", "yes", "identity", "B07"),
    ("q29", "en", "signage_violation", "What cancels a signage violation?", "yes", "valid permit", "B15"),
    ("q30", "en", "general", "Can the fine be reduced for good conduct?", "no", "", ""),
]

REQUEST_MEMO = """مذكرة داخلية
من: مدير الإدارة القانونية
إلى: فريق التحول الرقمي
الموضوع: مساعد ذكي لصياغة ردود الاعتراضات على المخالفات

يتأخر الرد على اعتراضات السكان على المخالفات البلدية، ويشكو المعترضون من ردود قصيرة لا تذكر أسباب القرار. ويقضي موظفو الاعتراضات وقتًا طويلًا في البحث في اللائحة وصياغة الرد.

نقترح مساعدًا يقرأ الاعتراض ومرفقاته ويقترح القرار ويصوغ الرد. نريد تقييم الجدوى ودراسة جدوى مقدرة التكاليف قبل عرضها على لجنة التوجيه.
"""

INTERVIEWS = """ملاحظات المقابلات (فريق التحول الرقمي)

1) رئيسة قسم الاعتراضات
- في القسم 14 موظفًا. يقرأ الموظف الاعتراض ومرفقاته، ويبحث في اللائحة، ويكتب الرد، ثم يعتمده مستشار قانوني.
- الوقت الأطول في مخالفات البناء.
- نصف الاعتراضات تقريبًا تُرفض، ويتظلم بعض المرفوضين أمام لجنة المراجعة.
- لو جاءت مسودة رد جاهزة، يحتاج الموظف نحو 4 دقائق ليتحقق منها ومن المادة التي تستند إليها.

2) أمين البيانات
- مواد اللائحة 24 مقالًا في قاعدة المعرفة، وفيها توجيهات داخلية للمستشارين فقط.
- انتقل نظام الاعتراضات إلى منصة جديدة في الصيف، ولم تُنقل بعض السجلات.
- قالب الرد جاء مع نظام المراسلات الحالي.

3) مسؤولة حماية البيانات
- ملفات الاعتراضات فيها هويات وصور وأحيانًا تقارير طبية يقدمها المعترض دليلًا.
- القرار في الاعتراض يمس مال المعترض وحقه، فلا يتخذه نظام آلي.

4) الشريك المالي
- التكلفة السنوية المحمَّلة لموظف الاعتراضات 240,000 ريال، وساعات العمل المنتجة 1,540 ساعة في السنة.
- قاعدة الاسترداد خلال 24 شهرًا نفسها.
"""

DATA_DICTIONARY = """قاموس بيانات سجل الاعتراضات (objections.csv)
الفترة: 26 أسبوعًا (182 يومًا) من 4 يناير 2026 إلى 4 يوليو 2026. اصطناعي بالكامل.

objection_id          معرّف الاعتراض
received_date         تاريخ الاستلام
channel               القناة: web_form أو app_chat أو email
language              لغة الاعتراض: ar أو en
category              نوع المخالفة
subject               عنوان الاعتراض كما كتبه المعترض
officer_id            معرّف الموظف
drafting_minutes      دقائق عمل الموظف على صياغة الرد
status                closed أو auto_closed (أغلقه النظام بعد بقائه مفتوحًا)
days_to_decision      الأيام حتى القرار
appealed              هل تظلم المعترض بعد الرد: yes أو no
qa_sample_type        none أو targeted أو random
qa_result             correct أو wrong_info أو incomplete؛ فارغ إن لم يُدقق

ملاحظة: انتقل النظام إلى منصة جديدة خلال الفترة.
"""

STAFF_COSTS = [
    ("عدد موظفي الاعتراضات", 14, "موظف"),
    ("التكلفة السنوية المحمَّلة للموظف", 240000, "ريال"),
    ("ساعات العمل المنتجة للموظف في السنة", 1540, "ساعة"),
    ("عدد المستشارين القانونيين المعتمِدين", 3, "مستشار"),
]

OPTIONS = {
    "A": {"name": "تغيير الإجراء: مكتبة ردود وقائمة تحقق للأسباب", "items": [
        ("مكتبة ردود معتمدة لكل نوع مخالفة", "one_off", 60000, "yes"),
        ("قائمة تحقق للأسباب والمواد", "one_off", 20000, "yes"),
        ("صيانة المكتبة", "annual", 25000, "yes")],
        "benefit": {"handling_cut": 0.15, "deflection": 0.0, "languages": "ar en", "ai": False}},
    "B": {"name": "شراء خدمة صياغة قانونية سحابية", "items": [
        ("التهيئة", "one_off", 70000, "yes"),
        ("ترخيص المقعد السنوي", "per_agent_year", 9000, "yes")],
        "benefit": {"languages": "ar en", "ai": True}},
    "C": {"name": "بناء «جواب» للاعتراضات", "items": [
        ("بناء الخدمة (فريق داخلي)", "one_off", 220000, "yes"),
        ("الاستضافة والفهرس", "annual", 30000, "yes"),
        ("الوحدات النصية للنموذج", "per_drafted_answer", 0.004, "yes")],
        "benefit": {"languages": "ar en", "ai": True}},
    "D": {"name": "الشراكة مع منصة «ركيزة»", "items": [
        ("الانضمام", "one_off", 90000, "yes"),
        ("رسوم كل مسودة", "per_drafted_answer", 1.2, "yes")],
        "benefit": {"languages": "ar", "ai": True}},
}

MISSING = [
    ("evaluation", "التقييم الدوري ومراجعة المستشار لعينة شهرية", "annual", 60000, "B C D"),
    ("kb_maintenance", "صيانة مواد اللائحة بعد كل تعديل", "annual", 25000, "B C D"),
    ("rights_fix", "قالب رد مستقل عن قالب المورد", "one_off", 8000, "C D"),
    ("local_hosting", "الاستضافة داخل المملكة: 30% فوق ترخيص المقعد", "per_agent_year", 2700, "B"),
]

ASSUMPTIONS = [
    ("growth", "نمو عدد الاعتراضات السنوي", 0.04),
    ("a_handling_cut", "الخيار A: نسبة خفض زمن الصياغة بمكتبة الردود", 0.15),
    ("a_deflection", "الخيار A: نسبة الاعتراضات التي تغني عنها الصفحات المحدثة", 0.0),
    ("hours", "ساعات العمل المنتجة للموظف في السنة", 1540),
    ("loaded_cost", "التكلفة السنوية المحمَّلة للموظف", 240000),
    ("agents", "عدد الموظفين", 14),
    ("saving_when_usable", "نسبة زمن الصياغة الموفَّرة حين تصلح المسودة (فرضية)", 0.45),
    ("review_minutes", "دقائق مراجعة كل مسودة", 4.0),
    ("adoption_y1", "نسبة الاستخدام في السنة الأولى", 0.6),
    ("adoption_y2", "نسبة الاستخدام في السنتين الثانية والثالثة", 0.9),
    ("ar_share", "نسبة الاعتراضات العربية", None),
    ("accuracy", "الدقة الإجمالية للنموذج (من تجربتك)", None),
    ("accuracy_low", "الحد الأدنى لفترة الثقة 95% (من تجربتك)", None),
    ("in_scope_annual", "الاعتراضات السنوية (سنة الأساس)", None),
    ("mean_handling", "متوسط دقائق الصياغة", None),
]

CASE_TOPICS = [
    ("shop_hygiene", "أعترض على مخالفة النظافة لأن المراقب زار محلًا آخر بالاسم نفسه.", None),
    ("building_violation", "الأعمال ترميم داخلي مرخص، وأرفقت الرخصة.", None),
    ("waste_dumping", "المخلفات ليست لي، وأرفقت صور الكاميرا.", None),
    ("licence_expired", "جددت الرخصة قبل يومين من المخالفة.", None),
    ("shop_hygiene", "كان المحل مغلقًا لأني كنت أتلقى علاجًا كيميائيًا، وأرفقت التقرير الطبي.", "health"),
    ("pavement_occupation", "الإشغال كان يومًا واحدًا لا خمسة أيام.", None),
    ("signage_violation", "اللوحة مرخصة، وأرفقت التصريح.", None),
    ("building_violation", "جاري المسن هو من بنى السور، وهذه بيانات هويته.", "third_party"),
    ("waste_dumping", "ابني ذو الثلاث عشرة سنة هو من وضع الكيس بجانب الحاوية.", "child"),
    ("licence_expired", "أرجو إعادة الغرامة إلى حسابي البنكي.", "iban"),
]
