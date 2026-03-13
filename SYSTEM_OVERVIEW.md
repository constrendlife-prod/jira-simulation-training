# CORE Engineer Training Portal - System Overview

## 🎯 Purpose
A Jira-style ticketing simulation system where CORE Engineers practice ticket resolution, communication, and escalation workflows. The system uses a simplified 2-role model where administrators can act as both Reporters and RD personnel.

---

## 👥 Two-Role System

### 1. **Admin Role** (Instructors/Evaluators)
**Login Accounts:**
- `admin` / `admin123` (System Administrator)
- `admin2` / `admin123` (SEG Administrator)

**Capabilities:**
- Create dispatch cases with training scenarios
- Assign tickets to CORE engineers
- View all tickets and filter by status/priority
- Reply as **"Admin"** (blue bubbles) or **"RD"** (green bubbles)
- Control ticket workflow (assign, reassign, mark resolved)
- Act as both Reporter (case creator) and RD (technical expert)

### 2. **Engineer Role** (Trainees)
**Login Accounts:**
- `engineer1` / `eng123` (John Smith)
- `engineer2` / `eng123` (Sarah Johnson)
- `engineer3` / `eng123` (Mike Chen)
- `engineer4` / `eng123` (Emily Davis)

**Capabilities:**
- View assigned tickets with training scenarios
- Reply as **"Engineer"** (purple bubbles) or **"RD"** (green bubbles)
- Practice both regular support AND advanced technical analysis
- Escalate tickets to Admin/RD
- Reassign tickets based on workflow

---

## 💬 Chat System with Role Selection

### Color-Coded Messages:
- **Blue Bubble (Admin)** - Administrative communication
- **Purple Bubble (Engineer)** - Regular engineer responses
- **Green Bubble (RD)** - Advanced technical guidance/analysis

### How It Works:
1. When replying, users select their reply role from dropdown
2. **Admin** can choose: "Admin" or "RD (Advanced Technical Guidance)"
3. **Engineer** can choose: "Engineer" or "RD (Advanced Technical Guidance)"
4. The message appears in a color-coded chat bubble based on selected role
5. This allows engineers to practice thinking at different technical levels

---

## 🔄 Ticket Workflow

### Complete Lifecycle:

```
┌──────────────────────────────────────────────────────────────┐
│  ADMIN CREATES CASE                                          │
│  - Assigns Reporter (Admin)                                  │
│  - Assigns CORE Engineer (Trainee)                           │
│  Status: "Assigned to CORE"                                  │
└──────────────────────────────────────────────────────────────┘
                         ↓
┌──────────────────────────────────────────────────────────────┐
│  ENGINEER WORKS ON TICKET                                    │
│  - Reads training scenario                                   │
│  - Adds replies (as "Engineer")                              │
│  - Can escalate if needed                                    │
└──────────────────────────────────────────────────────────────┘
                         ↓
         ┌───────────────┴───────────────┐
         │                               │
    Can Solve?                      Too Complex?
         │                               │
         NO                             YES
         │                               │
         ↓                               ↓
┌─────────────────┐            ┌──────────────────────┐
│ Escalate to RD  │            │ Work on it normally  │
│ Status:         │            │ Add Engineer replies │
│ "Escalated to   │            │                      │
│  RD"            │            │ Mark Resolved        │
└─────────────────┘            └──────────────────────┘
         ↓
┌──────────────────────────────────────────────────────────────┐
│  ADMIN REVIEWS ESCALATION                                    │
│  - Can reply as "RD" with technical guidance (green bubble)  │
│  - Can send back to CORE or Reporter                         │
└──────────────────────────────────────────────────────────────┘
         ↓
   ┌─────┴──────┐
   │            │
Back to CORE  Back to Reporter
   │            │
   ↓            ↓
Engineer    Need more info
continues   from customer
   │
   ↓
Resolved → Closed
```

---

## 📊 Ticket Statuses

| Status | Description | Who Can Set |
|--------|-------------|-------------|
| **Open** | Ticket created, not assigned | Admin |
| **Assigned to CORE** | CORE Engineer working on it | Admin |
| **Escalated to RD** | Engineer needs RD help | Engineer |
| **Assigned back to Reporter** | Need clarification from reporter | Admin (as RD) |
| **Assigned back to CORE** | RD provided guidance, engineer continues | Admin (as RD) |
| **Resolved** | Issue solved | Admin |
| **Closed** | Case complete | Admin |

---

## 🎨 Features

### Admin Dashboard
- **Statistics**: Total tickets, active, escalated to RD, resolved
- **Recent Tickets**: Quick view of latest 10 tickets
- **Filters**: Status and priority filtering
- **Actions**: Assign to CORE, Back to CORE, Back to Reporter, Mark Resolved
- **Chat**: Reply as Admin or RD with color-coded bubbles
- **Refresh Button**: Update view without page reload

