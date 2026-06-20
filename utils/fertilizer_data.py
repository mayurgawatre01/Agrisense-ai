"""
CropSense v3.0 — Fertilizer Data (ICAR Recommendations)
Source: ICAR (Indian Council of Agricultural Research) public guidelines
NPK values in kg/hectare, seed rate in kg/hectare
"""

FERTILIZER_DATA = {
    "Rice": {
        "seasons": ["Kharif"],
        "npk": {"N": 120, "P": 60, "K": 60},
        "seed_rate": 50,
        "spacing": "20x15 cm",
        "fertilizers": [
            {"name": "Urea",       "qty_per_ha": 261, "timing": "Split — 50% basal, 25% tillering, 25% panicle"},
            {"name": "DAP",        "qty_per_ha": 130, "timing": "Basal (sowing ke time)"},
            {"name": "MOP (K)",    "qty_per_ha": 100, "timing": "Basal"},
        ],
        "tips": "Zinc deficiency common hai — 25 kg ZnSO4/ha basal mein daalo."
    },
    "Wheat": {
        "seasons": ["Rabi"],
        "npk": {"N": 120, "P": 60, "K": 40},
        "seed_rate": 100,
        "spacing": "Row to row 22.5 cm",
        "fertilizers": [
            {"name": "Urea",       "qty_per_ha": 261, "timing": "50% basal, 25% CRI stage, 25% jointing"},
            {"name": "DAP",        "qty_per_ha": 130, "timing": "Basal"},
            {"name": "MOP (K)",    "qty_per_ha": 67,  "timing": "Basal"},
        ],
        "tips": "First irrigation (CRI) ke baad top dressing karo. Late sowing mein N 20% badhao."
    },
    "Maize": {
        "seasons": ["Kharif", "Rabi"],
        "npk": {"N": 150, "P": 75, "K": 75},
        "seed_rate": 20,
        "spacing": "60x25 cm",
        "fertilizers": [
            {"name": "Urea",       "qty_per_ha": 326, "timing": "1/3 basal, 1/3 knee-high, 1/3 tasseling"},
            {"name": "DAP",        "qty_per_ha": 163, "timing": "Basal"},
            {"name": "MOP (K)",    "qty_per_ha": 125, "timing": "Basal"},
        ],
        "tips": "FYM 10 t/ha basal mein mix karo — yield significantly badhti hai."
    },
    "Cotton": {
        "seasons": ["Kharif"],
        "npk": {"N": 120, "P": 60, "K": 60},
        "seed_rate": 4,
        "spacing": "90x60 cm (BT Cotton)",
        "fertilizers": [
            {"name": "Urea",       "qty_per_ha": 261, "timing": "25% basal, 25% square formation, 50% boll dev"},
            {"name": "DAP",        "qty_per_ha": 130, "timing": "Basal"},
            {"name": "MOP (K)",    "qty_per_ha": 100, "timing": "50% basal, 50% boll development"},
        ],
        "tips": "Boron (0.5 kg/ha) aur Zinc (5 kg/ha) micronutrients zaroor daalo."
    },
    "Sugarcane": {
        "seasons": ["Whole Year"],
        "npk": {"N": 250, "P": 85, "K": 115},
        "seed_rate": 5000,  # setts per hectare
        "spacing": "90 cm row spacing",
        "fertilizers": [
            {"name": "Urea",       "qty_per_ha": 543, "timing": "25% planting, 50% (3 months), 25% (5 months)"},
            {"name": "SSP",        "qty_per_ha": 531, "timing": "Basal"},
            {"name": "MOP (K)",    "qty_per_ha": 192, "timing": "50% basal, 50% at 3 months"},
        ],
        "tips": "Trash mulching karo — moisture conserve hogi aur ratoon crop better hogi."
    },
    "Soyabean": {
        "seasons": ["Kharif"],
        "npk": {"N": 30, "P": 60, "K": 40},
        "seed_rate": 70,
        "spacing": "45x5 cm",
        "fertilizers": [
            {"name": "Urea",       "qty_per_ha": 65,  "timing": "Basal only (rhizobium fix karta hai N)"},
            {"name": "DAP",        "qty_per_ha": 130, "timing": "Basal"},
            {"name": "MOP (K)",    "qty_per_ha": 67,  "timing": "Basal"},
        ],
        "tips": "Rhizobium + PSB seed treatment karo — N requirement 50% kam ho jaayegi."
    },
    "Groundnut": {
        "seasons": ["Kharif", "Rabi"],
        "npk": {"N": 25, "P": 50, "K": 75},
        "seed_rate": 100,
        "spacing": "30x10 cm",
        "fertilizers": [
            {"name": "Urea",       "qty_per_ha": 54,  "timing": "Basal"},
            {"name": "SSP",        "qty_per_ha": 313, "timing": "Basal (SSP preferred — S bhi deta hai)"},
            {"name": "MOP (K)",    "qty_per_ha": 125, "timing": "Basal"},
            {"name": "Gypsum",     "qty_per_ha": 500, "timing": "Pegging stage pe"},
        ],
        "tips": "Gypsum zaroor daalo pegging pe — pod filling improve hoti hai."
    },
    "Onion": {
        "seasons": ["Rabi", "Kharif"],
        "npk": {"N": 100, "P": 50, "K": 100},
        "seed_rate": 10,
        "spacing": "15x10 cm",
        "fertilizers": [
            {"name": "Urea",       "qty_per_ha": 217, "timing": "1/3 basal, 1/3 30 days, 1/3 45 days"},
            {"name": "DAP",        "qty_per_ha": 109, "timing": "Basal"},
            {"name": "MOP (K)",    "qty_per_ha": 167, "timing": "50% basal, 50% at 30 days"},
        ],
        "tips": "Sulfur (20 kg/ha) se pungency aur shelf life badhti hai."
    },
    "Tomato": {
        "seasons": ["Kharif", "Rabi"],
        "npk": {"N": 150, "P": 75, "K": 75},
        "seed_rate": 0.4,
        "spacing": "60x45 cm",
        "fertilizers": [
            {"name": "Urea",       "qty_per_ha": 326, "timing": "25% basal, rest in 3 splits every 20 days"},
            {"name": "DAP",        "qty_per_ha": 163, "timing": "Basal"},
            {"name": "MOP (K)",    "qty_per_ha": 125, "timing": "25% basal, 75% fruit development"},
        ],
        "tips": "Calcium spray karo (0.5% CaCl2) — blossom end rot rokta hai."
    },
    "Potato": {
        "seasons": ["Rabi"],
        "npk": {"N": 180, "P": 80, "K": 100},
        "seed_rate": 2500,  # kg/ha (tubers)
        "spacing": "60x20 cm",
        "fertilizers": [
            {"name": "Urea",       "qty_per_ha": 391, "timing": "50% basal, 50% earthing up"},
            {"name": "DAP",        "qty_per_ha": 174, "timing": "Basal"},
            {"name": "MOP (K)",    "qty_per_ha": 167, "timing": "50% basal, 50% earthing up"},
        ],
        "tips": "FYM 25 t/ha zaroor daalo. Seed treatment with fungicide karein."
    },
    "Bajra": {
        "seasons": ["Kharif"],
        "npk": {"N": 80, "P": 40, "K": 40},
        "seed_rate": 5,
        "spacing": "45x15 cm",
        "fertilizers": [
            {"name": "Urea",       "qty_per_ha": 174, "timing": "50% basal, 50% at 30 days"},
            {"name": "DAP",        "qty_per_ha": 87,  "timing": "Basal"},
            {"name": "MOP (K)",    "qty_per_ha": 67,  "timing": "Basal"},
        ],
        "tips": "Drought tolerant crop hai — over irrigation avoid karo."
    },
    "Jowar": {
        "seasons": ["Kharif", "Rabi"],
        "npk": {"N": 80, "P": 40, "K": 40},
        "seed_rate": 10,
        "spacing": "45x15 cm",
        "fertilizers": [
            {"name": "Urea",       "qty_per_ha": 174, "timing": "50% basal, 50% at knee-high stage"},
            {"name": "DAP",        "qty_per_ha": 87,  "timing": "Basal"},
            {"name": "MOP (K)",    "qty_per_ha": 67,  "timing": "Basal"},
        ],
        "tips": "Charcoal rot se bachne ke liye moisture stress avoid karo grain filling pe."
    },
}


