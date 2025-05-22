# 🍽️ Tawasy – AI-Driven Food Delivery Backend

**Tawasy** is a real-time, modular, AI-assisted food delivery backend built with Flask, PostgreSQL, and Redis. It is designed to support customer ordering, restaurant management, driver assignment, and smart order routing using OpenAI integrations.

---

## 🚀 Tech Stack

| Layer              | Technology                     |
|--------------------|-------------------------------|
| Web Framework      | Flask                          |
| ORM / DB Layer     | SQLAlchemy + PostgreSQL        |
| Authentication     | Flask-JWT-Extended (JWT)       |
| Caching / PubSub   | Redis                          |
| AI Assistant       | OpenAI API (GPT-4)             |
| Background Workers | (Planned) Celery + Redis       |
| Templating Engine  | Jinja2                         |
| Deployment         | Docker / Fly.io (Optional)     |

---

## 📁 Project Structure

```
tawasy_app/
│
├── app/                  # Core app modules (routes, models, logic)
│   ├── routes/           # Modular Flask blueprints
│   ├── models/           # SQLAlchemy models
│   ├── config.py         # App settings
│   └── extensions.py     # JWT, Redis, DB init
│
├── templates/            # HTML templates (Jinja2)
├── main.py               # Flask app factory + CLI commands
├── requirements.txt      # Dependencies
└── readme.md             # This file
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/tawasy.git
cd tawasy
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables (e.g. `.env` file)

```env
FLASK_APP=main.py
FLASK_ENV=development
DATABASE_URL=postgresql://user:pass@localhost/tawasy
JWT_SECRET_KEY=your-secret
REDIS_URL=redis://localhost:6379/0
```

### 5. Initialize Database

```bash
flask init-db
```

### 6. Create Admin User

```bash
flask create-admin
```

---

## 🧠 AI Features

Tawasy integrates OpenAI (GPT-4) to power intelligent assistants that help:
- Suggest restaurants or items
- Provide order support
- Auto-route requests to whitelisted restaurants

> AI is currently under integration and evolving.

---

## 🛣️ Roadmap

- ✅ Modular routing with blueprints
- ✅ JWT-based user authentication
- ✅ Redis integration for caching / queuing
- ✅ Admin CLI commands
- ⏳ AI ordering assistant (WIP)
- ⏳ Celery for background tasks (planned)
- ⏳ WebSocket support for real-time updates

---

## 🧪 Testing

Coming soon.

---

## 📜 License

MIT License