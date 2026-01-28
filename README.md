<div align="center">

# ⚗️ Chemical Equipment Parameter Visualizer

### *A Powerful Hybrid Web + Desktop Application for Chemical Engineering Analytics*

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://pypi.org/project/PyQt5/)

<img src="https://user-images.githubusercontent.com/placeholder/demo-animation.gif" width="600" alt="Demo Animation">

---

**[📖 Documentation](#-setup-instructions)** · **[🚀 Quick Start](#-quick-start)** · **[📊 Features](#-features)** · **[🔗 API](#-api-endpoints)**

</div>

---

## 🎯 What is This?

> Upload CSV files containing chemical equipment parameters and get **instant analytics**, **beautiful charts**, and **professional PDF reports** — all in a sleek dark-themed interface!

<table>
<tr>
<td width="50%">

### 🌐 Web Interface
- Modern React + Vite app
- Drag-and-drop file upload
- Interactive Chart.js visualizations
- Responsive design

</td>
<td width="50%">

### 🖥️ Desktop Interface
- Native PyQt5 application
- Embedded Matplotlib charts
- 4-tab analytics dashboard
- Mouse scroll zoom on charts

</td>
</tr>
</table>

---

## ✨ Features

<table>
<tr>
<td align="center" width="25%">
<img src="https://img.icons8.com/fluency/96/csv.png" width="48"><br>
<b>CSV Upload</b><br>
<sub>Drag & drop or browse</sub>
</td>
<td align="center" width="25%">
<img src="https://img.icons8.com/fluency/96/combo-chart.png" width="48"><br>
<b>8 Chart Types</b><br>
<sub>Bar, Pie, Scatter, Box, Radar...</sub>
</td>
<td align="center" width="25%">
<img src="https://img.icons8.com/fluency/96/analytics.png" width="48"><br>
<b>Live Analytics</b><br>
<sub>Stats cards & correlations</sub>
</td>
<td align="center" width="25%">
<img src="https://img.icons8.com/fluency/96/pdf.png" width="48"><br>
<b>PDF Reports</b><br>
<sub>Download professional reports</sub>
</td>
</tr>
</table>

### 📊 Analytics Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│  📈 Overview  │  🔗 Correlations  │  📊 Distributions  │  🏆 Compare  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │
│   │ 🔧 15    │ │ 💧 120.5 │ │ ⚡ 8.4   │ │ 🌡️ 118°  │         │
│   │ Equipment│ │ Avg Flow │ │ Max Press│ │ Avg Temp │         │
│   └──────────┘ └──────────┘ └──────────┘ └──────────┘         │
│                                                                 │
│   ┌─────────────────────────┐  ┌──────────────────┐            │
│   │                         │  │       🥧         │            │
│   │    📊 Bar Chart         │  │    Pie Chart     │            │
│   │   Flowrate & Pressure   │  │   Equipment Dist │            │
│   │                         │  │                  │            │
│   └─────────────────────────┘  └──────────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

<table>
<tr>
<th>Layer</th>
<th>Technology</th>
<th>Purpose</th>
</tr>
<tr>
<td>🔙 Backend</td>
<td><img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=django" height="20"> + DRF</td>
<td>REST API & Auth</td>
</tr>
<tr>
<td>💾 Database</td>
<td><img src="https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite" height="20"></td>
<td>Data Storage</td>
</tr>
<tr>
<td>🌐 Web</td>
<td><img src="https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black" height="20"> + <img src="https://img.shields.io/badge/Vite-646CFF?style=flat&logo=vite&logoColor=white" height="20"></td>
<td>Web Interface</td>
</tr>
<tr>
<td>🖥️ Desktop</td>
<td><img src="https://img.shields.io/badge/PyQt5-41CD52?style=flat&logo=qt" height="20"> + Matplotlib</td>
<td>Desktop App</td>
</tr>
<tr>
<td>📊 Charts</td>
<td><img src="https://img.shields.io/badge/Chart.js-FF6384?style=flat&logo=chartdotjs" height="20"> + Matplotlib</td>
<td>Data Visualization</td>
</tr>
</table>

---

## 📁 Project Structure

```
Fossee-2026/
├── 🔙 backend/                  # Django REST API
│   ├── config/                 # Settings & URLs
│   ├── api/                    # Models, Views, Serializers
│   └── requirements.txt
│
├── 🌐 web-frontend/            # React Web Application
│   ├── src/
│   │   ├── components/        # UI Components
│   │   ├── services/          # API Client
│   │   └── App.jsx
│   └── package.json
│
├── 🖥️ desktop-frontend/        # PyQt5 Desktop Application
│   ├── ui/                    # Charts, Login, Main Window
│   ├── services/              # API Client
│   └── main.py
│
└── 📄 sample_equipment_data.csv
```

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Version |
|-------------|---------|
| 🐍 Python | 3.9+ |
| 📦 Node.js | 18+ |
| 📂 Git | Latest |

### ⚡ One-Command Setup

```bash
# Clone the repo
git clone https://github.com/AnuranjanJain/fossee_si2026.git
cd fossee_si2026
```

<details>
<summary><b>📦 Backend Setup</b></summary>

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# 🚀 Start server
python manage.py runserver
```

> 🌐 API available at `http://localhost:8000/api/`

</details>

<details>
<summary><b>🌐 Web Frontend Setup</b></summary>

```bash
cd web-frontend

# Install dependencies
npm install

# 🚀 Start dev server
npm run dev
```

> 🌐 Web app at `http://localhost:5173/`

</details>

<details>
<summary><b>🖥️ Desktop Frontend Setup</b></summary>

```bash
cd desktop-frontend

# Install dependencies
pip install -r requirements.txt

# 🚀 Launch app
python main.py
```

</details>

---

## 🔐 Demo Credentials

<div align="center">

| Username | Password |
|:--------:|:--------:|
| `admin` | `admin123` |

</div>

---

## 📋 CSV Format

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120,5.2,110
Compressor-1,Compressor,95,8.4,95
Valve-1,Valve,60,4.1,105
HeatExchanger-1,HeatExchanger,150,6.2,130
```

> 💡 Use `sample_equipment_data.csv` to test!

---

## 🔗 API Endpoints

| Endpoint | Method | Description |
|----------|:------:|-------------|
| `/api/auth/login/` | `POST` | 🔓 User authentication |
| `/api/auth/logout/` | `POST` | 🔒 User logout |
| `/api/upload/` | `POST` | 📤 Upload CSV file |
| `/api/equipment/` | `GET` | 📋 List equipment |
| `/api/summary/` | `GET` | 📊 Get statistics |
| `/api/history/` | `GET` | 📜 Upload history |
| `/api/report/pdf/` | `GET` | 📄 Download PDF |

---

## 🎨 UI Highlights

<table>
<tr>
<td align="center">
<b>🌙 Dark Theme</b><br>
<sub>Easy on the eyes</sub>
</td>
<td align="center">
<b>💜 Purple Accents</b><br>
<sub>Modern gradient buttons</sub>
</td>
<td align="center">
<b>🔍 Scroll Zoom</b><br>
<sub>Zoom charts with mouse</sub>
</td>
<td align="center">
<b>✨ Ripple Effects</b><br>
<sub>Smooth button animations</sub>
</td>
</tr>
</table>

---

## 🧪 Development

```bash
# Run tests
cd backend && python manage.py test api

# Build for production
cd web-frontend && npm run build        # Web
cd desktop-frontend && pyinstaller --onefile main.py  # Desktop
```

---

## 📜 License

<div align="center">

Created for **FOSSEE Intern Screening Task 2026**

Made with ❤️ by [AnuranjanJain](https://github.com/AnuranjanJain)

[![GitHub](https://img.shields.io/badge/GitHub-AnuranjanJain-181717?style=for-the-badge&logo=github)](https://github.com/AnuranjanJain/fossee_si2026)

</div>
