📄 README.md
# EcoFinds – Sustainable Second-Hand Marketplace

EcoFinds is a hackathon project that promotes **sustainable consumption** by making it easy to **buy and sell second-hand items**.  
It’s a simple web app built with **Flask + SQLite** that allows users to register, create product listings, browse items, add to cart, and track previous purchases.

---

## 🚀 Features

- 🔑 **User Authentication** (Register/Login/Logout)
- 👤 **User Dashboard** – view your listings
- 📦 **Product Listings (CRUD)** – Add, view, edit, delete products
- 🔎 **Browse Products** – Feed view with title, price, and placeholder image
- 🛒 **Cart** – Add products to cart and purchase them
- 📜 **Previous Purchases** – Track past purchases

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite (via SQLAlchemy)
- **Auth:** Flask-Login
- **Frontend:** Bootstrap (CDN for fast styling)

---

## 📂 Project Structure

```
ecofinds/
├── app.py              # Main Flask app
├── ecofinds.db         # SQLite database
├── requirements.txt    # Python dependencies
├── .gitignore          # Ignore unnecessary files
├── templates/          # HTML templates (Bootstrap)
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── products.html
│   ├── add_product.html
│   ├── dashboard.html
│   ├── cart.html
│   └── purchases.html
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ecofinds.git
cd ecofinds
```

### 2. Create & activate virtual environment

For Linux / macOS:
```bash
python -m venv venv
source venv/bin/activate
```

For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser 🎉

---

## 📝 Usage

- Register/Login as a new user
- Add a product with title, category, description, price
- Browse products from the main feed
- Add to cart and purchase items
- View past purchases anytime

---

## 💡 Future Enhancements

- Image upload support (instead of placeholder URLs)
- Search + category filters
- Payment gateway integration
- Chat between buyers & sellers
- Mobile-friendly Progressive Web App (PWA)

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the MIT License.