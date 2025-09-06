#!/usr/bin/env python3
"""
EcoFinds Setup Script
Automatically sets up the database with sample data
"""

import os
import sys
import subprocess

def main():
    print("🌱 EcoFinds Setup Script")
    print("=" * 40)
    
    # Check if Python is available
    try:
        import flask
        import sqlalchemy
        print("✅ Required packages are installed")
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return
    
    # Run the seeding script
    print("\n📦 Populating database with sample data...")
    try:
        result = subprocess.run([sys.executable, "seed_database.py"], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print("Warnings:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error seeding database: {e}")
        print("Please run manually: python seed_database.py")
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\n🚀 To start the application:")
    print("   python app.py")
    print("\n🌐 Then visit: http://localhost:5000")
    print("\n👤 Demo login credentials:")
    print("   Email: sarah.green@example.com")
    print("   Password: password123")

if __name__ == '__main__':
    main()
