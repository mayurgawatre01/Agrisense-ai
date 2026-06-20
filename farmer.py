"""
CropSense v3.0 — Farmer Blueprint
Upgrades: weather API, crop recommender, export CSV, search history,
          bulk delete, retrain trigger, confidence chart data
"""
import os, io, csv
from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash, send_file, jsonify, current_app)
from functools import wraps
from extensions import db
from models import CropData, Prediction, User

farmer = Blueprint('farmer', __name__, url_prefix='/farmer')


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please login first.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


# ─── Dashboard ────────────────────────────────────────────────────────────────

@farmer.route('/dashboard')
@login_required
def dashboard():
    uid = session['user_id']

    total_records     = CropData.query.filter_by(user_id=uid).count()
    total_predictions = Prediction.query.filter_by(user_id=uid).count()

    crops  = CropData.query.filter_by(user_id=uid).all()
    yields = [c.yield_per_hectare for c in crops if c.yield_per_hectare]
    avg_yield = round(sum(yields) / len(yields), 2) if yields else 0

    recent_crops       = CropData.query.filter_by(user_id=uid).order_by(CropData.uploaded_at.desc()).limit(8).all()
    recent_predictions = Prediction.query.filter_by(user_id=uid).order_by(Prediction.created_at.desc()).limit(10).all()

    # Confidence chart data
    conf_labels = [f"{p.crop} ({p.season})" for p in recent_predictions]
    conf_values = [round((p.confidence or 0) * 100, 1) for p in recent_predictions]

    # Top crops by frequency
    from sqlalchemy import func
    top_crops = (db.session.query(CropData.crop, func.count(CropData.id).label('cnt'))
                 .filter_by(user_id=uid).group_by(CropData.crop)
                 .order_by(func.count(CropData.id).desc()).limit(6).all())
    top_crop_labels  = [r.crop for r in top_crops]
    top_crop_counts  = [r.cnt for r in top_crops]

    # Check model status
    from ml.predictor import model_status
    ml_status = model_status()

    return render_template('dashboard.html',
        total_records=total_records,
        total_predictions=total_predictions,
        avg_yield=avg_yield,
        recent_crops=recent_crops,
        recent_predictions=recent_predictions,
        conf_labels=conf_labels,
        conf_values=conf_values,
        top_crop_labels=top_crop_labels,
        top_crop_counts=top_crop_counts,
        ml_status=ml_status,
        charts={}
    )


# ─── Upload ───────────────────────────────────────────────────────────────────

@farmer.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            flash('Please select a file.', 'danger')
            return redirect(request.url)

        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ['.csv', '.xlsx']:
            flash('Only .csv and .xlsx files are supported.', 'danger')
            return redirect(request.url)

        os.makedirs('uploads', exist_ok=True)
        filepath = os.path.join('uploads', f"{session['user_id']}_{file.filename}")
        file.save(filepath)

        from utils.data_processor import process_crop_csv
        result = process_crop_csv(filepath, session['user_id'])

        if result['success']:
            flash(f"✅ {result['rows_inserted']} rows uploaded successfully!", 'success')
            return redirect(url_for('farmer.dashboard'))
        else:
            flash(f"Upload failed: {result['error']}", 'danger')

    return render_template('upload.html')


# ─── Predict ──────────────────────────────────────────────────────────────────

@farmer.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    result = None
    if request.method == 'POST':
        data = {
            'state':    request.form.get('state', ''),
            'district': request.form.get('district', ''),
            'season':   request.form.get('season', ''),
            'crop':     request.form.get('crop', ''),
            'area':     request.form.get('area', '0'),
        }

        from ml.predictor import predict_yield
        result = predict_yield(data)

        if result.get('success'):
            p = Prediction(
                user_id=session['user_id'],
                state=data['state'],
                district=data['district'],
                season=data['season'],
                crop=data['crop'],
                area=float(data['area']),
                predicted_yield=result['predicted_yield'],
                confidence=result['confidence'],
                total_production=result['total_production'],
                model_used=result['model_used']
            )
            db.session.add(p)
            db.session.commit()
            flash(f"Prediction saved! Estimated yield: {result['predicted_yield']} t/ha", 'success')
        else:
            flash(f"Prediction error: {result.get('error')}", 'danger')

    return render_template('prediction.html', result=result)


# ─── Crop Recommender ─────────────────────────────────────────────────────────

