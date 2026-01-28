# Chemical Equipment Parameter Visualizer

A hybrid Web + Desktop application for visualizing and analyzing chemical equipment parameters. Upload CSV files containing equipment data and get instant analytics, charts, and PDF reports.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![React](https://img.shields.io/badge/React-18-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15-orange.svg)

## Features

- **CSV Upload** - Upload equipment data via Web or Desktop interface
- **Data Analytics** - Automatic calculation of averages, min/max, and distributions
- **Interactive Charts** - Bar and pie charts using Chart.js (Web) and Matplotlib (Desktop)
- **History Management** - Keep track of last 5 uploaded datasets
- **PDF Reports** - Generate and download professional PDF reports
- **Authentication** - Token-based authentication for secure access

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Backend | Django + DRF | REST API |
| Database | SQLite | Data storage |
| Web Frontend | React + Vite + Chart.js | Web interface |
| Desktop Frontend | PyQt5 + Matplotlib | Desktop interface |
| Data Processing | Pandas | CSV parsing & analytics |
| PDF Generation | ReportLab | Report generation |

## Project Structure

```
Fossee-2026/
├── backend/                 # Django REST API
│   ├── config/             # Django settings
│   ├── api/                # API app (models, views, serializers)
│   └── requirements.txt
├── web-frontend/           # React Web Application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API client
│   │   └── App.jsx
│   └── package.json
├── desktop-frontend/       # PyQt5 Desktop Application
│   ├── ui/                # UI components
│   ├── services/          # API client
│   ├── main.py
│   └── requirements.txt
└── sample_equipment_data.csv
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 18+ and npm
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Fossee-2026.git
cd Fossee-2026
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (for demo: admin/admin123)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

### 3. Web Frontend Setup

```bash
cd web-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The web app will be available at `http://localhost:5173/`

### 4. Desktop Frontend Setup

```bash
cd desktop-frontend

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Usage

### Demo Credentials
- **Username:** admin
- **Password:** admin123

### Steps
1. Start the backend server
2. Launch either the Web or Desktop frontend
3. Login with the demo credentials
4. Upload a CSV file (use `sample_equipment_data.csv` for testing)
5. View data in the table, charts, and download PDF reports

### Expected CSV Format

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120,5.2,110
Compressor-1,Compressor,95,8.4,95
Valve-1,Valve,60,4.1,105
...
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/login/` | POST | User authentication |
| `/api/auth/logout/` | POST | User logout |
| `/api/upload/` | POST | Upload CSV file |
| `/api/equipment/` | GET | List equipment |
| `/api/summary/` | GET | Get summary statistics |
| `/api/history/` | GET | Get upload history |
| `/api/report/pdf/` | GET | Download PDF report |

## Screenshots

### Web Application
- Modern dark theme with gradient accents
- Drag-and-drop file upload
- Interactive Chart.js visualizations
- Responsive design

### Desktop Application
- Native PyQt5 interface
- Embedded Matplotlib charts
- Tab-based navigation
- Native file dialogs

## Development

### Running Tests

```bash
cd backend
python manage.py test api
```

### Building for Production

**Web:**
```bash
cd web-frontend
npm run build
```

**Desktop:**
```bash
cd desktop-frontend
pyinstaller --onefile main.py
```

## License

This project is created for the FOSSEE Intern Screening Task 2026.

## Author

Created as part of the FOSSEE Internship application.
