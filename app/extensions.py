from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import redis

db = SQLAlchemy()
jwt = JWTManager()

class RedisClient:
    def __init__(self):
        self.client = None

    def init_app(self, app):
        self.client = redis.Redis.from_url(app.config["REDIS_URL"])

redis_client = RedisClient()
