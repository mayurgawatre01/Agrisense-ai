"""
CropSense v3.1 — Mandi Price Data
Live source : data.gov.in "Current Daily Price of Various Commodities" (AGMARKNET)
              Resource ID: 9ef84268-d588-465a-a308-a864a43d0070
              Needs a free API key from https://data.gov.in/ (set DATA_GOV_API_KEY in .env)
Fallback    : SEED_PRICES below — curated typical modal-price ranges (Rs/quintal),
              shown automatically when the live API key is missing or the request fails,
              so the feature always works for the farmer.
"""
import os
import urllib.request
import urllib.parse
import json
from datetime import datetime

AGMARKNET_RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"
AGMARKNET_BASE_URL = f"https://api.data.gov.in/resource/{AGMARKNET_RESOURCE_ID}"

# A safe, well-known "test" key that data.gov.in publishes for public/demo use.
# Replace with your own free key from https://data.gov.in/ for production reliability.
PUBLIC_DEMO_KEY = "579b464db66ec23bdd0000010bb961a4072447a78659e3b1a3b8db3"

STATES = [
    "Maharashtra", "Punjab", "Haryana", "Uttar Pradesh", "Madhya Pradesh",
    "Rajasthan", "Gujarat", "Karnataka", "Tamil Nadu", "Andhra Pradesh",
    "Telangana", "Bihar", "West Bengal", "Odisha", "Chhattisgarh"
]

# Major districts per state, for the optional district filter dropdown.
# (data.gov.in doesn't expose a districts-list endpoint, so this is a
# curated list of well-known agricultural districts per state.)
DISTRICTS_BY_STATE = {
    "Maharashtra": ["Pune", "Nashik", "Nagpur", "Aurangabad", "Solapur", "Kolhapur", "Ahmednagar", "Jalgaon", "Latur", "Amravati"],
    "Punjab": ["Ludhiana", "Amritsar", "Patiala", "Jalandhar", "Bathinda", "Sangrur", "Ferozepur"],
    "Haryana": ["Karnal", "Hisar", "Rohtak", "Sirsa", "Kurukshetra", "Panipat", "Sonipat"],
    "Uttar Pradesh": ["Meerut", "Lucknow", "Kanpur", "Agra", "Bareilly", "Varanasi", "Aligarh", "Moradabad"],
    "Madhya Pradesh": ["Indore", "Bhopal", "Jabalpur", "Gwalior", "Ujjain", "Sagar", "Hoshangabad"],
    "Rajasthan": ["Jaipur", "Kota", "Jodhpur", "Bikaner", "Udaipur", "Alwar", "Sri Ganganagar"],
    "Gujarat": ["Ahmedabad", "Rajkot", "Surat", "Vadodara", "Bhavnagar", "Junagadh", "Kutch"],
    "Karnataka": ["Belagavi", "Mysuru", "Bengaluru Rural", "Hubballi", "Davangere", "Shivamogga", "Raichur"],
    "Tamil Nadu": ["Coimbatore", "Madurai", "Erode", "Salem", "Thanjavur", "Tiruchirappalli", "Vellore"],
    "Andhra Pradesh": ["Guntur", "Krishna", "East Godavari", "West Godavari", "Kurnool", "Chittoor", "Anantapur"],
    "Telangana": ["Warangal", "Karimnagar", "Nizamabad", "Khammam", "Nalgonda", "Adilabad", "Medak"],
    "Bihar": ["Patna", "Gaya", "Muzaffarpur", "Bhagalpur", "Darbhanga", "Purnia"],
    "West Bengal": ["Bardhaman", "Hooghly", "Murshidabad", "Nadia", "Malda", "Cooch Behar"],
    "Odisha": ["Cuttack", "Bhubaneswar", "Sambalpur", "Balasore", "Ganjam", "Mayurbhanj"],
    "Chhattisgarh": ["Raipur", "Bilaspur", "Durg", "Raigarh", "Rajnandgaon", "Korba"],
}

