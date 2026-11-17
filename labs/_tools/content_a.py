"""Texts of the course case: Al-Hadaba Municipal Services Agency, use case Jawab (enquiry answers).

Every name, number, fee and rule here is fictional and synthetic.
"""

CATEGORIES = [
    # key, Arabic name, share of demand, median handling minutes, repeat-contact probability
    ("renew_licence", "تجديد رخصة نشاط تجاري", 0.17, 8.0, 0.08),
    ("new_licence", "إصدار رخصة نشاط تجاري", 0.09, 12.0, 0.10),
    ("minor_works", "رخصة ترميم لأعمال بسيطة", 0.09, 11.0, 0.11),
    ("signage", "تصريح لوحة إعلانية", 0.06, 9.0, 0.09),
    ("waste", "حاويات النفايات ومخلفات البناء", 0.08, 6.0, 0.07),
    ("payments", "سداد الرسوم والاسترداد", 0.12, 7.0, 0.09),
    ("parks", "حجز مرافق الحدائق", 0.04, 6.0, 0.06),
    ("violations", "الاستعلام عن المخالفات", 0.07, 9.0, 0.12),
    ("excavation", "تصريح حفر", 0.06, 13.0, 0.14),
    ("street_vending", "تصريح البيع المتجول", 0.05, 10.0, 0.13),
    ("complaint_followup", "متابعة بلاغ أو شكوى", 0.12, 14.0, 0.27),
    ("other", "أخرى", 0.05, 8.0, 0.10),
]

SUBJECTS = {
    "renew_licence": ["تجديد الرخصة التجارية", "رسوم تجديد الرخصة", "انتهت رخصة المحل", "Licence renewal"],
    "new_licence": ["فتح محل جديد", "متطلبات رخصة نشاط", "New shop licence"],
    "minor_works": ["ترميم واجهة المنزل", "رخصة ترميم", "Renovation permit"],
    "signage": ["لوحة المحل", "مقاس اللوحة الإعلانية", "Shop sign permit"],
    "waste": ["طلب حاوية", "رفع مخلفات بناء", "Waste container"],
    "payments": ["سداد فاتورة", "استرداد مبلغ", "Refund request"],
    "parks": ["حجز قاعة الحديقة", "إلغاء حجز", "Park hall booking"],
    "violations": ["استعلام عن مخالفة", "مخالفة على المحل", "Violation notice"],
    "excavation": ["تصريح حفر لتمديد", "حفر أمام المنزل", "Excavation permit"],
    "street_vending": ["عربة طعام", "تصريح بيع متجول", "Food truck permit"],
    "complaint_followup": ["متابعة بلاغ سابق", "لم يُحل البلاغ", "Complaint follow-up"],
    "other": ["استفسار عام", "رسوم الرخصة", "اقتراح", "General question"],
}

