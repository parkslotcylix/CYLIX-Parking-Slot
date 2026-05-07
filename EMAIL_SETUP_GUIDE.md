# Email Setup Guide - SendGrid for Production

## Issue
Gmail SMTP is not working on Render. Emails are not being sent even though the response is successful.

## Why Gmail SMTP Fails on Render

1. **Port Blocking**: Render may block SMTP ports (587, 465)
2. **IP Reputation**: Render's IPs may be blacklisted by Gmail
3. **Security**: Gmail blocks connections from cloud servers
4. **Rate Limiting**: Gmail has strict rate limits

## Solution: Use SendGrid API

SendGrid is a reliable email service designed for production applications.

### Benefits
- ✅ **Free Tier**: 100 emails/day (enough for password resets)
- ✅ **Reliable**: 99.9% uptime
- ✅ **Fast**: API-based (no SMTP blocking)
- ✅ **Production-Ready**: Used by major companies
- ✅ **Easy Setup**: Just need API key

---

## Setup Instructions

### Step 1: Create SendGrid Account

1. Go to: https://signup.sendgrid.com/
2. Sign up for free account
3. Verify your email address
4. Complete the onboarding

### Step 2: Create API Key

1. Log in to SendGrid dashboard
2. Go to **Settings** → **API Keys**
3. Click **Create API Key**
4. Name: `ParkSlot Production`
5. Permissions: **Full Access** (or **Mail Send** only)
6. Click **Create & View**
7. **Copy the API key** (you won't see it again!)

Example API key:
```
SG.xxxxxxxxxxxxxxxxxxx.yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
```

### Step 3: Verify Sender Email

1. Go to **Settings** → **Sender Authentication**
2. Click **Verify a Single Sender**
3. Fill in details:
   - From Name: `ParkSlot`
   - From Email: `parkslotcylix@gmail.com` (or your domain email)
   - Reply To: Same as From Email
   - Company Address: Your address
4. Click **Create**
5. Check your email and click verification link

### Step 4: Configure Render Environment Variables

1. Go to Render dashboard
2. Select your service
3. Go to **Environment** tab
4. Add these variables:

| Variable | Value | Example |
|----------|-------|---------|
| `USE_SENDGRID` | `true` | `true` |
| `SENDGRID_API_KEY` | Your API key | `SG.xxx...` |
| `EMAIL_SENDER` | Verified email | `parkslotcylix@gmail.com` |

5. Click **Save Changes**
6. Render will auto-redeploy

---

## Alternative: Resend (Recommended for Simplicity)

Resend is even simpler than SendGrid.

### Benefits
- ✅ **Free Tier**: 100 emails/day
- ✅ **Simpler API**: Easier to use
- ✅ **Modern**: Built for developers
- ✅ **Great Docs**: Easy to follow

### Setup Resend

1. Go to: https://resend.com/signup
2. Sign up for free
3. Verify email
4. Go to **API Keys**
5. Create new API key
6. Copy the key (starts with `re_`)

### Configure for Resend

Add to Render environment variables:
```
USE_SENDGRID=false
EMAIL_SENDER=parkslotcylix@gmail.com
```

Then update the code to use Resend API (simpler than SendGrid).

---

## Testing

### Test SendGrid Setup

1. After configuring Render environment variables
2. Wait for auto-deploy (2-5 minutes)
3. Test forgot password:
   ```bash
   curl -X POST https://cylix-parking-slot.onrender.com/api/forgot-password \
     -H "Content-Type: application/json" \
     -d '{"email":"your-email@example.com"}'
   ```

4. Check Render logs:
   ```
   📧 Using SendGrid API
   ✅ Email sent successfully via SendGrid to: your-email@example.com
   ```

5. Check your email inbox (should arrive in seconds)

### Test Locally

1. Add to `.env` file:
   ```
   USE_SENDGRID=true
   SENDGRID_API_KEY=SG.your-api-key-here
   EMAIL_SENDER=parkslotcylix@gmail.com
   ```

2. Run app:
   ```bash
   python app.py
   ```

3. Test forgot password

---

## Troubleshooting

### SendGrid API Error 401
```
❌ SendGrid error: 401 - Unauthorized
```

**Solution**: Check API key is correct in Render environment variables

### SendGrid API Error 403
```
❌ SendGrid error: 403 - Forbidden
```

**Solution**: 
1. Verify sender email in SendGrid dashboard
2. Check API key has "Mail Send" permission

### Email Not Arriving
1. Check spam folder
2. Check SendGrid dashboard → Activity
3. Verify sender email is verified
4. Check recipient email is valid

### Still Using Gmail SMTP
```
📧 Using SMTP (Gmail)
```

**Solution**: 
1. Set `USE_SENDGRID=true` in Render
2. Set `SENDGRID_API_KEY` in Render
3. Redeploy

---

## Code Changes Made

### 1. Updated EMAIL_CONFIG
```python
EMAIL_CONFIG = {
    'sender_email': os.getenv('EMAIL_SENDER', 'parkslotcylix@gmail.com'),
    'sender_password': os.getenv('EMAIL_PASSWORD', 'dzxy kmck urft qodf'),
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', 587)),
    'use_sendgrid': os.getenv('USE_SENDGRID', 'false').lower() == 'true',
    'sendgrid_api_key': os.getenv('SENDGRID_API_KEY', '')
}
```

### 2. Updated send_email Function
```python
def send_email(recipient_email, subject, html_content):
    # Try SendGrid first if configured
    if EMAIL_CONFIG.get('use_sendgrid') and EMAIL_CONFIG.get('sendgrid_api_key'):
        # Use SendGrid API
        response = requests.post(sendgrid_url, headers=headers, json=data)
        if response.status_code == 202:
            return True
    
    # Fall back to SMTP (Gmail)
    # ... SMTP code ...
```

---

## Deployment Steps

### 1. Commit Changes
```bash
git add app.py EMAIL_SETUP_GUIDE.md
git commit -m "feat: Add SendGrid email support for production

- Add SendGrid API integration
- Fall back to Gmail SMTP if SendGrid not configured
- Add USE_SENDGRID and SENDGRID_API_KEY environment variables
- Improve email delivery reliability on Render"
```

### 2. Push to GitHub
```bash
git push origin main
```

### 3. Configure Render
1. Go to Render dashboard
2. Add environment variables:
   - `USE_SENDGRID=true`
   - `SENDGRID_API_KEY=your-key-here`
   - `EMAIL_SENDER=parkslotcylix@gmail.com`
3. Save (auto-redeploys)

### 4. Test
- Test forgot password
- Check email arrives
- Check Render logs

---

## Cost Comparison

| Service | Free Tier | Paid Plans | Best For |
|---------|-----------|------------|----------|
| **SendGrid** | 100/day | $15/mo (40k) | Production apps |
| **Resend** | 100/day | $20/mo (50k) | Modern apps |
| **Mailgun** | 100/day | $35/mo (50k) | Enterprise |
| **Gmail SMTP** | ~100/day | Free | Development only |

**Recommendation**: Use **SendGrid** for production (free tier is enough)

---

## Quick Start (SendGrid)

1. **Sign up**: https://signup.sendgrid.com/
2. **Create API Key**: Settings → API Keys → Create
3. **Verify Sender**: Settings → Sender Authentication → Verify Single Sender
4. **Add to Render**:
   ```
   USE_SENDGRID=true
   SENDGRID_API_KEY=SG.your-key-here
   EMAIL_SENDER=parkslotcylix@gmail.com
   ```
5. **Deploy**: Render auto-deploys
6. **Test**: Forgot password should work!

---

## Status
✅ Code updated to support SendGrid  
⏳ Waiting for SendGrid setup and Render configuration

## Next Steps
1. Create SendGrid account
2. Get API key
3. Verify sender email
4. Add to Render environment variables
5. Test forgot password
