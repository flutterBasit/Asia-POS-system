from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy ### import SQLALchemy for database handling
##import flask login for authentication
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

## creating the flask application project 
app = Flask(__name__)
#secret key used for sessions and security 
app.config['Secret_Key'] = 'asia_pos_secret'
## sql database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

##initilize database with flask
db = SQLAlchemy(app)

##initilize the login manager 
login_manager = LoginManager()

##attaching the login manager to flask app
login_manager.init_app(app)

##if User is not logged in redirect to the login page
login_manager.login_view = 'login'

##---------------------------------- DATABASE MODELS -------------------------------

#User table for login system
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key= True) #unique id 
    username = db.Column(db.String(50),unique = True) #Username
    password = db.Column(db.String(50)) # password
    role = db.Column(db.String(20))  #admin/cashier

#User table for inventory
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True) #product id
    name = db.Column(db.String(50),unique=True) # product name
    category = db.Column(db.String(50)) # category (pipes,gryser)
    price = db.Column(db.Float) # product price
    quantity = db.Column(db.Integer) # stock quantity


##---------------------------------LOGIN HANDLER-------------------------------
## load user from database using ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

##----------------------ROUTES--------------------------

## login page (GET = open page, POST = submit form)
@app.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #checking the user credentials from database
        user = User.query.filter_by(
            username = request.form['username'],
            password = request.form['password']
        ).first()

        if user:
            ##loging the user and starting the session
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            ## showing the error message
            flash('Invalid credentials')

    return render_template('login.html')

#Dashboard page
@app.route('/Dashboard')
@login_required # only logged in users are allowed 
def dashboard():
    ##counting the total product 
    total_products = Product.query.count()
    return render_template('dashboard.html',total_products=total_products)

#view product page
@app.route('/products')
@login_required
def products():
    ##fetching all the ptoduct from the database
    items = Product.query.all()
    return render_template('product.html',products=items)

##Adding new products page
@app.route('/add_product',methods=['GET','POST'])
@login_required
def add_product():
    if request.method == 'POST':
        ## creating new product object
        new_product = Product(
            name=request.form['name'],
            category = request.form['category'],
            price = request.form['price'],
            quantity = request.form['quantity']
        )
        ##saving the products to the database
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('products'))

    return render_template('add_product.html')

## Delete products by id
@app.route('/delete_product/<int:id>')
@login_required
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('products'))


