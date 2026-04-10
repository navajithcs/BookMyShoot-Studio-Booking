# 🚀 BookMyShoot - Running the Application

## Quick Start

### Option 1: Batch File (Easiest for Windows)
Simply double-click:
```
run.bat
```

### Option 2: PowerShell Script
```powershell
.\run.ps1
```

### Option 3: Python Script
```bash
python run.py
```

### Option 4: Manual Start

**Terminal 1 - Start Backend:**
```bash
cd backend
C:/Users/navaj/OneDrive/Desktop/main_project/.venv/Scripts/python.exe app.py
```

**Terminal 2 - Start Frontend:**
```bash
C:/Users/navaj/OneDrive/Desktop/main_project/.venv/Scripts/python.exe serve_frontend.py
```

---

## 🌐 Access the Application

Once both servers are running:

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000

---

## Deleting a remote MySQL/MariaDB database (optional)

If you previously used a remote MySQL/MariaDB instance and want to permanently
delete the `bookmyshoot` database, a helper script is available at
`backend/drop_database.py`.

Run it like this (it will ask for confirmation):

```bash
# set password via env var (optional)
export MYSQL_PASSWORD='your_db_password'
python backend/drop_database.py --user root --host localhost
```

Or on Windows PowerShell:

```powershell
$env:MYSQL_PASSWORD = 'your_db_password'
python backend\drop_database.py --user root --host localhost
```

WARNING: This permanently deletes the database and cannot be undone.

---

## 📋 What Gets Started

### Backend (Flask)
- Runs on `http://localhost:5000`
- Provides REST API endpoints
- Handles authentication, bookings, payments, etc.
- Database: SQLite (bookmyshoot.db)

### Frontend (HTTP Server)
- Runs on `http://localhost:5173`
- Serves static HTML/CSS/JS files
- Single page application

---

## 🛑 Stopping the Application

### If using batch/PowerShell/Python scripts:
- Close the command windows
- Or press Ctrl+C in the terminal

### For manual start:
- Close each terminal or press Ctrl+C in each

---

## ⚠️ Troubleshooting

**Port Already in Use?**
Edit the scripts to use different ports:
- Frontend: Change port 5173 in `serve_frontend.py`
- Backend: Change port 5000 in `backend/app.py`

**Virtual Environment Issues?**
Activate it manually first:
```powershell
.venv\Scripts\Activate.ps1
```

**Missing Dependencies?**
Install them:
```bash
python -m pip install -r backend/requirements.txt
```

---

## 📁 Project Structure

```
main_project/
├── backend/           # Flask backend
│   ├── app.py
│   ├── models.py
│   ├── config.py
│   └── requirements.txt
├── frontend/          # Static frontend files
│   ├── index.html
│   ├── css/
│   └── js/
├── run.py            # Python startup script
├── run.bat           # Batch startup script
├── run.ps1           # PowerShell startup script
└── serve_frontend.py # Frontend HTTP server
```

---

## 🎯 API Endpoints

See `DATABASE_SETUP.md` for the complete API documentation.

Popular endpoints:
- `POST /api/register` - Register user
- `POST /api/login` - Login user
- `GET /api/photographers` - List photographers
- `POST /api/bookings` - Create booking
- `POST /api/payments` - Process payment

---

**Happy Coding! 🎉**
