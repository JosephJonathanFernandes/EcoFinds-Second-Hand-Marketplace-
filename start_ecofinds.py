#!/usr/bin/env python3
"""
EcoFinds Complete Startup Script
Starts the application with dynamic data and real-time updates
"""

import os
import sys
import subprocess
import threading
import time
from datetime import datetime

def print_banner():
    """Print startup banner"""
    print("🌱" + "="*60 + "🌱")
    print("🚀 EcoFinds - Sustainable Second-Hand Marketplace")
    print("🌱" + "="*60 + "🌱")
    print("📊 Real-time Data Integration Active")
    print("🔄 Dynamic Product Generation Enabled")
    print("⚡ Live Market Updates Running")
    print("🌱" + "="*60 + "🌱")
    print()

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'flask', 'flask_sqlalchemy', 'flask_login', 
        'werkzeug', 'requests', 'faker', 'schedule'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("📦 Installing missing packages...")
        
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing_packages, 
                          check=True, capture_output=True)
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    else:
        print("✅ All dependencies are installed!")
    
    return True

def setup_database():
    """Set up the database with dynamic data"""
    print("\n🗄️ Setting up database with dynamic data...")
    
    try:
        # Run dynamic seeding
        result = subprocess.run([sys.executable, 'dynamic_seed_database.py'], 
                              capture_output=True, text=True, check=True)
        print("✅ Database populated with dynamic data!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Database setup failed: {e}")
        print("🔄 Trying fallback seeding...")
        
        try:
            # Try fallback seeding
            result = subprocess.run([sys.executable, 'seed_database.py'], 
                                  capture_output=True, text=True, check=True)
            print("✅ Database populated with fallback data!")
            return True
        except subprocess.CalledProcessError as e2:
            print(f"❌ Fallback seeding also failed: {e2}")
            return False

def start_realtime_updater():
    """Start the real-time updater in background"""
    print("\n🔄 Starting real-time updater...")
    
    try:
        # Start real-time updater in background
        updater_process = subprocess.Popen([sys.executable, 'realtime_updater.py'])
        print("✅ Real-time updater started!")
        return updater_process
    except Exception as e:
        print(f"⚠️ Real-time updater failed to start: {e}")
        print("   Application will run without real-time updates")
        return None

def start_application():
    """Start the main Flask application"""
    print("\n🚀 Starting EcoFinds application...")
    print("🌐 Application will be available at: http://localhost:5000")
    print("\n👤 Demo login credentials:")
    print("   Email: sarah.green@example.com")
    print("   Password: password123")
    print("\n🎯 Real-time Features:")
    print("   ✅ Dynamic product generation")
    print("   ✅ Live price updates")
    print("   ✅ Real-time market insights")
    print("   ✅ Trending categories")
    print("   ✅ Environmental impact tracking")
    print("\n" + "="*60)
    print("🎉 EcoFinds is ready for your hackathon presentation!")
    print("="*60)
    print("\nPress Ctrl+C to stop the application")
    print()
    
    try:
        # Start the Flask app
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n🛑 Shutting down EcoFinds...")
        print("✅ Application stopped successfully!")

def main():
    """Main startup function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed. Please install requirements manually:")
        print("   pip install -r requirements.txt")
        return
    
    # Setup database
    if not setup_database():
        print("❌ Database setup failed. Please check the error messages above.")
        return
    
    # Start real-time updater
    updater_process = start_realtime_updater()
    
    try:
        # Start the main application
        start_application()
    finally:
        # Clean up background processes
        if updater_process:
            print("\n🛑 Stopping real-time updater...")
            updater_process.terminate()
            updater_process.wait()
            print("✅ Real-time updater stopped!")

if __name__ == '__main__':
    main()
