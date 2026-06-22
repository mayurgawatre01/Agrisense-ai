"""
CropSense v3.1 — Tools Blueprint
New farmer-facing features:
  1. Mandi Price Tracker  — /tools/mandi
  2. Pest/Disease Identifier — /tools/pest
  3. Govt Scheme Finder   — /tools/schemes
"""
import os
from flask import (Blueprint, render_template, request, redirect,
                    url_for, session, flash, current_app, jsonify)
from functools import wraps

tools = Blueprint('tools', __name__, url_prefix='/tools')


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please login first.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


# ─── 1. Mandi Price Tracker ────────────────────────────────────────────────

@tools.route('/mandi', methods=['GET', 'POST'])
@login_required
def mandi_tracker():
    from utils.mandi_data import STATES, CROP_LIST, get_mandi_price, DISTRICTS_BY_STATE
    from utils.seasonal_data import get_seasonal_advice
    from models import User
    from datetime import datetime

    user = User.query.get(session['user_id'])
    result = None
    selected_state = request.values.get('state') or (user.state if user else '') or 'Maharashtra'
    selected_crop = request.values.get('commodity') or 'Rice'
    selected_district = request.values.get('district') or ''

    districts_for_state = DISTRICTS_BY_STATE.get(selected_state, [])
    # Reset district if it doesn't belong to the newly selected state
    if selected_district and selected_district not in districts_for_state:
        selected_district = ''

    if request.method == 'POST' or request.args.get('auto'):
        api_key = current_app.config.get('DATA_GOV_API_KEY', '')
        result = get_mandi_price(selected_state, selected_crop, api_key, selected_district)

    seasonal = get_seasonal_advice(selected_crop, datetime.now().month)

    return render_template(
        'mandi.html',
        states=STATES,
        crops=CROP_LIST,
        districts=districts_for_state,
        districts_by_state=DISTRICTS_BY_STATE,
        selected_state=selected_state,
        selected_crop=selected_crop,
        selected_district=selected_district,
        result=result,
        seasonal=seasonal
    )



# ─── 2. Pest / Disease Identifier ──────────────────────────────────────────

@tools.route('/pest', methods=['GET', 'POST'])
@login_required
def pest_identifier():
    from utils.pest_identifier import identify_pest_disease, COMMON_PROBLEMS

    result = None
    uploaded_image = None

    if request.method == 'POST':
        file = request.files.get('photo')
        if not file or file.filename == '':
            flash('Pehle ek photo upload karein.', 'danger')
            return render_template('pest.html', result=None, common_problems=COMMON_PROBLEMS, uploaded_image=None)

        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ('.jpg', '.jpeg', '.png', '.webp'):
            flash('Sirf JPG, PNG ya WEBP photo allowed hai.', 'danger')
            return render_template('pest.html', result=None, common_problems=COMMON_PROBLEMS, uploaded_image=None)

        os.makedirs('static/pest_uploads', exist_ok=True)
        import uuid
        filename = f"{session['user_id']}_{uuid.uuid4().hex[:10]}{ext}"
        filepath = os.path.join('static', 'pest_uploads', filename)
        file.save(filepath)
        uploaded_image = url_for('static', filename=f'pest_uploads/{filename}')

        gemini_key = current_app.config.get('GEMINI_API_KEY', '')
        anthropic_key = current_app.config.get('ANTHROPIC_API_KEY', '')
        analysis = identify_pest_disease(filepath, gemini_key, anthropic_key)

        if analysis['success']:
            result = analysis['data']
            result['provider'] = analysis.get('provider', '')
        else:
            flash(analysis['error'], 'warning')

    return render_template('pest.html', result=result, common_problems=COMMON_PROBLEMS, uploaded_image=uploaded_image)


# ─── 3. Govt Scheme Finder ──────────────────────────────────────────────────

