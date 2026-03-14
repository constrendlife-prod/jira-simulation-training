# ☁️ Streamlit Cloud Deployment Guide (FREE)

## Deploy your CORE Engineer Training Portal to Streamlit Cloud for FREE!

---

## 🎯 What You're Getting

**Streamlit Cloud (Community Tier) - FREE:**
- ✅ 1 GB RAM
- ✅ 1 private app (FREE)
- ✅ Unlimited public apps
- ✅ Auto-deploy from GitHub
- ✅ Free SSL/HTTPS
- ✅ Custom subdomain
- ✅ Secrets management
- ✅ View logs and metrics

**Cost: $0/month (forever!)**

---

## ✅ Prerequisites

Before you start, make sure you have:
- [x] Code pushed to GitHub ✅
- [x] Azure Cosmos DB created and configured
- [x] Cosmos DB credentials (URI, Key, Database Name)
- [ ] GitHub account
- [ ] Cosmos DB initialized with sample data

---

## 📋 Step 1: Sign Up for Streamlit Cloud

### 1.1 Go to Streamlit Cloud
```
URL: https://share.streamlit.io
```

### 1.2 Sign Up
1. Click **"Sign up"** button
2. Click **"Continue with GitHub"**
3. **Authorize Streamlit** to access your GitHub repos
4. Grant permissions when prompted

**Why GitHub auth?**
- Streamlit needs access to your repo
- Auto-deploys when you push updates
- No separate credentials to manage

---

## 📋 Step 2: Create Your App

### 2.1 New App
1. Click **"New app"** button (top right)
2. You'll see the deployment form

### 2.2 Repository Settings

**Repository:**
- **GitHub account:** `constrendlife-prod`
- **Repository:** `jira-simulation-training`
- **Branch:** `main`

**Main file path:**
- Enter: `src/app.py`
  - ⚠️ Important: Include the `src/` folder!

**App URL (optional):**
- Custom name: `cpdt-training` or `core-engineer-training`
- Your app will be: `https://cpdt-training.streamlit.app`
- Or Streamlit auto-generates one for you

---

## 📋 Step 3: Configure Secrets

### 3.1 Click "Advanced settings"

### 3.2 Add Secrets (TOML Format)

**In the "Secrets" text box, paste this:**

```toml
# Azure Cosmos DB Configuration
COSMOSDB_ENDPOINT = "https://cpdt-training-db.documents.azure.com:443/"
COSMOSDB_KEY = "your_primary_key_here_very_long_string=="
COSMOSDB_DATABASE_NAME = "JiraTraining"
STORAGE_BACKEND = "cosmosdb"

# Application Settings
APP_NAME = "CORE Engineer Training Portal"
ENVIRONMENT = "production"
DEBUG = "False"
LOG_LEVEL = "INFO"

# Admin Configuration
ADMIN_EMAILS = "joshua_avila@trendmicro.com"
```

**⚠️ IMPORTANT NOTES:**
- Replace `cpdt-training-db` with YOUR Cosmos DB account name
- Replace `your_primary_key_here_very_long_string==` with YOUR actual primary key
- Do NOT use quotes around values (TOML format different from .env)
- Indentation doesn't matter in TOML
- These secrets are encrypted and never exposed

### 3.3 Where to Find Your Values

**Get from Azure Portal:**
1. Go to your Cosmos DB account
2. Click **"Keys"** in left menu
3. Copy:
   - **URI** → Use as `COSMOSDB_ENDPOINT`
   - **PRIMARY KEY** → Use as `COSMOSDB_KEY`

---

## 📋 Step 4: Deploy!

### 4.1 Deploy App
1. Review all settings
2. Click **"Deploy!"** button
3. Wait 2-3 minutes

### 4.2 Deployment Process

You'll see:
```
Building...
⏳ Installing dependencies from requirements.txt
⏳ Starting app...
✅ App is live!
```

### 4.3 Access Your App

Your app will be available at:
```
https://cpdt-training.streamlit.app
(or your custom name)
```

