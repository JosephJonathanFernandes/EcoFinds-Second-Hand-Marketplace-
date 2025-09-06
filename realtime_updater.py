#!/usr/bin/env python3
"""
EcoFinds Real-time Data Updater
Background service for live data updates
"""

import os
import sys
import time
import schedule
import threading
from datetime import datetime
import random

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Product, User
from dynamic_data_service import dynamic_service

class RealTimeUpdater:
    """Real-time data updater service"""
    
    def __init__(self):
        self.running = False
        self.update_interval = 300  # 5 minutes
        self.last_update = None
        
    def start(self):
        """Start the real-time updater"""
        print("🚀 Starting EcoFinds Real-time Updater...")
        self.running = True
        
        # Schedule updates
        schedule.every(5).minutes.do(self.update_prices)
        schedule.every(10).minutes.do(self.update_availability)
        schedule.every(15).minutes.do(self.add_new_products)
        schedule.every(30).minutes.do(self.update_trending)
        schedule.every(1).hours.do(self.full_market_update)
        
        # Start the scheduler in a separate thread
        self.scheduler_thread = threading.Thread(target=self._run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        
        print("✅ Real-time updater started successfully!")
        print("   - Price updates every 5 minutes")
        print("   - Availability updates every 10 minutes")
        print("   - New products every 15 minutes")
        print("   - Trending updates every 30 minutes")
        print("   - Full market update every hour")
    
    def stop(self):
        """Stop the real-time updater"""
        print("🛑 Stopping EcoFinds Real-time Updater...")
        self.running = False
        schedule.clear()
    
    def _run_scheduler(self):
        """Run the scheduler in a separate thread"""
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def update_prices(self):
        """Update product prices based on market conditions"""
        try:
            with app.app_context():
                products = Product.query.all()
                updated_count = 0
                
                for product in products:
                    # 20% chance to update each product's price
                    if random.random() < 0.2:
                        old_price = product.price
                        new_price = dynamic_service.get_dynamic_pricing(
                            product.category, old_price
                        )
                        product.price = new_price
                        updated_count += 1
                
                if updated_count > 0:
                    db.session.commit()
                    print(f"💰 Updated {updated_count} product prices at {datetime.now().strftime('%H:%M:%S')}")
                
        except Exception as e:
            print(f"❌ Price update error: {e}")
    
    def update_availability(self):
        """Update product availability status"""
        try:
            with app.app_context():
                products = Product.query.all()
                updated_count = 0
                
                for product in products:
                    # 15% chance to update availability
                    if random.random() < 0.15:
                        # Simulate availability changes
                        statuses = ['In Stock', 'Limited Stock', 'Almost Gone', 'New Arrival']
                        weights = [0.6, 0.2, 0.15, 0.05]
                        new_status = random.choices(statuses, weights=weights)[0]
                        
                        # Store availability in description for now
                        # In a real app, you'd have an availability field
                        if 'Availability:' not in product.description:
                            product.description += f"\n\nAvailability: {new_status}"
                        else:
                            # Update existing availability
                            lines = product.description.split('\n')
                            for i, line in enumerate(lines):
                                if line.startswith('Availability:'):
                                    lines[i] = f"Availability: {new_status}"
                                    break
                            product.description = '\n'.join(lines)
                        
                        updated_count += 1
                
                if updated_count > 0:
                    db.session.commit()
                    print(f"📦 Updated {updated_count} product availability at {datetime.now().strftime('%H:%M:%S')}")
                
        except Exception as e:
            print(f"❌ Availability update error: {e}")
    
    def add_new_products(self):
        """Add new products to the marketplace"""
        try:
            with app.app_context():
                # Get random users to be product owners
                users = User.query.all()
                if not users:
                    return
                
                # Add 1-3 new products
                new_count = random.randint(1, 3)
                categories = list(dynamic_service.categories.keys())
                
                for _ in range(new_count):
                    category = random.choice(categories)
                    product_data = dynamic_service.generate_dynamic_product(category)
                    owner = random.choice(users)
                    
                    product = Product(
                        title=product_data['title'],
                        description=product_data['description'],
                        category=product_data['category'],
                        price=product_data['price'],
                        image=product_data['image'],
                        user_id=owner.id
                    )
                    db.session.add(product)
                
                db.session.commit()
                print(f"🆕 Added {new_count} new products at {datetime.now().strftime('%H:%M:%S')}")
                
        except Exception as e:
            print(f"❌ New product addition error: {e}")
    
    def update_trending(self):
        """Update trending categories and products"""
        try:
            with app.app_context():
                # Get trending categories
                trending = dynamic_service.get_trending_categories()
                
                # Update cache
                dynamic_service.update_cache()
                
                print(f"📈 Updated trending categories: {', '.join(trending)} at {datetime.now().strftime('%H:%M:%S')}")
                
        except Exception as e:
            print(f"❌ Trending update error: {e}")
    
    def full_market_update(self):
        """Perform a full market update"""
        try:
            with app.app_context():
                # Get market insights
                insights = dynamic_service.get_market_insights()
                
                # Update some products with fresh data
                products = Product.query.all()
                updated_count = 0
                
                for product in random.sample(products, min(5, len(products))):
                    new_data = dynamic_service.generate_dynamic_product(product.category)
                    product.title = new_data['title']
                    product.description = new_data['description']
                    product.price = new_data['price']
                    product.image = new_data['image']
                    updated_count += 1
                
                db.session.commit()
                
                print(f"🔄 Full market update completed at {datetime.now().strftime('%H:%M:%S')}")
                print(f"   - Updated {updated_count} products")
                print(f"   - New listings today: {insights['new_listings_today']}")
                print(f"   - Total CO2 saved: {insights['eco_impact_total']['co2_saved']} kg")
                
        except Exception as e:
            print(f"❌ Full market update error: {e}")
    
    def get_status(self):
        """Get updater status"""
        return {
            'running': self.running,
            'last_update': self.last_update,
            'next_update': schedule.next_run(),
            'scheduled_jobs': len(schedule.jobs)
        }

# Global updater instance
updater = RealTimeUpdater()

def start_realtime_updates():
    """Start real-time updates"""
    updater.start()

def stop_realtime_updates():
    """Stop real-time updates"""
    updater.stop()

if __name__ == '__main__':
    # Start the updater
    start_realtime_updates()
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping real-time updater...")
        stop_realtime_updates()
        print("✅ Real-time updater stopped.")
