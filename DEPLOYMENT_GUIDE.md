# 🚀 Deployment Guide - FREE Tier Setup

## Complete guide for deploying your CORE Engineer Training Portal for FREE using Azure Cosmos DB + Streamlit Cloud

---

## 📋 **Prerequisites**

- ✅ Azure account (free tier available)
- ✅ GitHub account (free)
- ✅ Code already pushed to GitHub ✅

---

# Part 1: Azure Cosmos DB Setup (FREE Tier)

## Step 1: Create Cosmos DB Account

### 1.1 Go to Azure Portal
- Navigate to: https://portal.azure.com
- Sign in with your Azure account

### 1.2 Create New Cosmos DB
1. Click **"+ Create a resource"**
2. Search for **"Azure Cosmos DB"**
3. Click **"Create"**
4. Select **"Azure Cosmos DB for NoSQL"** (Core SQL)
5. Click **"Create"**

### 1.3 Configure Cosmos DB

**Basics Tab:**
- **Subscription:** Select your subscription
- **Resource Group:** Create new or select existing (e.g., "rg-jira-training")
- **Account Name:** `cpdt-training-db` (must be unique globally)
- **Location:** Choose closest to you (e.g., "East US", "Southeast Asia")
- **Capacity mode:** ⭐ **Serverless** ← IMPORTANT for FREE tier
- **Apply Free Tier Discount:** ⭐ **YES** ← CHECK THIS BOX!

**Global Distribution Tab:**
- Leave defaults (single region)

**Networking Tab:**
- **Connectivity method:** ⭐ **All networks** (so Streamlit Cloud can connect)
  - OR select "Public endpoint (selected networks)" and add Streamlit Cloud IPs later

**Backup Policy Tab:**
- Leave defaults

**Encryption Tab:**
- Leave defaults

**Tags Tab:**
- Optional: Add tags like `Environment: Production`, `Project: CORE-Training`

### 1.4 Review and Create
1. Click **"Review + create"**
2. Verify **"Apply Free Tier Discount: Yes"** is shown
3. Click **"Create"**
4. Wait 3-5 minutes for deployment

---

## Step 2: Create Database and Containers

### 2.1 Navigate to Your Cosmos DB Account
1. Go to **"Resource groups"** → Select your resource group
2. Click on your Cosmos DB account (e.g., `cpdt-training-db`)

