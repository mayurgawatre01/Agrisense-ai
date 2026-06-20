# 🌾 CropSense v3.1 — Smart Agriculture Analytics

A Flask-based agricultural ML web app for farmers to upload crop data, predict yields, get soil-based crop recommendations, track mandi prices, identify crop pests/diseases via AI photo analysis, and find relevant government schemes.

---

## 🆕 What's New in v3.1 — "Kab Bechun?" Tools

| Feature | Description |
|---|---|
| 📊 **Mandi Price Tracker** | Live mandi (market) rates by state + crop from AGMARKNET (data.gov.in), with automatic offline fallback to curated price data when the live API is unavailable. Optional district filter compares prices across all mandis/talukas within a district, best price highlighted. Includes a "Kab Bechun?" seasonal price-pattern chart + verdict for 20 crops. |
| 🔬 **Pest/Disease Identifier** | Upload a crop photo → Google Gemini (primary) or Anthropic Claude (fallback) vision AI analyses it and returns the likely disease/pest, symptoms, organic + chemical treatment, and prevention tips in simple Hindi |
| 🏛️ **Govt Scheme Finder** | Select your state → see all relevant Central + State government farmer welfare schemes (PM-KISAN, PMFBY, KCC, Soil Health Card, etc.) with eligibility, documents needed, and how to apply |
| 🌱 **Fertilizer Calculator v2** | Visual NPK progress bars (instead of plain numbers), per-fertilizer quantity bars, and a downloadable PDF report button |

All three are fully bilingual-friendly (Hinglish), mobile-responsive, and built to match the existing CropSense dark theme.

## 🆕 What's New in v3.0

| Feature | Description |
|---|---|
| 🌱 **Crop Recommender** | Input NPK, pH, rainfall, temperature → get top 3 crop suggestions |
| ☁️ **Live Weather Widget** | Topbar + dashboard card showing real-time weather for any city |
| 🔁 **Model Retrain Button** | One-click retrain ML model from dashboard after uploading new data |
| 🔍 **History Search & Filter** | Search crops by name, filter by season |
| 🗑️ **Bulk Delete History** | Select multiple records and delete in one click |
| 📥 **Export CSV** | Download all crop history as a .csv file |
| 🛡️ **Admin Panel** | View all users, their record/prediction counts, delete users |
| 🔐 **dotenv support** | Secrets via `.env` file — no hardcoded API keys |
| 📊 **More Charts** | Prediction confidence line chart + top crops doughnut chart |

---

## 🚀 Quick Start

```bash
# 1. Clone / unzip project
cd cropsense5

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment (optional but recommended)
cp .env.example .env
# Edit .env to add your WEATHER_API_KEY (free from openweathermap.org)
# Add DATA_GOV_API_KEY for live Mandi prices (free from data.gov.in)
# Add ANTHROPIC_API_KEY to enable the AI Pest/Disease Identifier (console.anthropic.com)

# 5. Run
python app.py
```

Open `http://127.0.0.1:5000`

**Default admin:** `admin@cropsense.com` / `admin123`

---

## 📊 Mandi Price Tracker

Navigate to **Mandi Price Tracker** in the sidebar. Select your state and crop to see:
- Live modal/min/max prices per quintal from AGMARKNET (when `DATA_GOV_API_KEY` is set and reachable)
- An automatic offline estimate (clearly labelled) if the live API can't be reached — the feature never breaks
- **District/Taluka comparison**: optionally select a district to compare prices across all mandis (markets/talukas)
  within that district side-by-side, sorted with the best (highest) price on top — answers "konsi mandi mein abhi
  best rate hai" within your district. Note: true historical taluka-level *seasonal* data isn't available from any
  free public source, so the seasonal trend chart below remains crop-level (state/national pattern), clearly labelled as such.
- **"Kab Bechun?" seasonal pattern**: a month-wise historical price-index chart for the selected crop, plus a clear verdict
  ("Abhi Bechna Sahi Hai" / "Thoda Ruk Sakte Ho" / "Average Mahina Hai") with the best and worst months to sell —
  based on curated Indian agri-market seasonality data (`utils/seasonal_data.py`, 20 crops covered)