# article id, category, collection, source, last reviewed, Arabic text, English text or None
ARTICLES = [
    ("A01", "renew_licence", "kb_public", "agency", "2025-11-02",
     "رسوم تجديد رخصة النشاط التجاري 600 ريال للسنة الواحدة. تُدفع الرسوم إلكترونيًا قبل إصدار الرخصة المجددة. لا تشمل الرسوم غرامات التأخير.",
     "The renewal fee for a commercial activity licence is 600 riyals a year. The fee is paid online before the renewed licence is issued. It does not include late penalties."),
    ("A02", "renew_licence", "kb_public", "agency", "2026-02-10",
     "مستندات تجديد رخصة النشاط التجاري: سجل تجاري سارٍ، وعقد إيجار موثق، وشهادة سلامة سارية. تُرفع المستندات في تطبيق الهيئة.",
     None),
    ("A03", "renew_licence", "kb_public", "agency", "2026-03-01",
     "غرامة التأخير في تجديد رخصة النشاط التجاري 100 ريال عن كل شهر تأخير. تبدأ الغرامة بعد انتهاء الرخصة بشهر واحد.",
     "The late penalty for renewing a commercial activity licence is 100 riyals for each month of delay. The penalty starts one month after the licence expires."),
    ("A04", "renew_licence", "kb_public", "agency", "2026-01-15",
     "تُجدَّد رخصة النشاط التجاري من تطبيق الهيئة دون زيارة. الرخصة المجددة سارية سنة واحدة من تاريخ التجديد.",
     "A commercial activity licence is renewed in the Hadaba app without a visit. A renewed licence is valid for one year from the renewal date."),
    ("A05", "new_licence", "kb_public", "agency", "2026-06-20",
     "رسوم إصدار رخصة نشاط تجاري جديدة 1,200 ريال. تشمل الرسوم زيارة التفتيش الأولى.",
     "The fee for a new commercial activity licence is 1,200 riyals. It includes the first inspection visit."),
    ("A06", "new_licence", "kb_public", "agency", "2026-02-11",
     "مستندات إصدار رخصة نشاط تجاري جديدة: سجل تجاري، وعقد إيجار موثق، ومخطط للموقع، وصورة الهوية الوطنية لصاحب النشاط.",
     None),
    ("A07", "new_licence", "kb_public", "agency", "2026-03-05",
     "مدة إصدار رخصة النشاط التجاري الجديدة 3 أيام عمل من اكتمال المستندات. تتأخر المدة إذا احتاج النشاط تفتيشًا مسبقًا.",
     "A new commercial activity licence is issued within 3 business days of complete documents. It takes longer if the activity needs a prior inspection."),
    ("A08", "new_licence", "kb_public", "agency", "2025-12-01",
     "الأنشطة التي تحتاج تفتيشًا قبل الترخيص: المطاعم، ومحلات الأغذية، والصالونات، والورش. يحدد المفتش موعد الزيارة خلال أسبوع.",
     None),
    ("A09", "minor_works", "kb_public", "agency", "2025-10-20",
     "رسوم رخصة الترميم للأعمال البسيطة 300 ريال. تُدفع الرسوم بعد قبول الطلب.",
     None),
    ("A10", "minor_works", "kb_public", "agency", "2026-02-14",
     "مستندات رخصة الترميم: صك الملكية أو عقد الإيجار، ووصف الأعمال، وصور الموقع الحالية.",
     "Documents for a renovation permit: the title deed or lease, a description of the works, and current photos of the site."),
    ("A11", "minor_works", "kb_public", "agency", "2024-09-30",
     "مدة إصدار رخصة الترميم للأعمال البسيطة 10 أيام عمل.",
     None),
    ("A12", "minor_works", "kb_public", "agency", "2026-04-18",
     "بعد ربط الطلبات بالتطبيق أصبحت مدة إصدار رخصة الترميم للأعمال البسيطة 5 أيام عمل من اكتمال الطلب.",
     None),
    ("A13", "minor_works", "kb_public", "agency", "2026-01-22",
     "الأعمال البسيطة هي الأعمال الداخلية والدهان وتبديل البلاط وإصلاح الواجهة دون تغيير في الهيكل الإنشائي. أي تعديل في الهيكل يحتاج رخصة بناء.",
     None),
    ("A14", "signage", "kb_public", "agency", "2025-09-14",
     "رسوم تصريح اللوحة الإعلانية 200 ريال لكل متر مربع في السنة.",
     "The signage permit fee is 200 riyals per square metre a year."),
    ("A15", "signage", "vendor_pack", "vendor", "2026-03-10",
     "لإصدار تصريح لوحة إعلانية ارفع صورة الواجهة وتصميم اللوحة بمقاساتها ورخصة النشاط السارية.",
     "To get a signage permit, upload a photo of the shopfront, the sign design with its dimensions and the valid activity licence."),
    ("A16", "signage", "kb_public", "agency", "2026-02-01",
     "الحد الأقصى لمساحة اللوحة الإعلانية على واجهة المحل 12 مترًا مربعًا، ولا تتجاوز اللوحة عرض الواجهة.",
     None),
    ("A17", "signage", "kb_public", "agency", "2026-02-01",
     "يُجدَّد تصريح اللوحة الإعلانية سنويًا مع رخصة النشاط التجاري.",
     "A signage permit is renewed every year together with the commercial activity licence."),
    ("A18", "waste", "kb_public", "agency", "2025-12-12",
     "إيجار حاوية النفايات 150 ريالًا للأسبوع، ويشمل التفريغ مرة واحدة.",
     None),
    ("A19", "waste", "kb_public", "agency", "2026-03-20",
     "تُطلب حاوية النفايات من تطبيق الهيئة، وتُسلَّم خلال 3 أيام عمل من السداد.",
     "Request a waste container in the Hadaba app; it is delivered within 3 business days of payment."),
    ("A20", "waste", "vendor_pack", "vendor", "2026-01-05",
     "تُرفع مخلفات البناء خلال يومين من الطلب في الأحياء المشمولة بالخدمة.",
     "Construction waste is removed within two days of the request in the districts the service covers."),
    ("A21", "waste", "kb_public", "agency", "2026-02-25",
     "يُمنع وضع المواد الكيميائية والبطاريات والإطارات في حاويات النفايات، ولها نقاط تجميع خاصة.",
     None),
    ("A22", "payments", "kb_public", "agency", "2026-04-02",
     "تُسدَّد الرسوم البلدية من تطبيق الهيئة أو من بوابة الدفع الإلكتروني، ولا يُقبل الدفع النقدي في المراكز.",
     "Municipal fees are paid in the Hadaba app or on the online payment portal; cash is not accepted at service centres."),
    ("A23", "payments", "vendor_pack", "vendor", "2026-02-02",
     "يمكن تقسيط الرسوم التي تزيد على 5,000 ريال على ثلاث دفعات شهرية.",
     None),
    ("A24", "payments", "kb_public", "agency", "2026-03-15",
     "يُعاد المبلغ المدفوع عن طلب مرفوض خلال 14 يومًا إلى الحساب الذي دُفع منه.",
     "A payment for a rejected application is refunded within 14 days to the account it was paid from."),
    ("A25", "payments", "kb_public", "agency", "2026-03-15",
     "للاعتراض على فاتورة رسوم ارفع الاعتراض من التطبيق مع سبب الاعتراض، وتُعلَّق مهلة السداد حتى البت فيه.",
     None),
    ("A26", "parks", "kb_public", "agency", "2025-08-30",
     "رسوم حجز قاعة الحديقة 250 ريالًا لليوم الواحد.",
     None),
    ("A27", "parks", "kb_public", "agency", "2026-02-18",
     "يُحجز مرفق الحديقة قبل أسبوع على الأقل، ويُدفع تأمين قدره 500 ريال يُعاد بعد الفعالية.",
     None),
    ("A28", "parks", "vendor_pack", "vendor", "2026-01-12",
     "يُلغى حجز مرفق الحديقة دون رسوم إذا أُلغي قبل 48 ساعة من الموعد.",
     "A park facility booking is cancelled free of charge if cancelled 48 hours before the booking."),
    ("A29", "violations", "kb_public", "agency", "2026-03-03",
     "يُستعلم عن المخالفات البلدية من التطبيق برقم الهوية أو رقم السجل التجاري.",
     "Municipal violations can be checked in the app with the ID number or the commercial registration number."),
    ("A30", "violations", "kb_public", "agency", "2026-03-03",
     "يحصل المخالف على خصم 25% إذا سدد المخالفة خلال 15 يومًا من إشعاره.",
     "A 25% discount applies when a violation is paid within 15 days of the notice."),
    ("A31", "violations", "kb_public", "agency", "2026-03-03",
     "يُقدَّم الاعتراض على المخالفة خلال 30 يومًا من الإشعار، من التطبيق، مع ما يدعمه من صور ومستندات.",
     None),
    ("A32", "payments", "kb_public", "agency", "2026-04-10",
     "يُقدَّم طلب الإعفاء من الرسوم من التطبيق مع المستندات الداعمة، وتبت فيه لجنة الإعفاءات خلال 15 يوم عمل.",
     None),
    ("A33", "payments", "kb_supervisor", "agency", "2026-04-10",
     "شروط قبول طلب الإعفاء من الرسوم البلدية (داخلي): يُعفى من الرسوم من يقل دخله الشهري عن 8,000 ريال، ويُعرض على اللجنة من يزيد دخله على ذلك. لا تُبلَّغ هذه المعايير للمستفيدين.",
     None),
    ("A34", "violations", "enforcement_notes", "agency", "2026-05-02",
     "أولويات التفتيش للربع الثالث: المطاعم في الأحياء الشمالية، ثم الورش غير المرخصة. لا تُنشر هذه الخطة.",
     None),
    ("A35", "other", "kb_internal", "agency", "2026-02-20",
     "التصعيد الداخلي: يُصعَّد الاستفسار إلى المشرف إذا تكرر التواصل ثلاث مرات أو ذكر المستفيد جهة رقابية.",
     None),
    ("A36", "other", "kb_supervisor", "agency", "2026-01-30",
     "شروط عقد مورد منصة مركز الاتصال: سعر المقعد السنوي، ومدة العقد ثلاث سنوات، وغرامة الإنهاء المبكر.",
     None),
    ("A37", "other", "kb_public", "agency", "2026-01-10",
     "قنوات التواصل مع الهيئة: نموذج الموقع، ومحادثة التطبيق، والبريد الإلكتروني، ومراكز الخدمة.",
     "Ways to contact the agency: the website form, the app chat, email and the service centres."),
    ("A38", "other", "kb_public", "agency", "2026-01-10",
     "يُسجَّل الحساب في تطبيق الهيئة برقم الهوية ورقم الجوال المسجل.",
     "An account in the Hadaba app is registered with the ID number and the registered mobile number."),
    ("A39", "other", "kb_public", "agency", "2025-12-20",
     "يُشترط العنوان الوطني المحدث لكل طلب ترخيص.",
     None),
    ("A40", "other", "kb_public", "agency", "2026-01-10",
     "تتوفر خدمات التطبيق باللغتين العربية والإنجليزية.",
     "The app's services are available in Arabic and English."),
    ("A41", "other", "vendor_pack", "vendor", "2025-11-11",
     "تعمل نافذة المحادثة في الموقع بتحويل المحادثة إلى أول موظف متاح.",
     "The website chat window passes the conversation to the first available agent."),
    ("A42", "other", "vendor_pack", "vendor", "2025-11-11",
     "لاستعادة كلمة المرور اختر «نسيت كلمة المرور» وأدخل رقم الجوال المسجل.",
     "To reset the password, choose Forgot password and enter the registered mobile number."),
    ("A43", "other", "kb_public", "agency", "2026-02-01",
     "إشعار الخصوصية: تستخدم الهيئة بيانات المستفيد لتقديم الخدمة المطلوبة فقط، ولا تشاركها إلا وفق الأنظمة.",
     "Privacy notice: the agency uses a resident's data only to provide the service requested and shares it only as the law allows."),
    ("A44", "complaint_followup", "kb_public", "agency", "2026-02-05",
     "يُقدَّم البلاغ أو الشكوى من التطبيق، ويصل للمستفيد رقم البلاغ في رسالة نصية.",
     None),
    ("A45", "other", "kb_public", "agency", "2026-02-05",
     "تُحجز مواعيد مراكز الخدمة من التطبيق قبل الزيارة.",
     None),
    ("A46", "other", "kb_public", "agency", "2026-03-25",
     "تعمل الخدمات الإلكترونية طوال أيام الإجازات الرسمية، وتُغلق مراكز الخدمة.",
     None),
    ("A47", "parks", "kb_public", "agency", "2026-06-01",
     "افتتحت الهيئة ثلاث حدائق جديدة في الأحياء الشرقية مزودة بقاعات للمناسبات.",
     None),
    ("A48", "other", "kb_public", "agency", "2026-05-28",
     "التعميم رقم 14 لعام 2026 بشأن تحديث الرسوم البلدية، ويسري من 1 يونيو 2026.\n"
     "أصبحت رسوم تجديد رخصة النشاط التجاري 750 ريالًا للسنة.\n"
     "أصبحت رسوم رخصة الترميم للأعمال البسيطة 400 ريال.\n"
     "أصبحت رسوم تصريح اللوحة الإعلانية 240 ريالًا لكل متر مربع في السنة.\n"
     "أصبح إيجار حاوية النفايات 180 ريالًا للأسبوع.\n"
     "أصبحت رسوم حجز قاعة الحديقة 300 ريال لليوم الواحد.",
     "Circular 14 of 2026 on updated municipal fees, in force from 1 June 2026.\n"
     "The renewal fee for a commercial activity licence is now 750 riyals a year.\n"
     "The renovation permit fee for minor works is now 400 riyals.\n"
     "The signage permit fee is now 240 riyals per square metre a year.\n"
     "Waste container rental is now 180 riyals a week.\n"
     "The park hall booking fee is now 300 riyals a day."),
]

