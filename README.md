
## 📊 FinanceApp – Personal Finance Tracker

FinanceApp is a Django-based web application that allows users to track their income and expenses, view insightful reports, and forecast future expenses using machine learning.

---

### 🚀 Features

* ✅ **User Authentication** (Register, Login, Logout)
* ✅ **Add Income and Expenses**
* ✅ **Dashboard** with Total Income, Expense, and Savings
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

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/financeapp.git
   cd financeapp
   ```

2. **Create and Activate Virtual Environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Server**

   ```bash
   python manage.py runserver
   ```

7. Open your browser and go to:
   **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

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
> URL: `http://127.0.0.1:8000/admin`

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

### 📦 Requirements (sample `requirements.txt`)

```txt
Django>=4.2
pandas
numpy
scikit-learn
matplotlib
```


