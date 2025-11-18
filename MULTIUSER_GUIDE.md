# 👥 MULTI-USER BUDGET TRACKER

## What's New

✅ **User Accounts** - Each person creates their own account  
✅ **Private Data** - Your budget is only visible to you  
✅ **Secure Passwords** - SHA256 hashed passwords  
✅ **Login/Logout** - Session management  
✅ **Works on iPad** - Deploy once, everyone uses their own account

---

## 🎯 How It Works

### **For You (First User)**
1. Run the app
2. Click "Sign Up" tab
3. Create account: `unos` / password
4. Login and use normally

### **For Your Friend**
1. Opens the same URL (on iPad)
2. Clicks "Sign Up" tab
3. Creates account: `friend_name` / password
4. Login and uses their own budget

### **Data Storage**
- **User credentials**: `users.json` (stores usernames, hashed passwords)
- **Your budget**: `budget_data_unos.json`
- **Friend's budget**: `budget_data_friend.json`
- **Completely separate!** You can't see each other's data

---

## 🚀 How to Use Locally

### **Replace Your Current File**

```bash
# Stop current app (Ctrl + C)

cd /Users/sonuvelgekar/Desktop/BUDGET

# Backup old version
mv budget_tracker.py budget_tracker_single_user.py

# Download new multi-user version
# Save as: budget_tracker.py

# Run it
streamlit run budget_tracker.py
```

### **First Time Setup**

1. App opens → You see Login/Signup page
2. Click **"Sign Up"** tab
3. Fill in:
   - Username: `unos`
   - Email: (optional)
   - Password: `yourpassword`
   - Confirm password
4. Click **"Create Account"**
5. Switch to **"Login"** tab
6. Enter username + password
7. Click **"Login"**
8. You're in! 🎉

---

## 🌐 Deploy to Streamlit Cloud

Same process as before, but now multiple people can use it!

### **Step 1: Upload to GitHub**

Upload these files:
- `budget_tracker_multiuser.py` (rename to `budget_tracker.py`)
- `requirements.txt` (same as before)

### **Step 2: Deploy**

1. Go to share.streamlit.io
2. Deploy your repo
3. Get URL: `https://yourname-budget-tracker.streamlit.app`

### **Step 3: Share URL**

Send to your friend → They create account → Done!

---

## 👥 User Management

### **Create Account**
- Min 6 character password
- Username must be unique
- Email optional

### **Login**
- Enter username + password
- Stay logged in during session
- Click "Logout" to exit

### **Your Data**
- Saved per user
- Private and secure
- Export anytime

---

## 🔐 Security Features

✅ **Password Hashing** - Passwords never stored in plain text  
✅ **Session Management** - Secure login state  
✅ **Separate Files** - Each user's data isolated  
✅ **No Data Leakage** - Can't access other users' budgets

---

## 📱 iPad Experience

### **Your Friend on iPad**

1. Opens: `https://yourname-budget-tracker.streamlit.app`
2. Sees login page
3. Clicks "Sign Up"
4. Creates account
5. Logs in
6. Uses budget tracker normally!

### **Bookmark Tip**

On iPad Safari:
1. Open the app
2. Tap Share → "Add to Home Screen"
3. Now it's like a native app! 📱

---

## 🆚 Comparison

### **Old Version (Single User)**
- ❌ One budget for everyone
- ❌ No privacy
- ❌ Everyone sees same data

### **New Version (Multi-User)**
- ✅ Each person has own account
- ✅ Private data per user
- ✅ Secure login system
- ✅ Perfect for sharing app with friends

---

## 💡 Example Usage

**Scenario**: You and 3 friends want to track budgets

**Solution**:
1. You deploy once to Streamlit Cloud
2. Share URL with friends
3. Each person creates account:
   - `unos` (you)
   - `friend1`
   - `friend2`
   - `friend3`
4. Everyone uses same app URL
5. Everyone has private, separate budget data!

---

## 🔄 Migrating Your Existing Data

If you already have data in `budget_data.json`:

```bash
# Your old data
cp budget_data.json budget_data_unos.json

# Now when you login as "unos", you'll see your old data!
```

---

## 🆘 Troubleshooting

### "Username already exists"
- Choose a different username
- Or login if it's your account

### "Incorrect password"
- Check caps lock
- Password is case-sensitive
- Min 6 characters

### "Lost my password"
If running locally, you can reset:
```bash
# Delete users.json to start fresh
rm users.json

# All users need to re-signup
```

If deployed on Streamlit Cloud:
- Redeploy the app (clears data)
- Or access the server files (advanced)

---

## 📊 Files Created

After using the multi-user version:

```
/Users/sonuvelgekar/Desktop/BUDGET/
├── budget_tracker.py          ← Multi-user app
├── users.json                 ← User credentials (hashed)
├── budget_data_unos.json      ← Your budget
├── budget_data_friend.json    ← Friend's budget
└── requirements.txt           ← Dependencies
```

---

## 🎁 Pro Tips

1. **Strong Passwords**: Use at least 8 characters
2. **Unique Usernames**: Make them memorable
3. **Regular Backups**: Export data monthly
4. **Share Wisely**: Only share URL with trusted people
5. **Reset Option**: Keep `users.json` backed up

---

## ✨ What You Can Do Now

- ✅ Create account for yourself
- ✅ Login/logout anytime
- ✅ Friend creates their account
- ✅ Both use same URL
- ✅ Completely private data
- ✅ Works on iPad, iPhone, laptop, anywhere!

---

**Ready to try it?** Download the file and run it locally first, then deploy! 🚀