def get_fertilizer_plan(crop: str, area_acres: float) -> dict:
    """
    Returns complete fertilizer plan for given crop and area.
    area_acres: farmer input in acres (converted to hectares internally)
    """
    if crop not in FERTILIZER_DATA:
        return {"success": False, "error": f"Data not available for {crop}"}

    data = FERTILIZER_DATA[crop]
    area_ha = area_acres * 0.4047  # acres to hectares

    npk = data["npk"]
    # Reference max per-hectare values across the whole crop dataset, used to
    # scale the visual progress bars proportionately (not crop-relative 100%).
    npk_bar_max = {"N": 300, "P": 100, "K": 130}
    npk_pct = {
        k: min(100, round((v / npk_bar_max[k]) * 100)) for k, v in npk.items()
    }

    fertilizers = []
    max_fert_total = max(f["qty_per_ha"] for f in data["fertilizers"]) * area_ha if data["fertilizers"] else 1
    for f in data["fertilizers"]:
        total_kg = round(f["qty_per_ha"] * area_ha, 1)
        bags_50kg = round(total_kg / 50, 1)
        fertilizers.append({
            "name": f["name"],
            "per_ha": f["qty_per_ha"],
            "total_kg": total_kg,
            "bags_50kg": bags_50kg,
            "timing": f["timing"],
            "bar_pct": min(100, round((total_kg / max_fert_total) * 100)) if max_fert_total else 0,
        })

    seed_total = round(data["seed_rate"] * area_ha, 1)

    return {
        "success": True,
        "crop": crop,
        "area_acres": area_acres,
        "area_ha": round(area_ha, 2),
        "seasons": data["seasons"],
        "npk_per_ha": npk,
        "npk_total": {k: round(v * area_ha, 1) for k, v in npk.items()},
        "npk_pct": npk_pct,
        "fertilizers": fertilizers,
        "seed_rate_per_ha": data["seed_rate"],
        "seed_total": seed_total,
        "spacing": data["spacing"],
        "tips": data["tips"],
    }


def get_all_crops():
    return sorted(FERTILIZER_DATA.keys())
