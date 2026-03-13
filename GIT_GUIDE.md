# 🚀 Git Repository Guide

## Repository Information

- **Repository URL:** https://github.com/constrendlife-prod/jira-simulation-training
- **Repository Name:** jira-simulation-training
- **Owner:** constrendlife-prod

---

## ⚙️ Configuration Setup

Your GitHub credentials are securely stored in the `.env` file:

```bash
GITHUB_REPO_URL=https://github.com/constrendlife-prod/jira-simulation-training.git
GITHUB_TOKEN=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
GITHUB_USERNAME=constrendlife-prod
```

**⚠️ IMPORTANT SECURITY:**
- ✅ The `.env` file is in `.gitignore` (never committed)
- ✅ Your token is safe and not uploaded to GitHub
- ❌ NEVER share your GitHub token publicly
- ❌ NEVER commit `.env` to the repository

---

## 🎯 Quick Start: Push to GitHub

### Option 1: Use Helper Scripts (Recommended)

#### On Ubuntu/Linux:
```bash
./git-push.sh
```

#### On Windows CMD:
```cmd
git-push.bat
```

These scripts will:
1. Show you what files changed
2. Ask for confirmation
3. Commit and push to GitHub automatically

---

### Option 2: Manual Git Commands

#### Step 1: Check Status
```bash
git status
```

#### Step 2: Add Files
```bash
git add .
```

#### Step 3: Commit Changes
```bash
git commit -m "Your commit message here"
```

#### Step 4: Push to GitHub

**On Ubuntu/Linux:**
```bash
# Load credentials from .env
export $(cat .env | grep GITHUB_TOKEN)
export $(cat .env | grep GITHUB_USERNAME)

# Push using token
git push https://$GITHUB_USERNAME:$GITHUB_TOKEN@github.com/constrendlife-prod/jira-simulation-training.git main
```

**On Windows:**
```cmd
# You'll be prompted for username and password
# Username: constrendlife-prod
# Password: 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

git push origin main
```

---

## 📦 Common Git Operations

### View Repository Status
```bash
git status
```

### View Commit History
```bash
git log --oneline
```

### View Remote Repository
```bash
git remote -v
```

### Pull Latest Changes
```bash
git pull origin main
```

### Undo Last Commit (keep changes)
```bash
git reset --soft HEAD~1
```

### Discard All Local Changes
```bash
git reset --hard HEAD
```

---

## 🔄 Typical Workflow

1. **Make changes to your code**
2. **Check what changed:**
   ```bash
   git status
   ```
3. **Stage changes:**
   ```bash
   git add .
   ```
4. **Commit changes:**
   ```bash
   git commit -m "Description of what you changed"
   ```
5. **Push to GitHub:**
   ```bash
   ./git-push.sh  # or git-push.bat on Windows
   ```

---

## 🌿 Working with Branches

### Create New Branch
```bash
git checkout -b feature/new-feature
```

### Switch Branch
```bash
git checkout main
```

### List All Branches
```bash
git branch -a
```

### Push New Branch to GitHub
```bash
git push -u origin feature/new-feature
```

---

## 🔐 GitHub Personal Access Token

Your current token: `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`

**Token Permissions:** Should have `repo` access

**If token expires or needs to be regenerated:**
1. Go to: https://github.com/settings/tokens
2. Generate new token (classic)
3. Select scope: `repo` (full control of private repositories)
4. Copy the new token
5. Update in `.env` file

---

## 🆘 Troubleshooting

### "Authentication failed"
- Check your token in `.env` file
- Verify token hasn't expired
- Ensure token has `repo` permissions

### "Permission denied"
- Verify you're using the correct username: `constrendlife-prod`
- Check token permissions on GitHub

### "Repository not found"
- Verify URL: https://github.com/constrendlife-prod/jira-simulation-training.git
- Ensure you have access to the repository

### "Your branch is behind"
```bash
# Pull latest changes first
git pull origin main

# Then push
git push origin main
```

---

## 📝 Best Practices

1. **Commit Often** - Small, frequent commits are better
2. **Write Clear Messages** - Describe what and why, not how
3. **Pull Before Push** - Always pull latest changes before pushing
4. **Test Before Commit** - Make sure app works before committing
5. **Use Branches** - Create feature branches for new work

---

## 📖 Commit Message Examples

**Good commit messages:**
```
✅ Add RD role to ticket system
✅ Fix admin dashboard displaying incorrect assignees
✅ Update chat interface with color-coded messages
✅ Improve ticket workflow with bidirectional endorsement
```

**Bad commit messages:**
```
❌ Fix
❌ Update
❌ Changes
❌ WIP
```

---

## 🔗 Useful Links

- **Repository:** https://github.com/constrendlife-prod/jira-simulation-training
- **GitHub Docs:** https://docs.github.com
- **Git Cheat Sheet:** https://education.github.com/git-cheat-sheet-education.pdf

---

**Need help?** Contact: joshua_avila@trendmicro.com
