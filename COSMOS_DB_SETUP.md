# 🌐 Azure Cosmos DB Setup Guide (FREE Tier)

## Step-by-step guide to create and configure Azure Cosmos DB for your CORE Engineer Training Portal

---

## 🎯 What You're Setting Up

**Azure Cosmos DB FREE Tier:**
- 1000 RU/s (Request Units per second) - FREE
- 25 GB storage - FREE
- Perfect for your training portal
- Handles 1000s of tickets easily

---

## 📋 Step 1: Create Cosmos DB Account in Azure Portal

### 1. Navigate to Azure Portal
```
URL: https://portal.azure.com
```

### 2. Create Resource
- Click **"+ Create a resource"** (top left)
- In search box, type: **"Azure Cosmos DB"**
- Click **"Azure Cosmos DB"** from results
- Click **"Create"**

### 3. Select API
- Select **"Azure Cosmos DB for NoSQL"** (Core SQL API)
- Click **"Create"**

---

## 📋 Step 2: Configure Your Cosmos DB

### **Basics Tab**

| Field | Value | Notes |
|-------|-------|-------|
| **Subscription** | Your subscription | Select from dropdown |
| **Resource Group** | `rg-jira-training` | Create new or use existing |
| **Account Name** | `cpdt-training-db` | ⚠️ Must be globally unique |
| **Location** | East US / Southeast Asia | Choose closest region |
| **Capacity mode** | **Serverless** | ⭐ REQUIRED for free tier |
| **Apply Free Tier Discount** | **YES** | ⭐ CHECK THIS BOX! |
| **Limit total account throughput** | Unchecked | Not needed for serverless |

**⚠️ CRITICAL:**
- **Capacity mode MUST be "Serverless"**
- **"Apply Free Tier Discount" MUST be checked**
- Without these, you'll be charged!

### **Global Distribution Tab**
- **Geo-Redundancy:** Disabled (to save costs)
- **Multi-region Writes:** Disabled (to save costs)

### **Networking Tab**
- **Connectivity method:** **All networks**
  - ✅ Easiest option (allows Streamlit Cloud)
  - OR **Public endpoint (selected networks)** (more secure, but need to add Streamlit IPs)

### **Backup Policy Tab**
- **Backup storage redundancy:** Locally-redundant
- Leave other defaults

### **Encryption Tab**
- Leave all defaults

### **Tags Tab** (Optional)
- Add tags for organization:
  - `Environment`: `Production`
  - `Project`: `CORE-Training`
  - `Owner`: `joshua_avila@trendmicro.com`

---

## 📋 Step 3: Review and Create

1. Click **"Review + create"**
2. **VERIFY these settings:**
   - ✅ Capacity mode: **Serverless**
   - ✅ Apply Free Tier Discount: **Yes**
   - ✅ Estimated cost: **Free**

3. Click **"Create"**
4. **Wait 3-5 minutes** for deployment

---

## 📋 Step 4: Create Database and Containers

### Navigate to Data Explorer

1. Deployment complete → Click **"Go to resource"**
2. In left menu, click **"Data Explorer"**

### Create Database

1. Click **"New Container"** button
2. Select **"Create new database"**
3. Enter:
   - **Database id:** `JiraTraining`
