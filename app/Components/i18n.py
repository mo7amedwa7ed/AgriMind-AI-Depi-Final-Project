"""Centralized English / Arabic translation system for AgriMind AI.

Every user-visible string lives here.  Pages never hard-code text.

* ``t(key, **fmt)``      -> translated string for the active language
* ``get_lang()``         -> "en" or "ar" (stored in ``st.session_state["lang"]``)
* ``crop_label(raw)``    -> localized crop name for a model class label
* ``irrigation_label()`` -> localized Low / Medium / High
* ``feature_label()``    -> localized label for a dynamically discovered feature

This module has no dependency on other Components modules (no circular imports)
and only imports Streamlit lazily, so it can be unit-tested without Streamlit.
"""
from __future__ import annotations

DEFAULT_LANG = "en"
SUPPORTED = ("en", "ar")
LANG_NAMES = {"en": "English", "ar": "العربية"}
LANG_SHORT = {"en": "EN", "ar": "عربي"}  # compact labels for the navbar switch


def get_lang() -> str:
    try:
        import streamlit as st

        lang = st.session_state.get("lang", DEFAULT_LANG)
    except Exception:  # pragma: no cover - outside Streamlit
        lang = DEFAULT_LANG
    return lang if lang in SUPPORTED else DEFAULT_LANG


def is_rtl(lang: str | None = None) -> bool:
    return (lang or get_lang()) == "ar"


def t(key: str, lang: str | None = None, **fmt) -> str:
    lang = lang or get_lang()
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key  # visible fallback makes missing keys easy to spot
    text = entry.get(lang) or entry.get(DEFAULT_LANG, key)
    return text.format(**fmt) if fmt else text


def _tr(en: str, ar: str) -> dict:
    return {"en": en, "ar": ar}


