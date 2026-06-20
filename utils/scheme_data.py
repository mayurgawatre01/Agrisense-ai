"""
CropSense v3.1 — Govt Scheme Finder
Curated list of major Central Government farmer welfare schemes, with
state-wise relevance tags. Facts verified (PM-KISAN installment amount,
PMFBY premium rates, etc.) as of mid-2026.
NOTE: Always tell the farmer to confirm latest details on the official
portal before applying — scheme rules/dates can change.
"""

# Schemes that apply to farmers in ALL states (Central Govt schemes)
NATIONAL_SCHEMES = [
    {
        "id": "pm_kisan",
        "name_hi": "PM-KISAN Samman Nidhi Yojana",
        "icon": "💰",
        "category": "Income Support",
        "summary_hi": "Saal mein ₹6,000 seedha bank account mein — 3 kistein, har ek ₹2,000 ki, "
                      "har 4 mahine mein DBT (Direct Benefit Transfer) se.",
        "eligibility_hi": [
            "Zameen rakhne wale (landholding) kisan parivaar",
            "Aadhaar bank account se linked hona chahiye",
            "e-KYC complete hona zaroori hai",
        ],
        "not_eligible_hi": "Income tax bharne wale, sarkari naukri/pension wale, aur sansthagat zameen-malik is scheme mein eligible nahi hain.",
        "documents_hi": ["Aadhaar Card", "Bank Passbook", "Zameen ke kagzaat (Land records)"],
        "how_to_apply_hi": "Official website pmkisan.gov.in par 'New Farmer Registration' karein, ya apne CSC (Common Service Centre) jaakar register karein.",
        "official_link": "https://pmkisan.gov.in",
        "states": "all",
    },
    {
        "id": "pmfby",
        "name_hi": "PM Fasal Bima Yojana (PMFBY)",
        "icon": "🛡️",
        "category": "Crop Insurance",
        "summary_hi": "Prakritik aapda (baadh, sookha, ole) se fasal kharab hone par bima cover milta hai. "
                      "Premium bahut kam hai — Kharif crops ke liye sirf 2%, Rabi ke liye 1.5% aur "
                      "commercial/horticulture fasal ke liye 5% hi dena padta hai.",
        "eligibility_hi": [
            "Notified crop ugane wale sabhi kisan (loanee aur non-loanee dono)",
            "Sharecropper/tenant farmers bhi eligible hain",
        ],
        "not_eligible_hi": "Apna gaon/block ki notified crop list mein crop na ho to cover nahi milega — pehle check karein.",
        "documents_hi": ["Aadhaar Card", "Bank Passbook", "Zameen ke kagzaat", "Sowing certificate"],
        "how_to_apply_hi": "pmfby.gov.in par online apply karein ya bank/CSC ke through, seasonal deadline se pehle.",
        "official_link": "https://pmfby.gov.in",
        "states": "all",
    },
    {
        "id": "kcc",
        "name_hi": "Kisan Credit Card (KCC)",
        "icon": "💳",
        "category": "Credit / Loan",
        "summary_hi": "Kheti ke liye kam interest rate (4% tak, time par repayment karne par) par loan — "
                      "beej, khaad, aur dusre kharche ke liye.",
        "eligibility_hi": [
            "Sabhi kisan — zameen-malik, tenant farmer, sharecropper",
            "Animal husbandry aur fisheries karne wale bhi eligible",
        ],
        "not_eligible_hi": "—",
        "documents_hi": ["Aadhaar Card", "PAN Card (agar loan ₹1 lakh se zyada ho)", "Zameen ke kagzaat", "Photo"],
        "how_to_apply_hi": "Apne nearest bank branch (PSU bank, Cooperative bank, ya RRB) mein form bharkar apply karein.",
        "official_link": "https://www.myscheme.gov.in/schemes/kcc",
        "states": "all",
    },
    {
        "id": "soil_health_card",
        "name_hi": "Soil Health Card Scheme",
        "icon": "🧪",
        "category": "Soil & Advisory",
        "summary_hi": "Muft mein apni zameen ki mitti test karwayein — NPK aur dusre nutrients ki "
                      "report milti hai, jisse sahi khaad daal sakte hain.",
        "eligibility_hi": ["Sabhi kisan, koi income limit nahi"],
        "not_eligible_hi": "—",
        "documents_hi": ["Aadhaar Card", "Zameen ka record"],
        "how_to_apply_hi": "Apne nearest Krishi Vigyan Kendra (KVK) ya zila krishi office mein sample jama karein.",
        "official_link": "https://soilhealth.dac.gov.in",
        "states": "all",
    },
    {
        "id": "pmksy",
        "name_hi": "PM Krishi Sinchayee Yojana (Irrigation)",
        "icon": "💧",
        "category": "Irrigation",
        "summary_hi": "Drip aur sprinkler irrigation lagwane ke liye subsidy — 'Per Drop More Crop' "
                      "scheme ke through paani ki bachat ke saath better yield.",
        "eligibility_hi": ["Sabhi kisan jo micro-irrigation lagwana chahte hain"],
        "not_eligible_hi": "—",
        "documents_hi": ["Aadhaar Card", "Zameen ke kagzaat", "Bank Passbook"],
        "how_to_apply_hi": "Apne zila krishi/udyan vibhag office se sampark karein ya state portal par apply karein.",
        "official_link": "https://pmksy.gov.in",
        "states": "all",
    },
    {
        "id": "enam",
        "name_hi": "e-NAM (National Agriculture Market)",
        "icon": "📈",
        "category": "Market Access",
        "summary_hi": "Online platform jahan kisan apni fasal alag-alag mandiyon mein bech sakte "
                      "hain — best price milne ke chances badh jaate hain.",
        "eligibility_hi": ["Sabhi kisan, registered mandi traders ke through"],
        "not_eligible_hi": "—",
        "documents_hi": ["Aadhaar Card", "Bank Passbook", "Mobile number"],
        "how_to_apply_hi": "enam.gov.in par register karein ya apni nazdeeki e-NAM registered mandi mein jaakar poochein.",
        "official_link": "https://enam.gov.in",
        "states": "all",
    },
    {
        "id": "agri_infra_fund",
        "name_hi": "Agriculture Infrastructure Fund",
        "icon": "🏗️",
        "category": "Infrastructure Loan",
        "summary_hi": "Cold storage, warehouse, ya post-harvest infrastructure banane ke liye "
                      "loan par 3% interest subvention (chhoot).",
        "eligibility_hi": ["Kisan, FPO (Farmer Producer Organisation), Cooperatives, Startups"],
        "not_eligible_hi": "—",
        "documents_hi": ["Project proposal", "Aadhaar/PAN", "Bank details"],
        "how_to_apply_hi": "agriinfra.dac.gov.in par online apply karein ya bank branch se sampark karein.",
        "official_link": "https://agriinfra.dac.gov.in",
        "states": "all",
    },
]

