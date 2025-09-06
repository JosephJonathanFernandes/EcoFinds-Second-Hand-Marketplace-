# EcoFinds – Sustainable Second-Hand Marketplace

EcoFinds is a collaborative web application for buying and selling second-hand items, designed to promote sustainable consumption. Built with Flask and SQLite, it provides a secure, user-friendly platform for product listings, purchases, and user management.

---

## 🚀 Project Goals
- Make second-hand shopping easy and accessible
- Encourage sustainable consumption
- Provide a simple, intuitive user experience
- Enable team collaboration and easy onboarding

---

## 🧑‍💻 Getting Started (For Developers)
1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd ecofinds
   ```
2. **Set up your Python environment:**
   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Run the app:**
   ```sh
   python app.py
   ```
5. **Troubleshooting:**
   - If you see database errors, delete `instance/ecofinds.db` and restart.
   - For missing packages, run `pip install -r requirements.txt` again.
   - For static file issues, check the `static/` folder and file paths.

---

## 🚩 Features (Detailed)

- **User Authentication**
  - Secure registration, login, and logout using Flask-Login.
  - Passwords are hashed for safety.
  - Only registered users can add products, purchase, or access their dashboard.

- **User Dashboard**
  - Personalized dashboard for each user.
  - View all products you have listed for sale.
  - Edit or delete your listings directly from the dashboard.

- **Product Listings (CRUD)**
  - Create: Add new products with title, description, category, price, and image.
  - Read: View all products in the public feed or your dashboard.
  - Update: Edit product details and images.
  - Delete: Remove products you no longer wish to sell.

- **Product Feed & Search**
  - Browse all available products in a feed view.
  - Filter by category or search by keyword.
  - Each product displays title, price, description, and image.

- **Cart System**
  - Add products to your cart for later purchase.
  - View all items in your cart before checkout.
  - Remove items from your cart if you change your mind.

- **Purchasing & Purchase History**
  - Purchase all items in your cart with one click.
  - Purchased items are tracked in your purchase history.
  - View details of past purchases at any time.

- **Profile Management**
  - Update your username and email address.
  - Upload a custom avatar image.
  - Changes are reflected across the app instantly.

- **Responsive Design**
  - Uses Bootstrap for a clean, mobile-friendly interface.
  - Works well on desktops, tablets, and smartphones.

- **Security**
  - User authentication and session management.
  - Input validation for forms.
  - Database operations use SQLAlchemy ORM for safety.

---

## 🤝 Contributing
- Branch from `main` for new features or bug fixes
- Commit with clear messages (e.g., `feat: add product search`)
- Open a pull request and tag teammates for review
- Use issues to track bugs, ideas, and questions

---

## 👤 Example User Stories
- "As a new user, I want to register and log in so I can list my items."
- "As a buyer, I want to browse products and add them to my cart."
- "As a seller, I want to view my dashboard and manage my listings."
- "As a user, I want to update my profile and avatar."

---

## 🗂️ File & Folder Overview
| Name              | Purpose                                      |
|-------------------|----------------------------------------------|
| `app.py`          | Main Flask app and route definitions         |
| `models.py`       | Database models (User, Product, etc.)        |
| `forms.py`        | WTForms definitions for user/product forms   |
| `migrate_db.py`   | Database migration script                    |
| `requirements.txt`| Python dependencies                          |
| `.gitignore`      | Files/folders to ignore in git               |
| `instance/`       | Contains the SQLite database                 |
| `static/`         | CSS, avatars, and other static files         |
| `templates/`      | HTML templates (Bootstrap/Jinja2)            |

---

## 🖼️ Screenshots
*Add screenshots of the landing page, dashboard, product feed, etc. here for reference.*

---

## ❓ FAQ
- **How do I reset my password?**
  - Currently, password reset is not implemented. Contact the admin for help.
- **How do I add a new feature?**
  - Create a new branch, implement your feature, and open a pull request.
- **Where is the database stored?**
  - In `instance/ecofinds.db` (ignored by git).

---

## 📬 Contact & Support
- For questions, open an issue or contact the project owner.
- Team members: Add your name and contact info here!

---

## 📑 License
This project is for educational and demonstration purposes only.

---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)

---

## 🛠️ Continuous Integration (CI/CD)
- Recommended: Set up GitHub Actions for automated testing and linting.
- Example workflow:
  - On every push or pull request, run `pytest` and `flake8`.
  - Fail builds on test or lint errors.
- See [GitHub Actions documentation](https://docs.github.com/en/actions) for setup.

---

## 📚 Extended Documentation
- For API details, see the Endpoints section above.
- For database schema, see `models.py` and comments in code.
- For form usage, see `forms.py` and template files.
- For deployment, see Flask docs or use platforms like Heroku, Vercel, or Render.

---