# --------------------------------------------------------------------------- #
# Main translation table
# --------------------------------------------------------------------------- #
TRANSLATIONS: dict[str, dict[str, str]] = {
    # ---- brand / shell ------------------------------------------------------
    "app_name": _tr("AgriMind AI", "أجري مايند AI"),
    "tagline": _tr("Intelligent decisions for smarter farming", "قرارات ذكية لزراعة أكثر كفاءة"),
    "nav_dashboard": _tr("Home", "الرئيسية"),
    "menu": _tr("Menu", "القائمة"),
    "nav_crop": _tr("Crop Recommendation", "توصية المحاصيل"),
    "nav_irrigation": _tr("Irrigation Prediction", "التنبؤ باحتياج الري"),
    "nav_yield": _tr("Crop Yield Prediction", "التنبؤ بإنتاجية المحصول"),
    "nav_section": _tr("Navigation", "التنقل"),
    "language": _tr("Language", "اللغة"),
    "system_status": _tr("Model files", "ملفات النماذج"),
    "status_ready": _tr("Found", "موجود"),
    "status_missing": _tr("Missing", "غير موجود"),
    "model_crop": _tr("Crop recommendation model", "نموذج توصية المحاصيل"),
    "model_irrigation": _tr("Irrigation prediction model", "نموذج التنبؤ بالري"),
    "model_yield": _tr("Crop yield model + scaler", "نموذج الإنتاجية + المقياس"),
    "disclaimer": _tr(
        "Predictions are machine-learning estimates intended to support decisions. "
        "Validate them with local agronomic knowledge before acting.",
        "التنبؤات تقديرات قائمة على تعلّم الآلة لدعم اتخاذ القرار. "
        "يُرجى مراجعتها مع الخبرة الزراعية المحلية قبل التنفيذ.",
    ),
    # ---- generic UI ---------------------------------------------------------
    "predict": _tr("Run prediction", "تشغيل التنبؤ"),
    "reset": _tr("Reset inputs", "إعادة الضبط"),
    "results_title": _tr("Results", "النتائج"),
    "awaiting_title": _tr("Awaiting prediction", "في انتظار التنبؤ"),
    "awaiting_text": _tr(
        "Enter your values and press “Run prediction” to see the result here.",
        "أدخل القيم ثم اضغط «تشغيل التنبؤ» لعرض النتيجة هنا.",
    ),
    "stale_notice": _tr(
        "Inputs changed since this result was produced. Run the prediction again to update it.",
        "تغيّرت المدخلات منذ إنتاج هذه النتيجة. شغّل التنبؤ مجدداً لتحديثها.",
    ),
    "error_load": _tr("A model file could not be loaded: {detail}", "تعذّر تحميل ملف النموذج: {detail}"),
    "error_predict": _tr("The prediction could not be completed: {detail}", "تعذّر إكمال التنبؤ: {detail}"),
    "error_schema": _tr("Input schema problem: {detail}", "مشكلة في مخطط المدخلات: {detail}"),
    "input_summary": _tr("Input summary", "ملخص المدخلات"),
    "technical_details": _tr("Technical details", "تفاصيل تقنية"),
    "probability": _tr("Model probability", "احتمال النموذج"),
    "value": _tr("Value", "القيمة"),
    "parameter": _tr("Parameter", "المعامل"),
    # ---- dashboard ----------------------------------------------------------
    "hero_badge": _tr("AI-powered agriculture", "زراعة مدعومة بالذكاء الاصطناعي"),
    "hero_title": _tr("Smarter farm decisions, powered by machine learning", "قرارات زراعية أذكى بقوة تعلّم الآلة"),
    "hero_text": _tr(
        "AgriMind AI brings three trained models together in one platform: choose the right crop, "
        "estimate irrigation need, and forecast crop productivity — in English or Arabic.",
        "يجمع أجري مايند AI ثلاثة نماذج مدرَّبة في منصة واحدة: اختيار المحصول المناسب، "
        "وتقدير احتياج الري، والتنبؤ بإنتاجية المحصول — بالعربية أو الإنجليزية.",
    ),
    "cta_start": _tr("Start with crop recommendation", "ابدأ بتوصية المحاصيل"),
    "features_title": _tr("Platform tools", "أدوات المنصة"),
    "features_sub": _tr("Three focused tools, each backed by its own trained model.", "ثلاث أدوات متخصصة، يعتمد كل منها على نموذج مدرَّب خاص به."),
    "open_tool": _tr("Open tool", "افتح الأداة"),
    "card_crop_desc": _tr(
        "Enter soil nutrients and climate conditions to find the crop that best fits them.",
        "أدخل عناصر التربة والظروف المناخية لمعرفة المحصول الأنسب لها.",
    ),
    "card_crop_tag1": _tr("Soil nutrients + climate", "عناصر التربة + المناخ"),
    "card_crop_tag2": _tr("Top-ranked crops", "أفضل المحاصيل ترتيباً"),
    "card_irr_desc": _tr(
        "Estimate whether a field needs Low, Medium or High irrigation from its field conditions.",
        "قدّر ما إذا كان الحقل يحتاج ريّاً منخفضاً أو متوسطاً أو مرتفعاً بحسب ظروفه.",
    ),
    "card_irr_tag1": _tr("Field conditions", "ظروف الحقل"),
    "card_irr_tag2": _tr("Low · Medium · High", "منخفض · متوسط · مرتفع"),
    "card_yield_desc": _tr(
        "Forecast crop productivity per feddan and per hectare from soil, weather and farm inputs.",
        "تنبّأ بإنتاجية المحصول للفدان والهكتار اعتماداً على التربة والطقس ومدخلات المزرعة.",
    ),
    "card_yield_tag1": _tr("Soil, weather, farm inputs", "التربة والطقس ومدخلات المزرعة"),
    "card_yield_tag2": _tr("Tons / feddan · tons / ha", "طن/فدان · طن/هكتار"),
    "overview_title": _tr("Platform overview", "نظرة عامة على المنصة"),
    "overview_sub": _tr("What AgriMind AI is built on.", "ما الذي تقوم عليه المنصة."),
    "ov1_t": _tr("Trained models", "نماذج مدرَّبة"),
    "ov1_d": _tr("Each tool loads its own pre-trained model; nothing is retrained inside the app.", "تحمّل كل أداة نموذجها المدرَّب مسبقاً، ولا يُعاد التدريب داخل التطبيق."),
    "ov2_t": _tr("Bilingual by design", "ثنائية اللغة بالتصميم"),
    "ov2_d": _tr("Switch between English (LTR) and Arabic (RTL) at any time without losing your inputs.", "بدّل بين الإنجليزية (LTR) والعربية (RTL) في أي وقت دون فقدان مدخلاتك."),
    "ov3_t": _tr("Transparent results", "نتائج شفافة"),
    "ov3_d": _tr("Every result shows the inputs used and, where the model supports it, class probabilities.", "تعرض كل نتيجة المدخلات المستخدمة، وكذلك احتمالات الفئات متى دعمها النموذج."),
    "how_title": _tr("How it works", "كيف تعمل المنصة"),
    "how_sub": _tr("From field data to a decision in three steps.", "من بيانات الحقل إلى القرار في ثلاث خطوات."),
    "how1_t": _tr("Choose a tool", "اختر أداة"),
    "how1_d": _tr("Pick crop recommendation, irrigation prediction or yield prediction.", "اختر توصية المحاصيل أو التنبؤ بالري أو التنبؤ بالإنتاجية."),
    "how2_t": _tr("Enter field data", "أدخل بيانات الحقل"),
    "how2_d": _tr("Fill in the grouped input form. Your values are kept while you navigate or change language.", "املأ نموذج المدخلات المقسّم لمجموعات. تُحفظ قيمك أثناء التنقل أو تغيير اللغة."),
    "how3_t": _tr("Read the result", "اقرأ النتيجة"),
    "how3_d": _tr("Review the prediction, its chart and the input summary, then decide.", "راجع التنبؤ ورسمه البياني وملخص المدخلات، ثم اتخذ قرارك."),
    "ben_title": _tr("Why agricultural AI?", "لماذا الذكاء الاصطناعي الزراعي؟"),
    "ben_sub": _tr("What data-driven tools can add to everyday farm planning.", "ما الذي يمكن أن تضيفه الأدوات القائمة على البيانات لتخطيط المزرعة اليومي."),
    "ben1_t": _tr("Informed crop choice", "اختيار محصول مدروس"),
    "ben1_d": _tr("Match crops to soil and climate instead of relying on habit alone.", "واءِم بين المحصول والتربة والمناخ بدلاً من الاعتماد على العادة وحدها."),
    "ben2_t": _tr("Smarter water use", "استخدام أذكى للمياه"),
    "ben2_d": _tr("Anticipate irrigation need to support more efficient water management.", "توقّع احتياج الري لدعم إدارة أكثر كفاءة للمياه."),
    "ben3_t": _tr("Better planning", "تخطيط أفضل"),
    "ben3_d": _tr("Estimate productivity ahead of the season to plan inputs and resources.", "قدّر الإنتاجية قبل الموسم لتخطيط المدخلات والموارد."),
    "ben4_t": _tr("Consistent, repeatable", "ثابتة وقابلة للتكرار"),
    "ben4_d": _tr("The same inputs always give the same output, making comparisons easy.", "المدخلات نفسها تعطي المخرجات نفسها دائماً، ما يسهّل المقارنة."),
    # ---- crop recommendation -------------------------------------------------
    "crop_title": _tr("Crop Recommendation", "توصية المحاصيل"),
    "crop_sub": _tr("Find the crop that best matches your soil nutrients and local climate.", "اعثر على المحصول الأنسب لعناصر تربتك ومناخ منطقتك."),
    "crop_group_soil": _tr("Soil nutrients", "عناصر التربة"),
    "crop_group_climate": _tr("Climate & soil acidity", "المناخ وحموضة التربة"),
    "crop_N": _tr("Nitrogen (N)", "النيتروجين (N)"),
    "crop_P": _tr("Phosphorus (P)", "الفوسفور (P)"),
    "crop_K": _tr("Potassium (K)", "البوتاسيوم (K)"),
    "crop_temperature": _tr("Temperature (°C)", "درجة الحرارة (°م)"),
    "crop_humidity": _tr("Relative humidity (%)", "الرطوبة النسبية (%)"),
    "crop_ph": _tr("Soil pH", "حموضة التربة (pH)"),
    "crop_rainfall": _tr("Rainfall (mm)", "هطول الأمطار (مم)"),
    "crop_kicker": _tr("Recommended crop", "المحصول الموصى به"),
    "crop_top_chart": _tr("Most suitable crops", "أنسب المحاصيل"),
    "crop_npk_chart": _tr("Nutrient profile (input)", "ملف العناصر (المدخلات)"),
    "crop_prob_note": _tr("Probabilities come from the trained model and rank how well each crop fits the inputs.", "تأتي الاحتمالات من النموذج المدرَّب وترتّب مدى ملاءمة كل محصول للمدخلات."),
    "crop_no_proba": _tr("This model does not expose class probabilities.", "هذا النموذج لا يوفّر احتمالات الفئات."),
    # ---- irrigation -----------------------------------------------------------
    "irr_title": _tr("Irrigation Prediction", "التنبؤ باحتياج الري"),
    "irr_sub": _tr("Estimate the irrigation need level for a field.", "قدّر مستوى احتياج الحقل للري."),
    "irr_group_numeric": _tr("Measurements", "القياسات"),
    "irr_group_cat": _tr("Field characteristics", "خصائص الحقل"),
    "irr_schema_ok": _tr(
        "Input form generated from the trained pipeline: {n} features detected.",
        "نموذج المدخلات مبني من خط المعالجة المدرَّب: تم اكتشاف {n} من المتغيرات.",
    ),
    "irr_schema_json": _tr(
        "Input form generated from app/irrigation_schema.json: {n} features.",
        "نموذج المدخلات مبني من الملف app/irrigation_schema.json: {n} من المتغيرات.",
    ),
    "irr_schema_count_warn": _tr(
        "Expected 19 features but {n} were detected. Please verify the schema.",
        "المتوقع 19 متغيراً لكن تم اكتشاف {n}. يُرجى التحقق من المخطط.",
    ),
    "irr_schema_missing_title": _tr("Irrigation input schema could not be verified", "تعذّر التحقق من مخطط مدخلات الري"),
    "irr_schema_missing_body": _tr(
        "The saved pipeline does not store its input column names, so the app refuses to guess them. "
        "Create the file app/irrigation_schema.json listing the exact training columns (see README), then reload.",
        "خط المعالجة المحفوظ لا يخزّن أسماء الأعمدة، ولذلك يرفض التطبيق تخمينها. "
        "أنشئ الملف app/irrigation_schema.json بقائمة أعمدة التدريب الدقيقة (راجع README) ثم أعد التحميل.",
    ),
    "irr_kicker": _tr("Predicted irrigation need", "احتياج الري المتوقع"),
    "irr_chart": _tr("Class probabilities", "احتمالات الفئات"),
    "irr_training_range": _tr("Training range: {lo} – {hi}", "نطاق التدريب: {lo} – {hi}"),
    "irr_unused": _tr("{n} column(s) are required by the pipeline but dropped by it, so they are filled with 0 internally.", "{n} من الأعمدة يطلبها خط المعالجة لكنه يستبعدها، لذلك تُملأ بالقيمة 0 داخلياً."),
    "irr_advice_Low": _tr("Low irrigation need. Water only as required and keep monitoring soil moisture.", "احتياج الري منخفض. اروِ عند الحاجة فقط وواصل مراقبة رطوبة التربة."),
    "irr_advice_Medium": _tr("Moderate irrigation need. Plan regular irrigation and adjust to weather changes.", "احتياج الري متوسط. خطّط لريّ منتظم وعدّله وفق تغيّرات الطقس."),
    "irr_advice_High": _tr("High irrigation need. Prioritise water availability and schedule irrigation promptly.", "احتياج الري مرتفع. أعطِ أولوية لتوفير المياه وجدولة الري سريعاً."),
    "irr_class_Low": _tr("Low", "منخفض"),
    "irr_class_Medium": _tr("Medium", "متوسط"),
    "irr_class_High": _tr("High", "مرتفع"),
    # ---- crop yield -------------------------------------------------------------
    "yield_title": _tr("Crop Yield Prediction", "التنبؤ بإنتاجية المحصول"),
    "yield_sub": _tr("Forecast productivity per feddan and per hectare.", "تنبّأ بالإنتاجية للفدان وللهكتار."),
    "yield_group_soil": _tr("Soil & nutrients", "التربة والعناصر"),
    "yield_group_weather": _tr("Weather", "الطقس"),
    "yield_group_farm": _tr("Farm management", "إدارة المزرعة"),
    "yield_group_context": _tr("Crop, region & season", "المحصول والمنطقة والموسم"),
    "yield_units_note": _tr("Enter values in the same units used in the training data.", "أدخل القيم بنفس وحدات بيانات التدريب."),
    "yield_soil_ph": _tr("Soil pH", "حموضة التربة (pH)"),
    "yield_soil_moisture": _tr("Soil moisture", "رطوبة التربة"),
    "yield_avg_temperature": _tr("Average temperature", "متوسط درجة الحرارة"),
    "yield_total_rainfall": _tr("Total rainfall", "إجمالي هطول الأمطار"),
    "yield_fertilizer_amount": _tr("Fertilizer amount", "كمية السماد"),
    "yield_pesticide_usage": _tr("Pesticide usage", "استخدام المبيدات"),
    "yield_sunlight_hours": _tr("Sunlight hours", "ساعات الإشعاع الشمسي"),
    "yield_nitrogen_content": _tr("Nitrogen content", "محتوى النيتروجين"),
    "yield_phosphorus_content": _tr("Phosphorus content", "محتوى الفوسفور"),
    "yield_potassium_content": _tr("Potassium content", "محتوى البوتاسيوم"),
    "yield_irrigation_frequency": _tr("Irrigation frequency", "عدد مرات الري"),
    "yield_month": _tr("Month", "الشهر"),
    "yield_crop_type": _tr("Crop type", "نوع المحصول"),
    "yield_region": _tr("Region", "المنطقة"),
    "yield_season": _tr("Season", "الموسم"),
    "yield_baseline_note": _tr(
        "“Baseline” means none of the listed categories (all indicator columns = 0). "
        "Its real name is not stored with the model.",
        "«الفئة المرجعية» تعني عدم اختيار أي من الفئات المدرجة (كل أعمدة المؤشرات = 0). "
        "اسمها الفعلي غير محفوظ مع النموذج.",
    ),
    "yield_kicker": _tr("Predicted productivity", "الإنتاجية المتوقعة"),
    "yield_per_feddan": _tr("per Egyptian feddan", "لكل فدان مصري"),
    "yield_unit_feddan": _tr("tons / feddan", "طن / فدان"),
    "yield_unit_ha": _tr("tons / hectare", "طن / هكتار"),
    "yield_ha_label": _tr("Per hectare (model output)", "لكل هكتار (مخرج النموذج)"),
    "yield_feddan_label": _tr("Per feddan (× 0.42)", "لكل فدان (× 0.42)"),
    "yield_productivity_note": _tr(
        "These are productivity values (yield per unit of area), not the total production of a farm. "
        "Multiply by your cultivated area to estimate a total.",
        "هذه قيم إنتاجية (المحصول لكل وحدة مساحة) وليست إجمالي إنتاج المزرعة. "
        "اضرب في مساحتك المزروعة لتقدير الإجمالي.",
    ),
    "yield_chart": _tr("Productivity comparison", "مقارنة الإنتاجية"),
    "yield_conversion": _tr("Feddan value = hectare value × 0.42", "قيمة الفدان = قيمة الهكتار × 0.42"),
    "yield_scaler_mode": _tr("Scaler applied (transform only): {mode}", "المقياس المطبَّق (تحويل فقط): {mode}"),
    "baseline": _tr("Baseline (unlisted category)", "الفئة المرجعية (غير مدرجة)"),
    # ---- months ---------------------------------------------------------------
    **{
        f"month_{i}": _tr(en, ar)
        for i, (en, ar) in enumerate(
            [
                ("January", "يناير"), ("February", "فبراير"), ("March", "مارس"),
                ("April", "أبريل"), ("May", "مايو"), ("June", "يونيو"),
                ("July", "يوليو"), ("August", "أغسطس"), ("September", "سبتمبر"),
                ("October", "أكتوبر"), ("November", "نوفمبر"), ("December", "ديسمبر"),
            ],
            start=1,
        )
    },
    # ---- yield categorical values ------------------------------------------------
    "val_Corn": _tr("Corn", "ذرة"), "val_Rice": _tr("Rice", "أرز"),
    "val_Soybean": _tr("Soybean", "فول الصويا"), "val_Wheat": _tr("Wheat", "قمح"),
    "val_East": _tr("East", "الشرق"), "val_North": _tr("North", "الشمال"),
    "val_South": _tr("South", "الجنوب"), "val_West": _tr("West", "الغرب"),
    "val_Spring": _tr("Spring", "الربيع"), "val_Summer": _tr("Summer", "الصيف"),
}

