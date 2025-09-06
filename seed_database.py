#!/usr/bin/env python3
"""
EcoFinds Database Seeding Script
Populates the database with sample sustainable products and users
"""

import os
import sys
from datetime import datetime, timedelta
import random

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Product, Cart, Purchase
from werkzeug.security import generate_password_hash

def create_sample_users():
    """Create sample users for the marketplace"""
    users_data = [
        {
            'email': 'sarah.green@example.com',
            'username': 'SarahGreen',
            'password': 'password123',
            'avatar': 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face'
        },
        {
            'email': 'eco.mike@example.com',
            'username': 'EcoMike',
            'password': 'password123',
            'avatar': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face'
        },
        {
            'email': 'sustainable.sam@example.com',
            'username': 'SustainableSam',
            'password': 'password123',
            'avatar': 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face'
        },
        {
            'email': 'green.lisa@example.com',
            'username': 'GreenLisa',
            'password': 'password123',
            'avatar': 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150&h=150&fit=crop&crop=face'
        },
        {
            'email': 'recycle.ryan@example.com',
            'username': 'RecycleRyan',
            'password': 'password123',
            'avatar': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face'
        }
    ]
    
    users = []
    for user_data in users_data:
        user = User(
            email=user_data['email'],
            username=user_data['username'],
            password=generate_password_hash(user_data['password']),
            avatar=user_data['avatar']
        )
        users.append(user)
        db.session.add(user)
    
    db.session.commit()
    print(f"✅ Created {len(users)} sample users")
    return users

