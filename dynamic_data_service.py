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
    
    def get_unsplash_image(self, category: str, keywords: List[str], product_title: str = "") -> str:
        """Fetch real-time images from Unsplash API with robust fallbacks"""
        try:
            # Create more specific search query based on product title
            if product_title:
                # Extract key terms from product title for better image matching
                title_words = product_title.lower().split()
                key_terms = []
                
                # Look for specific product terms
                for word in title_words:
                    if word in ['macbook', 'iphone', 'ipad', 'nintendo', 'sony', 'samsung', 'dell', 'canon', 'microsoft']:
                        key_terms.append(word)
                    elif word in ['jeans', 'jacket', 'handbag', 'sneakers', 'yoga', 'bicycle', 'tennis', 'golf']:
                        key_terms.append(word)
                    elif word in ['bamboo', 'wooden', 'vintage', 'organic', 'leather', 'cotton']:
                        key_terms.append(word)
                
                if key_terms:
                    query = ' '.join(key_terms[:3]) + f" {category.lower()}"
                else:
                    query = f"{category.lower()} {' '.join(keywords[:2])}"
            else:
                query = f"{category.lower()} {' '.join(keywords[:2])}"
            
            # Check cache first
            cache_key = f"{category}_{query}"
            if cache_key in self.cache['images']:
                return self.cache['images'][cache_key]
            
            # Only try Unsplash if we have a valid access key
            if self.unsplash_access_key and self.unsplash_access_key != 'demo_key':
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
        
        # Use reliable fallback images
        return self._get_reliable_fallback_image(category, product_title)
    
    def _get_reliable_fallback_image(self, category: str, product_title: str = "") -> str:
        """Get reliable fallback images that always work"""
        # High-quality, reliable image sources
        reliable_images = {
            'Electronics': [
                'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=300&fit=crop&crop=center'
            ],
            'Clothing': [
                'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1551028719-001c2b5d2ac3?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=300&fit=crop&crop=center'
            ],
            'Home & Garden': [
                'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop&crop=center'
            ],
            'Books': [
                'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=300&fit=crop&crop=center'
            ],
            'Sports': [
                'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=300&fit=crop&crop=center'
            ],
            'Beauty': [
                'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1607619056574-7b8d3ee536b2?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1607619056574-7b8d3ee536b2?w=400&h=300&fit=crop&crop=center'
            ],
            'Furniture': [
                'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop&crop=center'
            ],
            'Toys': [
                'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1606092195730-5d7b9af1efc5?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1606092195730-5d7b9af1efc5?w=400&h=300&fit=crop&crop=center'
            ],
            'Automotive': [
                'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400&h=300&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400&h=300&fit=crop&crop=center'
            ]
        }
        
        # Get category images
        category_images = reliable_images.get(category, reliable_images['Clothing'])
        
        # If we have a product title, try to match it better
        if product_title:
            title_lower = product_title.lower()
            
            # Electronics matching
            if any(word in title_lower for word in ['macbook', 'laptop', 'computer']):
                return 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400&h=300&fit=crop&crop=center'
            elif any(word in title_lower for word in ['iphone', 'phone', 'mobile']):
                return 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=300&fit=crop&crop=center'
            elif any(word in title_lower for word in ['headphones', 'airpods', 'audio']):
                return 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400&h=300&fit=crop&crop=center'
            elif any(word in title_lower for word in ['ipad', 'tablet']):
                return 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=300&fit=crop&crop=center'
            
            # Clothing matching
            elif any(word in title_lower for word in ['jeans', 'pants']):
                return 'https://images.unsplash.com/photo-1551028719-001c2b5d2ac3?w=400&h=300&fit=crop&crop=center'
            elif any(word in title_lower for word in ['jacket', 'coat']):
                return 'https://images.unsplash.com/photo-1551028719-001c2b5d2ac3?w=400&h=300&fit=crop&crop=center'
            elif any(word in title_lower for word in ['handbag', 'bag', 'purse']):
                return 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=300&fit=crop&crop=center'
            elif any(word in title_lower for word in ['sneakers', 'shoes']):
                return 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=300&fit=crop&crop=center'
            
            # Home & Garden matching
            elif any(word in title_lower for word in ['bamboo', 'wooden', 'furniture']):
                return 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop&crop=center'
            elif any(word in title_lower for word in ['plant', 'succulent', 'garden']):
                return 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&h=300&fit=crop&crop=center'
            elif any(word in title_lower for word in ['kitchen', 'utensil']):
                return 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=300&fit=crop&crop=center'
            
            # Sports matching
            elif any(word in title_lower for word in ['yoga', 'mat', 'fitness']):
                return 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=300&fit=crop&crop=center'
            elif any(word in title_lower for word in ['bicycle', 'bike']):
                return 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400&h=300&fit=crop&crop=center'
            elif any(word in title_lower for word in ['tennis', 'racket']):
                return 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=300&fit=crop&crop=center'
            
            # Books matching
            elif any(word in title_lower for word in ['book', 'guide', 'manual']):
                return 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=300&fit=crop&crop=center'
            elif any(word in title_lower for word in ['vinyl', 'record', 'music']):
                return 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400&h=300&fit=crop&crop=center'
            
            # Beauty matching
            elif any(word in title_lower for word in ['skincare', 'beauty', 'cosmetic']):
                return 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=400&h=300&fit=crop&crop=center'
            elif any(word in title_lower for word in ['toothbrush', 'dental']):
                return 'https://images.unsplash.com/photo-1607619056574-7b8d3ee536b2?w=400&h=300&fit=crop&crop=center'
            
            # Toys matching
            elif any(word in title_lower for word in ['toy', 'game', 'puzzle']):
                return 'https://images.unsplash.com/photo-1606092195730-5d7b9af1efc5?w=400&h=300&fit=crop&crop=center'
            elif any(word in title_lower for word in ['block', 'building']):
                return 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400&h=300&fit=crop&crop=center'
            
            # Automotive matching
            elif any(word in title_lower for word in ['car', 'automotive', 'vehicle']):
                return 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400&h=300&fit=crop&crop=center'
        
        # Return random image from category
        return random.choice(category_images)
    
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
            
            # Generate realistic product names based on category
            title = self._generate_realistic_title(category)
            
            # Generate dynamic description
            description = self._generate_sustainable_description(category, category_info['keywords'], title)
            
            # Calculate dynamic pricing
            base_price = random.uniform(*category_info['base_price_range'])
            dynamic_price = self.get_dynamic_pricing(category, base_price)
            
            # Get real-time image
            image_url = self.get_unsplash_image(category, category_info['keywords'], title)
            
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
    
    def _generate_realistic_title(self, category: str) -> str:
        """Generate realistic product titles that match images"""
        realistic_titles = {
            'Electronics': [
                'MacBook Pro 13" (2020) - Excellent Condition',
                'iPhone 12 Pro - Space Gray, 128GB',
                'Sony WH-1000XM4 Noise-Canceling Headphones',
                'iPad Air 4th Gen - Space Gray, 64GB',
                'Nintendo Switch - Animal Crossing Edition',
                'Samsung Galaxy S21 - Phantom Black',
                'Dell XPS 13 Laptop - Silver',
                'AirPods Pro 2nd Generation',
                'Canon EOS R6 Camera Body',
                'Microsoft Surface Pro 8'
            ],
            'Clothing': [
                'Vintage Levi\'s 501 Jeans - Size 32',
                'Organic Cotton T-Shirt Collection (5 Pack)',
                'Vintage Coach Leather Handbag',
                'Nike Air Max 90 - White/Black',
                'Vintage Band T-Shirt - Nirvana',
                'Allbirds Tree Runners - Size 9',
                'Patagonia Fleece Jacket - Navy',
                'Vintage Denim Jacket - Levi\'s',
                'Lululemon Yoga Pants - Black',
                'Vintage Concert T-Shirt - The Beatles'
            ],
            'Home & Garden': [
                'Bamboo Kitchen Utensil Set (6 Pieces)',
                'Indoor Plant Collection - Succulents (6 Plants)',
                'Vintage Wooden Dining Table - Oak',
                'Bamboo Cutting Board Set (3 Sizes)',
                'Organic Herb Garden Kit',
                'Vintage Ceramic Plant Pots (Set of 4)',
                'Bamboo Bedding Set - King Size',
                'Indoor Herb Growing Kit',
                'Vintage Mason Jar Collection (12 Jars)',
                'Bamboo Bathroom Accessories Set'
            ],
            'Books': [
                'Zero Waste Living Guide - Book Collection',
                'Vinyl Record Collection - Classic Rock (10 Albums)',
                'Sustainable Living Books (3 Books)',
                'Vintage Cookbook Collection',
                'Environmental Science Textbooks',
                'Minimalism Guide - Digital Download',
                'Organic Gardening Handbook',
                'Vintage Children\'s Books (5 Books)',
                'Climate Change Awareness Books',
                'DIY Upcycling Project Guide'
            ],
            'Sports': [
                'Eco-Friendly Cork Yoga Mat',
                'Vintage Raleigh Bicycle - 26" Wheels',
                'Organic Cotton Yoga Block Set',
                'Bamboo Ski Poles - Adjustable',
                'Vintage Tennis Racket - Wilson',
                'Eco-Friendly Water Bottle - Stainless Steel',
                'Vintage Golf Club Set (7 Clubs)',
                'Organic Cotton Gym Towel',
                'Bamboo Badminton Racket Set',
                'Vintage Basketball - Spalding'
            ],
            'Beauty': [
                'Organic Skincare Set - All Natural',
                'Bamboo Toothbrush Set (4 Pack)',
                'Cruelty-Free Makeup Brush Set',
                'Organic Shampoo & Conditioner Set',
                'Vintage Perfume Bottle Collection',
                'Natural Face Mask Kit (5 Masks)',
                'Bamboo Hair Comb Set (3 Sizes)',
                'Organic Lip Balm Collection (6 Flavors)',
                'Vintage Makeup Mirror - Art Deco',
                'Natural Soap Collection (8 Bars)'
            ],
            'Furniture': [
                'Vintage Wooden Dining Table - Seats 6',
                'Mid-Century Modern Armchair - Teak',
                'Vintage Bookshelf - Oak Wood',
                'Bamboo Coffee Table - Round',
                'Vintage Desk - Mahogany',
                'Rattan Lounge Chair - Natural',
                'Vintage Nightstand - Cherry Wood',
                'Bamboo Floor Lamp - Adjustable',
                'Vintage Wardrobe - Pine Wood',
                'Recycled Plastic Garden Chair'
            ],
            'Toys': [
                'Wooden Building Blocks Set (50 Pieces)',
                'Vintage Board Game Collection (5 Games)',
                'Organic Cotton Stuffed Animals (3 Pack)',
                'Bamboo Puzzle Set (4 Puzzles)',
                'Vintage LEGO Set - Classic Space',
                'Eco-Friendly Art Supplies Kit',
                'Wooden Train Set - 20 Pieces',
                'Vintage Barbie Doll Collection (3 Dolls)',
                'Organic Cotton Play Mat',
                'Bamboo Musical Instruments Set'
            ],
            'Automotive': [
                'Bamboo Car Phone Mount - Universal',
                'Eco-Friendly Car Air Freshener Set',
                'Vintage Car Dashboard Clock',
                'Bamboo Car Organizer Tray',
                'Organic Cotton Car Seat Covers',
                'Vintage License Plate Collection',
                'Eco-Friendly Car Cleaning Kit',
                'Bamboo Car Cup Holder',
                'Vintage Car Manual Collection',
                'Organic Car Wax - Natural'
            ]
        }
        
        # Get category-specific titles
        category_titles = realistic_titles.get(category, realistic_titles['Clothing'])
        
        # Add some variation with condition/status
        base_title = random.choice(category_titles)
        conditions = [' - Excellent Condition', ' - Like New', ' - Good Condition', ' - Vintage', ' - Pre-owned']
        
        # 70% chance to add condition
        if random.random() < 0.7:
            condition = random.choice(conditions)
            if condition not in base_title:
                base_title += condition
        
        return base_title

    def _generate_sustainable_description(self, category: str, keywords: List[str], product_title: str = "") -> str:
        """Generate realistic sustainable product descriptions"""
        # Create specific descriptions based on product title
        if product_title:
            title_lower = product_title.lower()
            
            # Electronics descriptions
            if any(word in title_lower for word in ['macbook', 'iphone', 'ipad', 'laptop', 'phone', 'tablet']):
                return f"Pre-owned {product_title.split(' - ')[0]} in excellent condition. This device has been professionally cleaned and tested, ensuring optimal performance while reducing electronic waste. Perfect for students, professionals, or anyone looking for quality technology at a fraction of the retail price. Includes original accessories and comes with a 30-day warranty."
            
            elif any(word in title_lower for word in ['headphones', 'airpods', 'speaker', 'audio']):
                return f"High-quality {product_title.split(' - ')[0]} with excellent sound quality. This audio device has been gently used and maintained in perfect working condition. Ideal for music lovers, professionals, or anyone who appreciates premium audio without the premium price tag. Helps reduce electronic waste while delivering exceptional performance."
            
            # Clothing descriptions
            elif any(word in title_lower for word in ['jeans', 'jacket', 'shirt', 'pants', 'dress']):
                return f"Stylish {product_title.split(' - ')[0]} in great condition. This piece has been carefully maintained and shows minimal wear. Perfect for building a sustainable wardrobe while staying fashionable. Each purchase helps reduce textile waste and supports the circular fashion economy. Size and condition details included in listing."
            
            elif any(word in title_lower for word in ['handbag', 'bag', 'purse', 'backpack']):
                return f"Beautiful {product_title.split(' - ')[0]} with timeless appeal. This accessory has been gently used and maintained in excellent condition. Perfect for adding a touch of elegance to any outfit while supporting sustainable fashion. Each purchase helps reduce waste and promotes conscious consumption."
            
            # Home & Garden descriptions
            elif any(word in title_lower for word in ['bamboo', 'wooden', 'table', 'chair', 'furniture']):
                return f"Sustainable {product_title.split(' - ')[0]} made from eco-friendly materials. This piece has been crafted with environmental consciousness in mind, using renewable resources and sustainable manufacturing practices. Perfect for creating a green home while maintaining style and functionality. Each purchase supports sustainable living."
            
            elif any(word in title_lower for word in ['plant', 'succulent', 'garden', 'herb']):
                return f"Healthy {product_title.split(' - ')[0]} ready for your home or garden. These plants have been carefully nurtured and are ready to bring life and clean air to your space. Perfect for beginners or experienced gardeners looking to add greenery to their environment. Each purchase supports sustainable gardening practices."
            
            # Books descriptions
            elif any(word in title_lower for word in ['book', 'guide', 'manual', 'collection']):
                return f"Informative {product_title.split(' - ')[0]} in excellent condition. This collection provides valuable knowledge about sustainable living, environmental awareness, or practical skills. Perfect for anyone looking to expand their understanding of eco-friendly practices. Each purchase promotes education and environmental consciousness."
            
            # Sports descriptions
            elif any(word in title_lower for word in ['yoga', 'bicycle', 'tennis', 'golf', 'fitness']):
                return f"Quality {product_title.split(' - ')[0]} for active lifestyles. This equipment has been well-maintained and is ready for immediate use. Perfect for fitness enthusiasts, outdoor adventurers, or anyone looking to stay active while supporting sustainable practices. Each purchase promotes healthy living and environmental responsibility."
        
        # Fallback to generic descriptions
        descriptions = {
            'Electronics': [
                f"Energy-efficient {category.lower()} designed for sustainability. This device reduces environmental impact while maintaining high performance. Perfect for conscious consumers who value both quality and environmental responsibility.",
                f"Refurbished {category.lower()} with eco-friendly packaging. This device has been professionally restored to like-new condition, extending its useful life and reducing electronic waste.",
                f"Pre-owned {category.lower()} in excellent working condition. This device offers great value while promoting the circular economy and reducing environmental impact."
            ],
            'Clothing': [
                f"Vintage {category.lower()} made from sustainable materials. This piece offers timeless style while supporting ethical fashion practices and reducing textile waste.",
                f"Ethically produced {category.lower()} from eco-conscious manufacturers. This item combines style with sustainability, perfect for the conscious consumer.",
                f"Pre-loved {category.lower()} in great condition. This piece gives new life to quality clothing while reducing waste and supporting sustainable fashion."
            ],
            'Home & Garden': [
                f"Bamboo {category.lower()} set for eco-friendly living. These items promote sustainable home practices while maintaining functionality and style.",
                f"Zero-waste {category.lower()} designed to minimize environmental impact. Perfect for creating a sustainable home environment.",
                f"Organic {category.lower()} collection for conscious living. Made from renewable materials, these items support sustainable lifestyle choices."
            ],
            'Books': [
                f"Educational {category.lower()} collection focused on sustainability and environmental awareness. These books provide valuable knowledge for conscious living.",
                f"Vintage {category.lower()} collection in excellent condition. These books offer timeless knowledge while promoting the sharing economy.",
                f"Inspirational {category.lower()} about sustainable living and environmental responsibility. Perfect for anyone looking to make positive changes."
            ],
            'Sports': [
                f"Eco-friendly {category.lower()} for active lifestyles. This equipment promotes healthy living while supporting environmental sustainability.",
                f"Quality {category.lower()} designed for durability and performance. This equipment reduces waste through long-lasting design and materials.",
                f"Sustainable {category.lower()} for conscious athletes. This equipment combines performance with environmental responsibility."
            ],
            'Beauty': [
                f"Natural {category.lower()} made with organic ingredients. These products promote healthy beauty practices while supporting environmental sustainability.",
                f"Cruelty-free {category.lower()} from ethical brands. These products combine effectiveness with environmental and animal welfare consciousness.",
                f"Eco-friendly {category.lower()} with minimal packaging. These products promote sustainable beauty practices while maintaining quality."
            ],
            'Furniture': [
                f"Sustainable {category.lower()} made from renewable materials. This piece combines functionality with environmental consciousness.",
                f"Vintage {category.lower()} with character and history. This piece offers unique style while promoting the circular economy.",
                f"Eco-friendly {category.lower()} designed for longevity. This piece reduces waste through durable construction and timeless design."
            ],
            'Toys': [
                f"Educational {category.lower()} made from sustainable materials. These toys promote learning while supporting environmental responsibility.",
                f"Vintage {category.lower()} collection in excellent condition. These toys offer timeless fun while promoting the sharing economy.",
                f"Eco-friendly {category.lower()} designed for durability. These toys reduce waste through long-lasting design and materials."
            ],
            'Automotive': [
                f"Eco-friendly {category.lower()} for sustainable driving. This accessory promotes environmental consciousness while maintaining functionality.",
                f"Quality {category.lower()} designed for durability. This accessory reduces waste through long-lasting design and materials.",
                f"Sustainable {category.lower()} for conscious drivers. This accessory combines functionality with environmental responsibility."
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
