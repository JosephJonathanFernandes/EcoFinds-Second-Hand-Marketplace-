#!/usr/bin/env python3
"""
EcoFinds Realistic Database Seeding Script
Populates the database with realistic, image-matched products
"""

import os
import sys
import time
from datetime import datetime, timedelta
import random

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Product, Cart, Purchase
from werkzeug.security import generate_password_hash
from dynamic_data_service import dynamic_service

def create_realistic_users(count=8):
    """Create realistic users with proper profiles"""
    print(f"👥 Creating {count} realistic users...")
    
    user_profiles = [
        {
            'email': 'sarah.green@example.com',
            'username': 'SarahGreen',
            'password': 'password123',
            'avatar': 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face',
            'bio': 'Eco-conscious fashion enthusiast and sustainability advocate'
        },
        {
            'email': 'eco.mike@example.com',
            'username': 'EcoMike',
            'password': 'password123',
            'avatar': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face',
            'bio': 'Technology enthusiast focused on sustainable living'
        },
        {
            'email': 'sustainable.sam@example.com',
            'username': 'SustainableSam',
            'password': 'password123',
            'avatar': 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face',
            'bio': 'Home and garden expert promoting zero-waste lifestyle'
        },
        {
            'email': 'green.lisa@example.com',
            'username': 'GreenLisa',
            'password': 'password123',
            'avatar': 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150&h=150&fit=crop&crop=face',
            'bio': 'Vintage collector and sustainable fashion blogger'
        },
        {
            'email': 'recycle.ryan@example.com',
            'username': 'RecycleRyan',
            'password': 'password123',
            'avatar': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face',
            'bio': 'Sports enthusiast and environmental activist'
        },
        {
            'email': 'organic.anna@example.com',
            'username': 'OrganicAnna',
            'password': 'password123',
            'avatar': 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&h=150&fit=crop&crop=face',
            'bio': 'Beauty and wellness expert promoting natural products'
        },
        {
            'email': 'vintage.david@example.com',
            'username': 'VintageDavid',
            'password': 'password123',
            'avatar': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop&crop=face',
            'bio': 'Furniture restorer and vintage collector'
        },
        {
            'email': 'minimal.maya@example.com',
            'username': 'MinimalMaya',
            'password': 'password123',
            'avatar': 'https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=150&h=150&fit=crop&crop=face',
            'bio': 'Minimalist lifestyle advocate and conscious consumer'
        }
    ]
    
    users = []
    for i, user_data in enumerate(user_profiles[:count]):
        user = User(
            email=user_data['email'],
            username=user_data['username'],
            password=generate_password_hash(user_data['password']),
            avatar=user_data['avatar']
        )
        users.append(user)
        db.session.add(user)
        
        # Add some delay to simulate real-time generation
        time.sleep(0.1)
    
    db.session.commit()
    print(f"✅ Created {len(users)} realistic users")
    return users

def create_realistic_products(users, count=40):
    """Create realistic products with proper titles and descriptions"""
    print(f"📦 Creating {count} realistic products...")
    
    products = []
    categories = list(dynamic_service.categories.keys())
    
    for i in range(count):
        # Select random category
        category = random.choice(categories)
        
        # Generate realistic product
        product_data = dynamic_service.generate_dynamic_product(category)
        
        # Select random user as owner
        owner = random.choice(users)
        
        product = Product(
            title=product_data['title'],
            description=product_data['description'],
            category=product_data['category'],
            price=product_data['price'],
            image=product_data['image'],
            user_id=owner.id
        )
        products.append(product)
        db.session.add(product)
        
        # Add some delay to simulate real-time generation
        time.sleep(0.2)
        
        # Update progress
        if (i + 1) % 10 == 0:
            print(f"   Generated {i + 1}/{count} realistic products...")
    
    db.session.commit()
    print(f"✅ Created {len(products)} realistic products")
    return products

def create_realistic_cart_items(users, products):
    """Create realistic cart items for demo"""
    print("🛒 Creating realistic cart items...")
    
    cart_items = []
    
    # Create carts for multiple users
    for user in users[:3]:  # First 3 users get cart items
        # Random number of items per user
        item_count = random.randint(1, 4)
        user_products = random.sample(products, min(item_count, len(products)))
        
        for product in user_products:
            cart_item = Cart(user_id=user.id, product_id=product.id)
            cart_items.append(cart_item)
            db.session.add(cart_item)
    
    db.session.commit()
    print(f"✅ Created {len(cart_items)} realistic cart items")
    return cart_items

def create_realistic_purchases(users, products):
    """Create realistic purchase history"""
    print("📜 Creating realistic purchase history...")
    
    purchases = []
    
    # Create purchases for multiple users
    for user in users[:4]:  # First 4 users get purchase history
        # Random number of purchases per user
        purchase_count = random.randint(2, 6)
        user_products = random.sample(products, min(purchase_count, len(products)))
        
        for product in user_products:
            # Random purchase date in the past
            days_ago = random.randint(1, 90)
            purchase_date = datetime.now() - timedelta(days=days_ago)
            
            purchase = Purchase(user_id=user.id, product_id=product.id)
            purchase.created_at = purchase_date
            purchases.append(purchase)
            db.session.add(purchase)
    
    db.session.commit()
    print(f"✅ Created {len(purchases)} realistic purchases")
    return purchases

def main():
    """Main function to seed the database with realistic data"""
    print("🌱 EcoFinds Realistic Database Seeding")
    print("=" * 50)
    print("🎯 Creating realistic products with matching images")
    print("=" * 50)
    
    with app.app_context():
        # Clear existing data
        print("🧹 Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # Create realistic data
        print("\n👥 Creating realistic users...")
        users = create_realistic_users(8)
        
        print("\n📦 Creating realistic products...")
        products = create_realistic_products(users, 40)
        
        print("\n🛒 Creating realistic cart items...")
        cart_items = create_realistic_cart_items(users, products)
        
        print("\n📜 Creating realistic purchases...")
        purchases = create_realistic_purchases(users, products)
        
        print("\n✅ Realistic database seeding completed!")
        print(f"\n📊 Summary:")
        print(f"   - Users: {len(users)}")
        print(f"   - Products: {len(products)}")
        print(f"   - Cart Items: {len(cart_items)}")
        print(f"   - Purchases: {len(purchases)}")
        print(f"   - Categories: {len(set(p.category for p in products))}")
        
        # Show product examples
        print(f"\n🛍️ Sample Products:")
        for product in products[:5]:
            print(f"   - {product.title} (${product.price})")
        
        print(f"\n🚀 You can now run the application:")
        print(f"   python app.py")
        print(f"\n🌐 Then visit: http://localhost:5000")
        print(f"\n👤 Demo login credentials:")
        print(f"   Email: {users[0].email}")
        print(f"   Password: password123")
        
        print(f"\n🎯 Realistic Features:")
        print(f"   ✅ Product names match images")
        print(f"   ✅ Detailed, realistic descriptions")
        print(f"   ✅ Proper pricing and conditions")
        print(f"   ✅ Realistic user profiles")
        print(f"   ✅ Professional product listings")

if __name__ == '__main__':
    main()