def create_sample_products(users):
    """Create sample sustainable products"""
    products_data = [
        # Electronics
        {
            'title': 'MacBook Pro 13" (2020) - Excellent Condition',
            'description': 'Perfectly working MacBook Pro with minimal wear. Great for students or professionals. Includes original charger and box. Battery health at 95%.',
            'category': 'Electronics',
            'price': 899.99,
            'image': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=300&fit=crop',
            'owner': users[0]
        },
        {
            'title': 'iPhone 12 Pro - Space Gray',
            'description': 'Well-maintained iPhone 12 Pro with 128GB storage. Screen protector applied since day one. No scratches or dents. Includes case and charger.',
            'category': 'Electronics',
            'price': 649.99,
            'image': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400&h=300&fit=crop',
            'owner': users[1]
        },
        {
            'title': 'Sony WH-1000XM4 Noise-Canceling Headphones',
            'description': 'Premium wireless headphones with industry-leading noise cancellation. Perfect for work from home or travel. Like new condition.',
            'category': 'Electronics',
            'price': 199.99,
            'image': 'https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400&h=300&fit=crop',
            'owner': users[2]
        },
        
        # Clothing & Accessories
        {
            'title': 'Vintage Denim Jacket - Levi\'s',
            'description': 'Classic vintage Levi\'s denim jacket from the 90s. Perfect fit and authentic vintage look. Great for sustainable fashion enthusiasts.',
            'category': 'Clothing',
            'price': 45.99,
            'image': 'https://images.unsplash.com/photo-1551028719-001c2b5d2ac3?w=400&h=300&fit=crop',
            'owner': users[3]
        },
        {
            'title': 'Organic Cotton T-Shirt Collection (5 Pack)',
            'description': 'Set of 5 organic cotton t-shirts in various colors. Soft, comfortable, and eco-friendly. Perfect for everyday wear.',
            'category': 'Clothing',
            'price': 29.99,
            'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=300&fit=crop',
            'owner': users[0]
        },
        {
            'title': 'Vintage Leather Handbag - Coach',
            'description': 'Authentic vintage Coach leather handbag in excellent condition. Timeless design that never goes out of style.',
            'category': 'Clothing',
            'price': 89.99,
            'image': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=300&fit=crop',
            'owner': users[4]
        },
        
        # Home & Garden
        {
            'title': 'Bamboo Kitchen Utensil Set',
            'description': 'Complete set of bamboo kitchen utensils - eco-friendly alternative to plastic. Includes spoons, spatulas, and tongs.',
            'category': 'Home & Garden',
            'price': 24.99,
            'image': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=300&fit=crop',
            'owner': users[1]
        },
        {
            'title': 'Indoor Plant Collection - Succulents',
            'description': 'Beautiful collection of 6 different succulent plants in ceramic pots. Perfect for beginners. Includes care instructions.',
            'category': 'Home & Garden',
            'price': 35.99,
            'image': 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&h=300&fit=crop',
            'owner': users[2]
        },
        {
            'title': 'Vintage Wooden Dining Table',
            'description': 'Solid oak dining table from the 1970s. Seats 6 people comfortably. Some minor wear that adds character. Perfect for sustainable living.',
            'category': 'Furniture',
            'price': 299.99,
            'image': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop',
            'owner': users[3]
        },
        
        # Books & Media
        {
            'title': 'Zero Waste Living Guide - Book Collection',
            'description': 'Collection of 3 books on zero waste living, sustainable fashion, and minimalism. Great for eco-conscious readers.',
            'category': 'Books',
            'price': 19.99,
            'image': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=300&fit=crop',
            'owner': users[4]
        },
        {
            'title': 'Vinyl Record Collection - Classic Rock',
            'description': 'Collection of 10 classic rock vinyl records from the 70s and 80s. All in excellent condition. Perfect for music lovers.',
            'category': 'Books',
            'price': 79.99,
            'image': 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400&h=300&fit=crop',
            'owner': users[0]
        },
        
        # Sports & Fitness
        {
            'title': 'Yoga Mat - Eco-Friendly Cork',
            'description': 'Sustainable cork yoga mat with excellent grip. Non-toxic and biodegradable. Perfect for mindful living and fitness.',
            'category': 'Sports',
            'price': 39.99,
            'image': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=300&fit=crop',
            'owner': users[1]
        },
        {
            'title': 'Vintage Bicycle - Raleigh',
            'description': 'Classic Raleigh bicycle from the 80s. Recently serviced and ready to ride. Perfect for sustainable transportation.',
            'category': 'Sports',
            'price': 149.99,
            'image': 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400&h=300&fit=crop',
            'owner': users[2]
        },
        
        # Toys & Games
        {
            'title': 'Wooden Building Blocks Set',
            'description': 'Eco-friendly wooden building blocks for children. Made from sustainable materials. Great for creative play.',
            'category': 'Toys',
            'price': 34.99,
            'image': 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400&h=300&fit=crop',
            'owner': users[3]
        },
        {
            'title': 'Vintage Board Game Collection',
            'description': 'Collection of 5 classic board games from the 90s. All pieces included and in good condition. Perfect for family game nights.',
            'category': 'Toys',
            'price': 49.99,
            'image': 'https://images.unsplash.com/photo-1606092195730-5d7b9af1efc5?w=400&h=300&fit=crop',
            'owner': users[4]
        },
        
        # Beauty & Health
        {
            'title': 'Organic Skincare Set - All Natural',
            'description': 'Complete organic skincare routine with cleanser, moisturizer, and serum. All products are cruelty-free and sustainable.',
            'category': 'Beauty',
            'price': 59.99,
            'image': 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=400&h=300&fit=crop',
            'owner': users[0]
        },
        {
            'title': 'Bamboo Toothbrush Set (4 Pack)',
            'description': 'Eco-friendly bamboo toothbrushes with biodegradable bristles. Perfect for zero waste lifestyle. Includes travel case.',
            'category': 'Beauty',
            'price': 12.99,
            'image': 'https://images.unsplash.com/photo-1607619056574-7b8d3ee536b2?w=400&h=300&fit=crop',
            'owner': users[1]
        },
        
        # Automotive
        {
            'title': 'Car Phone Mount - Bamboo',
            'description': 'Sustainable bamboo car phone mount. Holds phone securely while driving. Eco-friendly alternative to plastic mounts.',
            'category': 'Automotive',
            'price': 18.99,
            'image': 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400&h=300&fit=crop',
            'owner': users[2]
        },
        
        # More Electronics
        {
            'title': 'iPad Air 4th Gen - Space Gray',
            'description': 'Lightly used iPad Air with 64GB storage. Perfect for students or digital artists. Includes Apple Pencil and case.',
            'category': 'Electronics',
            'price': 449.99,
            'image': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=300&fit=crop',
            'owner': users[3]
        },
        {
            'title': 'Nintendo Switch - Animal Crossing Edition',
            'description': 'Nintendo Switch with Animal Crossing design. Includes the game and extra controllers. Great for family entertainment.',
            'category': 'Electronics',
            'price': 299.99,
            'image': 'https://images.unsplash.com/photo-1606144042614-b2417e743c54?w=400&h=300&fit=crop',
            'owner': users[4]
        },
        
        # More Clothing
        {
            'title': 'Vintage Band T-Shirt Collection',
            'description': 'Collection of 3 vintage band t-shirts from the 90s. Authentic vintage pieces in good condition. Perfect for music lovers.',
            'category': 'Clothing',
            'price': 39.99,
            'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=300&fit=crop',
            'owner': users[0]
        },
        {
            'title': 'Sustainable Sneakers - Allbirds',
            'description': 'Comfortable Allbirds sneakers made from sustainable materials. Worn only a few times. Size 9. Perfect for eco-conscious fashion.',
            'category': 'Clothing',
            'price': 79.99,
            'image': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=300&fit=crop',
            'owner': users[1]
        }
    ]
    
    products = []
    for product_data in products_data:
        product = Product(
            title=product_data['title'],
            description=product_data['description'],
            category=product_data['category'],
            price=product_data['price'],
            image=product_data['image'],
            user_id=product_data['owner'].id
        )
        products.append(product)
        db.session.add(product)
    
    db.session.commit()
    print(f"✅ Created {len(products)} sample products")
    return products