# State-specific schemes (sample — easily extendable)
STATE_SCHEMES = {
    "Maharashtra": [
        {
            "id": "mh_namo_shetkari",
            "name_hi": "Namo Shetkari Mahasanman Nidhi",
            "icon": "🌾",
            "category": "Income Support (State)",
            "summary_hi": "Maharashtra sarkar PM-KISAN ke upar additional ₹6,000/saal deti hai — "
                          "yaani total ₹12,000/saal Maharashtra ke eligible kisano ko.",
            "eligibility_hi": ["PM-KISAN ke eligible kisan jo Maharashtra ke resident hain"],
            "not_eligible_hi": "—",
            "documents_hi": ["PM-KISAN registration", "Aadhaar", "Bank Passbook"],
            "how_to_apply_hi": "PM-KISAN mein registered kisano ko automatically is scheme mein add kiya jaata hai.",
            "official_link": "https://krishi.maharashtra.gov.in",
            "states": "Maharashtra",
        },
    ],
    "Telangana": [
        {
            "id": "ts_rythu_bandhu",
            "name_hi": "Rythu Bharosa (Investment Support)",
            "icon": "🌱",
            "category": "Income Support (State)",
            "summary_hi": "Telangana ke kisano ko per acre seedha investment support milta hai "
                          "Kharif aur Rabi dono season ke liye.",
            "eligibility_hi": ["Telangana ke zameen-malik kisan"],
            "not_eligible_hi": "—",
            "documents_hi": ["Pattadar Passbook", "Aadhaar", "Bank Passbook"],
            "how_to_apply_hi": "Apne agriculture extension officer (AEO) ya local Rythu Vedika se sampark karein.",
            "official_link": "https://rythubharosa.telangana.gov.in",
            "states": "Telangana",
        },
    ],
    "Karnataka": [
        {
            "id": "ka_raitha_siri",
            "name_hi": "Raitha Siri Scheme",
            "icon": "🌻",
            "category": "Income Support (State)",
            "summary_hi": "Millet (moti anaaj) ugane wale kisano ko per hectare additional "
                          "incentive milta hai.",
            "eligibility_hi": ["Karnataka ke kisan jo ragi, jowar, bajra jaisi millet fasal ugaate hain"],
            "not_eligible_hi": "—",
            "documents_hi": ["FID (Farmer ID)", "Aadhaar", "Bank Passbook"],
            "how_to_apply_hi": "Apne raitha samparka kendra ya local agriculture office mein register karein.",
            "official_link": "https://raitamitra.karnataka.gov.in",
            "states": "Karnataka",
        },
    ],
    "West Bengal": [
        {
            "id": "wb_krishak_bandhu",
            "name_hi": "Krishak Bandhu Scheme",
            "icon": "🤝",
            "category": "Income Support (State)",
            "summary_hi": "West Bengal ke kisano ko per acre saalana income support, plus "
                          "kisan ki death par parivaar ko ₹2 lakh ka one-time grant.",
            "eligibility_hi": ["West Bengal ke registered kisan (zameen-malik ya bargadar)"],
            "not_eligible_hi": "—",
            "documents_hi": ["Aadhaar", "Zameen ke kagzaat", "Bank Passbook"],
            "how_to_apply_hi": "Duare Sarkar camp ya local krishi office mein apply karein.",
            "official_link": "https://krishakbandhu.wb.gov.in",
            "states": "West Bengal",
        },
    ],
}

ALL_STATES_LIST = [
    "Maharashtra", "Punjab", "Haryana", "Uttar Pradesh", "Madhya Pradesh",
    "Rajasthan", "Gujarat", "Karnataka", "Tamil Nadu", "Andhra Pradesh",
    "Telangana", "Bihar", "West Bengal", "Odisha", "Chhattisgarh",
    "Assam", "Kerala", "Jharkhand", "Uttarakhand", "Himachal Pradesh",
]


def get_schemes_for_state(state: str):
    """Returns national schemes + any state-specific schemes for the given state."""
    schemes = list(NATIONAL_SCHEMES)
    state_specific = STATE_SCHEMES.get(state, [])
    return state_specific + schemes  # state-specific shown first
