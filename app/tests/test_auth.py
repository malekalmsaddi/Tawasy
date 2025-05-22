import pytest
from main import create_app
from app.extensions import db
from app.models.user import User

@pytest.fixture()
def app(tmp_path):
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///" + str(tmp_path / "test.db"),
        JWT_SECRET_KEY="test-secret",
        REDIS_URL="redis://localhost:6379/0",
    )
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

def register_user(client, email="user@example.com", password="password"):
    return client.post(
        "/api/auth/register",
        json={"email": email, "password": password},
    )

def login_user(client, email="user@example.com", password="password"):
    return client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )

def test_register_new_user(client, app):
    resp = register_user(client)
    assert resp.status_code == 201
    assert resp.get_json()["message"] == "User registered successfully"
    with app.app_context():
        assert User.query.filter_by(email="user@example.com").first() is not None

def test_login_returns_token_and_user_info(client):
    register_user(client)
    resp = login_user(client)
    data = resp.get_json()
    assert resp.status_code == 200
    assert "access_token" in data
    assert data["user"]["email"] == "user@example.com"


def test_logout_redirects_to_login(client):
    response = client.get("/logout")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")
