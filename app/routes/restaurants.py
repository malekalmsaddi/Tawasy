from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.extensions import db
from app.models.menu_item import MenuItem
from app.models.order import Order

restaurants_bp = Blueprint('restaurants', __name__)

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

@restaurants_bp.route('/menu', methods=['POST'])
@role_required(['restaurant'])
def add_menu_item():
    restaurant_id = get_jwt_identity()
    data = request.get_json()
    item = MenuItem(
        restaurant_id=restaurant_id,
        name=data['name'],
        price=data['price'],
        description=data.get('description', '')
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({'message': 'Menu item added', 'item_id': item.id}), 201

@restaurants_bp.route('/menu', methods=['GET'])
@jwt_required()
def get_my_menu():
    restaurant_id = get_jwt_identity()
    items = MenuItem.query.filter_by(restaurant_id=restaurant_id).all()
    return jsonify([i.to_dict() for i in items])

@restaurants_bp.route('/orders', methods=['GET'])
@role_required(['restaurant'])
def get_orders():
    restaurant_id = get_jwt_identity()
    orders = Order.query.filter_by(restaurant_id=restaurant_id).all()
    return jsonify([o.to_dict() for o in orders])
