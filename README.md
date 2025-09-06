# EcoFinds – Sustainable Second-Hand Marketplace

EcoFinds is a web application designed to promote sustainable consumption by enabling users to buy and sell second-hand items. Built with Flask and SQLite, EcoFinds provides a secure, user-friendly platform for listing products, managing purchases, and tracking activity.

---

## Features
- **User Authentication:** Register, login, and logout securely
- **User Dashboard:** View and manage your product listings
- **Product Listings:** Add, view, edit, and delete products
- **Product Feed:** Browse all available items with search and category filters
- **Cart:** Add products to cart and purchase them
- **Purchase History:** Track previous purchases
- **Profile Management:** Update username, email, and avatar

---

## Tech Stack
- **Backend:** Flask (Python)
- **Database:** SQLite (SQLAlchemy ORM)
- **Authentication:** Flask-Login
- **Forms:** Flask-WTF
- **Frontend:** Bootstrap (CDN)

---

## Setup Instructions
1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd ecofinds
   ```
2. **Create and activate a virtual environment:**
   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Run the application:**
   ```sh
   python app.py
   ```

---

## Usage
- Access the app at `http://localhost:5000`
- Register a new account or log in
- Add products, browse listings, manage your cart, and view purchase history

---

## API Endpoints
| Route                | Methods        | Description                       |
|----------------------|---------------|-----------------------------------|
| `/`                  | GET, POST     | Product feed/search               |
| `/register`          | GET, POST     | User registration                 |
| `/login`             | GET, POST     | User login                        |
| `/logout`            | GET           | User logout                       |
| `/dashboard`         | GET           | User dashboard                    |
| `/add_product`       | GET, POST     | Add new product                   |
| `/products`          | GET           | Browse all products               |
| `/cart`              | GET           | View cart                         |
| `/add_to_cart/<pid>` | GET           | Add product to cart               |
| `/purchase`          | GET           | Purchase items in cart            |
| `/purchases`         | GET           | View purchase history             |
| `/profile`           | GET, POST     | View/update user profile          |
| `/landing`           | GET           | Landing page                      |

---

## Project Structure
```
app.py            # Main Flask app
models.py         # Database models
forms.py          # WTForms definitions
migrate_db.py     # DB migration script
requirements.txt  # Python dependencies
.gitignore        # Ignore unnecessary files
instance/
    ecofinds.db   # SQLite database
static/
    style.css     # Custom styles
    avatars/      # Uploaded avatars
templates/
    *.html        # Jinja2 templates
```

---

## License
This project is provided for educational and demonstration purposes.