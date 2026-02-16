# Render Deployment Guide

## Step 1: Push Code to GitHub

```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

## Step 2: Create PostgreSQL Database on Render

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Fill in:
   - Name: `ems-database` (or any name)
   - Database: `ems_db`
   - User: `ems_user`
   - Region: Choose closest to your users
   - Plan: Free or paid
4. Click **"Create Database"**
5. Wait for database to be ready (1-2 minutes)
6. Copy the **"Internal Database URL"** (starts with `postgresql://`)

## Step 3: Create Web Service on Render

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Fill in:
   - **Name**: `ems-app` (or any name)
   - **Region**: Same as database
   - **Branch**: `main`
   - **Runtime**: `Docker`
   - **Plan**: Free or paid

## Step 4: Set Environment Variables

In the web service settings, add these environment variables:

### From Your Database:
Click on your PostgreSQL database, go to "Connect" tab, and copy:

```
POSTGRES_HOST=<Internal hostname from Render PostgreSQL>
POSTGRES_PORT=5432
POSTGRES_DB=<Database name>
POSTGRES_USER=<User name>
POSTGRES_PASSWORD=<Password>
```

### Additional Variables:
```
SECRET_KEY=django-insecure-8aa_+4cmt5z@+b6p9j_76n)t_+ah_3&%(zq9zj5a*5576*mwah
Debug=False
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_SAMESITE=None
CSRF_COOKIE_SAMESITE=None
```

## Step 5: Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Detect Dockerfile
   - Build Docker image
   - Run migrations
   - Start your app
3. Wait 5-10 minutes for first deployment

## Step 6: Access Your App

Your app will be available at:
```
https://ems-app.onrender.com
```
(Replace `ems-app` with your actual service name)

## Important Notes

### Free Tier Limitations:
- App spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- Database has 90-day expiration on free tier

### Automatic Deployments:
Render automatically redeploys when you push to GitHub

### Manual Redeploy:
1. Go to your web service dashboard
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

### View Logs:
1. Go to your web service
2. Click **"Logs"** tab
3. See real-time deployment and runtime logs

## Troubleshooting

### Build Fails
- Check that Dockerfile is in repository root
- Verify requirements.txt has all dependencies
- Check build logs for specific errors

### Database Connection Error
- Verify all POSTGRES_* variables are set correctly
- Use **Internal Database URL** hostname, not external
- Ensure database and web service are in same region

### App Not Starting
- Check logs for errors
- Verify migrations ran successfully
- Ensure port 8000 is exposed in Dockerfile

### Static Files Not Loading
- Static files are collected during build
- Check build logs for collectstatic errors
- Verify STATIC_ROOT is set in settings.py

## What the Dockerfile Does

✅ Installs all dependencies
✅ Collects static files during build
✅ Runs migrations on startup
✅ Starts Daphne server for WebSocket support
✅ Exposes port 8000

## Environment Variables Checklist

Before deploying, ensure these are set:
- [ ] POSTGRES_HOST
- [ ] POSTGRES_PORT
- [ ] POSTGRES_DB
- [ ] POSTGRES_USER
- [ ] POSTGRES_PASSWORD
- [ ] SECRET_KEY
- [ ] Debug=False

## Need Help?

Check Render documentation: https://render.com/docs
