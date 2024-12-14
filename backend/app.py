from flask import Flask, request, jsonify, make_response, render_template, session, flash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from extensions import db
from models import User, ScrapedContent
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'

jwt = JWTManager(app)
CORS(app)
db.init_app(app)

# Import and register workspace blueprint
from workspace import workspace_bp
app.register_blueprint(workspace_bp)

# Import and register scraper blueprint
from scraper import scraper_bp
app.register_blueprint(scraper_bp)

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 400

    new_user = User(email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=email)
    return jsonify({"access_token": access_token}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
