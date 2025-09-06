/**
 * EcoFinds Real-time Updates
 * Handles live data updates and dynamic features
 */

class RealTimeUpdater {
    constructor() {
        this.updateInterval = 30000; // 30 seconds
        this.isUpdating = false;
        this.lastUpdate = null;
        this.init();
    }

    init() {
        console.log('🚀 Initializing EcoFinds Real-time Updates...');
        this.startPeriodicUpdates();
        this.setupEventListeners();
        this.loadMarketInsights();
    }

    startPeriodicUpdates() {
        setInterval(() => {
            if (!this.isUpdating) {
                this.updateMarketData();
            }
        }, this.updateInterval);
    }

    setupEventListeners() {
        // Update prices when user clicks refresh
        const refreshButtons = document.querySelectorAll('[data-action="refresh-prices"]');
        refreshButtons.forEach(button => {
            button.addEventListener('click', () => this.updatePrices());
        });

        // Generate new product button
        const generateButtons = document.querySelectorAll('[data-action="generate-product"]');
        generateButtons.forEach(button => {
            button.addEventListener('click', () => this.generateNewProduct());
        });

        // Real-time search
        const searchInput = document.getElementById('search-query');
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    this.performRealTimeSearch(e.target.value);
                }, 500);
            });
        }
    }

    async updateMarketData() {
        try {
            this.isUpdating = true;
            
            // Update market insights
            await this.loadMarketInsights();
            
            // Update trending categories
            await this.updateTrendingCategories();
            
            // Update prices (less frequently)
            if (Math.random() < 0.3) { // 30% chance
                await this.updatePrices();
            }
            
            this.lastUpdate = new Date();
            this.showUpdateNotification('Market data updated successfully!');
            
        } catch (error) {
            console.error('❌ Market data update failed:', error);
        } finally {
            this.isUpdating = false;
        }
    }

    async loadMarketInsights() {
        try {
            const response = await fetch('/api/market-insights');
            const insights = await response.json();
            
            // Update market stats display
            this.updateMarketStats(insights);
            
        } catch (error) {
            console.error('❌ Failed to load market insights:', error);
        }
    }

    async updateTrendingCategories() {
        try {
            const response = await fetch('/api/trending-categories');
            const data = await response.json();
            
            // Update trending categories display
            this.updateTrendingDisplay(data.trending);
            
        } catch (error) {
            console.error('❌ Failed to update trending categories:', error);
        }
    }

    async updatePrices() {
        try {
            const response = await fetch('/api/update-prices?force=true');
            const data = await response.json();
            
            if (data.success && data.updated_count > 0) {
                this.showUpdateNotification(`${data.updated_count} prices updated!`);
                // Reload the page to show updated prices
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            }
            
        } catch (error) {
            console.error('❌ Failed to update prices:', error);
        }
    }

    async generateNewProduct() {
        try {
            const category = document.getElementById('product-category')?.value || 'Clothing';
            const response = await fetch(`/api/generate-product?category=${category}`);
            const data = await response.json();
            
            if (data.success) {
                this.showUpdateNotification('New product generated successfully!');
                // Reload the page to show the new product
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            }
            
        } catch (error) {
            console.error('❌ Failed to generate product:', error);
        }
    }

    async performRealTimeSearch(query) {
        if (query.length < 2) return;
        
        try {
            // Show loading indicator
            this.showSearchLoading(true);
            
            // Perform search
            const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
            const html = await response.text();
            
            // Update results
            this.updateSearchResults(html);
            
        } catch (error) {
            console.error('❌ Real-time search failed:', error);
        } finally {
            this.showSearchLoading(false);
        }
    }

    updateMarketStats(insights) {
        // Update CO2 saved
        const co2Element = document.getElementById('co2-saved');
        if (co2Element) {
            co2Element.textContent = insights.eco_impact_total.co2_saved.toLocaleString();
        }

        // Update items recycled
        const recycledElement = document.getElementById('items-recycled');
        if (recycledElement) {
            recycledElement.textContent = insights.eco_impact_total.items_recycled.toLocaleString();
        }

        // Update active users
        const usersElement = document.getElementById('active-users');
        if (usersElement) {
            usersElement.textContent = insights.eco_impact_total.users_active.toLocaleString();
        }

        // Update new listings
        const listingsElement = document.getElementById('new-listings');
        if (listingsElement) {
            listingsElement.textContent = insights.new_listings_today;
        }
    }

    updateTrendingDisplay(trending) {
        const trendingElement = document.getElementById('trending-categories');
        if (trendingElement) {
            trendingElement.innerHTML = trending.map(category => 
                `<span class="badge bg-success me-1">${category}</span>`
            ).join('');
        }
    }

    updateSearchResults(html) {
        // This would update the search results without full page reload
        // Implementation depends on the specific page structure
        console.log('Search results updated');
    }

    showSearchLoading(show) {
        const searchInput = document.getElementById('search-query');
        if (searchInput) {
            if (show) {
                searchInput.classList.add('loading');
            } else {
                searchInput.classList.remove('loading');
            }
        }
    }

    showUpdateNotification(message) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'alert alert-info alert-dismissible fade show position-fixed';
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            <i class="bi bi-info-circle me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 3000);
    }

    // Public method to manually trigger updates
    forceUpdate() {
        this.updateMarketData();
    }
}

// Initialize real-time updates when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.realTimeUpdater = new RealTimeUpdater();
    
    // Add real-time indicators to the page
    addRealTimeIndicators();
});

function addRealTimeIndicators() {
    // Add live indicator to the navbar
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        const liveIndicator = document.createElement('div');
        liveIndicator.className = 'd-flex align-items-center text-success';
        liveIndicator.innerHTML = `
            <div class="spinner-border spinner-border-sm me-2" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <small>Live Data</small>
        `;
        navbar.appendChild(liveIndicator);
    }

    // Add refresh buttons to product pages
    const productGrid = document.querySelector('.product-grid');
    if (productGrid) {
        const refreshButton = document.createElement('button');
        refreshButton.className = 'btn btn-outline-primary btn-sm mb-3';
        refreshButton.setAttribute('data-action', 'refresh-prices');
        refreshButton.innerHTML = '<i class="bi bi-arrow-clockwise me-1"></i>Refresh Prices';
        productGrid.parentNode.insertBefore(refreshButton, productGrid);
    }

    // Add generate product button to dashboard
    const dashboard = document.querySelector('.dashboard-stats');
    if (dashboard) {
        const generateButton = document.createElement('button');
        generateButton.className = 'btn btn-success btn-sm ms-2';
        generateButton.setAttribute('data-action', 'generate-product');
        generateButton.innerHTML = '<i class="bi bi-plus-circle me-1"></i>Generate Product';
        dashboard.appendChild(generateButton);
    }
}

// Export for use in other scripts
window.RealTimeUpdater = RealTimeUpdater;
