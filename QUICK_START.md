# Quick Start Guide - CORE Engineer Training Portal

## Step 1: Install Dependencies

Make sure you have Python 3.8+ installed, then:

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

## Step 2: Initialize Database

Run this once to create sample users and tickets:

```bash
python src/init_data.py
```

This will create:
- 1 Admin account
- 4 Engineer accounts
- 4 Sample dispatch cases with training scenarios

## Step 3: Run the Application

```bash
streamlit run src/app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## Step 4: Login and Explore

### Try the Admin View
1. Login with: `admin` / `admin123`
2. Explore the Dashboard to see all tickets
3. Create a new dispatch case from "Create Dispatch Case"
4. Manage tickets from "Manage Tickets"
5. Try the "Assign back Reported" feature

### Try the Engineer View
1. Logout and login with: `engineer1` / `eng123`
2. View your assigned tickets
3. Add replies to communicate
4. Try escalating a ticket to SEG
5. Practice the workflow!

## Ticket Workflow

```
Created (Admin)
    ↓
Assigned to CORE (Admin assigns to Engineer)
    ↓
Engineer works on ticket → Can Escalate to SEG
    ↓
Escalated to SEG (Admin can review)
    ↓
Assign back Reported (Admin action)
    ↓
Assign Back to CORE (Engineer action)
    ↓
Resolved → Closed
```

## Features Overview

### Admin Features
- **Dashboard**: Overview of all tickets and statistics
- **Create Dispatch Case**: Create new training scenarios for engineers
- **Manage Tickets**:
  - Filter by status and priority
  - Assign tickets to engineers
  - Handle escalations with "Assign back Reported"
  - View ticket history and conversation

### Engineer Features
- **My Tickets**: View all assigned tickets
- **Reply & Send Details**: Communicate findings and ask questions
- **Escalate to SEG**: Escalate complex issues to admin/SEG
- **Assign Back to CORE**: Re-assign tickets from reported status

## Tips for Training

1. **For Admins**: Create realistic scenarios that mirror actual support cases
2. **For Engineers**:
   - Practice clear communication
   - Document your troubleshooting steps
   - Know when to escalate
   - Use the reply feature to show your thought process

## Troubleshooting

**App won't start?**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're in the virtual environment

**Can't login?**
- Make sure you ran `python src/init_data.py` to create users
- Try the default credentials: `admin` / `admin123`

**Database errors?**
- Delete `data/tickets.db` and re-run `python src/init_data.py`

## Customization

- Modify scenarios in [src/init_data.py](src/init_data.py)
- Adjust theme colors in [.streamlit/config.toml](.streamlit/config.toml)
- Add more ticket statuses in [src/database.py](src/database.py)

## Support

For issues or questions, refer to the main [README.md](README.md) or contact your system administrator.