---

## 📋 Step 5: Initialize Data in Cosmos DB

### Option A: Run Locally with Cosmos Backend

1. **Update your local `.env` file:**
   ```bash
   STORAGE_BACKEND=cosmosdb
   COSMOSDB_ENDPOINT=https://YOUR-ACCOUNT.documents.azure.com:443/
   COSMOSDB_KEY=YOUR_PRIMARY_KEY
   COSMOSDB_DATABASE_NAME=JiraTraining
   ```

2. **Run init script:**
   ```bash
   cd "/home/joshuaav/Jira - Simulation Program"
   source venv/bin/activate
   python src/init_data.py
   ```

3. **Verify in Azure Portal:**
   - Data Explorer → JiraTraining → Users
   - Should see admin and engineer users

### Option B: Manually Create Initial Admin User

**Use Cosmos DB Data Explorer:**
1. Go to Azure Portal → Cosmos DB → Data Explorer
2. Expand JiraTraining → Users
3. Click "New Item"
4. Paste this JSON:
```json
{
  "id": "1",
  "username": "admin",
  "password_hash": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",
  "full_name": "System Administrator",
  "role": "Admin"
}
```
5. Click "Save"

**Login credentials:**
- Username: `admin`
- Password: `admin123`

---

## 📋 Step 6: Verify Deployment

### 6.1 Test Your Live App

1. Open: `https://cpdt-training.streamlit.app`
2. Click **"🔐 Login as Admin"**
3. Verify:
   - ✅ Dashboard loads
   - ✅ Can see tickets (if data initialized)
   - ✅ Can create new tickets
   - ✅ Tickets persist after page refresh

### 6.2 Check Streamlit Cloud Dashboard

1. Go to https://share.streamlit.io
2. Click on your app
3. **View tabs:**
   - **Analytics:** See visitor count, views
   - **Logs:** See errors and system logs
   - **Settings:** Update secrets, reboot app

---

## 📋 Step 7: Configure Auto-Deploy

### Already Configured! 🎉

Every time you push to GitHub:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

**Streamlit Cloud will:**
1. Detect the push (within 30 seconds)
2. Rebuild the app
3. Deploy new version
4. Takes 1-2 minutes

**You'll see in Streamlit dashboard:**
```
Building...
Deploying...
✅ Deployed!
```

---

## 🎨 Customize Your App

### Change App URL

**After deployment:**
1. Streamlit Cloud dashboard → Your app
2. Click **"Settings"**
3. **App URL:** Change subdomain
4. Save and redeploy

### Update Secrets

**To update Cosmos DB credentials:**
1. Streamlit dashboard → Your app → **"Settings"**
2. Scroll to **"Secrets"**
3. Edit the TOML configuration
4. Click **"Save"**
5. App will automatically restart

---

## 📊 Monitoring Your App

### Streamlit Cloud Analytics

**View metrics:**
1. Go to https://share.streamlit.io
2. Click on your app
3. **Analytics tab shows:**
   - Number of viewers
   - Page views
   - Active sessions
   - Usage over time

### View Logs

**Check for errors:**
1. Your app in Streamlit dashboard
2. **Logs tab**
3. See real-time logs:
   ```
   2026-03-13 10:30:15 - User logged in: admin
   2026-03-13 10:31:20 - Ticket created: CPDT-0005
   2026-03-13 10:32:45 - Error: [if any]
   ```

### App Management

**Reboot app:**
- Click **"☰ Menu"** → **"Reboot app"**
- Use if app is stuck or frozen

**Delete app:**
- Settings → **"Delete app"**
- Permanent! Cosmos DB data stays safe.

---

## 🔄 Update Workflow

### Making Changes

1. **Edit code locally**
2. **Test locally:**
   ```bash
   streamlit run src/app.py
   ```
3. **Commit and push:**
   ```bash
   git add .
   git commit -m "Add new feature"
   git push origin main
   ```
4. **Wait 2 minutes** - Streamlit Cloud auto-deploys!
5. **Refresh your app URL** - Changes are live!

