
## 📊 FinanceApp – Personal Finance Tracker

FinanceApp is a Django-based web application that allows users to track their income and expenses, view insightful reports, and forecast future expenses using machine learning.

---

### 🚀 Features

* ✅ **User Authentication** (Register, Login, Logout)
* ✅ **Add Income and Expenses**
* ✅ **Dashboard** with Total Income, Expense, and Savings
* ✅ **Dynamic Income/Expense Categories** Can be added/removed/edited on admin panel 
* ✅ **Expense Forecasting** using Linear Regression
* ✅ **Monthly & Yearly Reports**
* ✅ **Set Monthly Budgets** per user
* ✅ **Budget Alerts** when expenses exceed set budgets
* ✅ **Edit Budgets** directly from reports
* ✅ Responsive UI using Bootstrap

---

### 🛠️ Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML, CSS, Bootstrap
* **Database:** SQLite
* **Visualization:** Chart.js
* **ML Forecasting:** scikit-learn, pandas, numpy

---

### 🧩 Installation Instructions

1. **Clone the Repository, Delete db file**

   ```bash
   git clone https://github.com/GGurol/personal-finance-management.git
   cd personal-finance-management
   sudo rm db.sqlite3
   ```

2. **Create and Build Docker Environment**

   ```bash
   docker compose up --build -d
   ```

3. **Apply Migrations**

   ```bash
   docker compose exec web python manage.py makemigrations
   docker compose exec web python manage.py migrate
   ```

4. **Create Superuser**

   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

5. Open your browser and go to:
   **[http://localhost:8000/](http://localhost:8000/)**

---

### 📈 Forecasting Feature

* Uses linear regression to predict next **3 months’** expenses.
* Accessible from dashboard via **View Forecast** button.
* Requires minimum **2 months** of expense data to work.

---

### 🧾 Reports and Budget

* Monthly report table shows:

  * Income
  * Expenses
  * Savings
  * Budget
* Over-budget months are **highlighted in red**
* You can **edit monthly budgets** from the report table

---

### ✅ Sample Admin Login

> Use after running `createsuperuser`
> URL: `http://localhost:8000/admin`

---

### 📂 Directory Structure

```
financeapp/
├── finance/           # Main Django app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/     # HTML templates
│   └── ...
├── financeapp/        # Project settings
├── db.sqlite3
└── manage.py
```

---

### 📦 Requirements (`requirements.txt`)

```txt
Django~=5.2
django-extensions
gunicorn
pandas
scikit-learn
matplotlib
numpy
```


