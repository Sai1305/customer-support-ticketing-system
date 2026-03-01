from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, User
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        role = request.form.get('role') or 'customer'

        # 🚫 Prevent direct admin registration
        if role.lower() == 'admin':
            flash('Admin accounts cannot be created from this form.', 'danger')
            return redirect(url_for('auth.register'))

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please log in.', 'warning')
            return redirect(url_for('auth.login'))

        # Create new user
        user = User(email=email, name=name, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('auth.login'))

        # ✅ Restrict admin login only to those pre-created in DB
        if user.role == 'admin' and user.email not in ["admin@flipkart.com"]:
            flash('Unauthorized admin login attempt.', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            if user.role == 'admin':
                next_page = url_for('admin.dashboard')
            else:
                next_page = url_for('tickets.index')
        return redirect(next_page)

    return render_template('login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
