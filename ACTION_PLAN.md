# CORE Engineer Training Portal - Action Plan

## 📋 **Current Status: DEPLOYED & WORKING**

**Live URL:** https://jira-simulation-training-core.streamlit.app
**Backend:** Azure Cosmos DB (Free Tier)
**Status:** ✅ Ready for internal testing

---

## 🎯 **Phase 1: Testing & Feedback (Week 1-2)**

### **Immediate Actions:**

- [ ] **Test all features** with CORE Engineer team
  - Login (Admin & Engineer)
  - Create dispatch cases
  - Assign tickets
  - Reply/conversation system
  - Escalate to RD
  - Retract case
  - Resolution with FS fields

- [ ] **Collect user feedback** on:
  - UI/UX improvements
  - Missing features
  - Training scenario quality
  - Workflow efficiency

- [ ] **Create more training scenarios**
  - Write realistic dispatch cases
  - Cover different product areas
  - Include various priority levels (P0-P4)
  - Add edge cases for learning

- [ ] **Document known issues** and limitations

---

## 🔐 **Phase 2: MSAL Authentication (Week 3-4)**

### **Why MSAL:**
- ✅ Single Sign-On (SSO) with Azure AD
- ✅ No password management needed
- ✅ Enterprise-grade security
- ✅ Automatic role assignment from AD groups

### **Implementation Steps:**

#### **2.1 Azure AD App Registration**
- [ ] Register app in Azure Portal
  - Go to: Azure Portal → Azure Active Directory → App registrations
  - Click "New registration"
  - Name: "CORE Engineer Training Portal"
  - Redirect URI: `https://jira-simulation-training-core.streamlit.app`
  - Copy Application (client) ID
  - Copy Directory (tenant) ID

#### **2.2 Configure App Permissions**
- [ ] Add API permissions:
  - Microsoft Graph → Delegated permissions
  - User.Read (sign in and read user profile)
  - email, profile, openid

- [ ] Create client secret:
  - Certificates & secrets → New client secret
  - Name: "Streamlit App Secret"
  - Expiration: 24 months
  - Copy secret value

#### **2.3 Create Azure AD Groups**
- [ ] Create security groups:
  - "CORE-Training-Admins" (for Admin role)
  - "CORE-Training-Engineers" (for Engineer role)

- [ ] Add users to appropriate groups

#### **2.4 Update Streamlit App Code**
- [ ] Install MSAL library: `pip install msal msal-streamlit`
- [ ] Create `src/auth.py` for MSAL authentication
- [ ] Update `src/app.py` to use MSAL login
- [ ] Remove quick login buttons
- [ ] Map Azure AD groups to app roles
- [ ] Add logout functionality with Azure AD sign-out

#### **2.5 Configure Streamlit Secrets**
- [ ] Add to Streamlit Cloud secrets:
  ```toml
  AZURE_CLIENT_ID = "your-client-id"
  AZURE_CLIENT_SECRET = "your-client-secret"
  AZURE_TENANT_ID = "your-tenant-id"
  AZURE_AUTHORITY = "https://login.microsoftonline.com/your-tenant-id"
  AZURE_REDIRECT_URI = "https://jira-simulation-training-core.streamlit.app"
  ADMIN_GROUP_ID = "azure-ad-admin-group-id"
  ENGINEER_GROUP_ID = "azure-ad-engineer-group-id"
  ```

#### **2.6 Test MSAL Authentication**
- [ ] Test login flow
- [ ] Verify role assignment from AD groups
- [ ] Test logout
- [ ] Verify token refresh

---

## 🔔 **Phase 3: Teams Notifications via Power Automate (Week 5)**

### **Why Teams Notifications:**
- ✅ Real-time alerts for engineers
- ✅ Better engagement with training
- ✅ Centralized communication
- ✅ FREE with Microsoft 365

### **Implementation Steps:**

#### **3.1 Create Power Automate Flow**
- [ ] Go to: https://make.powerautomate.com
- [ ] Create new flow: "When a HTTP request is received"
- [ ] Configure trigger:
  - Method: POST
  - Generate sample JSON schema:
    ```json
    {
      "ticket_number": "CPDT-0001",
      "title": "Ticket Title",
      "assigned_to": "engineer@trendmicro.com",
      "status": "Assigned to CORE",
      "priority": "P1",
      "product": "VPN Proxy One Pro",
      "action": "assigned",
      "url": "https://jira-simulation-training-core.streamlit.app",
      "timestamp": "2026-03-20T10:30:00Z"
    }
    ```

#### **3.2 Configure Teams Actions**
- [ ] Add action: "Post a message in a chat or channel"
- [ ] Select Teams team/channel for notifications
- [ ] Design message card:
  ```
  **New Ticket Assigned** 🎫

  **Ticket:** [CPDT-0001] Ticket Title
  **Priority:** P1
  **Product:** VPN Proxy One Pro
  **Assigned to:** @engineer

  [View Ticket](ticket_url)
  ```

#### **3.3 Create Different Notification Types**
- [ ] **Ticket Assigned** → Notify engineer
- [ ] **Ticket Escalated** → Notify admin channel
- [ ] **Ticket Resolved** → Update team channel
- [ ] **New Reply Added** → Notify relevant parties
- [ ] **Ticket Retracted** → Notify original assignee

