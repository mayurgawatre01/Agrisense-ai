"""
CropSense v3.1 — Seasonal "Kab Bechun?" Price Pattern Data
Curated month-wise seasonal price index for major Indian crops, based on
well-documented agricultural market patterns (harvest timing → supply glut
→ low prices; lean/off-season → low arrivals → high prices). Sources:
AGMARKNET seasonal-index studies, ICAR/Ministry of Agriculture harvest
calendars, and published seasonality research (e.g. onion: high Aug-Jan,
low Mar-Jul due to Rabi harvest; wheat: low Apr-Jul at harvest, high Dec
due to thin arrivals).

Index values are relative (100 = annual average price). These are typical
historical PATTERNS, not live predictions — actual prices vary year to year
with weather, exports, and government policy. Farmers should treat this as
general seasonal guidance, not a guarantee.
"""

MONTH_NAMES_HI = [
    "Jan", "Feb", "Mar", "Apr", "Mai", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

# 12 monthly index values per crop (Jan..Dec), 100 = average.
# Higher index = historically better month to SELL (higher price).
SEASONAL_INDEX = {
    "Onion": {
        "index": [112, 106, 92, 85, 82, 84, 90, 108, 118, 122, 120, 114],
        "note": "Rabi harvest (Mar-Jul) ke time supply zyada hoti hai, price gir jaata hai. "
                "Lean season (Aug-Jan) mein storage wale kisano ko best price milta hai."
    },
    "Potato": {
        "index": [104, 96, 84, 82, 88, 96, 102, 108, 112, 114, 110, 106],
        "note": "Rabi harvest (Feb-Mar) ke baad price sabse kam hota hai. Cold storage karke "
                "Sept-Nov tak rakhna behtar price deta hai."
    },
    "Tomato": {
        "index": [98, 96, 90, 86, 88, 96, 104, 110, 112, 108, 102, 100],
        "note": "Tomato ka price bahut volatile hota hai — generally summer peak harvest "
                "(Mar-May) mein lowest, monsoon ke baad (Aug-Oct) mein highest."
    },
    "Wheat": {
        "index": [104, 102, 96, 88, 86, 90, 94, 98, 100, 102, 106, 110],
        "note": "Harvest (Apr-Jun) ke turant baad price sabse kam hota hai. Dec-Jan mein "
                "arrivals kam hone se price thoda better hota hai."
    },
    "Rice": {
        "index": [98, 100, 102, 104, 105, 104, 100, 96, 92, 88, 92, 98],
        "note": "Kharif harvest (Oct-Nov) ke baad price kam hota hai. Apr-Jun (lean season) "
                "mein storage wale kisano ko behtar rate milta hai."
    },
    "Maize": {
        "index": [102, 104, 105, 102, 98, 94, 90, 88, 92, 98, 100, 102],
        "note": "Kharif harvest (Sep-Oct) ke baad price low hota hai. Feb-Mar mein price "
                "recover hota hai jab purana stock kam ho jaata hai."
    },
    "Cotton": {
        "index": [96, 98, 100, 102, 104, 106, 104, 100, 94, 88, 90, 94],
        "note": "Harvest season (Oct-Dec) mein arrivals zyada hone se price dabta hai. "
                "Apr-Jun mein, jab fresh crop nahi aata, price better hota hai."
    },
    "Soyabean": {
        "index": [100, 102, 104, 102, 98, 94, 90, 88, 90, 96, 100, 102],
        "note": "Kharif harvest (Oct) ke turant baad price lowest hota hai. Feb-Apr tak "
                "stock karke bechna typically behtar rehta hai."
    },
    "Groundnut": {
        "index": [98, 100, 102, 104, 102, 98, 94, 90, 88, 92, 96, 100],
        "note": "Kharif harvest (Oct-Nov) ke baad price low. Mar-Apr mein price improve "
                "hota hai jab naya stock market mein kam aata hai."
    },
    "Sugarcane": {
        "index": [100, 100, 101, 101, 100, 99, 99, 100, 101, 101, 100, 99],
        "note": "Sugarcane mostly mill-contract/FRP rate par bikta hai, isliye seasonal "
                "price swing dusri fasal jitna nahi hota — saalbhar lagbhag stable rehta hai."
    },
    "Bajra": {
        "index": [100, 102, 104, 103, 100, 96, 92, 90, 92, 96, 100, 103],
        "note": "Kharif harvest (Sep-Oct) ke baad price low rehta hai. Feb-Mar mein "
                "thoda behtar price milta hai."
    },
    "Jowar": {
        "index": [101, 103, 104, 102, 99, 96, 93, 91, 93, 97, 100, 102],
        "note": "Harvest season (Oct-Nov) mein supply zyada, price kam. Mar-Apr mein "
                "price relatively behtar hota hai."
    },
    "Gram": {
        "index": [98, 96, 90, 88, 92, 98, 102, 106, 108, 106, 102, 100],
        "note": "Rabi harvest (Mar-Apr) ke baad price low hota hai. Aug-Oct (off-season) "
                "mein price best hota hai."
    },
    "Mustard": {
        "index": [100, 98, 92, 88, 90, 96, 100, 104, 108, 108, 104, 102],
        "note": "Harvest (Feb-Mar) ke turant baad price kam hota hai. Sep-Oct mein "
                "off-season demand se price behtar hota hai."
    },
    "Turmeric": {
        "index": [98, 96, 94, 96, 100, 104, 108, 110, 108, 104, 100, 98],
        "note": "Harvest (Jan-Mar) ke baad price thoda low rehta hai. Jul-Sep mein "
                "demand badhne se price improve hota hai."
    },
    "Chilli": {
        "index": [94, 92, 96, 102, 106, 108, 106, 102, 98, 96, 96, 98],
        "note": "Harvest season (Jan-Feb) mein supply zyada hone se price low. "
                "Apr-Jun mein price typically peak karta hai."
    },
    "Banana": {
        "index": [98, 100, 102, 102, 100, 98, 98, 100, 102, 102, 100, 98],
        "note": "Banana saalbhar harvest hota hai, isliye price relatively stable rehta hai — "
                "halka sa peak summer (Mar-Apr) mein dikhta hai jab demand badhti hai."
    },
    "Brinjal": {
        "index": [100, 98, 94, 92, 94, 100, 104, 106, 104, 100, 100, 102],
        "note": "Summer harvest (Mar-May) mein supply zyada, price low. Monsoon ke baad "
                "(Aug-Sep) demand-supply gap se price behtar hota hai."
    },
    "Cabbage": {
        "index": [88, 86, 90, 98, 104, 106, 104, 100, 96, 94, 96, 100],
        "note": "Winter harvest (Dec-Feb) mein bahut zyada supply, price sabse kam. "
                "Apr-Jul (off-season) mein price kaafi behtar hota hai."
    },
    "Cauliflower": {
        "index": [86, 84, 92, 100, 106, 108, 106, 102, 96, 92, 92, 96],
        "note": "Winter (Dec-Feb) mein supply flood hoti hai, price lowest. "
                "Apr-Jun off-season mein price typically double-triple ho jaata hai."
    },
}

DEFAULT_NOTE = "Is fasal ke liye detailed seasonal data abhi available nahi hai — apni nazdeeki mandi se pichle 2-3 saal ka pattern poochna behtar rahega."


def get_seasonal_advice(crop: str, current_month: int):
    """
    current_month: 1-12 (Jan=1)
    Returns dict with: index (12 values), month_names, current_month_index (0-based),
    best_month (name + index 0-based), current_verdict, current_score, note
    """
    entry = SEASONAL_INDEX.get(crop)
    if not entry:
        # Flat/neutral fallback so the chart still renders sensibly
        entry = {"index": [100] * 12, "note": DEFAULT_NOTE}

    idx = entry["index"]
    cur_i = max(0, min(11, current_month - 1))
    cur_val = idx[cur_i]

    best_i = idx.index(max(idx))
    worst_i = idx.index(min(idx))

    # Find next best selling month from current month onward (wrap around the year)
    rotated = [(cur_i + offset) % 12 for offset in range(12)]
    upcoming_best_i = max(rotated, key=lambda i: idx[i])

    avg = sum(idx) / 12
    if cur_val >= avg * 1.06:
        verdict = "Abhi Bechna Sahi Hai"
        verdict_class = "good"
        reason = f"{MONTH_NAMES_HI[cur_i]} typically is crop ke liye accha mahina hai — average se price zyada rehta hai."
    elif cur_val <= avg * 0.94:
        verdict = "Thoda Ruk Sakte Ho"
        verdict_class = "wait"
        reason = f"{MONTH_NAMES_HI[cur_i]} mein typically price average se kam rehta hai. " \
                  f"Agar storage hai to {MONTH_NAMES_HI[upcoming_best_i]} tak wait karna behtar ho sakta hai."
    else:
        verdict = "Average Mahina Hai"
        verdict_class = "neutral"
        reason = f"{MONTH_NAMES_HI[cur_i]} mein price na bahut high na bahut low rehta hai — apni zaroorat ke hisaab se decide karein."

    return {
        "crop": crop,
        "index": idx,
        "month_names": MONTH_NAMES_HI,
        "current_month_idx": cur_i,
        "current_value": cur_val,
        "best_month": MONTH_NAMES_HI[best_i],
        "best_month_idx": best_i,
        "worst_month": MONTH_NAMES_HI[worst_i],
        "worst_month_idx": worst_i,
        "upcoming_best_month": MONTH_NAMES_HI[upcoming_best_i],
        "verdict": verdict,
        "verdict_class": verdict_class,
        "reason": reason,
        "note": entry["note"],
    }