def create_sample_cart_items(users, products):
    """Create some sample cart items for demo purposes"""
    # Add some products to Sarah's cart
    sarah = users[0]
    cart_items = [
        Cart(user_id=sarah.id, product_id=products[1].id),  # iPhone
        Cart(user_id=sarah.id, product_id=products[5].id),  # Handbag
        Cart(user_id=sarah.id, product_id=products[8].id),  # Dining table
    ]
    
    for item in cart_items:
        db.session.add(item)
    
    db.session.commit()
    print(f"✅ Created {len(cart_items)} sample cart items")

def create_sample_purchases(users, products):
    """Create some sample purchase history"""
    # Create some past purchases for Sarah
    sarah = users[0]
    purchases = [
        Purchase(user_id=sarah.id, product_id=products[6].id),  # Bamboo utensils
        Purchase(user_id=sarah.id, product_id=products[10].id), # Vinyl records
        Purchase(user_id=sarah.id, product_id=products[12].id), # Yoga mat
    ]
    
    for purchase in purchases:
        db.session.add(purchase)
    
    db.session.commit()
    print(f"✅ Created {len(purchases)} sample purchases")

def main():
    """Main function to seed the database"""
    print("🌱 EcoFinds Database Seeding Script")
    print("=" * 50)
    
    with app.app_context():
        # Clear existing data
        print("🧹 Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # Create sample data
        print("\n👥 Creating sample users...")
        users = create_sample_users()
        
        print("\n📦 Creating sample products...")
        products = create_sample_products(users)
        
        print("\n🛒 Creating sample cart items...")
        create_sample_cart_items(users, products)
        
        print("\n📜 Creating sample purchases...")
        create_sample_purchases(users, products)
        
        print("\n✅ Database seeding completed successfully!")
        print(f"\n📊 Summary:")
        print(f"   - Users: {len(users)}")
        print(f"   - Products: {len(products)}")
        print(f"   - Categories: {len(set(p.category for p in products))}")
        
        print(f"\n🚀 You can now run the application:")
        print(f"   python app.py")
        print(f"\n🌐 Then visit: http://localhost:5000")
        print(f"\n👤 Demo login credentials:")
        print(f"   Email: sarah.green@example.com")
        print(f"   Password: password123")

if __name__ == '__main__':
    main()
