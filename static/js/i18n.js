// ===== CropSense i18n — Language Toggle =====
// Supports: English (en), Hindi (hi), Marathi (mr)
// Usage: add data-i18n="key" to any HTML element

const TRANSLATIONS = {
  en: {
    // Nav
    "nav.farmer_tools":      "Farmer Tools",
    "nav.kab_bechun":        "Kab Bechun? 🥇",
    "nav.reports":           "Reports",
    "nav.dashboard":         "Dashboard",
    "nav.upload_data":       "Upload Data",
    "nav.predict_yield":     "Predict Yield",
    "nav.crop_recommender":  "Crop Recommender",
    "nav.fertilizer_calc":   "Fertilizer Calc",
    "nav.mandi_tracker":     "Mandi Price Tracker",
    "nav.pest_identifier":   "Pest/Disease Identifier",
    "nav.scheme_finder":     "Govt Scheme Finder",
    "nav.history":           "History",
    "nav.pdf_report":        "PDF Report",
    "nav.export_csv":        "Export CSV",
    "nav.logout":            "Logout",

    // Dashboard
    "dash.title":            "My Farm Overview",
    "dash.welcome":          "Welcome back",
    "dash.retrain":          "Retrain Model",
    "dash.export_pdf":       "Export PDF",
    "dash.total_records":    "Total Records",
    "dash.uploaded_entries": "Uploaded crop entries",
    "dash.predictions":      "Predictions Made",
    "dash.ml_queries":       "ML model queries",
    "dash.avg_yield":        "Avg Yield (t/ha)",
    "dash.across_crops":     "Across all crops",
    "dash.recent_crops":     "Recent Crop Data",
    "dash.recent_preds":     "Recent Predictions",
    "dash.crop":             "Crop",
    "dash.state":            "State",
    "dash.season":           "Season",
    "dash.area":             "Area (ha)",
    "dash.yield":            "Yield (t/ha)",
    "dash.uploaded":         "Uploaded",
    "dash.confidence":       "Confidence",
    "dash.no_data":          "No data uploaded yet.",
    "dash.no_preds":         "No predictions yet.",

    // Crop Recommender
    "rec.title":             "Crop Recommender",
    "rec.subtitle":          "Enter your soil and climate data to get crop suggestions",
    "rec.soil_inputs":       "Soil & Climate Inputs",
    "rec.nitrogen":          "Nitrogen (N) kg/ha",
    "rec.phosphorus":        "Phosphorus (P) kg/ha",
    "rec.potassium":         "Potassium (K) kg/ha",
    "rec.soil_ph":           "Soil pH",
    "rec.rainfall":          "Avg Rainfall (mm/month)",
    "rec.temperature":       "Avg Temperature (°C)",
    "rec.get_recs":          "Get Recommendations",
    "rec.top_matches":       "Top Crop Matches",
    "rec.score_label":       "Best Match Suitability Score",
    "rec.match":             "match with your soil profile",
    "rec.profit":            "Est. Profit/Acre",
    "rec.water":             "Water Need",
    "rec.risk":              "Risk Level",
    "rec.duration":          "Duration",
    "rec.fertilizer_cta":    "Generate Fertilizer Plan →",
    "rec.comparison":        "Side-by-Side Comparison",
    "rec.how_it_works":      "How It Works",
    "rec.how_body":          "The recommender compares your NPK values, soil pH, rainfall, and temperature against optimal growing conditions for 12 common Indian crops. Match % shows how well your conditions align with each crop's ideal range. Profit estimates are approximate market averages per acre.",
    "rec.empty":             "Fill in the form to get personalized crop recommendations based on your soil profile.",
    "rec.match_col":         "Match",
    "rec.profit_col":        "Profit/Acre",
    "rec.water_col":         "Water",
    "rec.risk_col":          "Risk",

    // Fertilizer
    "fert.title":            "Fertilizer Calculator",
    "fert.subtitle":         "ICAR recommendations — exact quantity for your field size",
    "fert.enter":            "Enter Details",
    "fert.select_crop":      "Select Crop",
    "fert.placeholder":      "-- Select Crop --",
    "fert.area_label":       "Your Field Size (in Acres)",
    "fert.calc_btn":         "Calculate",
    "fert.summary":          "Summary",
    "fert.acres":            "Acres",
    "fert.hectares":         "Hectares",
    "fert.npk_req":          "Total NPK Required",
    "fert.seed_req":         "Seed Required",
    "fert.spacing":          "Spacing",
    "fert.plan_title":       "Fertilizer Plan — What, How Much, When",
    "fert.download":         "Download Report PDF",
    "fert.print":            "Print",
    "fert.name":             "Fertilizer",
    "fert.per_ha":           "Per Hectare",
    "fert.total":            "Your Total",
    "fert.bags":             "Bags (50kg)",
    "fert.when":             "When to Apply",
    "fert.tip_label":        "Expert Tip",
    "fert.source":           "Source: ICAR (Indian Council of Agricultural Research) recommendations. Adjust quantities after local soil test.",
    "fert.empty":            "Select crop and area — get exact fertilizer quantity, bag count, and timing.",

    // History
    "hist.title":            "Crop History",
    "hist.export_csv":       "Export CSV",
    "hist.search_crop":      "Search Crop",
    "hist.season":           "Season",
    "hist.all_seasons":      "All Seasons",
    "hist.filter":           "Filter",
    "hist.clear":            "Clear",
    "hist.no_records":       "No records found.",

    // Upload
    "upload.title":          "Upload Crop Data",
    "upload.subtitle":       "Upload your CSV or Excel file",
    "upload.btn":            "Upload File",

    // Mandi
    "mandi.title":           "Mandi Price Tracker",
    "mandi.state":           "State",
    "mandi.crop":            "Commodity",
    "mandi.district":        "District",
    "mandi.search":          "Search Prices",

    // Schemes
    "scheme.title":          "Government Scheme Finder",
    "scheme.state":          "Select State",
    "scheme.search":         "Find Schemes",

    // Common
    "common.loading":        "Loading...",
    "common.no_data":        "No data available.",
    "common.save":           "Save",
    "common.cancel":         "Cancel",
    "common.delete":         "Delete",
    "common.confirm_delete": "Confirm Delete",
  },

  hi: {
    // Nav
    "nav.farmer_tools":      "किसान औज़ार",
    "nav.kab_bechun":        "कब बेचूं? 🥇",
    "nav.reports":           "रिपोर्ट",
    "nav.dashboard":         "डैशबोर्ड",
    "nav.upload_data":       "डेटा अपलोड करें",
    "nav.predict_yield":     "उपज अनुमान",
    "nav.crop_recommender":  "फसल सुझाव",
    "nav.fertilizer_calc":   "खाद कैलकुलेटर",
    "nav.mandi_tracker":     "मंडी मूल्य ट्रैकर",
    "nav.pest_identifier":   "कीट पहचानकर्ता",
    "nav.scheme_finder":     "सरकारी योजनाएं",
    "nav.history":           "इतिहास",
    "nav.pdf_report":        "PDF रिपोर्ट",
    "nav.export_csv":        "CSV निर्यात",
    "nav.logout":            "लॉगआउट",

    // Dashboard
    "dash.title":            "मेरे खेत का सारांश",
    "dash.welcome":          "वापस स्वागत है",
    "dash.retrain":          "मॉडल पुनः प्रशिक्षित करें",
    "dash.export_pdf":       "PDF निर्यात करें",
    "dash.total_records":    "कुल रिकॉर्ड",
    "dash.uploaded_entries": "अपलोड की गई फसल प्रविष्टियां",
    "dash.predictions":      "अनुमान किए गए",
    "dash.ml_queries":       "ML मॉडल प्रश्न",
    "dash.avg_yield":        "औसत उपज (t/ha)",
    "dash.across_crops":     "सभी फसलों में",
    "dash.recent_crops":     "हाल की फसल डेटा",
    "dash.recent_preds":     "हाल के अनुमान",
    "dash.crop":             "फसल",
    "dash.state":            "राज्य",
    "dash.season":           "मौसम",
    "dash.area":             "क्षेत्र (हेक्टेयर)",
    "dash.yield":            "उपज (t/ha)",
    "dash.uploaded":         "अपलोड किया गया",
    "dash.confidence":       "विश्वास",
    "dash.no_data":          "अभी तक कोई डेटा अपलोड नहीं।",
    "dash.no_preds":         "अभी तक कोई अनुमान नहीं।",

    // Crop Recommender
    "rec.title":             "फसल सुझाव",
    "rec.subtitle":          "फसल सुझाव पाने के लिए मिट्टी और जलवायु डेटा दर्ज करें",
    "rec.soil_inputs":       "मिट्टी और जलवायु इनपुट",
    "rec.nitrogen":          "नाइट्रोजन (N) kg/ha",
    "rec.phosphorus":        "फास्फोरस (P) kg/ha",
    "rec.potassium":         "पोटेशियम (K) kg/ha",
    "rec.soil_ph":           "मिट्टी pH",
    "rec.rainfall":          "औसत वर्षा (mm/महीना)",
    "rec.temperature":       "औसत तापमान (°C)",
    "rec.get_recs":          "सुझाव प्राप्त करें",
    "rec.top_matches":       "शीर्ष फसल मिलान",
    "rec.score_label":       "सर्वश्रेष्ठ मिलान उपयुक्तता स्कोर",
    "rec.match":             "आपकी मिट्टी के साथ मिलान",
    "rec.profit":            "अनुमानित लाभ/एकड़",
    "rec.water":             "पानी की ज़रूरत",
    "rec.risk":              "जोखिम स्तर",
    "rec.duration":          "अवधि",
    "rec.fertilizer_cta":    "खाद योजना बनाएं →",
    "rec.comparison":        "साथ-साथ तुलना",
    "rec.how_it_works":      "यह कैसे काम करता है",
    "rec.how_body":          "यह सुझाव प्रणाली आपके NPK, pH, वर्षा और तापमान की तुलना 12 भारतीय फसलों की आदर्श परिस्थितियों से करती है।",
    "rec.empty":             "फसल सुझाव पाने के लिए फॉर्म भरें।",
    "rec.match_col":         "मिलान",
    "rec.profit_col":        "लाभ/एकड़",
    "rec.water_col":         "पानी",
    "rec.risk_col":          "जोखिम",

    // Fertilizer
    "fert.title":            "खाद कैलकुलेटर",
    "fert.subtitle":         "ICAR सिफारिशें — आपके खेत के अनुसार सटीक मात्रा",
    "fert.enter":            "विवरण दर्ज करें",
    "fert.select_crop":      "फसल चुनें",
    "fert.placeholder":      "-- फसल चुनें --",
    "fert.area_label":       "आपकी ज़मीन (एकड़ में)",
    "fert.calc_btn":         "गणना करें",
    "fert.summary":          "सारांश",
    "fert.acres":            "एकड़",
    "fert.hectares":         "हेक्टेयर",
    "fert.npk_req":          "कुल NPK आवश्यकता",
    "fert.seed_req":         "बीज की आवश्यकता",
    "fert.spacing":          "दूरी",
    "fert.plan_title":       "खाद योजना — क्या, कितना, कब",
    "fert.download":         "PDF रिपोर्ट डाउनलोड करें",
    "fert.print":            "प्रिंट",
    "fert.name":             "खाद",
    "fert.per_ha":           "प्रति हेक्टेयर",
    "fert.total":            "आपकी कुल",
    "fert.bags":             "बोरियां (50kg)",
    "fert.when":             "कब डालें",
    "fert.tip_label":        "विशेषज्ञ सुझाव",
    "fert.source":           "स्रोत: ICAR (भारतीय कृषि अनुसंधान परिषद) सिफारिशें।",
    "fert.empty":            "फसल और क्षेत्र दर्ज करें — सटीक खाद मात्रा, बोरी गिनती और समय पाएं।",

    // History
    "hist.title":            "फसल इतिहास",
    "hist.export_csv":       "CSV निर्यात",
    "hist.search_crop":      "फसल खोजें",
    "hist.season":           "मौसम",
    "hist.all_seasons":      "सभी मौसम",
    "hist.filter":           "फ़िल्टर",
    "hist.clear":            "साफ़ करें",
    "hist.no_records":       "कोई रिकॉर्ड नहीं मिला।",

    // Upload
    "upload.title":          "फसल डेटा अपलोड करें",
    "upload.subtitle":       "CSV या Excel फ़ाइल अपलोड करें",
    "upload.btn":            "फ़ाइल अपलोड करें",

    // Mandi
    "mandi.title":           "मंडी मूल्य ट्रैकर",
    "mandi.state":           "राज्य",
    "mandi.crop":            "फसल",
    "mandi.district":        "जिला",
    "mandi.search":          "कीमतें खोजें",

    // Schemes
    "scheme.title":          "सरकारी योजना खोजक",
    "scheme.state":          "राज्य चुनें",
    "scheme.search":         "योजनाएं खोजें",

    // Common
    "common.loading":        "लोड हो रहा है...",
    "common.no_data":        "कोई डेटा उपलब्ध नहीं।",
    "common.save":           "सहेजें",
    "common.cancel":         "रद्द करें",
    "common.delete":         "हटाएं",
    "common.confirm_delete": "हटाने की पुष्टि करें",
  },

  mr: {
    // Nav
    "nav.farmer_tools":      "शेतकरी साधने",
    "nav.kab_bechun":        "कधी विकू? 🥇",
    "nav.reports":           "अहवाल",
    "nav.dashboard":         "डॅशबोर्ड",
    "nav.upload_data":       "डेटा अपलोड करा",
    "nav.predict_yield":     "उत्पादन अंदाज",
    "nav.crop_recommender":  "पीक सुचवणी",
    "nav.fertilizer_calc":   "खत कॅल्क्युलेटर",
    "nav.mandi_tracker":     "बाजारभाव ट्रॅकर",
    "nav.pest_identifier":   "कीड ओळखणारा",
    "nav.scheme_finder":     "सरकारी योजना",
    "nav.history":           "इतिहास",
    "nav.pdf_report":        "PDF अहवाल",
    "nav.export_csv":        "CSV निर्यात",
    "nav.logout":            "बाहेर पडा",

    // Dashboard
    "dash.title":            "माझ्या शेताचा आढावा",
    "dash.welcome":          "पुन्हा स्वागत",
    "dash.retrain":          "मॉडेल पुन्हा प्रशिक्षित करा",
    "dash.export_pdf":       "PDF निर्यात करा",
    "dash.total_records":    "एकूण नोंदी",
    "dash.uploaded_entries": "अपलोड केलेल्या पीक नोंदी",
    "dash.predictions":      "अंदाज केलेले",
    "dash.ml_queries":       "ML मॉडेल प्रश्न",
    "dash.avg_yield":        "सरासरी उत्पादन (t/ha)",
    "dash.across_crops":     "सर्व पिकांमध्ये",
    "dash.recent_crops":     "अलीकडील पीक डेटा",
    "dash.recent_preds":     "अलीकडील अंदाज",
    "dash.crop":             "पीक",
    "dash.state":            "राज्य",
    "dash.season":           "हंगाम",
    "dash.area":             "क्षेत्र (हेक्टर)",
    "dash.yield":            "उत्पादन (t/ha)",
    "dash.uploaded":         "अपलोड केले",
    "dash.confidence":       "विश्वासार्हता",
    "dash.no_data":          "अद्याप कोणताही डेटा अपलोड नाही.",
    "dash.no_preds":         "अद्याप कोणताही अंदाज नाही.",

    // Crop Recommender
    "rec.title":             "पीक सुचवणी",
    "rec.subtitle":          "पीक सुचवणी मिळवण्यासाठी माती व हवामान डेटा भरा",
    "rec.soil_inputs":       "माती व हवामान इनपुट",
    "rec.nitrogen":          "नायट्रोजन (N) kg/ha",
    "rec.phosphorus":        "फॉस्फरस (P) kg/ha",
    "rec.potassium":         "पोटॅशियम (K) kg/ha",
    "rec.soil_ph":           "मातीचा pH",
    "rec.rainfall":          "सरासरी पाऊस (mm/महिना)",
    "rec.temperature":       "सरासरी तापमान (°C)",
    "rec.get_recs":          "सुचवणी मिळवा",
    "rec.top_matches":       "सर्वोत्तम पीक जुळणी",
    "rec.score_label":       "सर्वोत्तम जुळणी उपयुक्तता स्कोर",
    "rec.match":             "तुमच्या मातीशी जुळणी",
    "rec.profit":            "अंदाजित नफा/एकर",
    "rec.water":             "पाण्याची गरज",
    "rec.risk":              "जोखीम पातळी",
    "rec.duration":          "कालावधी",
    "rec.fertilizer_cta":    "खत योजना तयार करा →",
    "rec.comparison":        "बाजू-बाजू तुलना",
    "rec.how_it_works":      "हे कसे काम करते",
    "rec.how_body":          "ही सुचवणी प्रणाली तुमचे NPK, pH, पाऊस आणि तापमान 12 भारतीय पिकांच्या आदर्श परिस्थितींशी तुलना करते.",
    "rec.empty":             "पीक सुचवणी मिळवण्यासाठी फॉर्म भरा.",
    "rec.match_col":         "जुळणी",
    "rec.profit_col":        "नफा/एकर",
    "rec.water_col":         "पाणी",
    "rec.risk_col":          "जोखीम",

    // Fertilizer
    "fert.title":            "खत कॅल्क्युलेटर",
    "fert.subtitle":         "ICAR शिफारसी — तुमच्या शेतासाठी अचूक प्रमाण",
    "fert.enter":            "तपशील भरा",
    "fert.select_crop":      "पीक निवडा",
    "fert.placeholder":      "-- पीक निवडा --",
    "fert.area_label":       "तुमची जमीन (एकरात)",
    "fert.calc_btn":         "गणना करा",
    "fert.summary":          "सारांश",
    "fert.acres":            "एकर",
    "fert.hectares":         "हेक्टर",
    "fert.npk_req":          "एकूण NPK आवश्यकता",
    "fert.seed_req":         "बियाण्याची आवश्यकता",
    "fert.spacing":          "अंतर",
    "fert.plan_title":       "खत योजना — काय, किती, कधी",
    "fert.download":         "PDF अहवाल डाउनलोड करा",
    "fert.print":            "प्रिंट करा",
    "fert.name":             "खत",
    "fert.per_ha":           "प्रति हेक्टर",
    "fert.total":            "तुमचे एकूण",
    "fert.bags":             "पोती (50kg)",
    "fert.when":             "कधी घालावे",
    "fert.tip_label":        "तज्ज्ञ सल्ला",
    "fert.source":           "स्रोत: ICAR (भारतीय कृषी संशोधन परिषद) शिफारसी.",
    "fert.empty":            "पीक आणि क्षेत्र भरा — अचूक खत प्रमाण, पोती संख्या आणि वेळ मिळवा.",

    // History
    "hist.title":            "पीक इतिहास",
    "hist.export_csv":       "CSV निर्यात",
    "hist.search_crop":      "पीक शोधा",
    "hist.season":           "हंगाम",
    "hist.all_seasons":      "सर्व हंगाम",
    "hist.filter":           "फिल्टर",
    "hist.clear":            "साफ करा",
    "hist.no_records":       "कोणतीही नोंद सापडली नाही.",

    // Upload
    "upload.title":          "पीक डेटा अपलोड करा",
    "upload.subtitle":       "CSV किंवा Excel फाइल अपलोड करा",
    "upload.btn":            "फाइल अपलोड करा",

    // Mandi
    "mandi.title":           "बाजारभाव ट्रॅकर",
    "mandi.state":           "राज्य",
    "mandi.crop":            "पीक",
    "mandi.district":        "जिल्हा",
    "mandi.search":          "भाव शोधा",

    // Schemes
    "scheme.title":          "सरकारी योजना शोधक",
    "scheme.state":          "राज्य निवडा",
    "scheme.search":         "योजना शोधा",

    // Common
    "common.loading":        "लोड होत आहे...",
    "common.no_data":        "कोणताही डेटा उपलब्ध नाही.",
    "common.save":           "जतन करा",
    "common.cancel":         "रद्द करा",
    "common.delete":         "हटवा",
    "common.confirm_delete": "हटवण्याची पुष्टी करा",
  }
};

