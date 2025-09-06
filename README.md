# 🌱 EcoFinds - Sustainable Second-Hand Marketplace

A modern, full-stack web application built for the NMIT x ODOO Hackathon that promotes sustainable consumption through a user-friendly second-hand marketplace.

## 🚀 Features

### Core Functionality
- **User Authentication & Management**: Secure registration, login, and profile management
- **Product Listings**: Create, read, update, and delete product listings with image upload
- **Advanced Search & Filtering**: Real-time search with category, price range, and keyword filtering
- **Shopping Cart System**: Add items, manage quantities, and proceed to checkout
- **Purchase History**: Track all purchases with detailed transaction history
- **User Dashboard**: Comprehensive dashboard for managing listings and viewing analytics

### Advanced Features
- **Real-time Data**: Dynamic product listings and live inventory management
- **Responsive Design**: Mobile-first design that works seamlessly across all devices
- **Image Upload**: Secure file handling for product and profile images
- **Eco Impact Tracking**: Real-time environmental impact metrics for users
- **Advanced UI/UX**: Modern design with animations, micro-interactions, and intuitive navigation
- **Form Validation**: Robust client-side and server-side input validation
- **Security**: CSRF protection, input sanitization, and secure file uploads

## 🛠️ Technology Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: ORM for database management
- **SQLite**: Local database for reliability and offline capability
- **Flask-Login**: User session management
- **Werkzeug**: Security utilities for password hashing and file handling

### Frontend
- **Bootstrap 5**: Responsive CSS framework
- **Bootstrap Icons**: Comprehensive icon library
- **Custom CSS**: Modern styling with CSS variables and animations
- **JavaScript**: Enhanced user interactions and form validation
- **Jinja2**: Template engine for dynamic content

### Development Tools
- **Git**: Version control
- **Python 3.8+**: Programming language
- **HTML5 & CSS3**: Markup and styling
- **Responsive Design**: Mobile-first approach

## 📁 Project Structure

```
EcoFinds-Second-Hand-Marketplace/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── forms.py               # WTForms definitions
├── requirements.txt       # Python dependencies
├── static/
│   ├── style.css         # Custom CSS styles
│   ├── uploads/          # Product images
│   └── avatars/          # User avatars
├── templates/
│   ├── base.html         # Base template
│   ├── landing.html      # Homepage
│   ├── products.html     # Product listings
│   ├── dashboard.html    # User dashboard
│   ├── cart.html         # Shopping cart
│   ├── purchases.html    # Purchase history
│   ├── profile.html      # User profile
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   └── add_product.html  # Add product form
├── instance/
│   └── ecofinds.db       # SQLite database
└── README.md             # Project documentation
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/EcoFinds-Second-Hand-Marketplace.git
   cd EcoFinds-Second-Hand-Marketplace
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Populate with sample data (Recommended)**
   ```bash
   python seed_database.py
   ```
   Or run the automated setup:
   ```bash
   python setup.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

### Demo Login Credentials
- **Email**: sarah.green@example.com
- **Password**: password123

## 🎯 Hackathon Requirements Compliance

### ✅ Mandatory Requirements
- **Real-time/Dynamic Data**: Live product listings, real-time search, and dynamic cart updates
- **Responsive & Clean UI**: Mobile-first design with consistent eco-friendly color scheme
- **Robust Input Validation**: Client-side and server-side validation with real-time feedback
- **Intuitive Navigation**: Clear menu structure with logical user flow
- **Version Control**: Proper Git repository with meaningful commits

### ✅ Good-to-Have Features
- **Backend API Design**: RESTful endpoints with proper HTTP methods
- **Data Modeling**: Comprehensive database schema with relationships
- **Local Database**: SQLite for offline capability and reduced cloud dependency
- **Value-Added Technology**: Real-time features that enhance user experience

## 🌟 Key Features Highlights

### 1. **Eco Impact Tracking**
- Real-time CO₂ savings calculation
- Items recycled counter
- Money saved vs. new purchases
- Environmental impact visualization