@farmer.route('/recommend', methods=['GET', 'POST'])
@login_required
def recommend():
    result = None
    if request.method == 'POST':
        try:
            n   = float(request.form.get('nitrogen', 0))
            p   = float(request.form.get('phosphorus', 0))
            k   = float(request.form.get('potassium', 0))
            ph  = float(request.form.get('ph', 7.0))
            rf  = float(request.form.get('rainfall', 100))
            temp = float(request.form.get('temperature', 25))
            result = _rule_recommend(n, p, k, ph, rf, temp)
        except (TypeError, ValueError):
            flash('Please enter valid numbers for all fields.', 'danger')
    return render_template('recommend.html', result=result)


def _rule_recommend(n, p, k, ph, rainfall, temp):
    """
    Rule-based crop recommender using NPK + pH + rainfall + temp.
    Returns top 3 ranked suggestions with reasoning, profit estimate, and risk.
    """
    crops = [
        {'name': 'Rice',      'n': (60,120),  'p': (30,60),   'k': (30,60),   'ph': (5.5,7.0), 'rain': (150,300), 'temp': (20,35),
         'profit': 35000, 'water': 'High',   'risk': 'Medium', 'duration': '120–150 days'},
        {'name': 'Wheat',     'n': (80,150),  'p': (40,80),   'k': (40,80),   'ph': (6.0,7.5), 'rain': (50,150),  'temp': (10,25),
         'profit': 28000, 'water': 'Medium', 'risk': 'Low',    'duration': '100–130 days'},
        {'name': 'Maize',     'n': (100,200), 'p': (50,100),  'k': (50,100),  'ph': (5.8,7.5), 'rain': (60,110),  'temp': (18,32),
         'profit': 30000, 'water': 'Medium', 'risk': 'Low',    'duration': '90–120 days'},
        {'name': 'Cotton',    'n': (80,120),  'p': (40,60),   'k': (40,60),   'ph': (6.0,8.0), 'rain': (50,100),  'temp': (20,35),
         'profit': 55000, 'water': 'Low',    'risk': 'High',   'duration': '160–200 days'},
        {'name': 'Sugarcane', 'n': (150,250), 'p': (60,100),  'k': (80,120),  'ph': (6.0,8.0), 'rain': (100,200), 'temp': (20,35),
         'profit': 80000, 'water': 'High',   'risk': 'Medium', 'duration': '10–12 months'},
        {'name': 'Groundnut', 'n': (20,40),   'p': (40,80),   'k': (40,80),   'ph': (5.5,7.0), 'rain': (50,150),  'temp': (22,32),
         'profit': 45000, 'water': 'Low',    'risk': 'Low',    'duration': '100–130 days'},
        {'name': 'Soyabean',  'n': (20,40),   'p': (60,100),  'k': (40,80),   'ph': (6.0,7.5), 'rain': (60,120),  'temp': (20,30),
         'profit': 32000, 'water': 'Medium', 'risk': 'Low',    'duration': '90–110 days'},
        {'name': 'Potato',    'n': (120,200), 'p': (80,120),  'k': (100,150), 'ph': (5.0,6.5), 'rain': (50,100),  'temp': (10,25),
         'profit': 60000, 'water': 'Medium', 'risk': 'Medium', 'duration': '70–90 days'},
        {'name': 'Tomato',    'n': (80,150),  'p': (60,100),  'k': (80,120),  'ph': (5.5,7.0), 'rain': (40,80),   'temp': (20,30),
         'profit': 75000, 'water': 'Medium', 'risk': 'High',   'duration': '90–120 days'},
        {'name': 'Onion',     'n': (60,100),  'p': (40,80),   'k': (60,100),  'ph': (6.0,7.5), 'rain': (40,80),   'temp': (13,30),
         'profit': 50000, 'water': 'Medium', 'risk': 'Medium', 'duration': '100–130 days'},
        {'name': 'Bajra',     'n': (40,80),   'p': (20,40),   'k': (20,40),   'ph': (6.0,8.0), 'rain': (30,70),   'temp': (25,40),
         'profit': 22000, 'water': 'Low',    'risk': 'Low',    'duration': '65–85 days'},
        {'name': 'Jowar',     'n': (60,100),  'p': (30,60),   'k': (30,60),   'ph': (6.0,8.0), 'rain': (40,80),   'temp': (25,35),
         'profit': 20000, 'water': 'Low',    'risk': 'Low',    'duration': '100–120 days'},
    ]

    PARAM_LABELS = {
        'n': 'Nitrogen', 'p': 'Phosphorus', 'k': 'Potassium',
        'ph': 'Soil pH', 'rain': 'Rainfall', 'temp': 'Temperature'
    }

    def score_and_reasons(c):
        s = 0
        good, warn = [], []
        for key, val in [('n', n), ('p', p), ('k', k), ('ph', ph), ('rain', rainfall), ('temp', temp)]:
            lo, hi = c[key]
            label = PARAM_LABELS[key]
            if lo <= val <= hi:
                s += 2
                good.append(label)
            elif abs(val - lo) < (hi - lo) * 0.25 or abs(val - hi) < (hi - lo) * 0.25:
                s += 1
                warn.append(label)
            else:
                warn.append(label)
        return s, good, warn

    RISK_COLOR = {'Low': '#4ade80', 'Medium': '#fbbf24', 'High': '#f87171'}
    WATER_ICON = {'Low': '💧', 'Medium': '💧💧', 'High': '💧💧💧'}

    ranked = sorted(crops, key=lambda c: score_and_reasons(c)[0], reverse=True)[:3]

    results = []
    for r in ranked:
        s, good, warn = score_and_reasons(r)
        results.append({
            'crop':      r['name'],
            'match':     int(s / 12 * 100),
            'good':      good,
            'warn':      warn,
            'profit':    r['profit'],
            'water':     r['water'],
            'water_icon': WATER_ICON[r['water']],
            'risk':      r['risk'],
            'risk_color': RISK_COLOR[r['risk']],
            'duration':  r['duration'],
        })
    return results