// ──────────────────────────────────────────────
// Core engine
// ──────────────────────────────────────────────
const I18N_KEY = 'cs_lang';
const LANG_META = {
  en: { label: 'EN', flag: '🇬🇧', name: 'English' },
  hi: { label: 'हि', flag: '🇮🇳', name: 'हिंदी' },
  mr: { label: 'म',  flag: '🌾',  name: 'मराठी' },
};

function getCurrentLang() {
  return localStorage.getItem(I18N_KEY) || 'en';
}

function t(key) {
  const lang = getCurrentLang();
  return (TRANSLATIONS[lang] && TRANSLATIONS[lang][key]) ||
         (TRANSLATIONS['en'][key]) ||
         key;
}

function applyTranslations() {
  const lang = getCurrentLang();
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    const val = (TRANSLATIONS[lang] && TRANSLATIONS[lang][key]) || TRANSLATIONS['en'][key] || key;
    if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
      el.placeholder = val;
    } else {
      el.textContent = val;
    }
  });
  // Update html lang attribute
  document.documentElement.lang = lang === 'mr' ? 'mr' : lang === 'hi' ? 'hi' : 'en';
  // Update toggle button active state
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.lang === lang);
  });
}

function setLang(lang) {
  localStorage.setItem(I18N_KEY, lang);
  applyTranslations();
}

// ──────────────────────────────────────────────
// Toggle widget — injected into topbar
// ──────────────────────────────────────────────
function injectLangToggle() {
  const topbarActions = document.querySelector('.topbar-actions');
  if (!topbarActions) return;

  const wrap = document.createElement('div');
  wrap.className = 'lang-toggle';
  wrap.innerHTML = Object.entries(LANG_META).map(([code, meta]) =>
    `<button class="lang-btn" data-lang="${code}" onclick="setLang('${code}')" title="${meta.name}">${meta.flag} ${meta.label}</button>`
  ).join('');

  // Insert before first child of topbar-actions
  topbarActions.insertBefore(wrap, topbarActions.firstChild);
}

// ──────────────────────────────────────────────
// Init
// ──────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  injectLangToggle();
  applyTranslations();
});
