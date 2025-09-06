/**
 * EcoFinds Image Handler
 * Handles image loading, fallbacks, and error states
 */

class ImageHandler {
    constructor() {
        this.init();
    }

    init() {
        // Handle all product images
        this.handleProductImages();
        
        // Handle user avatars
        this.handleUserAvatars();
        
        // Set up image error handlers
        this.setupErrorHandlers();
    }

    handleProductImages() {
        const productImages = document.querySelectorAll('.card-img-top, .product-image');
        
        productImages.forEach(img => {
            // Add loading state
            this.addLoadingState(img);
            
            // Set up error handling
            img.addEventListener('error', (e) => {
                this.handleImageError(e.target);
            });
            
            // Set up load handling
            img.addEventListener('load', (e) => {
                this.handleImageLoad(e.target);
            });
        });
    }

    handleUserAvatars() {
        const avatars = document.querySelectorAll('.avatar, .user-avatar');
        
        avatars.forEach(img => {
            img.addEventListener('error', (e) => {
                this.handleAvatarError(e.target);
            });
        });
    }

    addLoadingState(img) {
        // Skip loading state - images load directly
        // Just ensure proper styling
        img.classList.add('product-image');
    }

    handleImageError(img) {
        console.log('Image failed to load:', img.src);
        
        // Try fallback image immediately
        this.tryFallbackImage(img);
    }

    handleImageLoad(img) {
        // Simple fade-in effect without loading states
        img.style.opacity = '0';
        img.style.transition = 'opacity 0.3s ease';
        
        setTimeout(() => {
            img.style.opacity = '1';
        }, 50);
    }

    handleAvatarError(img) {
        // Use default avatar
        img.src = 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face';
        img.alt = 'Default Avatar';
    }

    tryFallbackImage(img) {
        // Get category from parent card or use default
        const card = img.closest('.card');
        const category = this.getCategoryFromCard(card) || 'Clothing';
        
        // Get fallback image based on category
        const fallbackUrl = this.getFallbackImage(category);
        
        // Try to load fallback
        const fallbackImg = new Image();
        fallbackImg.onload = () => {
            img.src = fallbackUrl;
            img.style.display = 'block';
        };
        
        fallbackImg.onerror = () => {
            console.log('Fallback image also failed');
        };
        
        fallbackImg.src = fallbackUrl;
    }

    getCategoryFromCard(card) {
        if (!card) return null;
        
        // Look for category badge or text
        const categoryBadge = card.querySelector('.badge');
        if (categoryBadge) {
            return categoryBadge.textContent.trim();
        }
        
        // Look for category in product title or description
        const title = card.querySelector('.card-title');
        if (title) {
            const titleText = title.textContent.toLowerCase();
            
            if (titleText.includes('macbook') || titleText.includes('iphone') || titleText.includes('laptop')) {
                return 'Electronics';
            } else if (titleText.includes('jeans') || titleText.includes('jacket') || titleText.includes('shirt')) {
                return 'Clothing';
            } else if (titleText.includes('bamboo') || titleText.includes('plant') || titleText.includes('garden')) {
                return 'Home & Garden';
            } else if (titleText.includes('book') || titleText.includes('vinyl') || titleText.includes('guide')) {
                return 'Books';
            } else if (titleText.includes('yoga') || titleText.includes('bicycle') || titleText.includes('fitness')) {
                return 'Sports';
            } else if (titleText.includes('skincare') || titleText.includes('beauty') || titleText.includes('toothbrush')) {
                return 'Beauty';
            } else if (titleText.includes('table') || titleText.includes('chair') || titleText.includes('furniture')) {
                return 'Furniture';
            } else if (titleText.includes('toy') || titleText.includes('game') || titleText.includes('puzzle')) {
                return 'Toys';
            } else if (titleText.includes('car') || titleText.includes('automotive') || titleText.includes('vehicle')) {
                return 'Automotive';
            }
        }
        
        return null;
    }

    getFallbackImage(category) {
        const fallbackImages = {
            'Electronics': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400&h=300&fit=crop&crop=center',
            'Clothing': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400&h=300&fit=crop&crop=center',
            'Home & Garden': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop&crop=center',
            'Books': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=300&fit=crop&crop=center',
            'Sports': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=300&fit=crop&crop=center',
            'Beauty': 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=400&h=300&fit=crop&crop=center',
            'Furniture': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop&crop=center',
            'Toys': 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400&h=300&fit=crop&crop=center',
            'Automotive': 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400&h=300&fit=crop&crop=center'
        };
        
        return fallbackImages[category] || fallbackImages['Clothing'];
    }

    setupErrorHandlers() {
        // Global error handler for images
        document.addEventListener('error', (e) => {
            if (e.target.tagName === 'IMG') {
                this.handleImageError(e.target);
            }
        }, true);
    }

    // Public method to refresh images
    refreshImages() {
        this.handleProductImages();
        this.handleUserAvatars();
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.imageHandler = new ImageHandler();
});

// Export for use in other scripts
window.ImageHandler = ImageHandler;
