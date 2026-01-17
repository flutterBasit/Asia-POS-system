
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin,
    login_user, login_required, logout_user
)

# --------------------------------------------------
# APP CONFIGURATION
# --------------------------------------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asia_pos_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --------------------------------------------------
# DATABASE MODELS
# --------------------------------------------------

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=db.func.now())

# --------------------------------------------------
# LOGIN HANDLER
# --------------------------------------------------

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# --------------------------------------------------
# ROUTES
# --------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(
            username=request.form['username'],
            password=request.form['password']
        ).first()

        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password", "error")

    return render_template('login.html')

# ---------------- DASHBOARD ----------------

@app.route('/dashboard')
@login_required
def dashboard():
    total_products = Product.query.count()
    total_sales = db.session.query(db.func.sum(Sale.total)).scalar() or 0
    total_transactions = Sale.query.count()

    return render_template(
        'dashboard.html',
        total_products=total_products,
        total_sales=total_sales,
        total_transactions=total_transactions
    )

# ---------------- PRODUCTS ----------------

@app.route('/products')
@login_required
def products():
    return render_template(
        'products.html',
        products=Product.query.all()
    )

@app.route('/add_product', methods=['POST'])
@login_required
def add_product():
    try:
        name = request.form['name'].strip()
        category = request.form['category'].strip()
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])

        if price <= 0 or quantity < 0:
            flash("Price must be > 0 and quantity ≥ 0", "error")
            return redirect(url_for('products'))

        if Product.query.filter_by(name=name).first():
            flash("Product already exists", "error")
            return redirect(url_for('products'))

        product = Product(
            name=name,
            category=category,
            price=price,
            quantity=quantity
        )

        db.session.add(product)
        db.session.commit()

        flash("Product added successfully", "success")
        return redirect(url_for('products'))

    except ValueError:
        flash("Invalid numeric input", "error")
        return redirect(url_for('products'))

@app.route('/delete_product/<int:id>')
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    try:
        db.session.delete(product)
        db.session.commit()
        flash("Product deleted successfully", "success")
    except Exception as e:
        db.session.rollback()
        flash(str(e), "error")

    return redirect(url_for('products'))

# ---------------- BILLING ----------------

@app.route('/billing', methods=['GET', 'POST'])
@login_required
def billing():
    products = Product.query.all()

    if request.method == 'POST':
        try:
            pid = int(request.form['product'])
            qty = int(request.form['quantity'])

            if qty <= 0:
                flash("Quantity must be greater than zero", "error")
                return redirect(url_for('billing'))

            product = db.session.get(Product, pid)

            if not product:
                flash("Product not found", "error")
                return redirect(url_for('billing'))

            if product.quantity < qty:
                flash("Insufficient stock", "error")
                return redirect(url_for('billing'))

            total = qty * product.price
            product.quantity -= qty

            sale = Sale(
                product_name=product.name,
                quantity=qty,
                price=product.price,
                total=total
            )

            db.session.add(sale)
            db.session.commit()

            flash(f"Sale successful. Total: Rs. {total}", "success")
            return redirect(url_for('invoice', sale_id=sale.id))

        except Exception as e:
            db.session.rollback()
            flash(str(e), "error")

    return render_template('billing.html', products=products)


# ---------------- INVOICE ----------------
@app.route('/save_invoice', methods=['POST'])
@login_required
def save_invoice():
    data = request.get_json()

    session['invoice'] = {
        "customer": data['customer'],
        "cart": data['cart']
    }

    return {"success": True}

@app.route('/invoice/<int:sale_id>')
@login_required
def invoice(sale_id):
    sale = db.session.get(Sale, sale_id)
    if not sale:
        flash("Invoice not found", "error")
        return redirect(url_for('billing'))
    return render_template('invoice.html', sale=sale)


@app.route('/invoice_preview')
@login_required
def invoice_preview():
    invoice = session.get('invoice')

    if not invoice:
        flash("No invoice data found", "error")
        return redirect(url_for('billing'))

    cart = invoice.get('cart', [])
    customer = invoice.get('customer', {})

    if not cart:
        flash("Bill is empty", "error")
        return redirect(url_for('billing'))

    grand_total = sum(
        item['price'] * item['qty'] for item in cart
    )

    return render_template(
        'invoice_preview.html',
        cart=cart,
        customer=customer,
        grand_total=grand_total
    )

@app.route('/prepare_invoice', methods=['POST'])
@login_required
def prepare_invoice():
    data = request.get_json()
    session['invoice'] = data
    return jsonify(success=True)

# ---------------- SALES REPORT ----------------

@app.route('/sales_report')
@login_required
def sales_report():
    return render_template(
        'sales_report.html',
        sales=Sale.query.order_by(Sale.date.desc()).all()
    )


# ---------------- LOGOUT ----------------

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --------------------------------------------------
# DATABASE INITIALIZATION
# --------------------------------------------------

with app.app_context():
    db.create_all()

    if not User.query.first():
        db.session.add(User(
            username="admin",
            password="admin123",
            role="admin"
        ))

        db.session.add_all([
            Product(name="PVC Pipe 1 inch", category="Pipes", price=250, quantity=100),
            Product(name="Gas Pipe", category="Gas", price=400, quantity=50),
            Product(name="Geyser 25L", category="Geyser", price=18000, quantity=10),
            Product(name="Water Filter", category="Filter", price=12000, quantity=15),
        ])

        db.session.commit()

# --------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
