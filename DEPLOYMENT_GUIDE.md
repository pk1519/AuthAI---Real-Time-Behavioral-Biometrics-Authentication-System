# AuthAI Streamlit Cloud Deployment Guide

## 🚀 Complete Setup: From Login to Working

This guide will walk you through deploying your AuthAI project to Streamlit Cloud, ensuring everything works from authentication to behavioral monitoring.

### 📋 Prerequisites

1. **GitHub Account**: You'll need a GitHub account to deploy to Streamlit Cloud
2. **MongoDB Atlas Account** (Recommended): For cloud database access
3. **Streamlit Cloud Account**: Sign up at https://share.streamlit.io/

### 🗂 Step 1: Prepare Your Repository

#### 1.1 Create GitHub Repository
1. Create a new repository on GitHub (e.g., `authai-cloud`)
2. Make it public (required for free Streamlit Cloud)

#### 1.2 Upload Your Files
Upload these files to your repository:
```
authai-cloud/
├── authai_streamlit_app.py       # Main app
├── authai_core_cloud.py          # Cloud-compatible core
├── user_auth.py                  # Authentication system
├── auth_pages.py                 # Login/signup pages
├── requirements.txt              # Dependencies
├── README.md                     # Documentation
└── .streamlit/                   # Streamlit config (optional)
    └── config.toml
```

### 🗄 Step 2: Database Setup (MongoDB Atlas)

#### 2.1 Create MongoDB Atlas Cluster
1. Go to https://cloud.mongodb.com
2. Sign up for a free account
3. Create a new cluster (choose free tier M0)
4. Wait for cluster to be ready (2-3 minutes)

#### 2.2 Setup Database Access
1. **Database Access**:
   - Click "Database Access" in left sidebar
   - Add new database user
   - Username: `authai_user`
   - Password: Generate secure password
   - Built-in Role: `Read and write to any database`

2. **Network Access**:
   - Click "Network Access" in left sidebar
   - Add IP Address: `0.0.0.0/0` (Allow access from anywhere)
   - Confirm

#### 2.3 Get Connection String
1. Click "Database" in left sidebar
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string (looks like: `mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/`)

#### 2.4 Update Your Code
In your `user_auth.py`, you have two options:

**Option A: Use Streamlit Secrets (Recommended)**
```python
import streamlit as st

# MongoDB Configuration - use secrets for production
try:
    MONGODB_URI = st.secrets["MONGODB_URI"]
except:
    MONGODB_URI = "mongodb://localhost:27017/"  # Fallback for local development
```

**Option B: Direct Update (Less Secure)**
```python
MONGODB_URI = "mongodb+srv://authai_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/"
```

### ⚙️ Step 3: Streamlit Configuration

#### 3.1 Create .streamlit/config.toml (Optional)
```toml
[server]
headless = true
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

#### 3.2 Create .streamlit/secrets.toml (For local testing)
```toml
MONGODB_URI = "mongodb+srv://authai_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/"
```

**⚠️ Important: Add `.streamlit/secrets.toml` to your `.gitignore` file!**

### 🚀 Step 4: Deploy to Streamlit Cloud

#### 4.1 Access Streamlit Cloud
1. Go to https://share.streamlit.io/
2. Sign in with GitHub account

#### 4.2 Deploy New App
1. Click "New app"
2. Choose your repository
3. Branch: `main` (or `master`)
4. Main file path: `authai_streamlit_app.py`
5. App URL: Choose custom URL like `your-username-authai`

#### 4.3 Add Secrets
1. Click "Advanced settings"
2. In "Secrets" section, add:
```toml
MONGODB_URI = "mongodb+srv://authai_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/"
```

#### 4.4 Deploy
1. Click "Deploy!"
2. Wait for deployment (2-5 minutes)
3. Your app will be available at: `https://your-app-name.streamlit.app/`

### 🧪 Step 5: Test Your Deployment

#### 5.1 Access Your App
1. Visit your Streamlit app URL
2. You should see the login page

#### 5.2 Create Test Account
1. Click "Create New Account"
2. Fill in details:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `test123`
3. Click "Create Account"

