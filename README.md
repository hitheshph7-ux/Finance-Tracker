# 💰 Finance Tracker

A full-stack personal finance and expense tracking web application built with **Django** for the backend REST API and **HTML5/CSS3/JavaScript** for the responsive frontend dashboard.

---

## 📌 Features

- 🔒 **User Authentication**: Secure user registration and login endpoints with session management.
- 👤 **Profile Management**: View and edit user details including name, email, phone number, occupation, and monthly budget.
- 💵 **Income Tracking**: Record income sources, amounts, and dates.
- 💸 **Expense Categorization**: Log expenses with custom categories (e.g., Food, Transport, Rent, Entertainment, Bills).
- 📊 **Interactive Dashboard**: Real-time summary of Total Income, Total Expenses, and Net Balance.
- 📜 **Transaction History**: View combined history of income and expense records.
- 🔌 **REST API Architecture**: Clean Django JSON API endpoints with CORS support.

---

## 📁 Project Structure

```text
Finance-Tracker/
├── finance/                # Django Backend Application
│   ├── manage.py           # Django administrative CLI script
│   ├── db.sqlite3          # Local SQLite database (git-ignored)
│   ├── finance/            # Core Django configuration package
│   │   ├── settings.py     # Settings, installed apps, CORS config
│   │   ├── urls.py         # Main URL routing (APIs & static frontend)
│   │   ├── wsgi.py         # WSGI application entrypoint
│   │   └── asgi.py         # ASGI application entrypoint
│   └── my_app/             # Main Django app (Models, Views, URLs)
│       ├── models.py       # Category, Income, and Expense database models
│       ├── views.py        # REST API endpoints & business logic
│       └── urls.py         # API URL routing definitions
├── frontend/               # Web Frontend Files
│   ├── index.html          # Main Dashboard & Financial Overview
│   ├── login.html          # User Login page
│   ├── register.html       # User Registration page
│   ├── profile.html        # User Profile view page
│   ├── edit-profile.html   # Edit Profile details page
│   ├── css/                # Global and page styles
│   └── js/                 # Client-side API interactions and scripts
├── .gitignore              # Files ignored by Git (venv, db.sqlite3, pycache)
└── README.md               # Project documentation
```

---

## 🚀 Getting Started

Follow these instructions to set up and run the Finance Tracker on your local machine.

### Prerequisites

- **Python 3.10+**
- **pip** (Python package installer)
- Modern web browser (Chrome, Firefox, Safari, Edge)

---

### Backend Setup (Django)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/hitheshph7-ux/Finance-Tracker.git
   cd Finance-Tracker
   ```

2. **Create and Activate a Virtual Environment**
   ```bash
   # On macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate

   # On Windows:
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install django django-cors-headers
   ```

4. **Apply Database Migrations**
   ```bash
   python finance/manage.py migrate
   ```

5. **Start the Development Server**
   ```bash
   python finance/manage.py runserver
   ```

   The server will start at `http://127.0.0.1:8000/`.

---

## 📡 API Endpoints

### 🔑 Authentication & Users
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/register/` | Register a new user |
| `POST` | `/api/login/` | Authenticate and log in user |
| `GET` | `/api/users/` | Retrieve list of all registered users |
| `GET` | `/api/user/<username>/` | Fetch specific user details |

### 💵 Income Management
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/income/add/` | Add a new income record |
| `GET` | `/api/income/` | Fetch all income records |
| `GET` | `/api/income/<id>/` | Fetch income by ID |
| `PUT` | `/api/income/update/<id>/` | Update an existing income record |
| `DELETE` | `/api/income/delete/<id>/` | Delete an income record |

### 💸 Expense Management
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/expense/add/` | Add a new expense record |
| `GET` | `/api/expenses/` | Fetch all expense records |
| `GET` | `/api/expense/<id>/` | Fetch expense by ID |
| `PUT` | `/api/expense/update/<id>/` | Update an expense record |
| `DELETE` | `/api/expense/delete/<id>/` | Delete an expense record |

### 🏷️ Categories & History
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/category/add/` | Add a new expense category |
| `GET` | `/api/categories/` | Fetch all expense categories |
| `GET` | `/api/transactions/` | Retrieve combined income & expense history |

---

## 🛠️ Built With

- **Backend**: Python, Django 6.0, SQLite3
- **Frontend**: HTML5, CSS3, JavaScript (Fetch API)
- **CORS Support**: `django-cors-headers`

---

## 👨‍💻 Author

Developed by **[Hithesh](https://github.com/hitheshph7-ux)**.
