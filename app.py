

# ---------------- Routes ----------------
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hackathon-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecofinds.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ---------------- Models ----------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150))
    password = db.Column(db.String(150))
    avatar = db.Column(db.String(250), default=None)
    products = db.relationship('Product', backref='owner', lazy=True)
    purchases = db.relationship('Purchase', backref='buyer', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(250), default="https://via.placeholder.com/150")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------- Routes ----------------
@app.route('/', methods=['GET', 'POST'])
def index():
    search_query = request.args.get('search', '')
    category_filter = request.args.get('category', '')

    products = Product.query

    if search_query:
        products = products.filter(Product.title.ilike(f"%{search_query}%"))
    if category_filter:
        products = products.filter_by(category=category_filter)

    products = products.all()
    categories = [c[0] for c in db.session.query(Product.category).distinct()]

    return render_template('products.html',
                           products=products,
                           categories=categories,
                           search_query=search_query,
                           category_filter=category_filter)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        user = User(email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful, please log in!')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    my_products = Product.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', products=my_products)

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['description']
        category = request.form['category']
        price = float(request.form['price'])
        product = Product(title=title, description=desc, category=category,
                          price=price, owner=current_user)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_product.html')

@app.route('/cart')
@login_required
def cart():
    items = Cart.query.filter_by(user_id=current_user.id).all()
    products = [Product.query.get(i.product_id) for i in items]
    return render_template('cart.html', products=products)

@app.route('/add_to_cart/<int:pid>')
@login_required
def add_to_cart(pid):
    cart_item = Cart(user_id=current_user.id, product_id=pid)
    db.session.add(cart_item)
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/purchase')
@login_required
def purchase():
    items = Cart.query.filter_by(user_id=current_user.id).all()
    for item in items:
        new_purchase = Purchase(user_id=current_user.id, product_id=item.product_id)
        db.session.add(new_purchase)
        db.session.delete(item)
    db.session.commit()
    return redirect(url_for('purchases'))

@app.route('/purchases')
@login_required
def purchases():
    items = Purchase.query.filter_by(user_id=current_user.id).all()
    products = [Product.query.get(i.product_id) for i in items]
    return render_template('purchases.html', products=products)



@app.route('/products')
def products():
    all_products = Product.query.all()
    return render_template('products.html', products=all_products)

# Landing page route
@app.route('/landing')
def landing():
    featured_products = Product.query.limit(4).all()
    return render_template('landing.html', featured_products=featured_products)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        avatar_file = request.files.get('avatar')
        if username:
            current_user.username = username
        if email:
            current_user.email = email
        if avatar_file and avatar_file.filename:
            filename = secure_filename(avatar_file.filename)
            avatar_path = os.path.join('static', 'avatars', f"{current_user.id}_{filename}")
            os.makedirs(os.path.dirname(avatar_path), exist_ok=True)
            avatar_file.save(avatar_path)
            current_user.avatar = '/' + avatar_path.replace('\\', '/')
        db.session.commit()
        flash('Profile updated!')
        return redirect(url_for('profile'))
    return render_template('profile.html')

if __name__ == "__main__":
    if not os.path.exists("ecofinds.db"):
        with app.app_context():
            db.create_all()
    app.run(debug=True)
