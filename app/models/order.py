from datetime import datetime
from app.extensions import db
from app.models.menu_item import MenuItem

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(50), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # ✅ Added

    customer = db.relationship("User", back_populates="orders")
    items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan", lazy=True)

    def item_summary(self):
        return ", ".join(f"{i.menu_item.name} x{i.quantity}" for i in self.items)

    def __repr__(self):
        return f"<Order {self.id} - {self.status}>"
    
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_items.id"), nullable=False)  # ✅ Fixed FK
    quantity = db.Column(db.Integer, nullable=False, default=1)

    order = db.relationship("Order", back_populates="items")
    menu_item = db.relationship("MenuItem", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem {self.menu_item_id} x{self.quantity}>"