ARTICLE_TITLES = {
    "A01": "رسوم تجديد الرخصة", "A02": "مستندات التجديد", "A03": "غرامة التأخير", "A04": "التجديد ومدة الرخصة",
    "A05": "رسوم الرخصة الجديدة", "A06": "مستندات الرخصة الجديدة", "A07": "مدة إصدار الرخصة", "A08": "أنشطة تحتاج تفتيشًا",
    "A09": "رسوم رخصة الترميم", "A10": "مستندات الترميم", "A11": "مدة رخصة الترميم", "A12": "مدة رخصة الترميم بعد الربط",
    "A13": "تعريف الأعمال البسيطة", "A14": "رسوم اللوحة الإعلانية", "A15": "مستندات اللوحة الإعلانية",
    "A16": "مساحة اللوحة", "A17": "تجديد تصريح اللوحة", "A18": "إيجار الحاوية", "A19": "طلب الحاوية",
    "A20": "رفع مخلفات البناء", "A21": "المواد الممنوعة", "A22": "قنوات السداد", "A23": "تقسيط الرسوم",
    "A24": "استرداد المبالغ", "A25": "الاعتراض على فاتورة", "A26": "رسوم قاعة الحديقة", "A27": "قواعد حجز الحديقة",
    "A28": "إلغاء حجز الحديقة", "A29": "الاستعلام عن المخالفات", "A30": "خصم السداد المبكر", "A31": "الاعتراض على المخالفة",
    "A32": "طلب الإعفاء من الرسوم", "A33": "معايير الإعفاء الداخلية", "A34": "أولويات التفتيش", "A35": "التصعيد الداخلي",
    "A36": "شروط عقد المورد", "A37": "قنوات التواصل", "A38": "تسجيل الحساب", "A39": "العنوان الوطني",
    "A40": "لغات الخدمة", "A41": "نافذة المحادثة", "A42": "استعادة كلمة المرور", "A43": "إشعار الخصوصية",
    "A44": "تقديم البلاغ", "A45": "مواعيد المراكز", "A46": "الخدمة في الإجازات", "A47": "حدائق جديدة",
    "A48": "التعميم 14 لعام 2026: تحديث الرسوم",
}

