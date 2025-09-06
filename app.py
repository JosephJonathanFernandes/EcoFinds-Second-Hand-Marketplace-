

# ---------------- Routes ----------------
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import time
import threading
from dynamic_data_service import dynamic_service

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
        
        # Handle image upload
        image_url = "https://via.placeholder.com/150"
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                if filename:
                    # Create uploads directory if it doesn't exist
                    upload_dir = os.path.join('static', 'uploads')
                    os.makedirs(upload_dir, exist_ok=True)
                    
                    # Save file with unique name
                    unique_filename = f"{current_user.id}_{int(time.time())}_{filename}"
                    file_path = os.path.join(upload_dir, unique_filename)
                    file.save(file_path)
                    image_url = f"/static/uploads/{unique_filename}"
        
        product = Product(title=title, description=desc, category=category,
                          price=price, image=image_url, owner=current_user)
        db.session.add(product)
        db.session.commit()
        flash('Product listed successfully!', 'success')
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
        
        if username and username != current_user.username:
            # Check if username is already taken
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('Username already taken!', 'error')
                return redirect(url_for('profile'))
            current_user.username = username
            
        if email and email != current_user.email:
            # Check if email is already taken
            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                flash('Email already registered!', 'error')
                return redirect(url_for('profile'))
            current_user.email = email
            
        if avatar_file and avatar_file.filename:
            filename = secure_filename(avatar_file.filename)
            if filename:
                # Create avatars directory if it doesn't exist
                avatar_dir = os.path.join('static', 'avatars')
                os.makedirs(avatar_dir, exist_ok=True)
                
                # Save with unique filename
                unique_filename = f"{current_user.id}_{int(time.time())}_{filename}"
                avatar_path = os.path.join(avatar_dir, unique_filename)
                avatar_file.save(avatar_path)
                current_user.avatar = f"/static/avatars/{unique_filename}"
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html')

@app.route('/remove_from_cart/<int:product_id>')
@login_required
def remove_from_cart(product_id):
    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart!', 'info')
    return redirect(url_for('cart'))

@app.route('/clear_cart')
@login_required
def clear_cart():
    Cart.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('Cart cleared!', 'info')
    return redirect(url_for('cart'))

@app.route('/search')
def search():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort', 'newest')
    
    products = Product.query
    
    if query:
        products = products.filter(Product.title.ilike(f"%{query}%"))
    if category:
        products = products.filter_by(category=category)
    if min_price is not None:
        products = products.filter(Product.price >= min_price)
    if max_price is not None:
        products = products.filter(Product.price <= max_price)
    
    # Apply sorting
    if sort_by == 'price_low':
        products = products.order_by(Product.price.asc())
    elif sort_by == 'price_high':
        products = products.order_by(Product.price.desc())
    elif sort_by == 'name':
        products = products.order_by(Product.title.asc())
    else:  # newest
        products = products.order_by(Product.id.desc())
    
    products = products.all()
    categories = [c[0] for c in db.session.query(Product.category).distinct()]
    
    return render_template('products.html',
                         products=products,
                         categories=categories,
                         search_query=query,
                         category_filter=category)

# ---------------- Real-time API Endpoints ----------------

@app.route('/api/market-insights')
def market_insights():
    """Get real-time market insights"""
    try:
        insights = dynamic_service.get_market_insights()
        return jsonify(insights)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/trending-categories')
def trending_categories():
    """Get currently trending categories"""
    try:
        trending = dynamic_service.get_trending_categories()
        return jsonify({'trending': trending})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-product')
@login_required
def generate_product():
    """Generate a new dynamic product"""
    try:
        category = request.args.get('category', 'Clothing')
        product_data = dynamic_service.generate_dynamic_product(category)
        
        # Create the product
        product = Product(
            title=product_data['title'],
            description=product_data['description'],
            category=product_data['category'],
            price=product_data['price'],
            image=product_data['image'],
            user_id=current_user.id
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'product': {
                'id': product.id,
                'title': product.title,
                'price': product.price,
                'image': product.image
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/update-prices')
def update_prices():
    """Update product prices dynamically"""
    try:
        products = Product.query.all()
        updated_count = 0
        
        for product in products:
            if request.args.get('force') == 'true' or time.time() % 300 < 60:  # Update every 5 minutes
                old_price = product.price
                new_price = dynamic_service.get_dynamic_pricing(product.category, old_price)
                product.price = new_price
                updated_count += 1
        
        if updated_count > 0:
            db.session.commit()
        
        return jsonify({
            'success': True,
            'updated_count': updated_count,
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/eco-impact/<int:product_id>')
def eco_impact(product_id):
    """Get environmental impact for a product"""
    try:
        product = Product.query.get_or_404(product_id)
        impact = dynamic_service._calculate_eco_impact(product.category, product.price)
        return jsonify(impact)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    with app.app_context():
        # Check if database exists and has data
        if not os.path.exists("instance/ecofinds.db") or Product.query.count() == 0:
            print("🌱 Initializing EcoFinds database...")
            db.create_all()
            
            # Check if we should seed with sample data
            if Product.query.count() == 0:
                print("📦 No products found. Run 'python realistic_seed_database.py' to populate with realistic data.")
                print("   Or register a new account and add products manually.")
        else:
            print("✅ Database already initialized with data")
    
    print("🚀 Starting EcoFinds server...")
    print("🌐 Visit: http://localhost:5000")
    app.run(debug=True)
