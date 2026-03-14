# ⚡ Quick Start - Deploy in 30 Minutes (FREE)

## Get your CORE Engineer Training Portal live in under 30 minutes - completely FREE!

---

## 🎯 Overview

You'll set up:
1. ✅ Azure Cosmos DB (FREE tier) - 15 minutes
2. ✅ Streamlit Cloud hosting (FREE) - 5 minutes
3. ✅ Initialize data - 5 minutes
4. ✅ Test and share - 5 minutes

**Total: ~30 minutes**
**Cost: $0/month**

---

## ⏱️ Part 1: Azure Cosmos DB (15 minutes)

### Quick Steps:

1. **Azure Portal** → https://portal.azure.com
2. **Create resource** → Search "Azure Cosmos DB"
3. **Select** → "Azure Cosmos DB for NoSQL"
4. **Configure:**
   - Account name: `cpdt-training-db` (make it unique)
   - Capacity mode: ⭐ **Serverless**
   - Apply Free Tier: ⭐ **YES** (check the box!)
   - Networking: **All networks**
5. **Create** → Wait 3-5 minutes

6. **Data Explorer** → Create database and containers:
   - Database: `JiraTraining`
   - Containers (create 4):
     - `Users` (partition key: `/username`)
     - `Tickets` (partition key: `/ticket_number`)
     - `TicketHistory` (partition key: `/ticket_id`)
     - `TicketReplies` (partition key: `/ticket_id`)

7. **Keys** → Copy:
   - URI: `https://YOUR-NAME.documents.azure.com:443/`
   - PRIMARY KEY: `long-key-string...`

**✅ Cosmos DB ready!**

---

## ⏱️ Part 2: Streamlit Cloud (5 minutes)

### Quick Steps:

1. **Go to** → https://share.streamlit.io
2. **Sign up** → Use GitHub account
3. **New app** → Fill in:
   - Repo: `constrendlife-prod/jira-simulation-training`
   - Branch: `main`
   - File: `src/app.py`
   - URL: `cpdt-training` (or your choice)

4. **Advanced settings** → Add secrets:
```toml
COSMOSDB_ENDPOINT = "https://YOUR-NAME.documents.azure.com:443/"
COSMOSDB_KEY = "your_primary_key_here"
COSMOSDB_DATABASE_NAME = "JiraTraining"
STORAGE_BACKEND = "cosmosdb"
ENVIRONMENT = "production"
```

5. **Deploy!** → Wait 2 minutes

**✅ App is live!**

---

## ⏱️ Part 3: Initialize Data (5 minutes)

### Method 1: Local Script (Recommended)

1. **Update local `.env`:**
   ```bash
   STORAGE_BACKEND=cosmosdb
   COSMOSDB_ENDPOINT=https://YOUR-NAME.documents.azure.com:443/
   COSMOSDB_KEY=your_primary_key
   COSMOSDB_DATABASE_NAME=JiraTraining
   ```

2. **Run:**
   ```bash
   cd "/home/joshuaav/Jira - Simulation Program"
   source venv/bin/activate
   python src/init_data.py
   ```

3. **Check Cosmos DB:**
   - Azure Portal → Data Explorer
   - Verify Users and Tickets containers have data

**✅ Data initialized!**

---

## ⏱️ Part 4: Test & Share (5 minutes)

### Test Your Live App:

1. **Open:** `https://cpdt-training.streamlit.app`
2. **Login:**
   - Click "🔐 Login as Admin" → Test admin features
   - Click "👨‍💻 Login as Engineer" → Test engineer features
3. **Create a ticket** → Verify it saves
4. **Add conversation** → Verify it persists
5. **Refresh page** → Data should still be there!

### Share with Team:

```
🎉 CORE Engineer Training Portal is LIVE!

URL: https://cpdt-training.streamlit.app

Login:
• Admin: One-click login
• Engineer: One-click login

This is a simulation system for practicing ticket workflows.
Try creating tickets, escalating, and resolving cases!
```

**✅ Deployment complete!**

---

## 🎯 What You Get

### **100% FREE Forever:**
- ✅ Azure Cosmos DB Free Tier (1000 RU/s + 25 GB)
- ✅ Streamlit Cloud Free Tier (1 private app)
- ✅ Persistent data storage
- ✅ Auto-deploy from GitHub
- ✅ SSL/HTTPS included
- ✅ No credit card required

### **Your Portal Features:**
- ✅ CPDT-#### ticket numbering
- ✅ P0-P4 priority system
- ✅ 18 Trend Micro products
- ✅ Reporter → CORE → RD workflow
- ✅ Retract Case feature
- ✅ Resolution Summary with FS
- ✅ Color-coded conversations
- ✅ Full-page ticket views
- ✅ Card layout (3 per row)

---

## 📋 Checklist

### Pre-Deployment:
- [x] Code in GitHub ✅
- [ ] Azure account created
- [ ] GitHub account created

### Azure Cosmos DB:
- [ ] Cosmos DB account created (serverless, free tier)
- [ ] Database "JiraTraining" created
- [ ] 4 containers created
- [ ] Credentials copied (URI, Key)

### Streamlit Cloud:
- [ ] Signed up at share.streamlit.io
- [ ] New app created
- [ ] Secrets added (Cosmos DB credentials)
- [ ] App deployed successfully

### Data & Testing:
- [ ] Sample data initialized in Cosmos DB
- [ ] Can login to live app
- [ ] Tickets display correctly
- [ ] Conversations save properly
- [ ] Data persists after refresh

### Sharing:
- [ ] Tested all features work
- [ ] URL shared with team
- [ ] Training can begin!

---

## 🆘 Troubleshooting

### "Cannot connect to Cosmos DB"
- ✅ Check secrets in Streamlit Cloud
- ✅ Verify Cosmos DB allows "All networks"
- ✅ Verify PRIMARY KEY is correct (very long string)

### "No tickets showing"
- ✅ Initialize data with `python src/init_data.py`
- ✅ Check Cosmos DB Data Explorer for data
- ✅ Verify STORAGE_BACKEND=cosmosdb in secrets

### "App is slow to load"
- ✅ Normal for first load (app was sleeping)
- ✅ Subsequent loads are faster
- ✅ Consider keeping browser tab open

---

## 🚀 You're Done!

**Congratulations!** Your CORE Engineer Training Portal is now:
- 🌐 Live on the internet
- 💾 Using permanent cloud storage
- 🆓 Completely FREE
- 🔄 Auto-deploying from GitHub

**URL:** https://cpdt-training.streamlit.app

**Start training your CORE Engineers!** 🎉

---

## 📞 Support

- **Detailed Guides:**
  - [COSMOS_DB_SETUP.md](COSMOS_DB_SETUP.md)
  - [STREAMLIT_CLOUD_DEPLOYMENT.md](STREAMLIT_CLOUD_DEPLOYMENT.md)
  - [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

- **Contact:** joshua_avila@trendmicro.com
- **GitHub Issues:** https://github.com/constrendlife-prod/jira-simulation-training/issues