# ── Seed / fallback data ───────────────────────────────────────────────────
# Typical modal price ranges in Rs per Quintal (100 kg), based on recent
# AGMARKNET trends. Used ONLY when the live API is unavailable, clearly
# labelled to the farmer as an approximate offline estimate.
SEED_PRICES = {
    "Rice":       {"min": 1850, "max": 2400, "modal": 2100, "unit": "Quintal"},
    "Wheat":      {"min": 2150, "max": 2500, "modal": 2300, "unit": "Quintal"},
    "Maize":      {"min": 1700, "max": 2150, "modal": 1950, "unit": "Quintal"},
    "Cotton":     {"min": 6800, "max": 7700, "modal": 7200, "unit": "Quintal"},
    "Sugarcane":  {"min": 300,  "max": 380,  "modal": 340,  "unit": "Quintal"},
    "Groundnut":  {"min": 5800, "max": 6800, "modal": 6300, "unit": "Quintal"},
    "Soyabean":   {"min": 4200, "max": 4800, "modal": 4500, "unit": "Quintal"},
    "Potato":     {"min": 900,  "max": 1600, "modal": 1200, "unit": "Quintal"},
    "Tomato":     {"min": 600,  "max": 2200, "modal": 1200, "unit": "Quintal"},
    "Onion":      {"min": 900,  "max": 2000, "modal": 1400, "unit": "Quintal"},
    "Bajra":      {"min": 1900, "max": 2300, "modal": 2100, "unit": "Quintal"},
    "Jowar":      {"min": 2800, "max": 3400, "modal": 3100, "unit": "Quintal"},
    "Gram":       {"min": 4800, "max": 5600, "modal": 5200, "unit": "Quintal"},
    "Mustard":    {"min": 5200, "max": 5800, "modal": 5500, "unit": "Quintal"},
    "Turmeric":   {"min": 7500, "max": 9500, "modal": 8500, "unit": "Quintal"},
    "Chilli":     {"min": 11000,"max": 16000,"modal": 13500,"unit": "Quintal"},
    "Banana":     {"min": 800,  "max": 1500, "modal": 1100, "unit": "Quintal"},
    "Brinjal":    {"min": 700,  "max": 1700, "modal": 1100, "unit": "Quintal"},
    "Cabbage":    {"min": 400,  "max": 1100, "modal": 700,  "unit": "Quintal"},
    "Cauliflower":{"min": 600,  "max": 1500, "modal": 1000, "unit": "Quintal"},
}

CROP_LIST = sorted(SEED_PRICES.keys())


def get_mandi_price(state: str, commodity: str, api_key: str = "", district: str = ""):
    """
    Try the live AGMARKNET API first. On any failure (no key, network,
    no matching records), fall back to curated seed data so the page
    never breaks for the farmer.

    If `district` is given, filters to that district and returns up to 20
    mandi-wise rows (useful for taluka/mandi comparison within a district).
    Without a district, returns up to 10 rows for the whole state.

    Returns a dict with: success, source ('live'|'fallback'), records, message
    """
    key = api_key or os.environ.get("DATA_GOV_API_KEY", "") or PUBLIC_DEMO_KEY
    row_limit = "20" if district else "10"

    try:
        params = {
            "api-key": key,
            "format": "json",
            "limit": row_limit,
            "filters[state]": state,
            "filters[commodity]": commodity,
        }
        if district:
            params["filters[district]"] = district

        url = AGMARKNET_BASE_URL + "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"User-Agent": "CropSense/3.1"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        records = data.get("records", [])
        if records:
            cleaned = []
            for r in records[:int(row_limit)]:
                cleaned.append({
                    "market":   r.get("market", "—"),
                    "district": r.get("district", "—"),
                    "variety":  r.get("variety", "—"),
                    "min":      r.get("min_price", "—"),
                    "max":      r.get("max_price", "—"),
                    "modal":    r.get("modal_price", "—"),
                    "date":     r.get("arrival_date", "—"),
                })
            # Sort by modal price descending so the best-paying mandi is on top
            try:
                cleaned.sort(key=lambda r: float(r["modal"]), reverse=True)
            except (ValueError, TypeError):
                pass
            return {
                "success": True,
                "source": "live",
                "records": cleaned,
                "message": "AGMARKNET (data.gov.in) se live rate mila."
            }
    except Exception:
        pass  # fall through to seed data

    # ── Fallback ──
    seed = SEED_PRICES.get(commodity)
    if not seed:
        return {
            "success": False,
            "source": "none",
            "records": [],
            "message": f"'{commodity}' ke liye abhi data available nahi hai."
        }

    label = f"{district}, {state}" if district else f"{state} (Approx. Average)"
    fallback_msg = (
        "Live mandi data abhi unavailable hai — yeh estimated average rate hai (offline data)."
        if not district else
        "Live taluka/mandi-wise data abhi unavailable hai — yeh state-level estimated average hai. "
        "Apni nazdeeki mandi mein confirm karein."
    )

    return {
        "success": True,
        "source": "fallback",
        "records": [{
            "market":   label,
            "district": district or "—",
            "variety":  "Standard",
            "min":      seed["min"],
            "max":      seed["max"],
            "modal":    seed["modal"],
            "date":     datetime.now().strftime("%d-%m-%Y"),
        }],
        "message": fallback_msg
    }
