#!/usr/bin/env python3
"""
Test script to verify image handling improvements
"""

import os
import sys
import requests
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Product
from dynamic_data_service import dynamic_service

def test_image_urls():
    """Test if image URLs are accessible"""
    print("🖼️ Testing Image URL Accessibility")
    print("=" * 50)
    
    with app.app_context():
        products = Product.query.limit(10).all()
        
        if not products:
            print("❌ No products found. Run seeding script first.")
            return
        
        working_images = 0
        failed_images = 0
        
        for i, product in enumerate(products, 1):
            print(f"\n{i}. Testing: {product.title}")
            print(f"   URL: {product.image}")
            
            try:
                response = requests.head(product.image, timeout=10)
                if response.status_code == 200:
                    print(f"   ✅ Status: {response.status_code}")
                    working_images += 1
                else:
                    print(f"   ❌ Status: {response.status_code}")
                    failed_images += 1
            except Exception as e:
                print(f"   ❌ Error: {str(e)[:50]}...")
                failed_images += 1
        
        print(f"\n📊 Results:")
        print(f"   ✅ Working images: {working_images}")
        print(f"   ❌ Failed images: {failed_images}")
        print(f"   📈 Success rate: {(working_images / (working_images + failed_images)) * 100:.1f}%")

def test_fallback_images():
    """Test fallback image generation"""
    print("\n🔄 Testing Fallback Image Generation")
    print("=" * 50)
    
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Books', 'Sports']
    
    for category in categories:
        print(f"\n{category}:")
        
        # Test with product title
        test_titles = [
            f"MacBook Pro 13\" (2020) - Excellent Condition",
            f"Vintage Levi's 501 Jeans - Size 32",
            f"Bamboo Kitchen Utensil Set (6 Pieces)",
            f"Zero Waste Living Guide - Book Collection",
            f"Eco-Friendly Cork Yoga Mat"
        ]
        
        for title in test_titles:
            if category.lower() in title.lower() or 'macbook' in title.lower():
                fallback_url = dynamic_service._get_reliable_fallback_image(category, title)
                print(f"   {title[:30]}... -> {fallback_url[:50]}...")
                break

def test_dynamic_generation():
    """Test dynamic product generation"""
    print("\n🎯 Testing Dynamic Product Generation")
    print("=" * 50)
    
    categories = ['Electronics', 'Clothing', 'Home & Garden']
    
    for category in categories:
        print(f"\n{category}:")
        product_data = dynamic_service.generate_dynamic_product(category)
        
        print(f"   Title: {product_data['title']}")
        print(f"   Image: {product_data['image'][:50]}...")
        print(f"   Price: ${product_data['price']}")
        print(f"   Description: {product_data['description'][:80]}...")

def main():
    """Main test function"""
    print("🧪 EcoFinds Image Testing Suite")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Test image URLs
    test_image_urls()
    
    # Test fallback images
    test_fallback_images()
    
    # Test dynamic generation
    test_dynamic_generation()
    
    print("\n✅ Image testing completed!")
    print("\n💡 If images are failing:")
    print("   1. Check internet connection")
    print("   2. Run: python realistic_seed_database.py")
    print("   3. Check browser console for errors")
    print("   4. Images should fallback to reliable Unsplash URLs")

if __name__ == '__main__':
    main()
