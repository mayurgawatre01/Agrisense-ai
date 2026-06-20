"""
CropSense v3.0 — Admin Blueprint
Features: user list, platform stats, delete user
"""
from flask import Blueprint, render_template, redirect, url_for, session, flash, request, jsonify
from functools import wraps
from extensions import db
from models import User, CropData, Prediction

admin = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please login first.', 'warning')
            return redirect(url_for('auth.login'))
        if session.get('role') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('farmer.dashboard'))
        return f(*args, **kwargs)
    return decorated


@admin.route('/dashboard')
@admin_required
def dashboard():
    users         = User.query.order_by(User.created_at.desc()).all()
    total_users   = User.query.count()
    total_crops   = CropData.query.count()
    total_preds   = Prediction.query.count()

    # Per-user stats
    user_stats = []
    for u in users:
        user_stats.append({
            'user': u,
            'crops': CropData.query.filter_by(user_id=u.id).count(),
            'preds': Prediction.query.filter_by(user_id=u.id).count(),
        })

    return render_template('admin_dashboard.html',
        user_stats=user_stats,
        total_users=total_users,
        total_crops=total_crops,
        total_preds=total_preds,
    )


@admin.route('/delete_user/<int:uid>', methods=['POST'])
@admin_required
def delete_user(uid):
    if uid == session.get('user_id'):
        flash("Can't delete yourself.", 'danger')
        return redirect(url_for('admin.dashboard'))
    user = User.query.get_or_404(uid)
    CropData.query.filter_by(user_id=uid).delete()
    Prediction.query.filter_by(user_id=uid).delete()
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.email} deleted.', 'success')
    return redirect(url_for('admin.dashboard'))
