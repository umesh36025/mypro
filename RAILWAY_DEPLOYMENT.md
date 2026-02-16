# Railway Deployment Instructions

## Prerequisites
- Railway account (https://railway.app)
- PostgreSQL database (can be created in Railway)

## Step 1: Push Code to GitHub/GitLab
```bash
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

## Step 2: Create New Project in Railway
1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository

## Step 3: Add PostgreSQL Database
1. In your Railway project, click "+ New"
2. Select "Database" → "Add PostgreSQL"
3. Railway will automatically create a PostgreSQL instance

## Step 4: Set Environment Variables
In Railway project settings, add these variables:

### Required Variables:
```
POSTGRES_DB=<from Railway PostgreSQL>
POSTGRES_USER=<from Railway PostgreSQL>
POSTGRES_PASSWORD=<from Railway PostgreSQL>
POSTGRES_HOST=<from Railway PostgreSQL>
POSTGRES_PORT=<from Railway PostgreSQL>
SECRET_KEY=django-insecure-8aa_+4cmt5z@+b6p9j_76n)t_+ah_3&%(zq9zj5a*5576*mwah
Debug=False
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_SAMESITE=None
CSRF_COOKIE_SAMESITE=None
```

### Railway Auto-Provides:
- `PORT` (automatically set by Railway)
- Database credentials (if using Railway PostgreSQL)

## Step 5: Configure Build Settings
Railway will automatically detect the Dockerfile and use it.

If needed, you can set:
- **Build Command**: (leave empty, Dockerfile handles it)
- **Start Command**: (leave empty, Dockerfile CMD handles it)

## Step 6: Deploy
1. Railway will automatically deploy when you push to GitHub
2. Wait for build to complete (2-5 minutes)
3. Check logs for any errors

## Step 7: Access Your Application
Railway will provide a public URL like:
```
https://your-app-name.up.railway.app
```

## Troubleshooting

### Database Connection Error
If you see database connection errors:
1. Verify all POSTGRES_* environment variables are set correctly
2. Check that Railway PostgreSQL is running
3. Ensure your app and database are in the same Railway project

### Static Files Not Loading
The Dockerfile automatically runs `collectstatic` during build.
If issues persist, check Railway logs.

### Port Issues
Railway automatically sets the PORT environment variable.
The Dockerfile uses `${PORT:-8000}` to handle this.

### Migration Errors
Migrations run automatically on container start.
Check Railway logs if migrations fail.

## Important Notes

1. **Environment Variables**: Railway uses environment variables, not .env files
2. **Database**: Use Railway PostgreSQL or external database (Render, AWS RDS, etc.)
3. **Static Files**: Collected during Docker build
4. **Migrations**: Run automatically on each deployment
5. **Logs**: Check Railway dashboard for deployment logs

## Automatic Deployments
Railway automatically redeploys when you push to your connected Git branch.

## Manual Redeploy
In Railway dashboard:
1. Go to your project
2. Click "Deployments"
3. Click "Deploy" button

## Health Checks
The Dockerfile includes health checks. Railway will monitor your app automatically.
