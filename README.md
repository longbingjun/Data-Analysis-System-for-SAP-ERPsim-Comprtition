
# ERP Competition Data Analysis System

> A Django-based data analytics system built for **ERPsim competitions**, providing automated sales analysis, profit insights, and intelligent inventory recommendations.

🏆 **Competition Proven**:
This system was developed during the **ERPsim INTERNATIONAL Competition 2025** and contributed to the team achieving **International 3rd Place**.

---

## 🚀 Features

* 📊 **Excel Import & Export** (Market & Team Sales Data)
* 📈 **Market Sales Trend Analysis** (by round & region)
* 💰 **Product Profit Analysis** (cost-based pricing support)
* 📍 **Regional Preference Insights**
* 📦 **Intelligent Inventory Allocation Recommendations**
* 📉 **Team vs Market Price Comparison**
* 📊 **Interactive Data Visualization (Charts & Dashboards)**

---

## 🧠 Why This Project?

ERPsim competitions generate large volumes of sales and market data under time pressure.
This project helps teams:

* Quickly transform raw Excel data into actionable insights
* Optimize pricing and inventory strategies
* Make data-driven decisions during competitive rounds

---

## 🛠 Tech Stack

| Layer           | Technology                       |
| --------------- | -------------------------------- |
| Backend         | Django 5.1.6                     |
| Database        | MySQL                            |
| Admin UI        | Django Admin + SimpleUI          |
| Data Processing | pandas                           |
| Import / Export | django-import-export             |
| Visualization   | JavaScript (custom admin charts) |

---

## 📁 Project Structure

```
ERP/
├── ERP/                # Project configuration
├── ErpSim/             # Core application logic
├── datasets/           # Competition datasets (Excel)
├── templates/          # Custom admin templates
├── manage.py
└── README.md
```

---

## 🔑 Core Modules

### 📊 Data Import & Export

* Batch Excel upload/download
* Fast ingestion of market & team sales data

### 📈 Market Sales Analysis

* Sales trends by round
* Product-level sales volume & revenue
* Regional demand comparison

### 📉 Team Sales Analysis

* Team vs market price comparison
* Pricing strategy evaluation

### 📦 Intelligent Inventory Allocation

* Data-driven inventory distribution recommendations
* Improved turnover and sales efficiency

### 💰 Profit Analysis

* Cost-based profit calculation
* Pricing decision support

### 📊 Visualization

* Sales trends by round
* Product price comparison charts
* Regional preference charts

---

## 🧱 Data Models (Simplified)

### MarketSalesData

* date
* material_description
* area
* qty
* value
* price

### GroupSalesData

* round
* day
* area
* sloc
* distribution_channel
* material
* material_description
* price
* qty
* value
* cost

---

## ⚙️ Installation

### Requirements

* Python 3.8+
* MySQL 5.7+
* Django 5.1.6+

### Setup

```bash
git clone <repository-url>
cd ERP
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS / Linux
pip install -r requirements.txt
```

### Database Configuration

1. Create MySQL database: `erp_analysis`
2. Update database settings in `ERP/settings.py`

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 📘 Usage

### Import Data

1. Login to admin panel
2. Navigate to Market / Team Sales Data
3. Upload Excel files
4. Data is automatically parsed and stored

### Analyze

* View dashboards and charts
* Compare team pricing vs market trends
* Review inventory and pricing recommendations

### Export

* Export data in Excel / CSV format directly from admin panel

---

## 🌟 Highlights

* 🏆 **International Competition Proven**
* 🤖 Automated analytics & decision support
* 📊 Clear visual insights
* ⚡ Fast Excel batch processing
* 🧩 Modular & extensible Django architecture

---

## 🤝 Contributing

Contributions are welcome!

```bash
git checkout -b feature/your-feature
git commit -m "Add new feature"
git push origin feature/your-feature
```

Then open a Pull Request 🚀

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

## 📬 Contact

* **Author**: Bingjun Long
* **Email**: [bingjunlong@link.cuhk.edu.cn](mailto:bingjunlong@link.cuhk.edu.cn)
* **Achievement**: ERPsim INTERNATIONAL Competition 2025 — **International 3rd Place**

---

⭐ *If you find this project useful, feel free to give it a star!*

