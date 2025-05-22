from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.extensions import db
from app.models.order import Order

drivers_bp = Blueprint('drivers', __name__)

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

@drivers_bp.route('/orders', methods=['GET'])
@role_required(['driver'])
def view_assigned_orders():
    driver_id = get_jwt_identity()
    orders = Order.query.filter_by(driver_id=driver_id).all()
    return jsonify([o.to_dict() for o in orders])

@drivers_bp.route('/orders/<int:order_id>', methods=['PATCH'])
@role_required(['driver'])
def update_order_status(order_id):
    driver_id = get_jwt_identity()
    order = Order.query.get(order_id)

    if not order or order.driver_id != driver_id:
        return jsonify({"error": "Order not found or access denied"}), 404

    data = request.get_json()
    new_status = data.get('status')

    if new_status not in ['out_for_delivery', 'delivered']:
        return jsonify({"error": "Invalid status"}), 400

    order.status = new_status
    db.session.commit()
    return jsonify({'message': 'Order status updated', 'order': order.to_dict()})
