#!/usr/bin/env python3
"""
EcoFinds Dynamic Data Service
Real-time data integration for sustainable marketplace
"""

import os
import requests
import random
import time
from datetime import datetime, timedelta
from faker import Faker
from typing import Dict, List, Optional
import json

class DynamicDataService:
    """Service for generating and managing dynamic marketplace data"""
    
    def __init__(self):
        self.fake = Faker()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'EcoFinds-Marketplace/1.0'
        })
        
        # API configurations
        self.unsplash_access_key = os.getenv('UNSPLASH_ACCESS_KEY', 'demo_key')
        self.currency_api_key = os.getenv('CURRENCY_API_KEY', 'demo_key')
        
        # Cache for API responses
        self.cache = {
            'images': {},
            'prices': {},
            'weather': {},
            'last_update': None
        }
        
        # Sustainable product categories with real-time relevance
        self.categories = {
            'Electronics': {
                'keywords': ['sustainable', 'eco-friendly', 'recycled', 'energy-efficient'],
                'base_price_range': (50, 2000),
                'trending': True
            },
            'Clothing': {
                'keywords': ['vintage', 'organic', 'sustainable', 'ethical', 'second-hand'],
                'base_price_range': (10, 500),
                'trending': True
            },
            'Home & Garden': {
                'keywords': ['bamboo', 'organic', 'eco-friendly', 'sustainable', 'zero-waste'],
                'base_price_range': (5, 300),
                'trending': False
            },
            'Books': {
                'keywords': ['sustainability', 'environment', 'zero-waste', 'eco-living'],
                'base_price_range': (5, 50),
                'trending': False
            },
            'Sports': {
                'keywords': ['eco-friendly', 'sustainable', 'outdoor', 'fitness'],
                'base_price_range': (20, 400),
                'trending': True
            },
            'Beauty': {
                'keywords': ['organic', 'natural', 'cruelty-free', 'sustainable'],
                'base_price_range': (5, 100),
                'trending': True
            },
            'Furniture': {
                'keywords': ['vintage', 'recycled', 'sustainable', 'upcycled'],
                'base_price_range': (50, 1500),
                'trending': False
            },
            'Toys': {
                'keywords': ['wooden', 'eco-friendly', 'sustainable', 'educational'],
                'base_price_range': (10, 200),
                'trending': False
            }
        }
    
    def get_unsplash_image(self, category: str, keywords: List[str]) -> str:
        """Fetch real-time images from Unsplash API"""
        try:
            # Create search query
            query = f"{category} {' '.join(keywords[:2])} sustainable eco-friendly"
            
            # Check cache first
            cache_key = f"{category}_{query}"
            if cache_key in self.cache['images']:
                return self.cache['images'][cache_key]
            
            # Make API request
            url = "https://api.unsplash.com/search/photos"
            params = {
                'query': query,
                'per_page': 10,
                'orientation': 'landscape',
                'client_id': self.unsplash_access_key
            }
            
            response = self.session.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    # Select random image from results
                    image = random.choice(data['results'])
                    image_url = image['urls']['regular']
                    
                    # Cache the result
                    self.cache['images'][cache_key] = image_url
                    return image_url
            
        except Exception as e:
            print(f"Unsplash API error: {e}")
        
        # Fallback to placeholder
        return f"https://picsum.photos/400/300?random={hash(category + str(time.time()))}"
    
    def get_dynamic_pricing(self, category: str, base_price: float) -> float:
        """Calculate dynamic pricing based on market conditions"""
        try:
            # Simulate real-time market fluctuations
            market_multiplier = random.uniform(0.8, 1.3)
            
            # Category-specific trends
            if category in ['Electronics', 'Clothing']:
                market_multiplier *= random.uniform(0.9, 1.2)  # Higher demand
            
            # Time-based pricing (weekend vs weekday)
            now = datetime.now()
            if now.weekday() >= 5:  # Weekend
                market_multiplier *= 1.1
            
            # Seasonal adjustments
            month = now.month
            if category == 'Clothing' and month in [3, 4, 9, 10]:  # Spring/Fall
                market_multiplier *= 1.15
            
            return round(base_price * market_multiplier, 2)
            
        except Exception as e:
            print(f"Pricing calculation error: {e}")
            return base_price
    
    def get_weather_influence(self) -> Dict:
        """Get weather data to influence product availability"""
        try:
            # Simulate weather-based product trends
            weather_conditions = ['sunny', 'rainy', 'cloudy', 'snowy']
            current_weather = random.choice(weather_conditions)
            
            # Weather influences product availability
            weather_impact = {
                'sunny': {'outdoor_gear': 1.3, 'indoor_items': 0.9},
                'rainy': {'indoor_items': 1.2, 'outdoor_gear': 0.8},
                'cloudy': {'neutral': 1.0},
                'snowy': {'winter_gear': 1.4, 'summer_items': 0.7}
            }
            
            return weather_impact.get(current_weather, {'neutral': 1.0})
            
        except Exception as e:
            print(f"Weather API error: {e}")
            return {'neutral': 1.0}
    
    def generate_dynamic_product(self, category: str) -> Dict:
        """Generate a dynamic product with real-time data"""
        try:
            category_info = self.categories.get(category, self.categories['Clothing'])
            
            # Generate dynamic title
            title_templates = [
                f"Eco-Friendly {self.fake.word().title()} {category}",
                f"Sustainable {self.fake.word().title()} for {self.fake.word().title()}",
                f"Vintage {self.fake.word().title()} {category}",
                f"Organic {self.fake.word().title()} {category}",
                f"Zero-Waste {self.fake.word().title()} {category}"
            ]
            
            title = random.choice(title_templates)
            
            # Generate dynamic description
            description = self._generate_sustainable_description(category, category_info['keywords'])
            
            # Calculate dynamic pricing
            base_price = random.uniform(*category_info['base_price_range'])
            dynamic_price = self.get_dynamic_pricing(category, base_price)
            
            # Get real-time image
            image_url = self.get_unsplash_image(category, category_info['keywords'])
            
            # Generate dynamic availability
            availability = self._generate_availability_status()
            
            # Calculate environmental impact
            eco_impact = self._calculate_eco_impact(category, dynamic_price)
            
            return {
                'title': title,
                'description': description,
                'category': category,
                'price': dynamic_price,
                'image': image_url,
                'availability': availability,
                'eco_impact': eco_impact,
                'trending': category_info['trending'],
                'created_at': datetime.now()
            }
            
        except Exception as e:
            print(f"Product generation error: {e}")
            return self._get_fallback_product(category)
    
    def _generate_sustainable_description(self, category: str, keywords: List[str]) -> str:
        """Generate realistic sustainable product descriptions"""
        descriptions = {
            'Electronics': [
                f"Energy-efficient {category.lower()} designed for sustainability. {random.choice(keywords).title()} technology reduces environmental impact while maintaining high performance.",
                f"Refurbished {category.lower()} with eco-friendly packaging. Perfect for conscious consumers who value both quality and sustainability.",
                f"Modular {category.lower()} designed for easy repair and upgrade. Reduces e-waste and promotes circular economy principles."
            ],
            'Clothing': [
                f"Vintage {category.lower()} made from {random.choice(['organic cotton', 'recycled materials', 'sustainable fibers'])}. Timeless design that never goes out of style.",
                f"Ethically produced {category.lower()} from {random.choice(['fair-trade', 'sustainable', 'eco-conscious'])} manufacturers. Perfect for the conscious consumer.",
                f"Upcycled {category.lower()} giving new life to pre-loved materials. Unique piece with a story to tell."
            ],
            'Home & Garden': [
                f"Bamboo {category.lower()} set for eco-friendly living. {random.choice(keywords).title()} materials promote sustainable home practices.",
                f"Zero-waste {category.lower()} designed to minimize environmental impact. Perfect for the modern sustainable home.",
                f"Organic {category.lower()} collection for conscious living. Made from {random.choice(['renewable', 'biodegradable', 'sustainable'])} materials."
            ]
        }
        
        category_descriptions = descriptions.get(category, descriptions['Clothing'])
        return random.choice(category_descriptions)
    
    def _generate_availability_status(self) -> str:
        """Generate dynamic availability status"""
        statuses = ['In Stock', 'Limited Stock', 'Almost Gone', 'New Arrival']
        weights = [0.6, 0.2, 0.15, 0.05]  # Weighted random selection
        return random.choices(statuses, weights=weights)[0]
    
    def _calculate_eco_impact(self, category: str, price: float) -> Dict:
        """Calculate real-time environmental impact"""
        # Base CO2 savings by category
        co2_savings = {
            'Electronics': random.uniform(50, 200),
            'Clothing': random.uniform(10, 50),
            'Home & Garden': random.uniform(5, 30),
            'Books': random.uniform(1, 10),
            'Sports': random.uniform(15, 60),
            'Beauty': random.uniform(2, 15),
            'Furniture': random.uniform(30, 150),
            'Toys': random.uniform(5, 25)
        }
        
        base_co2 = co2_savings.get(category, 20)
        
        # Price-based adjustment
        price_factor = min(price / 100, 3.0)  # Cap at 3x
        co2_saved = base_co2 * price_factor
        
        return {
            'co2_saved': round(co2_saved, 2),
            'water_saved': round(co2_saved * 0.5, 2),
            'waste_diverted': round(co2_saved * 0.3, 2),
            'renewable_energy': round(co2_saved * 0.8, 2)
        }
    
    def _get_fallback_product(self, category: str) -> Dict:
        """Fallback product if dynamic generation fails"""
        return {
            'title': f"Sustainable {category} Item",
            'description': f"Eco-friendly {category.lower()} for conscious consumers.",
            'category': category,
            'price': random.uniform(10, 100),
            'image': f"https://picsum.photos/400/300?random={hash(category)}",
            'availability': 'In Stock',
            'eco_impact': {'co2_saved': 25, 'water_saved': 12.5, 'waste_diverted': 7.5, 'renewable_energy': 20},
            'trending': False,
            'created_at': datetime.now()
        }
    
    def generate_dynamic_user(self) -> Dict:
        """Generate dynamic user profile with realistic data"""
        try:
            # Generate realistic user data
            first_name = self.fake.first_name()
            last_name = self.fake.last_name()
            username = f"{first_name}{last_name}{random.randint(10, 99)}"
            
            # Generate sustainable interests
            interests = random.sample([
                'Zero Waste Living', 'Sustainable Fashion', 'Eco-Friendly Home',
                'Renewable Energy', 'Organic Gardening', 'Minimalism',
                'Circular Economy', 'Green Technology', 'Ethical Shopping'
            ], random.randint(2, 4))
            
            # Generate eco-friendly bio
            bio_templates = [
                f"Passionate about {', '.join(interests[:2])}. Building a sustainable future, one purchase at a time.",
                f"Eco-conscious consumer focused on {', '.join(interests[:2])}. Love finding quality second-hand items.",
                f"Sustainability advocate interested in {', '.join(interests[:2])}. Committed to reducing environmental impact."
            ]
            
            bio = random.choice(bio_templates)
            
            # Generate avatar from Unsplash
            avatar_url = self.get_unsplash_image('portrait', ['person', 'profile', 'avatar'])
            
            return {
                'email': f"{username.lower()}@ecofinds.com",
                'username': username,
                'password': 'password123',  # Default for demo
                'avatar': avatar_url,
                'bio': bio,
                'interests': interests,
                'member_since': self.fake.date_between(start_date='-2y', end_date='today'),
                'eco_score': random.randint(70, 100)
            }
            
        except Exception as e:
            print(f"User generation error: {e}")
            return {
                'email': f"user{random.randint(1000, 9999)}@ecofinds.com",
                'username': f"user{random.randint(1000, 9999)}",
                'password': 'password123',
                'avatar': 'https://picsum.photos/150/150?random=avatar',
                'bio': 'Eco-conscious consumer',
                'interests': ['Sustainability'],
                'member_since': datetime.now().date(),
                'eco_score': 80
            }
    
    def get_trending_categories(self) -> List[str]:
        """Get currently trending categories based on real-time data"""
        # Simulate trending analysis
        trending = []
        for category, info in self.categories.items():
            if info['trending'] and random.random() > 0.3:
                trending.append(category)
        
        return trending or ['Clothing', 'Electronics', 'Beauty']
    
    def update_cache(self):
        """Update cached data periodically"""
        self.cache['last_update'] = datetime.now()
        # Clear old cache entries
        if len(self.cache['images']) > 100:
            self.cache['images'] = dict(list(self.cache['images'].items())[-50:])
    
    def get_market_insights(self) -> Dict:
        """Get real-time market insights"""
        return {
            'trending_categories': self.get_trending_categories(),
            'average_price_change': random.uniform(-0.05, 0.05),
            'new_listings_today': random.randint(5, 25),
            'eco_impact_total': {
                'co2_saved': random.randint(1000, 5000),
                'items_recycled': random.randint(500, 2000),
                'users_active': random.randint(50, 200)
            },
            'last_updated': datetime.now().isoformat()
        }

# Global instance
dynamic_service = DynamicDataService()