CLASSIFICATION = {"kb_public": "عام", "vendor_pack": "مقيد", "kb_internal": "مقيد", "kb_supervisor": "مقيد",
                  "enforcement_notes": "مقيد"}
OWNER = {"kb_public": "إدارة تجربة المستفيد", "vendor_pack": "مورد منصة مركز الاتصال", "kb_internal": "مركز الاتصال",
         "kb_supervisor": "مركز الاتصال", "enforcement_notes": "إدارة الرقابة"}
LICENCE = {
    "agency": "محتوى من إعداد الهيئة",
    "vendor": "مرخص للاستخدام داخل منصة المورد فقط، ولا يجوز نسخه أو استخدامه خارجها (عقد المورد، البند 9)",
}

# qid, lang, category, question, answerable, gold fact(s) separated by |, gold article(s) separated by spaces
QUESTIONS = [
    ("q01", "ar", "renew_licence", "كم رسوم تجديد رخصة النشاط التجاري للسنة؟", "yes", "750", "A48"),
    ("q02", "ar", "renew_licence", "ما المستندات المطلوبة لتجديد رخصة النشاط التجاري؟", "yes", "عقد إيجار موثق", "A02"),
    ("q03", "ar", "renew_licence", "كم غرامة التأخير في تجديد الرخصة التجارية عن كل شهر؟", "yes", "100 ريال", "A03"),
    ("q04", "ar", "new_licence", "كم رسوم إصدار رخصة نشاط تجاري جديدة؟", "yes", "1200", "A05"),
    ("q05", "ar", "new_licence", "كم تستغرق مدة إصدار رخصة النشاط التجاري الجديدة؟", "yes", "3 أيام عمل", "A07"),
    ("q06", "ar", "minor_works", "كم رسوم رخصة الترميم للأعمال البسيطة؟", "yes", "400", "A48"),
    ("q07", "ar", "minor_works", "ما مدة إصدار رخصة الترميم للأعمال البسيطة؟", "yes", "5 أيام عمل", "A12"),
    ("q08", "ar", "signage", "ما أقصى مساحة مسموحة للوحة الإعلانية على واجهة المحل؟", "yes", "12 متر", "A16"),
    ("q09", "ar", "waste", "كم إيجار حاوية النفايات في الأسبوع؟", "yes", "180", "A48"),
    ("q10", "ar", "waste", "ما المواد الممنوع وضعها في حاويات النفايات؟", "yes", "المواد الكيميائية", "A21"),
    ("q11", "ar", "payments", "متى يعاد المبلغ إذا رُفض طلبي؟", "yes", "14 يوم", "A24"),
    ("q12", "ar", "payments", "كيف أسدد الرسوم البلدية؟", "yes", "تطبيق الهيئة", "A22"),
    ("q13", "ar", "parks", "هل يمكن إلغاء حجز مرفق الحديقة دون رسوم؟", "yes", "48 ساعة", "A28"),
    ("q14", "ar", "violations", "ما المهلة المتاحة للاعتراض على مخالفة بلدية؟", "yes", "30 يوم", "A31"),
    ("q15", "ar", "payments", "دخلي محدود، فكيف أطلب الإعفاء من رسوم رخصة الترميم؟", "yes", "15 يوم عمل", "A32"),
    ("q16", "ar", "payments", "ما شروط قبول طلب الإعفاء من الرسوم البلدية؟", "yes", "لجنة", "A32"),
    ("q17", "ar", "excavation", "كم رسوم تصريح الحفر لتمديد خط مياه أمام المنزل؟", "no", "", ""),
    ("q18", "ar", "street_vending", "ما شروط تصريح عربة الطعام المتجولة؟", "no", "", ""),
    ("q19", "ar", "complaint_followup", "ما حالة بلاغي الذي قدمته الأسبوع الماضي عن إنارة الشارع؟", "no", "", ""),
    ("q20", "ar", "parks", "كم رسوم حجز قاعة الحديقة لليوم؟", "yes", "300", "A48"),
    ("q21", "en", "renew_licence", "How long is a renewed commercial licence valid?", "yes", "one year", "A04"),
    ("q22", "en", "signage", "What is the signage permit fee per square metre?", "yes", "240", "A48"),
    ("q23", "en", "new_licence", "Which documents do I need for a new shop licence?", "yes", "lease|title deed", "A06"),
    ("q24", "en", "waste", "How soon is a waste container delivered after I pay?", "yes", "3 business days", "A19"),
    ("q25", "en", "payments", "When is my money refunded if my application is rejected?", "yes", "14 days", "A24"),
    ("q26", "en", "parks", "How much is the deposit for booking a park facility?", "yes", "500", "A27"),
    ("q27", "en", "minor_works", "Does repainting my house count as minor works?", "yes", "minor works|painting|paint", "A13"),
    ("q28", "en", "excavation", "Do I need a permit to dig in front of my house for a water line?", "no", "", ""),
    ("q29", "en", "payments", "Can I pay municipal fees in cash?", "yes", "cash is not accepted|app", "A22"),
    ("q30", "en", "violations", "Is there a discount if I pay a violation early?", "yes", "25%", "A30"),
]