# --------------------------------------------------------------------------- #
# Crop names (labels produced by the crop recommendation model)
# --------------------------------------------------------------------------- #
CROP_NAMES_AR = {
    "rice": "أرز", "maize": "ذرة", "chickpea": "حمص", "kidneybeans": "فاصوليا حمراء",
    "pigeonpeas": "بسلة الحمام", "mothbeans": "فاصوليا العثّ", "mungbean": "فاصوليا المونج",
    "blackgram": "ماش أسود", "lentil": "عدس", "pomegranate": "رمان", "banana": "موز",
    "mango": "مانجو", "grapes": "عنب", "watermelon": "بطيخ", "muskmelon": "شمام",
    "apple": "تفاح", "orange": "برتقال", "papaya": "بابايا", "coconut": "جوز الهند",
    "cotton": "قطن", "jute": "جوت", "coffee": "بن (قهوة)",
}


def _norm(label) -> str:
    return str(label).strip().lower().replace(" ", "").replace("_", "")


def crop_label(raw, lang: str | None = None) -> str:
    lang = lang or get_lang()
    text = str(raw)
    if lang == "ar":
        return CROP_NAMES_AR.get(_norm(raw), text.capitalize())
    return text.capitalize()


def irrigation_label(raw, lang: str | None = None) -> str:
    key = _norm(raw).capitalize()
    full = f"irr_class_{key}"
    return t(full, lang) if full in TRANSLATIONS else str(raw)


