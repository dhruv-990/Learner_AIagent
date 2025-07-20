# 🚀 Deployment Guide

## Quick Deploy Options

### 1. **Railway (Recommended - Easiest)**

#### Step 1: Prepare Your Repository
```bash
# Make sure your code is pushed to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main
```

#### Step 2: Deploy on Railway
1. Go to [Railway](https://railway.app/)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will automatically detect it's a Python app

#### Step 3: Set Environment Variables
In Railway dashboard:
1. Go to your project
2. Click "Variables" tab
3. Add these environment variables:
   ```
   GOOGLE_API_KEY=your_google_api_key
   YOUTUBE_API_KEY=your_youtube_api_key
   PORT=8000
   ```

#### Step 4: Deploy
- Railway will automatically deploy your app
- You'll get a URL like: `https://your-app-name.railway.app`

---

### 2. **Render (Alternative)**

#### Step 1: Prepare Repository
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

#### Step 2: Deploy on Render
1. Go to [Render](https://render.com/)
2. Sign up with GitHub
3. Click "New" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: `learning-path-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

#### Step 3: Set Environment Variables
In Render dashboard:
1. Go to your service
2. Click "Environment" tab
3. Add variables:
   ```
   GOOGLE_API_KEY=your_google_api_key
   YOUTUBE_API_KEY=your_youtube_api_key
   ```

#### Step 4: Deploy
- Render will build and deploy automatically
- You'll get a URL like: `https://your-app-name.onrender.com`

---

### 3. **Heroku (Legacy but Reliable)**

#### Step 1: Install Heroku CLI
```bash
# Download from: https://devcenter.heroku.com/articles/heroku-cli
```

#### Step 2: Deploy
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set GOOGLE_API_KEY=your_google_api_key
heroku config:set YOUTUBE_API_KEY=your_youtube_api_key

# Deploy
git push heroku main

# Open app
heroku open
```

---

## 🔧 **Pre-Deployment Checklist**

### ✅ **Code Ready**
- [ ] All files committed to GitHub
- [ ] `.env` file is in `.gitignore`
- [ ] `env_example.txt` is included
- [ ] `requirements.txt` is up to date
- [ ] `Procfile` is created
- [ ] `runtime.txt` is created

### ✅ **API Keys Ready**
- [ ] Google Gemini API key
- [ ] YouTube API key (optional)
- [ ] Keys are valid and working

### ✅ **Testing**
- [ ] App works locally
- [ ] All features tested
- [ ] No sensitive data in code

---

## 🌐 **Post-Deployment**

### **Share Your App**
Once deployed, you can share your app URL with others:
- **Railway**: `https://your-app-name.railway.app`
- **Render**: `https://your-app-name.onrender.com`
- **Heroku**: `https://your-app-name.herokuapp.com`

### **Monitor Usage**
- Check your API usage in Google Cloud Console
- Monitor YouTube API quotas
- Watch for any errors in deployment logs

### **Scale Up**
- Upgrade to paid plans for more resources
- Add custom domains
- Set up monitoring and logging

---

## 🆘 **Troubleshooting**

### **Common Issues:**

1. **Build Fails**
   - Check `requirements.txt` is complete
   - Verify Python version in `runtime.txt`
   - Check build logs for errors

2. **App Crashes**
   - Verify environment variables are set
   - Check logs for API key errors
   - Ensure all dependencies are installed

3. **API Errors**
   - Verify API keys are correct
   - Check API quotas and billing
   - Test APIs locally first

4. **Port Issues**
   - Make sure app uses `$PORT` environment variable
   - Check `Procfile` is correct
   - Verify `main.py` handles port properly

---

## 💡 **Tips for Production**

1. **Security**
   - Use strong, unique API keys
   - Rotate keys regularly
   - Monitor for unusual usage

2. **Performance**
   - Add caching for API responses
   - Optimize database queries
   - Use CDN for static files

3. **Monitoring**
   - Set up error tracking (Sentry)
   - Monitor API usage
   - Track user analytics

4. **Backup**
   - Regular database backups
   - Version control for all code
   - Document configuration

---

## 🎉 **Success!**

Once deployed, your Learning Path Mentor Bot will be available to users worldwide! 

**Share your app URL and let people create personalized learning paths!** 🚀 