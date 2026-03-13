# How to Run the CORE Engineer Training Portal

## For Windows (Command Prompt / PowerShell)

### Step 1: Open Command Prompt
- Press `Win + R`
- Type `cmd` and press Enter

### Step 2: Navigate to Project Folder
```cmd
cd "C:\path\to\Jira - Simulation Program"
```
Replace `C:\path\to\` with your actual folder location.

### Step 3: Create Virtual Environment (First Time Only)
```cmd
python -m venv venv
```

### Step 4: Activate Virtual Environment
```cmd
venv\Scripts\activate
```
You should see `(venv)` at the beginning of your command prompt.

### Step 5: Install Dependencies (First Time Only)
```cmd
pip install -r requirements.txt
```

### Step 6: Initialize Database (First Time Only)
```cmd
python src\init_data.py
```

### Step 7: Run the Application
```cmd
streamlit run src\app.py
```

The application will automatically open in your browser at `http://localhost:8501`

### To Stop the Application:
Press `Ctrl + C` in the command prompt

### Next Time You Run:
You only need to do steps 2, 4, and 7:
```cmd
cd "C:\path\to\Jira - Simulation Program"
venv\Scripts\activate
streamlit run src\app.py
```

---

## For Ubuntu/Linux/Mac (Terminal)

### Step 1: Open Terminal
- Ubuntu: Press `Ctrl + Alt + T`
- Mac: Press `Cmd + Space`, type "Terminal"

### Step 2: Navigate to Project Folder
```bash
cd /home/joshuaav/Jira\ -\ Simulation\ Program
```
Or use your actual path:
```bash
cd ~/Jira\ -\ Simulation\ Program
```

### Step 3: Create Virtual Environment (First Time Only)
```bash
python3 -m venv venv
```

### Step 4: Activate Virtual Environment
```bash
source venv/bin/activate
```
You should see `(venv)` at the beginning of your terminal prompt.

### Step 5: Install Dependencies (First Time Only)
```bash
pip install -r requirements.txt
```

### Step 6: Initialize Database (First Time Only)
```bash
python src/init_data.py
```

### Step 7: Run the Application
```bash
streamlit run src/app.py
```

The application will automatically open in your browser at `http://localhost:8501`

### To Stop the Application:
Press `Ctrl + C` in the terminal

### Next Time You Run:
You only need to do steps 2, 4, and 7:
```bash
cd ~/Jira\ -\ Simulation\ Program
source venv/bin/activate
streamlit run src/app.py
```

---

## Quick Start Script

### For Windows - Create a file named `start.bat`:
```batch
@echo off
cd /d "%~dp0"
call venv\Scripts\activate
streamlit run src\app.py
pause
```
Double-click `start.bat` to run the application.

### For Linux/Mac - Create a file named `start.sh`:
```bash
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
streamlit run src/app.py
```
Make it executable and run:
```bash
chmod +x start.sh
./start.sh
```

---

## Troubleshooting

### Issue: "python: command not found" (Linux/Mac)
Try using `python3` instead:
```bash
python3 -m venv venv
```

### Issue: "pip: command not found"
Make sure you activated the virtual environment first.

### Issue: "streamlit: command not found"
Make sure dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Port 8501 already in use
Kill the existing process:
- **Windows**: Open Task Manager, find Python, End Task
- **Linux/Mac**:
```bash
lsof -ti:8501 | xargs kill -9
```

### Issue: Database errors
Delete the database and reinitialize:
```bash
rm -f data/tickets.db
python src/init_data.py
```

---

## Access the Application

Once running, open your browser and go to:
- **Local URL**: http://localhost:8501
- **Network URL**: http://YOUR_IP:8501 (for access from other devices)

### Login Credentials:
- **Admin**: `admin` / `admin123`
- **Engineer**: `engineer1` / `eng123`

---

## Deploy to Web (Optional)

### Deploy to Streamlit Cloud (Free):
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub repository
4. Deploy!

Your app will be available at: `https://yourapp.streamlit.app`