def irrigation_advice(raw, lang: str | None = None) -> str | None:
    key = f"irr_advice_{_norm(raw).capitalize()}"
    return t(key, lang) if key in TRANSLATIONS else None


# Cosmetic Arabic labels for irrigation features.  They are ONLY applied when the
# loaded pipeline itself reports a column with the same (normalized) name, so this
# table never adds or changes model inputs.
IRRIGATION_FEATURE_AR = {
    "soilph": "حموضة التربة (pH)", "soilmoisture": "رطوبة التربة",
    "organiccarbon": "الكربون العضوي", "electricalconductivity": "التوصيل الكهربائي",
    "temperaturec": "درجة الحرارة (°م)", "temperature": "درجة الحرارة",
    "humidity": "الرطوبة", "rainfallmm": "هطول الأمطار (مم)", "rainfall": "هطول الأمطار",
    "sunlighthours": "ساعات الإشعاع الشمسي", "windspeedkmh": "سرعة الرياح (كم/س)",
    "windspeed": "سرعة الرياح", "soiltype": "نوع التربة", "croptype": "نوع المحصول",
    "cropgrowthstage": "مرحلة نمو المحصول", "season": "الموسم",
    "irrigationtype": "نوع الري", "watersource": "مصدر المياه",
    "fieldareahectare": "مساحة الحقل (هكتار)", "mulchingused": "استخدام التغطية (المالتش)",
    "previousirrigationmm": "الري السابق (مم)", "region": "المنطقة",
}


def feature_label(name: str, lang: str | None = None) -> str:
    lang = lang or get_lang()
    pretty = str(name).replace("_", " ").strip()
    pretty = pretty[:1].upper() + pretty[1:]
    if lang == "ar":
        return IRRIGATION_FEATURE_AR.get(_norm(name), pretty)
    return pretty
