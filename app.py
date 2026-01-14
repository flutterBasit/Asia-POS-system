# # from flask import Flask, render_template, request, redirect, url_for, flash
# # from flask_sqlalchemy import SQLAlchemy ### import SQLALchemy for database handling
# # ##import flask login for authentication
# # from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

# # ## creating the flask application project 
# # app = Flask(__name__)
# # #secret key used for sessions and security 
# # app.config['Secret_Key'] = 'asia_pos_secret'
# # ## sql database configuration
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# # ##initilize database with flask
# # db = SQLAlchemy(app)

# # ##initilize the login manager 
# # login_manager = LoginManager()

# # ##attaching the login manager to flask app
# # login_manager.init_app(app)

# # ##if User is not logged in redirect to the login page
# # login_manager.login_view = 'login'

# # ##---------------------------------- DATABASE MODELS -------------------------------

# # #User table for login system
# # class User(UserMixin,db.Model):
# #     id = db.Column(db.Integer, primary_key= True) #unique id 
# #     username = db.Column(db.String(50),unique = True) #Username
# #     password = db.Column(db.String(50)) # password
# #     role = db.Column(db.String(20))  #admin/cashier

# # #User table for inventory
# # class Product(db.Model):
# #     id = db.Column(db.Integer, primary_key = True) #product id
# #     name = db.Column(db.String(50),unique=True) # product name
# #     category = db.Column(db.String(50)) # category (pipes,gryser)
# #     price = db.Column(db.Float) # product price
# #     quantity = db.Column(db.Integer) # stock quantity


# # ##---------------------------------LOGIN HANDLER-------------------------------
# # ## load user from database using ID
# # @login_manager.user_loader
# # def load_user(user_id):
# #     return User.query.get(int(user_id))

# # ##----------------------ROUTES--------------------------

# # ## login page (GET = open page, POST = submit form)
# # @app.route('/',methods=['GET','POST'])
# # def login():
# #     if request.method == 'POST':
# #         #checking the user credentials from database
# #         user = User.query.filter_by(
# #             username = request.form['username'],
# #             password = request.form['password']
# #         ).first()

# #         if user:
# #             ##loging the user and starting the session
# #             login_user(user)
# #             return redirect(url_for('dashboard'))
# #         else:
# #             ## showing the error message
# #             flash('Invalid credentials')

# #     return render_template('login.html')

# # #Dashboard page
# # @app.route('/Dashboard')
# # @login_required # only logged in users are allowed 
# # def dashboard():
# #     ##counting the total product 
# #     total_products = Product.query.count()
# #     return render_template('dashboard.html',total_products=total_products)

# # #view product page
# # @app.route('/products')
# # @login_required
# # def products():
# #     ##fetching all the ptoduct from the database
# #     items = Product.query.all()
# #     return render_template('product.html',products=items)

# # ##Adding new products page
# # @app.route('/add_product',methods=['GET','POST'])
# # @login_required
# # def add_product():
# #     if request.method == 'POST':
# #         ## creating new product object
# #         new_product = Product(
# #             name=request.form['name'],
# #             category = request.form['category'],
# #             price = request.form['price'],
# #             quantity = request.form['quantity']
# #         )
# #         ##saving the products to the database
# #         db.session.add(new_product)
# #         db.session.commit()
# #         return redirect(url_for('products'))

# #     return render_template('add_product.html')

# # ## Delete products by id
# # @app.route('/delete_product/<int:id>')
# # @login_required
# # def delete_product(id):
# #     product = Product.query.get(id)
# #     db.session.delete(product)
# #     db.session.commit()
# #     return redirect(url_for('products'))

# # # billing (POS) page
# # @app.route('/billing',methods=['GET', 'POST'])
# # @login_required
# # def billing():
# #     products = Product.query.all()

# #     if request.method == 'POST':
# #            product_id = int(request.form['prodcut'])
# #            qunatity = int(request.form['quantity'])

# #            product = Product.query.get(product_id)

# #            ##checking the stock availablity 
# #            if product.quantity >= qunatity:
# #                product.quantity -= qunatity ## reduct the stock qunatity 
# #                db.session.commit()
# #                flash("Sale completed successfully!")
# #            else:
# #                flash("Insufficient stock!")

# #     return render_template('billing.html', products=products)

# # ## logout route 
# # @app.route('/logout')
# # @login_required
# # def logout():
# #     logout_user() ## End user session
# #     return redirect(url_for('login'))

# # ### -----------------------INITIAL DATA---------------------
# # @app.before_first_request
# # def create_tables():
# #     db.create_all() ##creating tables