### Create Dispatch Case
- **Ticket Details**: Title, description, training scenario
- **Priority**: Low, Medium, High, Critical
- **Assignment**: Select Reporter (Admin) and CORE Engineer
- **Auto-numbering**: Tickets numbered as CORE-0001, CORE-0002, etc.

### Engineer Dashboard
- **Statistics**: Total assigned, active, escalated
- **Assigned Tickets**: Only tickets assigned to logged-in engineer
- **Chat**: Reply as Engineer or RD with color-coded bubbles
- **Actions**: Send Reply, Escalate to RD, Back to CORE
- **Refresh Button**: Update view without page reload

### Conversation System
- **Chat-like interface** with message bubbles
- **Timestamps** on all messages
- **Role badges** showing who sent the message
- **Automatic updates** when new messages sent
- **Message history** preserved for training review

---

## 🚀 Training Value

### For CORE Engineers:
1. **Practice Communication** - Learn to document findings clearly
2. **Decision Making** - Know when to escalate vs. continue working
3. **Dual-Role Thinking** - Practice both support and advanced technical analysis
4. **Workflow Mastery** - Understand ticket lifecycle and handoffs
5. **Professional Skills** - Real-world ticketing system experience

### For Admins/Instructors:
1. **Create Realistic Scenarios** - Build training cases based on real issues
2. **Provide Guidance** - Reply as RD when engineers need help
3. **Monitor Progress** - See all communication and decision-making
4. **Control Workflow** - Guide tickets through appropriate statuses
5. **Evaluate Skills** - Review conversation history and audit trail

---

## 📁 File Structure

```
src/
├── app.py              # Main Streamlit application
├── database.py         # Database models and operations
├── init_data.py        # Sample data initialization
├── config.py           # Configuration (if needed)

data/
├── tickets.db          # SQLite database (auto-created)

.streamlit/
├── config.toml         # Jira-like theme configuration
```

---

## 🔧 Key Functions

### Database Operations
- `create_user()` - Create admin or engineer accounts
- `create_ticket()` - Create new dispatch case
- `add_ticket_reply()` - Add message with role selection
- `update_ticket_status()` - Change ticket status
- `get_tickets_by_user()` - Get engineer's assigned tickets
- `get_all_tickets()` - Get all tickets (admin view)

### UI Components
- `render_chat_message()` - Display color-coded chat bubbles
- `admin_dashboard()` - Admin overview and ticket management
- `admin_create_ticket()` - Dispatch case creation form
- `admin_manage_tickets()` - Detailed ticket management with filters
- `engineer_dashboard()` - Engineer's assigned tickets view

---

## 🎓 Training Scenarios Included

1. **Email Access Issues** (High Priority)
   - Assigned to: John Smith
   - Reporter: SEG Administrator
   - Focus: Authentication troubleshooting

2. **Network Connectivity** (Critical Priority)
   - Assigned to: Sarah Johnson
   - Reporter: System Administrator
   - Focus: Infrastructure diagnostics

3. **Software Installation** (Medium Priority)
   - Unassigned
   - Reporter: SEG Administrator
   - Focus: Project planning and communication

4. **VPN Connection Failures** (High Priority)
   - Unassigned
   - Reporter: System Administrator
   - Focus: Remote access troubleshooting

---

## 💡 Best Practices

### For Creating Dispatch Cases:
1. Write clear, realistic scenarios
2. Include expected troubleshooting steps
3. Set appropriate priority levels
4. Assign to specific engineers for targeted training

### For Engineers:
1. Read the entire scenario before responding
2. Reply as "Engineer" for initial investigation
3. Switch to "RD" role when providing advanced technical analysis
4. Escalate when genuinely stuck or need guidance
5. Document your thought process in replies

### For Admins:
1. Reply as "Admin" for workflow guidance
2. Reply as "RD" for technical/architectural guidance
3. Use "Back to Reporter" when requirements are unclear
4. Use "Back to CORE" when RD has provided sufficient guidance

---

## 🌐 Deployment Ready

The application is ready to deploy to:
- **Streamlit Cloud** (recommended, free)
- **Azure App Services**
- **Heroku**
- **AWS / GCP**
- Any platform supporting Python + Streamlit

Simply push to GitHub and connect to Streamlit Cloud for instant web hosting!

---

## 📞 Support

For issues or questions:
- Check [QUICK_START.md](QUICK_START.md) for setup help
- See [RUN_INSTRUCTIONS.md](RUN_INSTRUCTIONS.md) for platform-specific commands
- Review [README.md](README.md) for project overview
