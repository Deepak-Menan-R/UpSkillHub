#professor_routes.py

from flask import Blueprint, jsonify, request
from models import Course, Content, User, db
from flask_jwt_extended import jwt_required, get_jwt_identity

professor_bp = Blueprint('professor', __name__)

@professor_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def professor_dashboard():
    user_id = get_jwt_identity()
    return jsonify({"message": f"Welcome Professor {user_id}! Upload courses & track student progress here."})

@professor_bp.route('/create_course', methods=['POST'])
@jwt_required()
def create_course():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user.role != 'professor':
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    new_course = Course(name=data['name'], professor_id=user.id)
    
    db.session.add(new_course)
    db.session.commit()

    return jsonify({"message": "Course created successfully!", "course_id": new_course.id, "course_name": new_course.name})

@professor_bp.route('/upload_content', methods=['POST'])
@jwt_required()
def upload_content():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user.role != 'professor':
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    new_content = Content(
        course_id=data['course_id'],
        professor_id=user.id,
        content_type=data['content_type'],  # 'video' or 'pdf'
        content_url=data['content_url']
    )

    db.session.add(new_content)
    db.session.commit()

    return jsonify({"message": "Content uploaded successfully!"})
