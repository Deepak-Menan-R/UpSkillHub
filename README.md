# UpSkillHub (BackEnd)

## Overview
This is a Flask-based university learning platform that allows professors to upload courses and content, and students to access them. It includes authentication, role-based access, WebSocket-based discussions, and tracking features.

## Features
- **User Authentication** (JWT-based login and registration for professors and students)
- **Role-based Access** (Professors can create courses and upload content; students can access courses and track progress)
- **Course & Content Management** (Professors can create courses and upload videos or PDFs)
- **Quiz System** (AI-generated quizzes based on course content)
- **Tracking System** (Logs student interactions with course content)
- **WebSocket-based Discussions** (Real-time chat functionality for courses)

## Installation

1. **Clone the Repository**
   ```sh
   git clone [<repository_url>](https://github.com/Deepak-Menan-R/UpSkillHub.git)
   cd UpSkillHub
   ```

2. **Create a Virtual Environment**
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Setup Environment Variables**
   Create a `.env` file and add:
   ```
   SECRET_KEY=your_secret_key
   SQLALCHEMY_DATABASE_URI=sqlite:///database.db  # or another DB URI
   ```

5. **Initialize the Database**
   ```sh
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

6. **Run the Application**
   ```sh
   python app.py
   ```

## API Endpoints

### Authentication
- `POST /auth/register` - Register as a professor (if email ends with `@university.edu`) or student
- `POST /auth/login` - Login and receive a JWT token

### Professor Routes
- `GET /professor/dashboard` - Access professor dashboard
- `POST /professor/create_course` - Create a new course
- `POST /professor/upload_content` - Upload videos or PDFs for a course

### Student Routes
- `GET /student/dashboard` - Access student dashboard
- `GET /student/courses` - View available courses
- `GET /student/course/<course_id>/contents` - Get course content
- `POST /student/track_content` - Track content interactions

### WebSocket Discussion
- Professors and students can participate in real-time discussions for each course

## Technologies Used
- **Flask** (Web framework)
- **Flask-JWT-Extended** (Authentication)
- **Flask-SQLAlchemy** (Database ORM)
- **Flask-SocketIO** (WebSockets for discussions)
- **SQLite/PostgreSQL** (Database)

## Future Enhancements
- AI-based quiz generation
- Video progress tracking
- Multi-user live discussions

## Author
Deepak Menan

## License
MIT License