# #     ###if no user exists, create admin user 
# #     if not User.query.first():
# #         admin = User(username ="admin",password = "admin123", role = "admin")
# #         db.session.add(admin)

# #         ## dummy products for the shop
# #         products=[
# #             Product(name= "PVC pipe 1 inch", category = "Pipes", price = 250, quantity = 100),
# #             Product(name="Gas Pipe", category="Gas", price=400, quantity=50),
# #             Product(name="Geyser 25L", category="Geyser", price=18000, quantity=10),
# #             Product(name="Water Filter", category="Filter", price=12000, quantity=15)
# #         ]
# #         db.session.add_all(products)
# #         db.session.commit()

# # ## running the flask app 
# # if __name__ == '__main__':
# #     app.run(debug=True)

# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# app = Flask(__name__)
# # Fixed: Proper case for SECRET_KEY
# app.config['SECRET_KEY'] = 'asia_pos_secret'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# # --- MODELS ---
# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True)
#     password = db.Column(db.String(50)) 
#     role = db.Column(db.String(20))

# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), unique=True)
#     category = db.Column(db.String(50))
#     price = db.Column(db.Float)
#     quantity = db.Column(db.Integer)

# @login_manager.user_loader
# def load_user(user_id):
#     return db.session.get(User, int(user_id))

# # --- ROUTES ---

# @app.route('/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         user = User.query.filter_by(
#             username=request.form['username'],
#             password=request.form['password']
#         ).first()
#         if user:
#             login_user(user)
#             return redirect(url_for('dashboard'))
#         flash('Invalid credentials')
#     return render_template('login.html')

# @app.route('/dashboard')
# @login_required
# def dashboard():
#     total_products = Product.query.count()
#     return render_template('dashboard.html', total_products=total_products)

# @app.route('/products')
# @login_required
# def products():
#     items = Product.query.all()
#     # Fixed typo: changed product.html to products.html to match your list
#     return render_template('products.html', products=items)

# @app.route('/add_product', methods=['GET', 'POST'])
# @login_required
# def add_product():
#     if request.method == 'POST':
#         new_product = Product(
#             name=request.form['name'],
#             category=request.form['category'],
#             price=float(request.form['price']), # Convert to float
#             quantity=int(request.form['quantity']) # Convert to int
#         )
#         db.session.add(new_product)
#         db.session.commit()
#         return redirect(url_for('products'))
#     return render_template('add_product.html')

# @app.route('/billing', methods=['GET', 'POST'])
# @login_required
# def billing():
#     all_items = Product.query.all()
#     if request.method == 'POST':
#         # Added a try/except to prevent crash if form data is missing
#         try:
#             p_id = int(request.form['product'])
#             qty = int(request.form['quantity'])
#             product = db.session.get(Product, p_id)

#             if product and product.quantity >= qty:
#                 product.quantity -= qty
#                 db.session.commit()
#                 flash(f"Sold {qty} units of {product.name}")
#             else:
#                 flash("Insufficient stock!")
#         except Exception as e:
#             flash("Error processing sale")
            
#     return render_template('billing.html', products=all_items)

# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('login'))

# # --- INITIAL DATA (Modern Approach) ---
# with app.app_context():
#     db.create_all()
#     if not User.query.first():
#         admin = User(username="admin", password="admin123", role="admin")
#         db.session.add(admin)
        
#         # Adding dummy data
#         if not Product.query.first():
#             dummy_data = [
#                 Product(name="PVC pipe 1 inch", category="Pipes", price=250, quantity=100),
#                 Product(name="Gas Pipe", category="Gas", price=400, quantity=50)
#             ]
#             db.session.add_all(dummy_data)
#         db.session.commit()

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash
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

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        try:
            name = request.form['name'].strip()
            category = request.form['category'].strip()
            price = float(request.form['price'])
            quantity = int(request.form['quantity'])

            if price <= 0 or quantity < 0:
                flash("Price must be > 0 and quantity ≥ 0", "error")
                return redirect(url_for('add_product'))

            if Product.query.filter_by(name=name).first():
                flash("Product already exists", "error")
                return redirect(url_for('add_product'))

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

    return render_template('add_product.html')

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

@app.route('/invoice/<int:sale_id>')
@login_required
def invoice(sale_id):
    sale = db.session.get(Sale, sale_id)
    if not sale:
        flash("Invoice not found", "error")
        return redirect(url_for('billing'))
    return render_template('invoice.html', sale=sale)

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
