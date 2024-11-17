from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import get_db, User

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        db = next(get_db())  # Получаем сессию базы данных
        new_user = User(username=username, password=hashed_password)
        db.add(new_user)
        db.commit()

        flash('Registration successful! Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('register.html')


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = next(get_db())  # Получаем сессию базы данных
        user = db.query(User).filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Logged in successfully!')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your credentials.')
    return render_template('login.html')


@auth_blueprint.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!')
    return redirect(url_for('home'))
