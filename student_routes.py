#student_routes.py
from flask import Blueprint, jsonify, request
from models import Course, Content, Tracking, db
from flask_jwt_extended import jwt_required, get_jwt_identity

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def student_dashboard():
    user_id = get_jwt_identity()
    return jsonify({"message": f"Welcome Student {user_id}! Access your courses & quizzes here."})

@student_bp.route('/courses', methods=['GET'])
@jwt_required()
def get_courses():
    courses = Course.query.all()
    result = [{"id": c.id, "name": c.name, "professor": c.professor.name} for c in courses]

    return jsonify(result)

@student_bp.route('/course/<int:course_id>/contents', methods=['GET'])
@jwt_required()
def get_course_contents(course_id):
    contents = Content.query.filter_by(course_id=course_id).all()
    result = [{"id": c.id, "type": c.content_type, "url": c.content_url} for c in contents]

    return jsonify(result)

@student_bp.route('/track_content', methods=['POST'])
@jwt_required()
def track_content():
    user_id = get_jwt_identity()
    data = request.get_json()

    new_tracking = Tracking(
        student_id=user_id,
        content_id=data['content_id'],
        action=data['action']  # 'watched' or 'downloaded'
    )

    db.session.add(new_tracking)
    db.session.commit()

    return jsonify({"message": "Action recorded!"})

