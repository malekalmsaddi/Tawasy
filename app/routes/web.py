from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from app.models.user import User
from app.models.order import Order
from app.models.menu_item import MenuItem
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from app.models.user import User
from app.models.order import Order, OrderItem
from app.models.menu_item import MenuItem


web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def index():
    return redirect(url_for('web.admin_login'))

@web_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, role='admin').first()
        if user and user.check_password(password):
            session['admin_id'] = user.id
            return redirect(url_for('web.dashboard'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@web_bp.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('web.admin_login'))

@web_bp.route('/admin/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('web.admin_login'))

    if request.method == 'POST':
        name = request.form['name']
        try:
            price = float(request.form['price'])
            restaurant_id = int(request.form['restaurant_id'])
        except (ValueError, TypeError):
            users = User.query.all()
            orders = Order.query.order_by(Order.created_at.desc()).all()
            restaurants = User.query.filter_by(role='restaurant').all()
            menus = MenuItem.query.order_by(MenuItem.restaurant_id).all()
            return render_template(
                'dashboard.html',
                error="Invalid input data",
                users=users,
                orders=orders,
                restaurants=restaurants,
                menus=menus
            )
        description = request.form.get('description', '')

        new_item = MenuItem(
            name=name,
            price=price,
            restaurant_id=restaurant_id,
            description=description
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('web.dashboard'))

    users = User.query.all()
    orders = Order.query.order_by(Order.created_at.desc()).all()
    restaurants = User.query.filter_by(role='restaurant').all()
    menus = MenuItem.query.order_by(MenuItem.restaurant_id).all()

    return render_template(
        'dashboard.html',
        users=users,
        orders=orders,
        restaurants=restaurants,
        menus=menus
    )
@web_bp.route('/admin/restaurants/<int:restaurant_id>', methods=['GET', 'POST'])
def restaurant_profile(restaurant_id):
    if 'admin_id' not in session:
        return redirect(url_for('web.admin_login'))

    restaurant = User.query.filter_by(id=restaurant_id, role='restaurant').first_or_404()

    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form.get('description', '')

        item = MenuItem(name=name, price=price, restaurant_id=restaurant.id, description=description)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('web.restaurant_profile', restaurant_id=restaurant.id))

    menus = MenuItem.query.filter_by(restaurant_id=restaurant.id).all()
    return render_template('restaurant_profile.html', restaurant=restaurant, menus=menus)

@web_bp.route('/admin/menu/<int:item_id>/delete')
def delete_menu_item(item_id):
    if 'admin_id' not in session:
        return redirect(url_for('web.admin_login'))
    item = MenuItem.query.get_or_404(item_id)
    rid = item.restaurant_id
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('web.restaurant_profile', restaurant_id=rid))

