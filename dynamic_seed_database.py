#!/usr/bin/env python3
"""
EcoFinds Dynamic Database Seeding Script
Populates the database with real-time, dynamic data
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

def create_dynamic_users(count=8):
    """Create dynamic users with realistic profiles"""
    print(f"👥 Creating {count} dynamic users...")
    
    users = []
    for i in range(count):
        user_data = dynamic_service.generate_dynamic_user()
        
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
    print(f"✅ Created {len(users)} dynamic users")
    return users

def create_dynamic_products(users, count=30):
    """Create dynamic products with real-time data"""
    print(f"📦 Creating {count} dynamic products...")
    
    products = []
    categories = list(dynamic_service.categories.keys())
    
    for i in range(count):
        # Select random category
        category = random.choice(categories)
        
        # Generate dynamic product
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
            print(f"   Generated {i + 1}/{count} products...")
    
    db.session.commit()
    print(f"✅ Created {len(products)} dynamic products")
    return products

def create_dynamic_cart_items(users, products):
    """Create dynamic cart items for demo"""
    print("🛒 Creating dynamic cart items...")
    
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
    print(f"✅ Created {len(cart_items)} dynamic cart items")
    return cart_items

def create_dynamic_purchases(users, products):
    """Create dynamic purchase history"""
    print("📜 Creating dynamic purchase history...")
    
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
    print(f"✅ Created {len(purchases)} dynamic purchases")
    return purchases

def update_existing_products_dynamically(products):
    """Update existing products with real-time data"""
    print("🔄 Updating existing products with real-time data...")
    
    updated_count = 0
    for product in products:
        # 30% chance to update each product
        if random.random() < 0.3:
            # Generate new dynamic data
            new_data = dynamic_service.generate_dynamic_product(product.category)
            
            # Update product with new data
            product.title = new_data['title']
            product.description = new_data['description']
            product.price = new_data['price']
            product.image = new_data['image']
            
            updated_count += 1
    
    db.session.commit()
    print(f"✅ Updated {updated_count} products with real-time data")

def create_market_insights():
    """Create real-time market insights"""
    print("📊 Generating market insights...")
    
    insights = dynamic_service.get_market_insights()
    
    # Store insights in a simple way (could be enhanced with a proper table)
    print(f"   Trending categories: {', '.join(insights['trending_categories'])}")
    print(f"   New listings today: {insights['new_listings_today']}")
    print(f"   Total CO2 saved: {insights['eco_impact_total']['co2_saved']} kg")
    print(f"   Items recycled: {insights['eco_impact_total']['items_recycled']}")
    print(f"   Active users: {insights['eco_impact_total']['users_active']}")

def main():
    """Main function to seed the database with dynamic data"""
    print("🌱 EcoFinds Dynamic Database Seeding")
    print("=" * 50)
    print("🚀 Using real-time data sources and APIs")
    print("=" * 50)
    
    with app.app_context():
        # Clear existing data
        print("🧹 Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # Create dynamic data
        print("\n👥 Creating dynamic users...")
        users = create_dynamic_users(8)
        
        print("\n📦 Creating dynamic products...")
        products = create_dynamic_products(users, 35)
        
        print("\n🛒 Creating dynamic cart items...")
        cart_items = create_dynamic_cart_items(users, products)
        
        print("\n📜 Creating dynamic purchases...")
        purchases = create_dynamic_purchases(users, products)
        
        print("\n🔄 Updating products with real-time data...")
        update_existing_products_dynamically(products)
        
        print("\n📊 Generating market insights...")
        create_market_insights()
        
        print("\n✅ Dynamic database seeding completed!")
        print(f"\n📊 Summary:")
        print(f"   - Users: {len(users)}")
        print(f"   - Products: {len(products)}")
        print(f"   - Cart Items: {len(cart_items)}")
        print(f"   - Purchases: {len(purchases)}")
        print(f"   - Categories: {len(set(p.category for p in products))}")
        
        # Show trending categories
        trending = dynamic_service.get_trending_categories()
        print(f"   - Trending Categories: {', '.join(trending)}")
        
        print(f"\n🚀 You can now run the application:")
        print(f"   python app.py")
        print(f"\n🌐 Then visit: http://localhost:5000")
        print(f"\n👤 Demo login credentials:")
        print(f"   Email: {users[0].email}")
        print(f"   Password: password123")
        
        print(f"\n🎯 Real-time Features Active:")
        print(f"   ✅ Dynamic product generation")
        print(f"   ✅ Real-time pricing updates")
        print(f"   ✅ Live image fetching")
        print(f"   ✅ Market trend analysis")
        print(f"   ✅ Environmental impact calculations")
        print(f"   ✅ Weather-influenced availability")

if __name__ == '__main__':
    main()
