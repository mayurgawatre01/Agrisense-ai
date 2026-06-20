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
