from .auth import auth_bp
from .orders import orders_bp
from .restaurants import restaurants_bp
from .drivers import drivers_bp

all_blueprints = [
    (auth_bp, '/api/auth'),
    (orders_bp, '/api/orders'),
    (restaurants_bp, '/api/restaurants'),
    (drivers_bp, '/api/drivers'),
]
