# Storage Upload Error - Diagnostic Guide

## 🔴 Error: 500 Internal Server Error

You're seeing this error because the Supabase Storage bucket hasn't been set up yet.

---

## 🔍 Step 1: Test Storage Connection

After Render finishes deploying (wait 2-3 minutes), test the storage connection:

**Open this URL in your browser:**
```
https://cylix-parking-slot.onrender.com/api/test_storage
```

### Possible Responses:

#### ✅ Success (200)
```json
{
  "success": true,
  "message": "Supabase Storage bucket 'avatars' is accessible",
  "bucket_exists": true
}
```
**Action:** Storage is ready! Try uploading again.

#### ❌ Bucket Not Found (404)
```json
{
  "success": false,
  "message": "Storage bucket 'avatars' not found",
  "bucket_exists": false,
  "instructions": "Create bucket in Supabase Dashboard..."
}
```
**Action:** Go to Step 2 below to create the bucket.

#### ❌ Permission Denied (403)
```json
{
  "success": false,
  "message": "Permission denied - storage policies not set",
  "bucket_exists": true,
  "instructions": "Set storage policies..."
}
```
**Action:** Bucket exists but policies are missing. Go to Step 3 below.

---

## 🔧 Step 2: Create Supabase Storage Bucket

### Quick Method (5 minutes):

1. **Go to Supabase Storage:**
   ```
   https://supabase.com/dashboard/project/bhsofudngyukxkkialwi/storage/buckets
   ```

2. **Click "New bucket"** (green button, top right)

3. **Fill in the form:**
   - **Name:** `avatars` (exactly this, lowercase)
   - **Public bucket:** ✅ **CHECK THIS BOX** (very important!)
   - **File size limit:** 5242880 (5MB - default is fine)

4. **Click "Create bucket"**

5. **Verify:** You should see `avatars` in the bucket list

---

## 🔐 Step 3: Set Storage Policies

### Method 1: Using Supabase SQL Editor (Fastest)

1. **Go to SQL Editor:**
   ```
   https://supabase.com/dashboard/project/bhsofudngyukxkkialwi/sql/new
   ```

2. **Paste this SQL and click "Run":**
   ```sql
   -- Policy 1: Public read access
   CREATE POLICY "Public Access"
   ON storage.objects FOR SELECT
   USING ( bucket_id = 'avatars' );

   -- Policy 2: Authenticated upload
   CREATE POLICY "Authenticated users can upload"
   ON storage.objects FOR INSERT
   WITH CHECK ( bucket_id = 'avatars' AND auth.role() = 'authenticated' );

   -- Policy 3: Service role full access
   CREATE POLICY "Service role full access"
   ON storage.objects FOR ALL
   USING ( bucket_id = 'avatars' );
   ```

3. **Verify:** Go to Storage → avatars → Policies - you should see 3 policies

### Method 2: Using Supabase UI (Manual)

1. **Go to Storage → avatars → Policies tab**

2. **Click "New Policy"** (3 times, once for each policy)

3. **Policy 1: Public Access**
   - Click "For full customization"
   - Policy name: `Public Access`
   - Allowed operation: **SELECT** ✅
   - Target roles: **public** ✅
   - USING expression: `bucket_id = 'avatars'`
   - Click "Review" → "Save policy"

4. **Policy 2: Authenticated Upload**
   - Click "New Policy" → "For full customization"
   - Policy name: `Authenticated users can upload`
   - Allowed operation: **INSERT** ✅
   - Target roles: **authenticated** ✅
   - WITH CHECK expression: `bucket_id = 'avatars' AND auth.role() = 'authenticated'`
   - Click "Review" → "Save policy"

5. **Policy 3: Service Role Full Access**
   - Click "New Policy" → "For full customization"
   - Policy name: `Service role full access`
   - Allowed operation: **ALL** ✅ (check all: SELECT, INSERT, UPDATE, DELETE)
   - Target roles: **service_role** ✅
   - USING expression: `bucket_id = 'avatars'`
   - Click "Review" → "Save policy"

---

## ✅ Step 4: Verify Setup

### Test 1: Storage Connection
```
https://cylix-parking-slot.onrender.com/api/test_storage
```
Should return: `"success": true`

### Test 2: Upload Profile Picture
1. Go to: https://cylix-parking-slot.onrender.com/account
2. Click the **"+"** button on avatar
3. Select an image file
4. Upload should succeed ✅

### Test 3: Verify URL Format
Check browser DevTools (F12) → Network tab → Response should show:
```json
{
  "success": true,
  "picture_url": "https://bhsofudngyukxkkialwi.supabase.co/storage/v1/object/public/avatars/profile-pictures/admin_1_1234567890.jpg"
}
```

---

## 🐛 Troubleshooting

### Issue: Still getting 500 error after setup
**Cause:** Render hasn't finished deploying the new code  
**Fix:** Wait 2-3 minutes for Render deployment to complete, then try again

### Issue: Test endpoint returns 404
**Cause:** Bucket name is wrong or doesn't exist  
**Fix:** Bucket MUST be named exactly `avatars` (lowercase, plural)

### Issue: Test endpoint returns 403
**Cause:** Storage policies are missing or incorrect  
**Fix:** Run the SQL script in Step 3 Method 1

### Issue: Upload succeeds but image doesn't load
**Cause:** Bucket is not public  
**Fix:** Storage → avatars → Settings → Enable "Public bucket" toggle

### Issue: "bucket_id = 'avatars'" error in SQL
**Cause:** Bucket doesn't exist yet  
**Fix:** Complete Step 2 first, then Step 3

---

## 📊 Current Status

### What's Deployed:
✅ Improved error messages (commit: 231e225)  
✅ Storage test endpoint added  
✅ Better debugging information  

### What's Needed:
⚠️ Create Supabase Storage bucket `avatars`  
⚠️ Set 3 storage policies  

---

## 🚀 Quick Start (TL;DR)

1. **Wait 2-3 minutes** for Render to finish deploying
2. **Test:** https://cylix-parking-slot.onrender.com/api/test_storage
3. **If 404:** Create bucket `avatars` (public) in Supabase
4. **If 403:** Run the SQL script from Step 3
5. **Try upload again:** https://cylix-parking-slot.onrender.com/account

---

## 📞 Need More Help?

Check the detailed guides:
- `SUPABASE_SETUP_QUICK_GUIDE.md` - Step-by-step setup
- `PROFILE_PICTURE_FIX_COMPLETE.md` - Full documentation

---

**Next:** Wait for Render deployment, then test the storage endpoint! 🎯