### 2. **Advanced Search & Filtering**
- Keyword search across product titles
- Category-based filtering
- Price range filtering
- Multiple sorting options (price, name, newest)

### 3. **Modern UI/UX**
- Smooth animations and transitions
- Hover effects and micro-interactions
- Responsive grid layouts
- Intuitive form design with real-time validation

### 4. **Security Features**
- Password hashing with Werkzeug
- CSRF protection
- Input sanitization
- Secure file upload handling

### 5. **User Experience**
- Progressive enhancement
- Loading states and user feedback
- Error handling with helpful messages
- Mobile-optimized interface

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Product listings with search/filter |
| GET | `/landing` | Homepage with featured products |
| GET/POST | `/register` | User registration |
| GET/POST | `/login` | User authentication |
| GET | `/dashboard` | User dashboard |
| GET/POST | `/add_product` | Add new product listing |
| GET | `/cart` | Shopping cart |
| GET | `/purchases` | Purchase history |
| GET/POST | `/profile` | User profile management |
| POST | `/add_to_cart/<id>` | Add item to cart |
| POST | `/purchase` | Complete purchase |
| GET | `/search` | Advanced search with filters |

## 🎨 Design System

### Color Palette
- **Primary Green**: #00C851
- **Secondary Green**: #00A041
- **Accent Green**: #43ea7c
- **Light Green**: #E8F5E8
- **Dark Green**: #006400

### Typography
- **Font Family**: Inter (Google Fonts)
- **Headings**: Bold weights (600-800)
- **Body Text**: Regular weight (400)
- **Small Text**: Light weight (300)

### Components
- **Cards**: Rounded corners with subtle shadows
- **Buttons**: Gradient backgrounds with hover effects
- **Forms**: Clean inputs with validation states
- **Navigation**: Fixed header with smooth scrolling

## 📦 Sample Data

The application comes with pre-populated sample data including:

### **👥 Sample Users (5 users)**
- **Sarah Green** - Eco-conscious fashion enthusiast
- **Eco Mike** - Technology and sustainability advocate  
- **Sustainable Sam** - Home and garden expert
- **Green Lisa** - Vintage and retro collector
- **Recycle Ryan** - Sports and fitness enthusiast

### **🛍️ Sample Products (25+ items)**
- **Electronics**: MacBook Pro, iPhone 12 Pro, Sony Headphones, iPad Air, Nintendo Switch
- **Clothing**: Vintage denim jacket, organic cotton tees, leather handbag, vintage band shirts
- **Home & Garden**: Bamboo kitchen utensils, succulent plants, vintage dining table
- **Books & Media**: Zero waste living guides, vinyl record collection
- **Sports & Fitness**: Eco-friendly yoga mat, vintage bicycle
- **Toys & Games**: Wooden building blocks, vintage board games
- **Beauty & Health**: Organic skincare set, bamboo toothbrushes
- **Automotive**: Bamboo car phone mount

### **🛒 Demo Features**
- Pre-filled shopping cart with sample items
- Purchase history with environmental impact metrics
- User profiles with avatars and eco stats
- Realistic product descriptions and pricing

## 🚀 Future Enhancements

- **Real-time Notifications**: WebSocket integration for live updates
- **Payment Integration**: Stripe/PayPal integration for secure payments
- **AI Recommendations**: Machine learning for product suggestions
- **Mobile App**: React Native mobile application
- **Social Features**: User reviews, ratings, and social sharing
- **Analytics Dashboard**: Advanced analytics for sellers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

**WizCoders** - NMIT x ODOO Hackathon 2025
- Full-stack development
- UI/UX design
- Database architecture
- Security implementation

## 🙏 Acknowledgments

- Bootstrap team for the excellent CSS framework
- Flask community for comprehensive documentation
- Unsplash for beautiful placeholder images
- All contributors and testers

---

**Built with ❤️ for a sustainable future**

*Every purchase on EcoFinds contributes to a circular economy and reduces environmental waste. Join us in making a difference!*