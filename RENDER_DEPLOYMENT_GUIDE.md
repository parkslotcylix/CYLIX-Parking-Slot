# Deploying ParkSlot to Render

This guide walks you through deploying your Flask parking management application to Render.

## Prerequisites

1. **GitHub Account** - Your code must be in a GitHub repository
2. **Render Account** - Sign up at [render.com](https://render.com)
3. **Supabase Account** - Already configured (you have the credentials)

## Step 1: Prepare Your Repository

### 1.1 Create a `.gitignore` file (if not already present)

```
.env
.venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.egg-info/
dist/
build/
.DS_Store
```

### 1.2 Update `requirements.txt`

✅ Already done - includes `gunicorn` for production server

### 1.3 Create `Procfile`

✅ Already created - tells Render how to start your app

### 1.4 Create `render.yaml` (optional but recommended)

✅ Already created - Infrastructure as Code for Render

### 1.5 Push to GitHub

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

## Step 2: Set Up on Render

### 2.1 Connect GitHub to Render

1. Go to [render.com](https://render.com) and sign in
2. Click **"New +"** → **"Web Service"**
3. Select **"Build and deploy from a Git repository"**
4. Click **"Connect account"** and authorize GitHub
5. Select your repository

### 2.2 Configure the Web Service

**Basic Settings:**
- **Name:** `parkslot-api` (or your preferred name)
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- **Plan:** Free (or Starter for production)

### 2.3 Add Environment Variables

Click **"Advanced"** and add these environment variables:

```
SUPABASE_URL=https://bhsofudngyukxkkialwi.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=parkslot_secret_key_2026
EMAIL_SENDER=parkslotcylix@gmail.com
EMAIL_PASSWORD=dzxy kmck urft qodf
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
CORS_ORIGINS=*
```

⚠️ **Security Note:** For production, use environment-specific secrets:
- Store sensitive keys in Render's environment variables, not in `.env`
- Never commit `.env` to GitHub
- Use different credentials for production

### 2.4 Deploy

Click **"Create Web Service"** and Render will:
1. Clone your repository
2. Install dependencies from `requirements.txt`
3. Build the application
4. Start the service with `gunicorn app:app`

## Step 3: Verify Deployment

Once deployed, Render will provide you with a URL like:
```
https://parkslot-api.onrender.com
```

### Test the API:

```bash
# Health check
curl https://parkslot-api.onrender.com/api/health

# Login endpoint
curl -X POST https://parkslot-api.onrender.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"password"}'

# Get slots
curl https://parkslot-api.onrender.com/api/get_slots
```

## Step 4: Update Frontend Configuration

Update your frontend (HTML/JavaScript) to use the new Render URL:

```javascript
// In your JavaScript files, replace:
const API_URL = 'http://localhost:5000';

// With:
const API_URL = 'https://parkslot-api.onrender.com';
```

Or use environment-based configuration:

```javascript
const API_URL = process.env.REACT_APP_API_URL || 'https://parkslot-api.onrender.com';
```

## Step 5: Configure CORS (if needed)

Your `app.py` already has CORS enabled:

```python
CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
```

For production, restrict to specific origins:

```python
CORS(app, origins=[
    "https://yourdomain.com",
    "https://www.yourdomain.com"
], methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
```

## Step 6: Set Up Auto-Deployment

Render automatically deploys when you push to your main branch. To disable:
1. Go to your service settings
2. Disable **"Auto-Deploy"** if you want manual deployments

## Troubleshooting

### Build Fails

**Check logs:**
1. Go to your Render dashboard
2. Click your service
3. View the **"Logs"** tab

**Common issues:**
- Missing dependencies in `requirements.txt`
- Python version mismatch
- Environment variables not set

### Application Crashes

**Check runtime logs:**
1. Click **"Logs"** tab
2. Look for error messages

**Common issues:**
- Database connection failed → Check `SUPABASE_*` variables
- Port binding error → Ensure `FLASK_PORT=5000`
- Missing static files → Check `static/` folder exists

### Slow Performance

- Render free tier has limited resources
- Upgrade to **Starter** or **Standard** plan for better performance
- Consider caching strategies

## Production Checklist

- [ ] Environment variables set in Render (not in `.env`)
- [ ] `FLASK_DEBUG=False` in production
- [ ] CORS configured for your domain
- [ ] Database backups enabled in Supabase
- [ ] Email credentials secured
- [ ] SSL/HTTPS enabled (automatic on Render)
- [ ] Monitoring and alerts configured
- [ ] Error logging set up

## Useful Render Commands

### View Logs
```bash
# Via Render Dashboard → Logs tab
```

### Redeploy
```bash
# Push to main branch (auto-deploys)
# Or manually trigger in Render dashboard
```

### Environment Variables
```bash
# Update in Render Dashboard → Environment
```

## Next Steps

1. **Custom Domain:** Add your domain in Render settings
2. **SSL Certificate:** Automatic with Render
3. **Database Backups:** Configure in Supabase
4. **Monitoring:** Set up alerts in Render dashboard
5. **CI/CD:** Consider GitHub Actions for testing before deploy

## Support

- **Render Docs:** https://render.com/docs
- **Flask Deployment:** https://flask.palletsprojects.com/deployment/
- **Supabase Docs:** https://supabase.com/docs

---

**Deployment URL:** `https://parkslot-api.onrender.com` (replace with your actual URL)
