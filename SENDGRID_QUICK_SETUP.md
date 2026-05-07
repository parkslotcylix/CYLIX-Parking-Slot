# SendGrid Quick Setup - 5 Minutes

## ✅ Code Updated!
Your code now supports SendGrid for reliable email delivery on Render.

---

## 🚀 Quick Setup (5 Steps)

### Step 1: Create SendGrid Account (2 min)
1. Go to: **https://signup.sendgrid.com/**
2. Sign up (free)
3. Verify your email

### Step 2: Get API Key (1 min)
1. Log in to SendGrid
2. Go to: **Settings** → **API Keys**
3. Click: **Create API Key**
4. Name: `ParkSlot`
5. Permission: **Full Access**
6. Click: **Create & View**
7. **COPY THE KEY** (starts with `SG.`)

### Step 3: Verify Sender Email (1 min)
1. Go to: **Settings** → **Sender Authentication**
2. Click: **Verify a Single Sender**
3. Fill in:
   - From Name: `ParkSlot`
   - From Email: `parkslotcylix@gmail.com`
   - Reply To: `parkslotcylix@gmail.com`
4. Click: **Create**
5. Check email and click verification link

### Step 4: Add to Render (1 min)
1. Go to: **Render Dashboard**
2. Select your service
3. Go to: **Environment** tab
4. Add these 3 variables:

```
USE_SENDGRID = true
SENDGRID_API_KEY = SG.your-api-key-here
EMAIL_SENDER = parkslotcylix@gmail.com
```

5. Click: **Save Changes**
6. Render will auto-deploy

### Step 5: Test (30 sec)
1. Wait 2-3 minutes for deployment
2. Go to your app
3. Test forgot password
4. Email should arrive in seconds! ✅

---

## 📋 Environment Variables for Render

Copy these to Render:

| Variable | Value |
|----------|-------|
| `USE_SENDGRID` | `true` |
| `SENDGRID_API_KEY` | `SG.your-actual-key-here` |
| `EMAIL_SENDER` | `parkslotcylix@gmail.com` |

---

## 🧪 Testing

### After Setup
1. Go to: https://cylix-parking-slot.onrender.com
2. Click: **Forgot Password**
3. Enter email
4. Click: **Send Reset Link**
5. Check email (arrives in seconds)

### Check Render Logs
```
📧 Using SendGrid API
✅ Email sent successfully via SendGrid to: user@example.com
```

---

## ❓ Troubleshooting

### Email Not Arriving?
1. ✅ Check spam folder
2. ✅ Verify sender email in SendGrid
3. ✅ Check API key is correct
4. ✅ Check `USE_SENDGRID=true` in Render

### Still Using Gmail?
```
📧 Using SMTP (Gmail)
```

**Fix**: Set `USE_SENDGRID=true` in Render environment variables

---

## 💰 Cost

**SendGrid Free Tier:**
- ✅ 100 emails/day
- ✅ Perfect for password resets
- ✅ No credit card required
- ✅ Upgrade later if needed

---

## 🎯 Result

After setup:
- ✅ Emails deliver in seconds
- ✅ No SMTP blocking
- ✅ Production-ready
- ✅ Reliable delivery
- ✅ Free tier sufficient

---

## 📞 Support

### SendGrid Support
- Docs: https://docs.sendgrid.com/
- Support: https://support.sendgrid.com/

### Need Help?
Check `EMAIL_SETUP_GUIDE.md` for detailed instructions.

---

## Status
✅ Code deployed to GitHub  
⏳ Waiting for SendGrid setup  
⏳ Waiting for Render configuration

**Next**: Follow the 5 steps above to complete setup!