# ─── Weather ──────────────────────────────────────────────────────────────────

@farmer.route('/api/weather')
@login_required
def weather_api():
    city = request.args.get('city', 'Pune')
    api_key = current_app.config.get('WEATHER_API_KEY', '')

    if not api_key:
        # Return mock data when no API key configured
        return jsonify({
            'success': True,
            'mock': True,
            'city': city,
            'temp': 28,
            'feels_like': 31,
            'humidity': 72,
            'description': 'Partly cloudy',
            'wind_speed': 12,
            'icon': '02d',
        })

    try:
        import urllib.request, json as _json
        url = (f"https://api.openweathermap.org/data/2.5/weather"
               f"?q={city}&appid={api_key}&units=metric")
        with urllib.request.urlopen(url, timeout=5) as r:
            d = _json.loads(r.read())
        return jsonify({
            'success': True,
            'mock': False,
            'city': d['name'],
            'temp': round(d['main']['temp']),
            'feels_like': round(d['main']['feels_like']),
            'humidity': d['main']['humidity'],
            'description': d['weather'][0]['description'].capitalize(),
            'wind_speed': round(d['wind']['speed'] * 3.6),  # m/s → km/h
            'icon': d['weather'][0]['icon'],
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


# ─── History (with search + bulk delete) ──────────────────────────────────────

@farmer.route('/history')
@login_required
def history():
    uid     = session['user_id']
    q       = request.args.get('q', '').strip()
    season  = request.args.get('season', '')

    query = CropData.query.filter_by(user_id=uid)
    if q:
        query = query.filter(CropData.crop.ilike(f'%{q}%'))
    if season:
        query = query.filter(CropData.season == season)

    records = query.order_by(CropData.uploaded_at.desc()).all()
    seasons = db.session.query(CropData.season).filter_by(user_id=uid).distinct().all()
    seasons = [s[0] for s in seasons if s[0]]

    return render_template('history.html', records=records, seasons=seasons, q=q, active_season=season)


@farmer.route('/history/delete', methods=['POST'])
@login_required
def delete_history():
    uid = session['user_id']
    ids = request.form.getlist('ids')
    if ids:
        CropData.query.filter(CropData.id.in_(ids), CropData.user_id == uid).delete(synchronize_session=False)
        db.session.commit()
        flash(f'Deleted {len(ids)} record(s).', 'success')
    else:
        flash('No records selected.', 'warning')
    return redirect(url_for('farmer.history'))


# ─── Export CSV ───────────────────────────────────────────────────────────────

@farmer.route('/history/export')
@login_required
def export_csv():
    uid = session['user_id']
    records = CropData.query.filter_by(user_id=uid).order_by(CropData.uploaded_at.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['State', 'District', 'Crop Year', 'Season', 'Crop', 'Area (ha)', 'Production', 'Yield (t/ha)', 'Uploaded At'])
    for r in records:
        writer.writerow([r.state, r.district, r.crop_year, r.season, r.crop,
                         r.area, r.production, r.yield_per_hectare, r.uploaded_at])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='cropsense_history.csv'
    )


# ─── Retrain trigger ──────────────────────────────────────────────────────────

@farmer.route('/retrain', methods=['POST'])
@login_required
def retrain():
    """Background retrain — runs synchronously for simplicity."""
    try:
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, 'ml/train_model.py', '--min-rows', '10'],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            from ml.predictor import clear_cache
            clear_cache()
            flash('✅ Model retrained successfully!', 'success')
        else:
            flash(f'Retrain failed: {result.stderr[-300:]}', 'danger')
    except Exception as e:
        flash(f'Retrain error: {str(e)}', 'danger')
    return redirect(url_for('farmer.dashboard'))