Get a free key at [data.gov.in](https://data.gov.in/) (Sign Up → My Account → API Key):
```
DATA_GOV_API_KEY=your_key_here
```

## 🔬 Pest/Disease Identifier

Navigate to **Pest/Disease Identifier** in the sidebar. Upload a clear photo of an affected leaf/stem/fruit:
- Tries **Google Gemini** (vision) first — it has a generous free tier, recommended for getting started quickly
- Automatically falls back to **Anthropic Claude** (vision) if Gemini's key is missing or the call fails
- Returns the likely problem, confidence level, symptoms, organic treatment, chemical treatment, and prevention — all in simple Hindi
- A built-in offline quick-reference table of common pests/diseases is always shown alongside, even without any API key
- Without **either** key configured, the page clearly tells the farmer the AI analysis isn't set up yet (no fake results are ever shown)

```
GEMINI_API_KEY=your_key_here       # get free at aistudio.google.com/apikey
ANTHROPIC_API_KEY=your_key_here    # optional fallback, console.anthropic.com
```

## 🏛️ Govt Scheme Finder

Navigate to **Govt Scheme Finder** in the sidebar. Select your state to see:
- All major Central Government schemes (PM-KISAN, PMFBY, KCC, Soil Health Card, PMKSY, e-NAM, Agri Infrastructure Fund)
- Any extra State-specific schemes available for that state
- Eligibility, required documents, how-to-apply steps, and a direct link to the official portal for each scheme

---

## 🌱 Fertilizer Calculator v2

Navigate to **Fertilizer Calc** in the sidebar. Select crop + area to see:
- **Visual progress bars** for total NPK (Nitrogen/Phosphorus/Potassium) required, scaled proportionately across crops
- **Per-fertilizer quantity bars** in the application table (Urea/DAP/MOP etc.), alongside bag counts and timing
- **Download Report PDF** — a clean printable PDF of the full fertilizer plan (crop, area, NPK totals, application
  table, expert tip), generated with `utils/pdf_generator.py::generate_fertilizer_report()`
- Existing browser Print button still available alongside the new PDF download

> Roadmap items not yet built (tracked for a future update): soil-test-based dynamic NPK adjustment, cost calculator,
> weather-based application timing, yield prediction, crop calendar timeline, and a full EN/Hindi/Marathi language
> toggle across the whole app (large scope — planned as a separate dedicated pass).

---

## 🌤️ Weather Integration

Weather works in two modes:
- **Without API key:** Shows mock/demo data (still functional for UI/demo)
- **With API key:** Live real-time weather from OpenWeatherMap (free tier)

Get a free key at [openweathermap.org/api](https://openweathermap.org/api) and add it to `.env`:
```
WEATHER_API_KEY=your_key_here
```

---

## 📁 Project Structure

```
cropsense5/
├── app.py              # Flask factory + admin creation
├── auth.py             # Login / register / logout
├── farmer.py           # Main farmer routes (v3: +weather, +recommend, +export, +retrain)
├── admin.py            # Admin panel blueprint
├── tools.py             # NEW v3.1: Mandi Tracker, Pest Identifier, Scheme Finder blueprint
├── models.py            # SQLAlchemy models
├── extensions.py        # db, bcrypt
├── requirements.txt
├── .env.example         # Environment template (v3.1: +DATA_GOV_API_KEY, +ANTHROPIC_API_KEY)
├── ml/
│   ├── predictor.py     # predict_yield() with caching
│   └── train_model.py   # Random Forest training script
├── utils/
│   ├── data_processor.py
│   ├── pdf_generator.py
│   ├── fertilizer_data.py
│   ├── mandi_data.py      # NEW v3.1: AGMARKNET live + offline fallback price data
│   ├── seasonal_data.py   # NEW v3.1: "Kab Bechun?" seasonal price-index data (20 crops)
│   ├── pest_identifier.py # NEW v3.1: Gemini + Claude vision diagnosis + offline guide
│   └── scheme_data.py     # NEW v3.1: Govt scheme data (national + state-specific)
├── templates/
│   ├── base.html        # v3.1: nav links for the 3 new tools
│   ├── dashboard.html   # v3.1: "Sabse Tagdi" quick-access feature row
│   ├── mandi.html        # NEW v3.1: Mandi Price Tracker
│   ├── pest.html         # NEW v3.1: Pest/Disease Identifier
│   ├── schemes.html      # NEW v3.1: Govt Scheme Finder
│   └── ...
└── static/
    ├── css/main.css     # v3.1: feature-card link styling appended
    ├── js/main.js
    └── pest_uploads/    # NEW v3.1: uploaded crop photos for AI analysis
```

---

## 🤖 ML Pipeline

1. Upload CSV (`State, District, Crop_Year, Season, Crop, Area, Production`)
2. Go to Dashboard → click **Retrain Model**
3. Model trains with Random Forest (300 trees, k-fold CV)
4. Future predictions use the trained model automatically
5. If no model trained → rule-based fallback (still useful)

---

## 🌱 Crop Recommender

Navigate to **Crop Recommender** in the sidebar. Enter:
- Nitrogen, Phosphorus, Potassium (kg/ha)
- Soil pH
- Average monthly rainfall (mm)
- Average temperature (°C)

The system scores 12 common Indian crops against your inputs and returns the top 3 matches with a percentage score.

---

## 🔐 Roles

| Role | Access |
|---|---|
| `farmer` | Dashboard, Upload, Predict, Recommend, History, Reports |
| `admin` | Everything above + Admin Panel (user management) |