#### **3.4 Get Webhook URL**
- [ ] Save flow
- [ ] Copy HTTP POST URL from trigger
- [ ] Add to Streamlit secrets:
  ```toml
  TEAMS_WEBHOOK_ASSIGNED = "https://prod-xx.logic.azure.com/..."
  TEAMS_WEBHOOK_ESCALATED = "https://prod-xx.logic.azure.com/..."
  TEAMS_WEBHOOK_RESOLVED = "https://prod-xx.logic.azure.com/..."
  ```

#### **3.5 Update Application Code**
- [ ] Create `src/notifications.py`:
  ```python
  def send_teams_notification(webhook_url, data):
      """Send notification to Teams via Power Automate"""
      import requests
      response = requests.post(webhook_url, json=data)
      return response.status_code == 200
  ```

- [ ] Add notification calls in `src/app.py`:
  - After ticket assignment
  - After escalation
  - After resolution
  - After new replies (optional)

#### **3.6 Test Notifications**
- [ ] Test ticket assignment notification
- [ ] Test escalation notification
- [ ] Test resolution notification
- [ ] Verify @mentions work in Teams
- [ ] Test notification formatting

---

## 🚀 **Phase 4: Production Readiness (Week 6)**

### **Security Hardening:**
- [ ] Remove all quick login code
- [ ] Implement rate limiting for API calls
- [ ] Add HTTPS enforcement
- [ ] Review Cosmos DB access permissions
- [ ] Rotate Cosmos DB keys
- [ ] Set up secret rotation policy

### **Performance Optimization:**
- [ ] Load test with 10+ concurrent users
- [ ] Optimize Cosmos DB queries (add indexes)
- [ ] Cache frequently accessed data
- [ ] Monitor response times

### **Audit & Compliance:**
- [ ] Add audit logging for all actions:
  - User logins
  - Ticket assignments
  - Status changes
  - Replies added
  - Resolutions
- [ ] Store audit logs in Cosmos DB
- [ ] Create audit report dashboard

### **Documentation:**
- [ ] **Admin Guide:**
  - How to create training scenarios
  - How to manage users
  - How to assign tickets
  - How to review engineer performance

- [ ] **Engineer Guide:**
  - How to access the portal
  - How to work tickets
  - When to escalate
  - How to resolve with FS fields

- [ ] **IT Admin Guide:**
  - How to manage Azure AD groups
  - How to rotate secrets
  - How to monitor Cosmos DB
  - Troubleshooting guide

---

## 💰 **Phase 5: Hosting Decision**

### **Current Setup:**
- **Streamlit Cloud (Community):** FREE
  - Limitation: App sleeps after inactivity
  - Good for: Testing, light usage

### **Options for Production:**

#### **Option A: Streamlit Cloud Pro** ($20/month)
- ✅ 3 private apps
- ✅ More resources
- ✅ Better performance
- ✅ Easier to manage
- ❌ Still sleeps (less frequently)

#### **Option B: Azure App Service B1** ($13/month)
- ✅ Always on
- ✅ All in Azure ecosystem
- ✅ Better MSAL integration
- ✅ More control
- ❌ Manual deployment setup

#### **Option C: Keep Free Tier**
- ✅ $0/month
- ✅ Works for internal testing
- ✅ Can upgrade anytime
- ❌ App sleeps after inactivity

**Recommendation:** Start with FREE, upgrade to Azure App Service B1 when ready for production.

---

## 📊 **Phase 6: Optional Enhancements**

### **Nice-to-Have Features:**
- [ ] File attachments (screenshots, logs)
- [ ] Advanced ticket search
- [ ] Analytics dashboard:
  - Average resolution time
  - Engineer performance metrics
  - Escalation rates
  - FS distribution

- [ ] Ticket templates for common scenarios
- [ ] Bulk ticket creation
- [ ] Export tickets to CSV/Excel
- [ ] Integration with actual Jira (optional)
- [ ] Mobile-responsive UI improvements
- [ ] Dark mode toggle
- [ ] Keyboard shortcuts

---

## 📅 **Timeline Summary:**

| Phase | Duration | Status |
|-------|----------|--------|
| **Testing & Feedback** | Week 1-2 | 🟡 Ready to start |
| **MSAL Authentication** | Week 3-4 | ⚪ Not started |
| **Teams Notifications** | Week 5 | ⚪ Not started |
| **Production Readiness** | Week 6 | ⚪ Not started |
| **Hosting Decision** | Week 6 | ⚪ Not started |
| **Optional Enhancements** | Week 7+ | ⚪ Future |

**Total Time to Production:** ~6 weeks

---

## ✅ **Success Criteria:**

### **For Testing Phase:**
- ✅ All CORE Engineers can access the portal
- ✅ Can create and manage tickets successfully
- ✅ Workflows are intuitive
- ✅ No critical bugs

### **For Production Deployment:**
- ✅ MSAL authentication working
- ✅ Teams notifications sending
- ✅ All features tested and working
- ✅ Documentation complete
- ✅ Admin approval obtained
- ✅ Hosting decision made

---

## 📞 **Support & Contacts:**

**Project Owner:** Joshua Avila (joshua_avila@trendmicro.com)
**Azure Admin:** [Azure admin contact]
**Streamlit Cloud:** https://share.streamlit.io
**GitHub Repo:** https://github.com/constrendlife-prod/jira-simulation-training

---

## 📝 **Notes:**

- All phases can be adjusted based on feedback
- MSAL and Teams notifications can be swapped in priority
- Optional enhancements can be added anytime
- Keep this document updated as you progress

---

**Last Updated:** 2026-03-20
**Version:** 1.0
**Status:** 🟢 ACTIVE TESTING PHASE