REQUEST_MEMO = """مذكرة داخلية
من: إيثار الرحيلي، نائبة الرئيس لخدمات السكان
إلى: فريق التحول الرقمي
الموضوع: روبوت محادثة لمركز الاتصال

تصلنا شكاوى كثيرة من تأخر الرد على الاستفسارات المكتوبة، وقد أطلقت جهات أخرى روبوتات محادثة. أريد روبوت محادثة بالذكاء الاصطناعي يجيب عن استفسارات السكان في الموقع والتطبيق والبريد، بالعربية والإنجليزية.

أريد أن يكون جاهزًا قبل بداية السنة المالية القادمة، وأن نعرض على لجنة التوجيه في اجتماعها القادم ما سنحتاجه من ميزانية. أتوقع أن يخفف الضغط على الموظفين وأن يرفع رضا السكان.

أرجو تقييم الجدوى وتقديم توصية واضحة بالتكلفة.
"""

INTERVIEWS = """ملاحظات المقابلات (فريق التحول الرقمي)

1) بتول النجراني، مديرة مركز الاتصال
- في المركز 42 موظفًا للاستفسارات المكتوبة. يوم الأحد أثقل الأيام، وتتراكم فيه الاستفسارات.
- يبحث الموظف في قاعدة المعرفة عن الإجابة، ويقول الموظفون إن بعض المقالات قديمة، خصوصًا الرسوم بعد التعميم الأخير.
- الاستفسارات الإنجليزية أبطأ لأن نصف المقالات تقريبًا لا نسخة إنجليزية لها.
- استفسارات متابعة البلاغات لا يجيب عنها الموظف من قاعدة المعرفة؛ يفتح نظام البلاغات ويبحث برقم البلاغ.
- في الأسابيع الستة الأولى من الربع اختار المشرفون عينة التدقيق من الاستفسارات المصعَّدة، ثم صارت العينة عشوائية.
- لو جاءت مسودة جاهزة، يحتاج الموظف نحو دقيقة واحدة ليتحقق منها قبل الإرسال، سواء صلحت المسودة أم لم تصلح.

2) مؤيد الصاعدي، أمين البيانات
- قاعدة المعرفة 48 مقالًا. لا يراجعها أحد بانتظام، ولكل مقال تاريخ آخر مراجعة.
- ست مقالات جاءت ضمن حزمة محتوى من مورد منصة مركز الاتصال الحالية، ولم يراجع أحد شروط استخدامها.
- بعض المقالات للمشرفين فقط، وبعضها ملاحظات تفتيش لإدارة الرقابة، وكلها في المستودع نفسه.
- حساب الخدمة الذي جُرّب به النموذج الأولي يقرأ المستودع كله.

3) ريماز الشراري، مسؤولة حماية البيانات
- ملفات الحالات فيها أرقام هويات وجوالات وعناوين، وأحيانًا بيانات صحية أو بيانات أطفال.
- أي خيار يرسل استفسارات السكان إلى خدمة مستضافة خارج المملكة يحتاج تقييمًا لنقل البيانات قبل أي تجربة على بيانات حقيقية.
- لا أعترض على تجربة على وثائق اصطناعية.

4) أيهم الطائفي، شريك الأعمال المالي
- لجنة التوجيه لا توافق على استثمار لا يسترد تكلفته خلال 24 شهرًا.
- التكلفة السنوية المحمَّلة للموظف 198,000 ريال، وساعات العمل المنتجة 1,540 ساعة في السنة.
- لا تُحتسب الدقائق الموفَّرة ريالات إلا إذا تحولت إلى عمل آخر أو إلى تقليل التعاقد الإضافي في المواسم.
"""

