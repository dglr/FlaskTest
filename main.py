from flask import Flask, request, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from passlib.hash import pbkdf2_sha256
from flask_mail import Mail, Message
from flask_httpauth import HTTPBasicAuth
from functools import wraps
import re
import random
import string
import datetime

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'email@example.com'
app.config['MAIL_PASSWORD'] = 'password'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# In-memory database for demonstration purposes only
users = {
'admin@example.com': {'password': pbkdf2_sha256.hash('adminpassword'), 'role': 'admin','logged_in': False,
            'last_interaction': None}
}
verification_codes = {}

def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

def password_valid(password):
    return bool(re.match('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,}$', password))

def username_valid(username):
    return bool(re.match(r'^1[3-9]\d{9}$', username) or re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', username))

# 验证管理员装饰器
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        user = users.get(token)
        if user is None or user['role'] != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username_valid(username) or not password_valid(password):
        return jsonify({'error': 'Invalid username or password'}), 400

    verification_code = generate_verification_code()
    verification_codes[username] = verification_code

    msg = Message('Verification code', sender='email@example.com', recipients=[username])
    msg.body = f'Your verification code is {verification_code}'
    mail.send(msg)

    return jsonify({'message': 'Verification code sent'}), 200

@app.route('/verify', methods=['POST'])
def verify():
    username = request.json.get('username')
    code = request.json.get('code')
    password = request.json.get('password')

    if verification_codes.get(username) == code:
        users[username] = {
            'password': pbkdf2_sha256.hash(password),
            'role': 'user',
            'logged_in': False,
            'last_interaction': None
        }
        return jsonify({'message': 'User registered successfully'}), 200
    else:
        return jsonify({'error': 'Verification failed'}), 400

# 管理员添加用户路由
@app.route('/admin/add_user', methods=['POST'])
@admin_required
def add_user():
    # Security check (replace with real security measures)
    secret_key = request.headers.get('X-Secret-Key')
    if secret_key != 'adminsecret':
        return jsonify({'error': 'Unauthorized'}), 401

    username = request.json.get('username')
    password = request.json.get('password')

    if not password_valid(password):
        return jsonify({'error': 'Invalid  password'}), 397

    if not username_valid(username):
        return jsonify({'error': 'Invalid username '}), 399

        # 检查用户名是否已存在
        if get_user(username):
            return jsonify({'error': 'Username already exists'}), 409

    users[username] = {
        'password': pbkdf2_sha256.hash(password),
        'role': 'user',
        'logged_in': False,
        'last_interaction': None
    }

    return jsonify({'message': 'User added successfully'}), 200

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = users.get(username)

    if user and pbkdf2_sha256.verify(password, user['password']):
        user['logged_in'] = True
        user['last_interaction'] = datetime.datetime.now()
        response = make_response(jsonify({'message': 'Login successful'}))
        response.headers['Authorization'] = username
        return response, 200
    else:
        return jsonify({'error': 'Login failed'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    username = request.headers.get('Authorization')
    user = users.get(username)
    if user:
        user['logged_in'] = False
        return jsonify({'message': 'Logout successful'}), 200
    else:
        return jsonify({'error': 'Logout failed'}), 401

@app.route('/status', methods=['GET'])
def status():
    username = request.headers.get('Authorization')
    user = users.get(username)

    if user:
        if user['logged_in']:
            last_interaction = user['last_interaction']
            if last_interaction and (datetime.datetime.now() - last_interaction).days > 1:
                user['logged_in'] = False
                return jsonify({'status': 'expired'}), 200
            else:
                user['last_interaction'] = datetime.datetime.now()
                return jsonify({'status': 'logged in'}), 200
        else:
            return jsonify({'status': 'logged out'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