#### 5.3 Test Authentication
1. Login with your test account
2. You should be redirected to the dashboard
3. The system should auto-initialize

#### 5.4 Test AuthAI Features
1. The system should auto-start monitoring
2. Click "🤖 Run Bot Simulator" to test detection
3. View real-time charts and predictions

### 🔧 Step 6: Customization & Features

#### 6.1 Available Features
- ✅ **User Authentication**: Registration, login, logout
- ✅ **User Profiles**: View and edit user information
- ✅ **Behavioral Monitoring**: Simulated behavioral biometrics
- ✅ **Real-time Dashboard**: Live charts and metrics
- ✅ **Bot Detection**: Simulated bot behavior detection
- ✅ **Data Logging**: All detections saved to CSV

#### 6.2 Cloud vs Local Differences
| Feature | Cloud Version | Local Version |
|---------|---------------|---------------|
| Mouse Tracking | Simulated | Real hardware |
| Keyboard Tracking | Simulated | Real hardware |
| Bot Detection | ML Model | ML Model |
| Authentication | MongoDB Atlas | MongoDB Local |
| Performance | Good | Excellent |

### 🛠 Step 7: Troubleshooting

#### 7.1 Common Issues

**App Won't Start**
- Check requirements.txt for typos
- Ensure all files are uploaded to GitHub
- Check Streamlit Cloud logs for errors

**Database Connection Failed**
- Verify MongoDB Atlas connection string
- Check network access settings (0.0.0.0/0)
- Ensure database user has correct permissions

**Authentication Not Working**
- Check secrets configuration
- Verify MongoDB URI format
- Test connection string locally first

**Missing Dependencies**
- Update requirements.txt
- Restart Streamlit Cloud app
- Check for package version conflicts

#### 7.2 Logs and Debugging
1. In Streamlit Cloud, click "Manage app"
2. Click "Logs" to see detailed error messages
3. Look for import errors, connection issues, etc.

### 🎯 Step 8: Going Live

#### 8.1 Production Checklist
- [ ] MongoDB Atlas cluster configured
- [ ] Database users and permissions set
- [ ] Secrets properly configured
- [ ] All tests passing
- [ ] Performance acceptable
- [ ] Security considerations reviewed

#### 8.2 Share Your App
Your app will be available at:
```
https://your-app-name.streamlit.app/
```

Share this URL with users for access!

### 📈 Step 9: Monitoring & Maintenance

#### 9.1 Monitor Usage
- Check Streamlit Cloud analytics
- Monitor MongoDB Atlas metrics
- Review detection logs

#### 9.2 Updates
To update your app:
1. Push changes to GitHub
2. Streamlit Cloud auto-deploys
3. Check logs for any issues

### 🚨 Important Notes

1. **Free Tier Limitations**:
   - Streamlit Cloud free tier has resource limits
   - MongoDB Atlas free tier has storage limits
   - Consider upgrading for production use

2. **Security**:
   - Never commit secrets to GitHub
   - Use Streamlit secrets for sensitive data
   - Consider IP restrictions for production

3. **Performance**:
   - Cloud simulation is slower than local
   - Real-time updates may have delays
   - Consider optimizing for cloud environment

### ✅ Success Checklist

After deployment, verify:
- [ ] App loads without errors
- [ ] Login/signup works
- [ ] Dashboard appears after login
- [ ] AuthAI system initializes
- [ ] Monitoring starts automatically
- [ ] Bot simulation works
- [ ] Charts display data
- [ ] User profile accessible
- [ ] Logout works properly

## 🎉 Congratulations!

Your AuthAI system is now live on Streamlit Cloud! Users can:

1. **Register** for new accounts
2. **Login** securely
3. **Monitor** their behavior in real-time
4. **Test** bot detection
5. **View** analytics and charts
6. **Manage** their profile

Your complete authentication-to-monitoring pipeline is working in the cloud!

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review Streamlit Cloud documentation
3. Check MongoDB Atlas documentation
4. Examine app logs for specific errors

---

**AuthAI** - Now available in the cloud! 🚀🔒