# ─── PDF Report ───────────────────────────────────────────────────────────────

@farmer.route('/report/pdf')
@login_required
def report_pdf():
    uid  = session['user_id']
    user = User.query.get(uid)

    crops       = CropData.query.filter_by(user_id=uid).order_by(CropData.uploaded_at.desc()).limit(20).all()
    predictions = Prediction.query.filter_by(user_id=uid).order_by(Prediction.created_at.desc()).limit(10).all()

    yields    = [c.yield_per_hectare for c in crops if c.yield_per_hectare]
    avg_yield = round(sum(yields) / len(yields), 2) if yields else 0

    stats = {
        'total_records':     CropData.query.filter_by(user_id=uid).count(),
        'avg_yield':         avg_yield,
        'total_predictions': Prediction.query.filter_by(user_id=uid).count(),
    }

    charts_dir = os.path.join('static', 'charts')
    try:
        from utils.pdf_generator import generate_farmer_report
        generate_farmer_report(uid, user.name, stats, crops, predictions, charts_dir)
        abs_path = os.path.abspath(os.path.join('static', 'charts', f'report_{uid}.pdf'))
        return send_file(abs_path, as_attachment=True,
                         download_name=f"CropSense_Report_{user.name}.pdf",
                         mimetype='application/pdf')
    except Exception as e:
        flash(f"PDF generation failed: {str(e)}", 'danger')
        return redirect(url_for('farmer.dashboard'))


# ─── Fertilizer Calculator ────────────────────────────────────────────────────

@farmer.route('/fertilizer', methods=['GET', 'POST'])
@login_required
def fertilizer():
    from utils.fertilizer_data import get_fertilizer_plan, get_all_crops
    result = None
    crops = get_all_crops()

    # Pre-fill crop from recommender redirect (?crop=Rice)
    prefill_crop = request.args.get('crop', '')

    if request.method == 'POST':
        crop = request.form.get('crop', '')
        try:
            area = float(request.form.get('area', 0))
            if area <= 0:
                flash('Area must be greater than 0.', 'danger')
            else:
                result = get_fertilizer_plan(crop, area)
                if not result['success']:
                    flash(result['error'], 'danger')
                    result = None
        except ValueError:
            flash('Please enter a valid area.', 'danger')

    return render_template('fertilizer.html', crops=crops, result=result, prefill_crop=prefill_crop)


@farmer.route('/fertilizer/pdf', methods=['POST'])
@login_required
def fertilizer_pdf():
    from utils.fertilizer_data import get_fertilizer_plan

    crop = request.form.get('crop', '')
    try:
        area = float(request.form.get('area', 0))
    except ValueError:
        flash('Invalid area for PDF export.', 'danger')
        return redirect(url_for('farmer.fertilizer'))

    plan = get_fertilizer_plan(crop, area)
    if not plan.get('success'):
        flash(plan.get('error', 'Could not generate fertilizer plan.'), 'danger')
        return redirect(url_for('farmer.fertilizer'))

    try:
        from utils.pdf_generator import generate_fertilizer_report
        path = generate_fertilizer_report(crop, plan)
        abs_path = os.path.abspath(path)
        return send_file(abs_path, as_attachment=True,
                         download_name=f"CropSense_Fertilizer_{crop}.pdf",
                         mimetype='application/pdf')
    except Exception as e:
        flash(f"PDF generation failed: {str(e)}", 'danger')
        return redirect(url_for('farmer.fertilizer'))
