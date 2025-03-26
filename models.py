#models.py 

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

# User model (Professors & Students)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'student' or 'professor'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# Course model
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    professor = db.relationship('User', backref=db.backref('courses', lazy=True))


# Content model (Videos & PDFs)
class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content_type = db.Column(db.String(10), nullable=False)  # 'video' or 'pdf'
    content_url = db.Column(db.Text, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    course = db.relationship('Course', backref=db.backref('contents', lazy=True))
    professor = db.relationship('User', backref=db.backref('uploaded_contents', lazy=True))


# Quiz model (AI-generated)
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.Text, nullable=False)
    option_b = db.Column(db.Text, nullable=False)
    option_c = db.Column(db.Text, nullable=False)
    option_d = db.Column(db.Text, nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)  # 'A', 'B', 'C', or 'D'

    course = db.relationship('Course', backref=db.backref('quizzes', lazy=True))
    content = db.relationship('Content', backref=db.backref('quizzes', lazy=True))


# Quiz Attempts model (Stores student responses)
class QuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    selected_option = db.Column(db.String(1), nullable=False)  # 'A', 'B', 'C', 'D'
    is_correct = db.Column(db.Boolean, nullable=False)
    attempt_time = db.Column(db.DateTime, default=datetime.utcnow)

    quiz = db.relationship('Quiz', backref=db.backref('attempts', lazy=True))
    student = db.relationship('User', backref=db.backref('quiz_attempts', lazy=True))


# Tracking model (Track video views & PDF downloads)
class Tracking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    action = db.Column(db.String(20), nullable=False)  # 'watched' or 'downloaded'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('User', backref=db.backref('tracking', lazy=True))
    content = db.relationship('Content', backref=db.backref('tracking', lazy=True))


# Discussion model (WebSocket-based real-time chat)
class Discussion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    course = db.relationship('Course', backref=db.backref('discussions', lazy=True))
    sender = db.relationship('User', backref=db.backref('messages', lazy=True))
