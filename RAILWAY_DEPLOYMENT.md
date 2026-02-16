# Railway Deployment Instructions - COMPLETE GUIDE

## The Error You're Seeing
```
connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed
```
This means Django can't find the database because environment variables are not set in Railway.

## SOLUTION: Follow These Steps Exactly

### Step 1: Create PostgreSQL Database in Railway

1. Go to your Railway project dashboard
2. Click **"+ New"** button
3. Select **"Database"** → **"Add PostgreSQL"**
4. Wait for PostgreSQL to provision (takes 1-2 minutes)

### Step 2: Get Database Connection Details

After PostgreSQL is created, click on it and go to **"Variables"** tab. You'll see:
- `PGHOST` (this is your POSTGRES_HOST)
- `PGPORT` (this is your POSTGRES_PORT)
- `PGDATABASE` (this is your POSTGRES_DB)
- `PGUSER` (this is your POSTGRES_USER)
- `PGPASSWORD` (this is your POSTGRES_PASSWORD)

### Step 3: Set Environment Variables in Your App Service

1. Click on your **app service** (not the database)
2. Go to **"Variables"** tab
3. Click **"+ New Variable"** and add these **ONE BY ONE**:

```
POSTGRES_HOST=<copy PGHOST value from database>
POSTGRES_PORT=<copy PGPORT value from database>
POSTGRES_DB=<copy PGDATABASE value from database>
POSTGRES_USER=<copy PGUSER value from database>
POSTGRES_PASSWORD=<copy PGPASSWORD value from database>
SECRET_KEY=django-insecure-8aa_+4cmt5z@+b6p9j_76n)t_+ah_3&%(zq9zj5a*5576*mwah
Debug=False
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_SAMESITE=None
CSRF_COOKIE_SAMESITE=None
```

**IMPORTANT**: 
- Copy the exact values from the PostgreSQL service variables
- Do NOT include `<` or `>` symbols
- Make sure there are NO spaces around the `=` sign

### Step 4: Redeploy

After setting all variables:
1. Railway will automatically redeploy
2. OR click **"Deploy"** button manually
3. Check the **"Deployments"** tab to see logs

### Step 5: Verify Deployment

Watch the deployment logs. You should see:
```
Waiting for PostgreSQL...
Database is ready!
Running migrations...
Starting Daphne server...
```

If you see errors, check that all environment variables are set correctly.

---

## Alternative: Use Railway's Reference Variables (EASIER METHOD)

Railway can automatically link services. Here's the easier way:

### Step 1: Create PostgreSQL Database (same as above)

### Step 2: Use Reference Variables

In your app service Variables tab, add:

```
POSTGRES_HOST=${{Postgres.PGHOST}}
POSTGRES_PORT=${{Postgres.PGPORT}}
POSTGRES_DB=${{Postgres.PGDATABASE}}
POSTGRES_USER=${{Postgres.PGUSER}}
POSTGRES_PASSWORD=${{Postgres.PGPASSWORD}}
SECRET_KEY=django-insecure-8aa_+4cmt5z@+b6p9j_76n)t_+ah_3&%(zq9zj5a*5576*mwah
Debug=False
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_SAMESITE=None
CSRF_COOKIE_SAMESITE=None
```

**Note**: Replace `Postgres` with your actual PostgreSQL service name in Railway.

---

## Using External Database (Render, AWS, etc.)

If you're using an external database:

```
POSTGRES_HOST=singapore-postgres.render.com
POSTGRES_PORT=5432
POSTGRES_DB=emp_db_y2mb
POSTGRES_USER=emp_db_y2mb_user
POSTGRES_PASSWORD=02qxArKKXkNVQXXOMX6EyTJ5NWiNcbDo
SECRET_KEY=django-insecure-8aa_+4cmt5z@+b6p9j_76n)t_+ah_3&%(zq9zj5a*5576*mwah
Debug=False
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_SAMESITE=None
CSRF_COOKIE_SAMESITE=None
```

---

## Troubleshooting

### Error: "POSTGRES_HOST environment variable is not set"
**Solution**: You forgot to set environment variables. Go back to Step 3.

### Error: "Could not connect to database after 30 attempts"
**Solutions**:
1. Check that PostgreSQL service is running in Railway
2. Verify POSTGRES_HOST and POSTGRES_PORT are correct
3. Make sure your app and database are in the same Railway project
4. Check database service logs for errors

### Error: "password authentication failed"
**Solution**: POSTGRES_USER or POSTGRES_PASSWORD is wrong. Copy exact values from database service.

### Error: "database does not exist"
**Solution**: POSTGRES_DB is wrong. Copy exact value from database service.

### Migrations Not Running
**Solution**: Check deployment logs. The Dockerfile automatically runs migrations. If they fail, you'll see the error in logs.

### Static Files Not Loading
**Solution**: Static files are collected during Docker build. Check build logs for errors.

---

## What the Dockerfile Does Automatically

✅ Waits for database to be ready (up to 60 seconds)
✅ Checks that all environment variables are set
✅ Runs database migrations automatically
✅ Collects static files during build
✅ Starts Daphne server on Railway's PORT
✅ Shows helpful error messages if something is wrong

---

## Quick Checklist

Before deploying, make sure:
- [ ] PostgreSQL database is created in Railway
- [ ] All 5 POSTGRES_* variables are set in app service
- [ ] SECRET_KEY is set
- [ ] Code is pushed to GitHub/GitLab
- [ ] Railway is connected to your repository

---

## Need Help?

Check Railway deployment logs:
1. Go to your project in Railway
2. Click on your app service
3. Click "Deployments" tab
4. Click on the latest deployment
5. Read the logs to see what went wrong

The Dockerfile will show clear error messages if environment variables are missing or database connection fails.