DATA_DICTIONARY = """قاموس بيانات سجل الاستفسارات المكتوبة (enquiries.csv)
الفترة: 13 أسبوعًا (91 يومًا) من 28 يونيو 2026 إلى 26 سبتمبر 2026. اصطناعي بالكامل.

enquiry_id            معرّف الاستفسار
received_date         تاريخ الاستلام
channel               القناة: web_form (نموذج الموقع)، app_chat (محادثة التطبيق)، email (البريد)
language              لغة الاستفسار: ar أو en
category              فئة الاستفسار كما صنفها الموظف (انظر القائمة أدناه)
subject               عنوان الاستفسار كما كتبه المستفيد
agent_id              معرّف الموظف
handling_minutes      دقائق عمل الموظف على الاستفسار
status                closed (أغلقه الموظف) أو auto_closed (أغلقه النظام بعد بقائه مفتوحًا في قائمة الموظف)
first_response_hours  الساعات حتى أول رد
repeat_within_7d      هل تواصل المستفيد مرة أخرى في الموضوع نفسه خلال 7 أيام: yes أو no
qa_sample_type        none، أو targeted (اختاره مشرف)، أو random (عينة عشوائية)
qa_result             نتيجة التدقيق: correct، أو wrong_info (معلومة خاطئة)، أو incomplete (ناقصة)؛ فارغ إن لم يُدقق

الفئات: renew_licence, new_licence, minor_works, signage, waste, payments, parks, violations,
excavation, street_vending, complaint_followup, other

ملاحظة: صُدِّر السجل من النظام مرتين لبعض الأيام عند انقطاع التصدير الليلي.
"""