4. **Do NOT check** "Share throughput across containers" (serverless doesn't use this)

### Create Container 1: Users

**Container Settings:**
- **Database id:** Use existing `JiraTraining`
- **Container id:** `Users`
- **Partition key:** `/username`
- Click **"OK"**

**What this stores:**
- User accounts (Admin, Engineers)
- Authentication data
- User profiles

### Create Container 2: Tickets

Click **"New Container"** again:
- **Database id:** Use existing `JiraTraining`
- **Container id:** `Tickets`
- **Partition key:** `/ticket_number`
- Click **"OK"**

**What this stores:**
- All tickets (CPDT-0001, CPDT-0002, etc.)
- Ticket details, status, priority
- Assignments (Reporter, CORE Engineer)

### Create Container 3: TicketHistory

Click **"New Container"** again:
- **Database id:** Use existing `JiraTraining`
- **Container id:** `TicketHistory`
- **Partition key:** `/ticket_id`
- Click **"OK"**

**What this stores:**
- Audit trail
- Status changes
- Assignment history

### Create Container 4: TicketReplies

Click **"New Container"** again:
- **Database id:** Use existing `JiraTraining`
- **Container id:** `TicketReplies`
- **Partition key:** `/ticket_id`
- Click **"OK"**

**What this stores:**
- All conversations
- Replies from Reporter, RD, Engineers
- Chat history

---

## 📋 Step 5: Get Connection Credentials

### Get Your Keys

1. In left menu, click **"Keys"**
2. You'll see a screen with credentials

### Copy These Values:

**You need 3 values:**

1. **URI (Endpoint):**
   ```
   https://cpdt-training-db.documents.azure.com:443/
   ```
   ⚠️ Your account name will be different!

2. **PRIMARY KEY:**
   ```
   Very long string like:
   abc123def456ghi789jkl012mno345pqr678stu901vwx234yz==
   ```
   ⚠️ Keep this SECRET! Don't share publicly!

3. **DATABASE NAME:**
   ```
   JiraTraining
   ```

### Save These Securely

**Add to your local `.env` file:**
```bash
COSMOSDB_ENDPOINT=https://YOUR-ACCOUNT-NAME.documents.azure.com:443/
COSMOSDB_KEY=YOUR_PRIMARY_KEY_HERE
COSMOSDB_DATABASE_NAME=JiraTraining
STORAGE_BACKEND=cosmosdb
```

**For Streamlit Cloud Secrets:**
```toml
COSMOSDB_ENDPOINT = "https://YOUR-ACCOUNT-NAME.documents.azure.com:443/"
COSMOSDB_KEY = "YOUR_PRIMARY_KEY_HERE"
COSMOSDB_DATABASE_NAME = "JiraTraining"
STORAGE_BACKEND = "cosmosdb"
```

---

## 📋 Step 6: Verify Setup

### Check in Azure Portal

1. Go to **Data Explorer**
2. Expand **JiraTraining** database
3. You should see 4 containers:
   - ✅ Users
   - ✅ Tickets
   - ✅ TicketHistory
   - ✅ TicketReplies

### Test Locally

```bash
cd "/home/joshuaav/Jira - Simulation Program"
source venv/bin/activate

# Make sure .env has STORAGE_BACKEND=cosmosdb
python src/init_data.py
```

**Expected Output:**
```
Using Cosmos DB backend
Creating containers...
Initializing sample data...
✅ Success!
```

---

## 🔒 Security Best Practices

### Firewall Rules (Optional - More Secure)

1. In Cosmos DB account, click **"Firewall and virtual networks"**
2. Select **"Selected networks"**
3. Add:
   - Your office IP
   - Your home IP
   - Streamlit Cloud IP ranges (contact Streamlit support for IPs)

### Rotate Keys Regularly

- Go to **"Keys"** → **"Regenerate keys"**
- Update in `.env` and Streamlit secrets
- Recommended: Every 90 days

### Use Read-Only Keys for Reporting

- **Primary Key:** Full access (use for app)
- **Read-Only Key:** View-only (use for analytics)

---

## 💰 Cost Monitoring

### Set Up Cost Alerts

1. Go to **"Cost Management + Billing"**
2. Click **"Cost alerts"**
3. Create alert:
   - **Budget:** $1/month
   - **Alert at:** 50%, 80%, 100%
   - **Email:** joshua_avila@trendmicro.com

**Why:**
- Free tier should cost $0
- Alert catches if you accidentally exceed limits

### Monitor Usage

**Check monthly:**
1. Azure Portal → Cosmos DB
2. **"Metrics"** → Check RU/s usage
3. **"Storage"** → Check data size
4. Should be well under limits!

---

## 📊 Cosmos DB Data Structure

### Users Collection
```json
{
  "id": "1",
  "username": "admin",
  "password_hash": "sha256_hash",
  "full_name": "System Administrator",
  "role": "Admin"
}
```

### Tickets Collection
```json
{
  "id": "1",
  "ticket_number": "CPDT-0001",
  "title": "Customer Unable to Access Email",
  "description": "...",
  "scenario": "...",
  "status": "Assigned to CORE",
  "priority": "P1",
  "product": "Maximum Security",
  "fundamental_solution": "FS:None",
  "reporter_id": "2",
  "core_engineer_id": "3",
  "created_at": "2026-03-13T10:30:00",
  "updated_at": "2026-03-13T11:00:00"
}
```

### TicketReplies Collection
```json
{
  "id": "1",
  "ticket_id": "1",
  "user_id": "3",
  "message": "Investigating the issue...",
  "reply_role": "Engineer",
  "created_at": "2026-03-13T10:35:00"
}
```

---

## ✅ Setup Complete!

Once you've completed these steps:
- ✅ Cosmos DB is running (FREE)
- ✅ Data persists permanently
- ✅ Ready for Streamlit Cloud deployment
- ✅ Scalable for production use

**Next:** Deploy to Streamlit Cloud (see DEPLOYMENT_GUIDE.md)

---

**Questions?** Contact: joshua_avila@trendmicro.com