@tools.route('/schemes', methods=['GET', 'POST'])
@login_required
def scheme_finder():
    from utils.scheme_data import get_schemes_for_state, ALL_STATES_LIST
    from models import User

    user = User.query.get(session['user_id'])
    selected_state = request.values.get('state') or (user.state if user else '') or 'Maharashtra'
    schemes = get_schemes_for_state(selected_state)

    return render_template(
        'schemes.html',
        states=ALL_STATES_LIST,
        selected_state=selected_state,
        schemes=schemes
    )


# ─── 4. AI Chatbot Assistant ───────────────────────────────────────────────

@tools.route('/chat', methods=['POST'])
@login_required
def chat_assistant():
    import urllib.request, json as _json
    
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    if not message:
        return jsonify({'success': False, 'error': 'Empty message'})

    gemini_key = current_app.config.get('GEMINI_API_KEY', '')
    
    if not gemini_key:
        response_text = _offline_chatbot_response(message)
        return jsonify({'success': True, 'response': response_text, 'offline': True})
    
    try:
        system_prompt = (
            "You are FarmOS AI, a premium agricultural advisor for Indian farmers. "
            "Help them choose crops, advise on pest control, fertilizers, and smart watering. "
            "Answer the query in a simple, practical, and highly encouraging manner. "
            "Use Devanagari script for simple Hindi queries or Hinglish for casual conversational prompts. "
            "Keep the response concise (2-4 sentences max)."
        )
        
        payload = {
            "contents": [{
                "parts": [{"text": f"{system_prompt}\n\nFarmer Query: {message}"}]
            }],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 300
            }
        }
        
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        req = urllib.request.Request(
            url,
            data=_json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "x-goog-api-key": gemini_key},
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=10) as resp:
            res_data = _json.loads(resp.read().decode("utf-8"))
            
        candidates = res_data.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            response_text = "\n".join(p.get("text", "") for p in parts).strip()
            return jsonify({'success': True, 'response': response_text, 'offline': False})
        else:
            raise ValueError("No output generated")
            
    except Exception as e:
        response_text = _offline_chatbot_response(message)
        return jsonify({'success': True, 'response': response_text, 'offline': True, 'error': str(e)})


def _offline_chatbot_response(message: str) -> str:
    msg = message.lower()
    if "grow" in msg or "ugayein" in msg or "fasal" in msg or "what should i grow" in msg or "what to grow" in msg:
        return (
            "Farming choices depend on your climate and soil. "
            "For high water availability, grow Rice or Sugarcane. "
            "For medium water, grow Wheat or Maize. "
            "For dry regions, grow Cotton, Groundnut or Pearl Millet (Bajra). "
            "Check our Crop Recommender page in the sidebar for personalized calculations!"
        )
    elif "pest" in msg or "disease" in msg or "insect" in msg or "kida" in msg or "bimari" in msg:
        return (
            "Pest problems? Go to the 'Disease Detection' tool in the sidebar, "
            "upload a photo of the affected plant leaf, and our AI will analyze "
            "the symptoms and suggest organic or chemical treatments."
        )
    elif "fertilizer" in msg or "khad" in msg or "urea" in msg or "npk" in msg:
        return (
            "A balanced fertilizer schedule is key. You can use our 'Fertilizer Calc' "
            "tool to enter your crop type and field size. It will give you the exact quantity "
            "of Urea, DAP, and Potash required, along with an application timeline."
        )
    elif "weather" in msg or "mausam" in msg or "rain" in msg or "baarish" in msg:
        return (
            "To view weather information, check your Dashboard weather card! "
            "If rain is predicted, postpone fertilizer spray to prevent it from washing off. "
            "Keep soil drained if heavy rainfall is warning."
        )
    elif "mandi" in msg or "rate" in msg or "price" in msg or "daam" in msg:
        return (
            "You can track daily market prices via our Mandi Price Tracker in the sidebar. "
            "Choose your commodity and state to view active prices and decide when to sell."
        )
    else:
        return (
            "Hello! I am your FarmOS assistant. I can help with crop suggestions, fertilizer "
            "quantities, pest identifier, mandi prices, and government schemes. "
            "Ask me things like 'What should I grow?' or 'How do I identify leaf blight?'."
        )

