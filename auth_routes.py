#auth_routes.py

import jwt
import datetime
from flask import request, jsonify, Blueprint
from models import User, db
from config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({"message": "Invalid credentials"}), 401

    token = jwt.encode(
        {"sub": str(user.id), "user_id": user.id, "role": user.role, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        Config.SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({"token": token, "role": user.role})


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data['email']
    name = data['name']
    password = data['password']

    role = "professor" if email.endswith("@university.edu") else "student"

    new_user = User(email=email, name=name, role=role)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!", "role": role})