STAFF_COSTS = [
    ("عدد موظفي الاستفسارات المكتوبة", 42, "موظف"),
    ("التكلفة السنوية المحمَّلة للموظف", 198000, "ريال"),
    ("ساعات العمل المنتجة للموظف في السنة", 1540, "ساعة"),
    ("التكلفة السنوية المحمَّلة للمشرف", 264000, "ريال"),
    ("عدد المشرفين", 4, "مشرف"),
    ("تكلفة التعاقد الإضافي في المواسم (للسنة الماضية)", 310000, "ريال"),
]

# role, then R or - for: kb_public, vendor_pack, kb_internal, kb_supervisor, enforcement_notes, case_files, enquiry_logs
ACCESS = [
    ("agent", "R", "R", "R", "-", "-", "R", "-"),
    ("supervisor", "R", "R", "R", "R", "-", "R", "R"),
    ("inspector", "R", "-", "-", "-", "R", "-", "-"),
    ("data_analyst", "R", "-", "-", "-", "-", "-", "R"),
    ("svc-jawab", "R", "R", "R", "R", "R", "R", "R"),
]
ACCESS_COLUMNS = ["role", "kb_public", "vendor_pack", "kb_internal", "kb_supervisor", "enforcement_notes", "case_files",
                  "enquiry_logs"]
