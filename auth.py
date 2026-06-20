"""
CropSense v2.0 — Auth Blueprint
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from extensions import db, bcrypt
from models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('farmer.dashboard'))

    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id']   = user.id
            session['user_name'] = user.name
            session['role']      = user.role
            flash(f'Welcome back, {user.name}! 👋', 'success')
            return redirect(url_for('farmer.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        return redirect(url_for('farmer.dashboard'))

    if request.method == 'POST':
        name     = request.form.get('name', '').strip()
        email    = request.form.get('email', '').strip().lower()
        phone    = request.form.get('phone', '').strip()
        state    = request.form.get('state', '')
        district = request.form.get('district', '').strip()
        password = request.form.get('password', '')

        if not name or not email or not password or not state or not district:
            flash('Please fill all required fields.', 'danger')
            return render_template('register.html')

        if len(password) < 8:
            flash('Password must be at least 8 characters.', 'danger')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login.', 'warning')
            return redirect(url_for('auth.login'))

        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(
            name=name, email=email, phone=phone,
            password=hashed, state=state, district=district,
            role='farmer'
        )
        db.session.add(user)
        db.session.commit()

        flash('Account created! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