@web_bp.route('/admin/menu/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_menu_item(item_id):
    if 'admin_id' not in session:
        return redirect(url_for('web.admin_login'))

    item = MenuItem.query.get_or_404(item_id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.price = float(request.form['price'])
        item.description = request.form.get('description', '')
        db.session.commit()
        return redirect(url_for('web.restaurant_profile', restaurant_id=item.restaurant_id))

    return render_template('edit_menu_item.html', item=item)

@web_bp.route('/admin/restaurants/add', methods=['POST'])
def add_restaurant():
    if 'admin_id' not in session:
        return redirect(url_for('web.admin_login'))
    email = request.form['email']
    password = request.form['password']
    existing = User.query.filter_by(email=email).first()
    if existing:
        users = User.query.all()
        orders = Order.query.order_by(Order.created_at.desc()).all()
        restaurants = User.query.filter_by(role='restaurant').all()
        menus = MenuItem.query.order_by(MenuItem.restaurant_id).all()
        return render_template(
            'dashboard.html',
            error="Email already exists",
            users=users,
            orders=orders,
            restaurants=restaurants,
            menus=menus
        )

    new_rest = User(email=email, role='restaurant')
    new_rest.set_password(password)
    db.session.add(new_rest)
    db.session.commit()
    return redirect(url_for('web.dashboard'))

@web_bp.route('/admin/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    if 'admin_id' not in session:
        return redirect(url_for('web.admin_login'))

    r = User.query.filter_by(id=restaurant_id, role='restaurant').first_or_404()

    if request.method == 'POST':
        new_email = request.form['email']
        existing = User.query.filter(User.email == new_email, User.id != restaurant_id).first()
        if existing:
            menus = MenuItem.query.filter_by(restaurant_id=restaurant_id).all()
            return render_template('edit_restaurant.html', restaurant=r, menus=menus, error="Email already in use")
        r.email = new_email
        db.session.commit()
        return redirect(url_for('web.dashboard'))

    menus = MenuItem.query.filter_by(restaurant_id=restaurant_id).all()
    return render_template('edit_restaurant.html', restaurant=r, menus=menus)

@web_bp.route('/admin/restaurants/<int:restaurant_id>/delete')
def delete_restaurant(restaurant_id):
    if 'admin_id' not in session:
        return redirect(url_for('web.admin_login'))
    r = User.query.filter_by(id=restaurant_id, role='restaurant').first_or_404()
    db.session.delete(r)
    db.session.commit()
    return redirect(url_for('web.dashboard'))

@web_bp.route('/admin/restaurants/<int:restaurant_id>/edit/add-item', methods=['POST'])
def add_menu_item_to_edit(restaurant_id):
    if 'admin_id' not in session:
        return redirect(url_for('web.admin_login'))

    restaurant = User.query.filter_by(id=restaurant_id, role='restaurant').first_or_404()

    name = request.form['name']
    try:
        price = float(request.form['price'])
    except ValueError:
        price = 0.0
    description = request.form.get('description', '')

    new_item = MenuItem(name=name, price=price, description=description, restaurant_id=restaurant.id)
    db.session.add(new_item)
    db.session.commit()

    return redirect(url_for('web.edit_restaurant', restaurant_id=restaurant.id))

@web_bp.route("/register", methods=["GET", "POST"])
def user_register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if User.query.filter_by(email=email).first():
            return render_template("user_register.html", error="Email already registered.")
        user = User(email=email, password=generate_password_hash(password), role="customer")
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        return redirect(url_for("web.home"))
    return render_template("user_register.html")

@web_bp.route("/login", methods=["GET", "POST"])
def user_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return render_template("login.html", error="Invalid email or password")

        session["user_id"] = user.id
        return redirect(url_for("web.user_dashboard"))

    return render_template("login.html")

@web_bp.route("/logout")
def user_logout():
    session.pop("user_id", None)
    return redirect(url_for("web.user_login"))

@web_bp.route("/restaurant/<int:restaurant_id>/order", methods=["POST"])
def place_order(restaurant_id):
    if "user_id" not in session:
        return redirect(url_for("web.user_login"))

    item_ids = request.form.getlist("item_ids")
    if not item_ids:
        flash("No items selected.")
        return redirect(url_for("web.view_menu", restaurant_id=restaurant_id))

    order = Order(customer_id=session["user_id"])
    db.session.add(order)
    db.session.flush()  # Get order.id before commit

    for item_id in item_ids:
        order_item = OrderItem(order_id=order.id, menu_item_id=int(item_id), quantity=1)
        db.session.add(order_item)

    db.session.commit()
    flash("Order placed!")
    return redirect(url_for("web.my_orders"))

@web_bp.route("/admin/add_user", methods=["POST"])
def add_user():
    email = request.form.get("email")
    password = request.form.get("password")
    role = request.form.get("role", "customer")

    if not email or not password:
        flash("Email and password required", "danger")
        return redirect(url_for("web.dashboard"))

    if User.query.filter_by(email=email).first():
        flash("User already exists", "warning")
        return redirect(url_for("web.dashboard"))

    new_user = User(email=email, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    flash(f"{role.title()} created successfully", "success")
    return redirect(url_for("web.dashboard"))


@web_bp.route("/admin/add_driver", methods=["POST"])
def add_driver():
    email = request.form.get("email")
    password = request.form.get("password")
    role = request.form.get("role", "customer")

    if not email or not password:
        flash("Email and password required", "danger")
        return redirect(url_for("web.dashboard"))

    if User.query.filter_by(email=email).first():
        flash("User already exists", "warning")
        return redirect(url_for("web.dashboard"))

    new_user = User(email=email, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    flash(f"{role.title()} created successfully", "success")
    return redirect(url_for("web.dashboard"))

@web_bp.route("/user/dashboard")
def user_dashboard():
    if "user_id" not in session:
        return redirect(url_for("web.user_login"))

    user = User.query.get(session["user_id"])
    return render_template("user_dashboard.html", user=user)

@web_bp.route("/my-orders")
def my_orders():
    if "user_id" not in session:
        return redirect(url_for("web.user_login"))

    user = User.query.get(session["user_id"])
    return render_template("my_orders.html", orders=user.orders)
