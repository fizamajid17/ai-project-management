# AI Project Management System

A full-stack AI-powered project management platform where teams can manage projects, collaborate on tasks, and use AI for planning and productivity.

## 🔗 Links

- **Live Demo:** https://ai-project-management-production-46b6.up.railway.app
- **API Docs:** https://ai-project-management-production-46b6.up.railway.app/api/docs/
- **GitHub:** https://github.com/fizamajid17/ai-project-management

## ✨ Features

- User Registration & Login (JWT Authentication)
- Team Management
- Project Creation & Management
- Task Assignment & Tracking
- Comments & Collaboration
- AI Task Breakdown
- AI Sprint Planning
- Dashboard & Analytics
- REST API with Swagger Documentation

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript (Single Page Application)
- **Backend:** Django, Django REST Framework
- **Database:** SQLite
- **AI:** Anthropic Claude API
- **Authentication:** JWT (SimpleJWT)
- **Deployment:** Railway
- **CI/CD:** GitHub Actions

## 🚀 Local Setup

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# Clone the repo
git clone https://github.com/fizamajid17/ai-project-management.git
cd ai-project-management

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

Visit `http://127.0.0.1:8000`

## 📡 API Documentation

Full Swagger UI available at:
```
https://ai-project-management-production-46b6.up.railway.app/api/docs/
```

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register/ | Register new user |
| POST | /api/auth/login/ | Login & get JWT token |
| GET | /api/projects/ | List all projects |
| POST | /api/projects/ | Create project |
| GET | /api/teams/ | List all teams |

## 🤖 AI Features

- **AI Task Breakdown** — Input a task description, AI breaks it into subtasks
- **AI Sprint Planning** — AI suggests sprint plan based on tasks and deadline

## 🔐 Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `ANTHROPIC_API_KEY` | Anthropic Claude API key |

## 👩‍💻 Author

**Fiza Majid** — [@fizamajid17](https://github.com/fizamajid17)
