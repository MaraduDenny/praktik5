from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'rahasia123'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)
bcrypt = Bcrypt(app)

users = []

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    username = request.form['username']
    password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    users.append({'username': username, 'password': password})
    return redirect('/')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    user = next((u for u in users if u['username'] == username), None)
    if user and bcrypt.check_password_hash(user['password'], password):
        session['user'] = username
        return redirect('/dashboard')
    return 'Login gagal'

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    return redirect('/')