---

## 🛡️ Security Settings

### Make App Private

**Your app is currently:**
- **Private** (if you used 1 private app slot)
- Only accessible to you and people you share with

**To manage access:**
1. Streamlit dashboard → Your app → **"Settings"**
2. **Sharing:**
   - Private (viewers need Streamlit account)
   - Public (anyone with link can view)

**For CORE Engineer Training:**
- Keep **Private**
- Share link only with trainees
- They'll need to create free Streamlit account to access

---

## 🔧 Troubleshooting

### Issue 1: App Won't Start

**Check:**
- Logs tab in Streamlit dashboard
- Verify `src/app.py` path is correct
- Check if requirements.txt is valid

**Solution:**
- Review error in logs
- Fix code and push again

### Issue 2: "ModuleNotFoundError"

**Cause:**
- Missing package in requirements.txt

**Solution:**
- Add missing package to `requirements.txt`
- Push to GitHub
- Streamlit Cloud will reinstall

### Issue 3: Can't Connect to Cosmos DB

**Check:**
- Secrets are configured correctly
- COSMOSDB_ENDPOINT has correct URL
- COSMOSDB_KEY is the full key (very long)
- Cosmos DB firewall allows connections

**Solution:**
- Update secrets in Streamlit dashboard
- Set Cosmos DB to "All networks"
- Reboot app

### Issue 4: App is Slow

**Reasons:**
- Free tier shares resources
- App was sleeping (cold start)
- High traffic

**Solutions:**
- First load after sleep takes ~30 sec (normal)
- Keep app active by visiting regularly
- Or upgrade to Streamlit Pro ($20/month, priority resources)

---

## 📈 Scaling Up

### When Free Tier is Not Enough

**Upgrade to Streamlit Pro ($20/month) if:**
- ❌ Need more than 1 private app
- ❌ Need priority support
- ❌ Need better performance
- ❌ Need more resources

**Benefits of Pro:**
- ✅ 3 private apps
- ✅ Priority compute resources
- ✅ Faster cold starts
- ✅ Priority support
- ✅ More concurrent users

---

## 🎯 Quick Reference

### Your App URLs

**Streamlit Cloud Dashboard:**
```
https://share.streamlit.io
```

**Your Live App:**
```
https://cpdt-training.streamlit.app
(or your custom subdomain)
```

**GitHub Repo:**
```
https://github.com/constrendlife-prod/jira-simulation-training
```

### Useful Commands

**Local development:**
```bash
streamlit run src/app.py
```

**Push updates:**
```bash
git push origin main
```

**Check Streamlit version:**
```bash
streamlit --version
```

---

## ✅ Deployment Checklist

### Before Deployment:
- [x] Code pushed to GitHub
- [ ] Azure Cosmos DB created
- [ ] Cosmos DB containers created (Users, Tickets, TicketHistory, TicketReplies)
- [ ] Cosmos DB credentials copied
- [ ] Free tier discount applied

### During Deployment:
- [ ] Signed up for Streamlit Cloud
- [ ] Connected GitHub account
- [ ] Created new app
- [ ] Set main file path: `src/app.py`
- [ ] Added secrets (Cosmos DB credentials)
- [ ] Clicked "Deploy"

### After Deployment:
- [ ] App is accessible
- [ ] Initialized Cosmos DB with sample data
- [ ] Tested login (Admin and Engineer)
- [ ] Verified tickets display
- [ ] Verified conversations save
- [ ] Shared URL with team

---

## 🎉 Success!

Your CORE Engineer Training Portal is now:
- ✅ Deployed to Streamlit Cloud
- ✅ Using Azure Cosmos DB for storage
- ✅ Accessible from anywhere
- ✅ Auto-deploys on git push
- ✅ Completely FREE!

**Share your app:**
```
https://cpdt-training.streamlit.app
```

**Cost:** $0/month permanently! 🎉

---

**Need help?** Check logs in Streamlit Cloud dashboard or contact: joshua_avila@trendmicro.com
