from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.extensions import db
from app.models.order import Order
from app.models.user import User

orders_bp = Blueprint('orders', __name__)

def role_required(required_roles):
    def wrapper(fn):
        @jwt_required()
        def decorated(*args, **kwargs):
            claims = get_jwt()
            if claims.get('role') not in required_roles:
                return jsonify({"error": "Access denied"}), 403
            return fn(*args, **kwargs)
        decorated.__name__ = fn.__name__
        return decorated
    return wrapper

@orders_bp.route('/', methods=['POST'])
@role_required(['customer'])
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()

    new_order = Order(
        customer_id=user_id,
        items=data.get('items'),
        status='pending'
    )
    db.session.add(new_order)
    db.session.commit()

    return jsonify({'message': 'Order created', 'order_id': new_order.id}), 201

@orders_bp.route('/', methods=['GET'])
@jwt_required()
def get_my_orders():
    user_id = get_jwt_identity()
    claims = get_jwt()
    role = claims.get('role')

    if role == 'customer':
        orders = Order.query.filter_by(customer_id=user_id).all()
    elif role == 'restaurant':
        orders = Order.query.filter_by(restaurant_id=user_id).all()
    elif role == 'driver':
        orders = Order.query.filter_by(driver_id=user_id).all()
    else:
        orders = Order.query.all()

    return jsonify([o.to_dict() for o in orders])
