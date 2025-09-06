#!/usr/bin/env python3
"""
EcoFinds Test Script
Simple functionality tests for the EcoFinds application
"""

import os
import sys
import tempfile
import unittest
from app import app, db, User, Product, Cart, Purchase

class EcoFindsTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test database and client"""
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
            # Create test user
            test_user = User(
                email='test@example.com',
                username='testuser',
                password='hashed_password'
            )
            db.session.add(test_user)
            db.session.commit()
            
            # Create test product
            test_product = Product(
                title='Test Product',
                description='A test product for testing',
                category='Electronics',
                price=99.99,
                image='https://via.placeholder.com/150',
                user_id=1
            )
            db.session.add(test_product)
            db.session.commit()

    def tearDown(self):
        """Clean up after tests"""
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_homepage(self):
        """Test homepage loads correctly"""
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'EcoFinds', rv.data)

    def test_landing_page(self):
        """Test landing page loads correctly"""
        rv = self.app.get('/landing')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Sustainable Shopping', rv.data)

    def test_products_page(self):
        """Test products page loads correctly"""
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Browse Sustainable Finds', rv.data)

    def test_register_page(self):
        """Test registration page loads correctly"""
        rv = self.app.get('/register')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Join EcoFinds', rv.data)

    def test_login_page(self):
        """Test login page loads correctly"""
        rv = self.app.get('/login')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Welcome Back', rv.data)

    def test_user_registration(self):
        """Test user registration functionality"""
        rv = self.app.post('/register', data={
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

    def test_product_creation(self):
        """Test product creation (requires login)"""
        # This would require proper session handling in a real test
        # For now, just test the page loads
        rv = self.app.get('/add_product')
        self.assertEqual(rv.status_code, 302)  # Redirects to login

    def test_search_functionality(self):
        """Test search functionality"""
        rv = self.app.get('/search?q=test')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Search Results', rv.data)

    def test_database_models(self):
        """Test database models work correctly"""
        with app.app_context():
            # Test User model
            user = User.query.filter_by(email='test@example.com').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.username, 'testuser')
            
            # Test Product model
            product = Product.query.filter_by(title='Test Product').first()
            self.assertIsNotNone(product)
            self.assertEqual(product.price, 99.99)
            self.assertEqual(product.category, 'Electronics')

def run_tests():
    """Run all tests"""
    print("🧪 Running EcoFinds Tests...")
    print("=" * 50)
    
    # Run the tests
    unittest.main(verbosity=2, exit=False)
    
    print("\n✅ Tests completed!")
    print("\n🚀 To run the application:")
    print("   python app.py")
    print("\n🌐 Then visit: http://localhost:5000")

if __name__ == '__main__':
    run_tests()