### 2.2 Create Database
1. In left menu, click **"Data Explorer"**
2. Click **"New Container"**
3. Select **"Create new database"**
4. **Database id:** `JiraTraining`
5. Leave **"Share throughput across containers"** UNCHECKED (serverless doesn't need this)

### 2.3 Create Containers

**Container 1: Users**
- **Container id:** `Users`
- **Partition key:** `/username`
- Click **"OK"**

**Container 2: Tickets**
- Click **"New Container"** again
- **Database id:** Select existing `JiraTraining`
- **Container id:** `Tickets`
- **Partition key:** `/ticket_number`
- Click **"OK"**

**Container 3: TicketHistory**
- Click **"New Container"** again
- **Database id:** Select existing `JiraTraining`
- **Container id:** `TicketHistory`
- **Partition key:** `/ticket_id`
- Click **"OK"**

**Container 4: TicketReplies**
- Click **"New Container"** again
- **Database id:** Select existing `JiraTraining`
- **Container id:** `TicketReplies`
- **Partition key:** `/ticket_id`
- Click **"OK"**

---

## Step 3: Get Connection Credentials

### 3.1 Get Connection String
1. In your Cosmos DB account, click **"Keys"** in left menu
2. You'll see:
   - **URI** (endpoint)
   - **PRIMARY KEY**
   - **PRIMARY CONNECTION STRING**

### 3.2 Copy These Values
**Copy the following (you'll need them):**
- **URI:** `https://cpdt-training-db.documents.azure.com:443/`
- **PRIMARY KEY:** `very-long-key-string-here...`
- **DATABASE NAME:** `JiraTraining`

---

## Step 4: Update Your Local .env File

Add these values to your `.env` file:

```bash
# ── Azure Cosmos DB Configuration ────────────────────────────────────────
COSMOSDB_ENDPOINT=https://cpdt-training-db.documents.azure.com:443/
COSMOSDB_KEY=your_primary_key_here
COSMOSDB_DATABASE_NAME=JiraTraining
STORAGE_BACKEND=cosmosdb
```

**IMPORTANT:**
- Replace `cpdt-training-db` with YOUR account name
- Replace `your_primary_key_here` with your ACTUAL primary key
- Set `STORAGE_BACKEND=cosmosdb` to use Cosmos DB
- Set `STORAGE_BACKEND=sqlite` to use SQLite (local testing)

---

# Part 2: Test Cosmos DB Locally

## Step 1: Test Connection

Run this command to test if Cosmos DB works:

**On Ubuntu:**
```bash
cd "/home/joshuaav/Jira - Simulation Program"
source venv/bin/activate
python src/init_data.py
```

**On Windows:**
```cmd
cd "C:\path\to\Jira - Simulation Program"
venv\Scripts\activate
python src\init_data.py
```

**Expected Output:**
```
Initializing sample data...
Using Cosmos DB backend
Creating admin users...
Creating engineer users...
Creating sample dispatch cases...
Sample data initialized successfully!
```

## Step 2: Run the App Locally

```bash
streamlit run src/app.py
```

- Login and test all features
- Create tickets, add replies
- Verify data persists in Cosmos DB

---

# Part 3: Deploy to Streamlit Cloud

## Step 1: Prepare Your Repository

### 1.1 Ensure Code is Pushed
Your code is already pushed to:
`https://github.com/constrendlife-prod/jira-simulation-training`

### 1.2 Create requirements.txt Check
Verify `requirements.txt` includes:
```
streamlit>=1.31.0
azure-cosmos>=4.5.0
azure-identity>=1.15.0
python-dotenv>=1.0.0
```
✅ Already included!

---

## Step 2: Deploy to Streamlit Cloud

### 2.1 Sign Up for Streamlit Cloud
1. Go to: https://share.streamlit.io
2. Click **"Sign up"**
3. **Sign in with GitHub**
4. Authorize Streamlit to access your repos

### 2.2 Create New App
1. Click **"New app"** button
2. Fill in the form:
   - **Repository:** `constrendlife-prod/jira-simulation-training`
   - **Branch:** `main`
   - **Main file path:** `src/app.py`
   - **App URL:** Choose a name (e.g., `cpdt-training`)

### 2.3 Advanced Settings - Add Secrets

Click **"Advanced settings"** and add your secrets:

**In the secrets box, paste:**
```toml
# Cosmos DB Configuration
COSMOSDB_ENDPOINT = "https://cpdt-training-db.documents.azure.com:443/"
COSMOSDB_KEY = "your_primary_key_here"
COSMOSDB_DATABASE_NAME = "JiraTraining"
STORAGE_BACKEND = "cosmosdb"

# Application Settings
APP_NAME = "CORE Engineer Training Portal"
ENVIRONMENT = "production"
DEBUG = "False"
```

**⚠️ IMPORTANT:**
- Replace `cpdt-training-db` with YOUR Cosmos DB account name
- Replace `your_primary_key_here` with YOUR actual primary key
- Do NOT include quotes around the values in Streamlit secrets

### 2.4 Deploy
1. Click **"Deploy!"**
2. Wait 2-3 minutes
3. Your app will be live at: `https://cpdt-training.streamlit.app`

---

## Step 3: Initialize Cosmos DB Data

### 3.1 First Time Setup
After deployment, you need to initialize the Cosmos DB with sample data.

**Option A: Run init script locally with Cosmos DB**
```bash
# Set STORAGE_BACKEND=cosmosdb in .env
python src/init_data.py
```

**Option B: Use Streamlit Cloud Python terminal** (if available)
- Access app terminal
- Run init script

**Option C: Manually create test users via admin panel** (if we add this feature)

---

## Step 4: Access Your App

### 4.1 Your App URL
```
https://cpdt-training.streamlit.app
(or whatever name you chose)
```

### 4.2 Share with Team
- Send URL to CORE Engineers
- They can start training immediately!

### 4.3 Monitor Usage
- Streamlit Cloud dashboard shows:
  - App status
  - Visitor count
  - Error logs

---

# Part 4: Verify Free Tier Limits

## Cosmos DB Free Tier Check

### Check Your Usage:
1. Go to Azure Portal → Your Cosmos DB account
2. Click **"Metrics"** in left menu
3. Verify:
   - **Request Units:** Under 1000 RU/s ✅
   - **Storage:** Under 25 GB ✅

**Your app will likely use:**
- **~10-50 RU/s** (normal usage)
- **~100-500 MB storage** (1000s of tickets)
- **Well within free tier!** 🎉

---

## Streamlit Cloud Free Tier Check

### Check Your Usage:
1. Go to: https://share.streamlit.io
2. View your apps
3. Check:
   - **Private apps:** 1 of 1 used ✅
   - **Public apps:** Unlimited ✅

**If you need more private apps:**
- Upgrade to Pro: $20/month (3 private apps)

---

# Part 5: Ongoing Maintenance

## Auto-Deploy Setup

**Already configured!** Every time you push to GitHub main branch:
```bash
git add .
git commit -m "Update features"
git push origin main
```

**Streamlit Cloud automatically:**
1. Detects the push
2. Rebuilds the app
3. Deploys new version
4. Takes ~2-3 minutes

---

## Monitoring

### Streamlit Cloud Logs
1. Go to https://share.streamlit.io
2. Click on your app
3. View **"Logs"** tab for errors

### Cosmos DB Monitoring
1. Azure Portal → Cosmos DB account
2. Click **"Metrics"**
3. Monitor:
   - Request Units (stay under 1000 RU/s)
   - Storage (stay under 25 GB)
   - Throttled requests (should be 0)

---

## Backup Strategy

**Cosmos DB Automatic Backups:**
- ✅ Automatic backups every 4 hours
- ✅ Retained for 8 hours
- ✅ Free tier included
- ✅ Can restore from Azure support

**Manual Export (recommended):**
```bash
# Export data periodically
python scripts/export_data.py
```

---

# Part 6: Troubleshooting

## Common Issues

### Issue 1: "Connection refused" to Cosmos DB

**Solution:**
- Check Cosmos DB Firewall settings
- Add Streamlit Cloud IP ranges
- OR set to "All networks"

### Issue 2: "Request rate too large" (429 error)

**Solution:**
- You've exceeded 1000 RU/s
- Optimize queries
- Add indexing
- Or upgrade Cosmos DB tier

### Issue 3: App crashes on Streamlit Cloud

**Solution:**
- Check logs in Streamlit Cloud dashboard
- Verify secrets are correct
- Check if Cosmos DB is accessible

### Issue 4: Data not persisting

**Solution:**
- Verify `STORAGE_BACKEND=cosmosdb` in secrets
- Check Cosmos DB credentials
- Verify containers were created

---

# Part 7: Scaling Up (When Needed)

## When to Upgrade Cosmos DB

**Upgrade if:**
- ❌ Hitting 1000 RU/s limit (many concurrent users)
- ❌ Exceeding 25 GB storage (10,000+ tickets)
- ❌ Need faster performance

**Upgrade to:**
- **Provisioned throughput:** ~$24/month for 400 RU/s
- Still very affordable!

## When to Upgrade Streamlit Cloud

**Upgrade if:**
- ❌ Need more than 1 private app
- ❌ Need more resources (RAM/CPU)
- ❌ Need team collaboration features

**Upgrade to:**
- **Pro:** $20/month (3 private apps)
- **Teams:** $250/month (unlimited, SSO)

---

# Summary Checklist

## ✅ Azure Cosmos DB Setup
- [ ] Create Cosmos DB account with Free Tier discount
- [ ] Create JiraTraining database
- [ ] Create 4 containers (Users, Tickets, TicketHistory, TicketReplies)
- [ ] Copy URI and Primary Key
- [ ] Update .env file locally
- [ ] Test connection locally
- [ ] Initialize data in Cosmos DB

## ✅ Streamlit Cloud Deployment
- [ ] Sign up at share.streamlit.io
- [ ] Connect GitHub account
- [ ] Create new app from your repo
- [ ] Add secrets (Cosmos DB credentials)
- [ ] Deploy app
- [ ] Verify app is accessible
- [ ] Test login and features

## ✅ Verification
- [ ] Login works
- [ ] Tickets display correctly
- [ ] Can create new tickets
- [ ] Conversations save properly
- [ ] Data persists after app restart
- [ ] Share URL with team

---

# 🎯 Expected Timeline

- **Cosmos DB Setup:** 15-20 minutes
- **Code Testing Locally:** 10 minutes
- **Streamlit Cloud Deployment:** 5 minutes
- **Total:** ~30-35 minutes

---

# 💰 Cost Breakdown

| Service | Tier | Cost |
|---------|------|------|
| Azure Cosmos DB | Free Tier | $0/month |
| Streamlit Cloud | Community | $0/month |
| Azure AD (MSAL) | Existing | $0/month |
| **TOTAL** | | **$0/month** |

---

# 🆘 Support

**Need help?**
- Azure Cosmos DB: https://docs.microsoft.com/azure/cosmos-db/
- Streamlit Cloud: https://docs.streamlit.io/streamlit-community-cloud
- GitHub Issues: https://github.com/constrendlife-prod/jira-simulation-training/issues

**Contact:** joshua_avila@trendmicro.com

---

**Ready to deploy!** Follow the steps above and you'll have a production-ready CORE Engineer Training Portal running for FREE! 🚀
