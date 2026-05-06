# Supabase Storage Setup - Quick Guide

## 🎯 Goal
Create a storage bucket in Supabase to store profile pictures that persist across Render restarts.

---

## ⏱️ Time Required: 5 minutes

---

## 📋 Step-by-Step Instructions

### STEP 1: Create Storage Bucket (2 minutes)

1. **Open Supabase Dashboard:**
   ```
   https://supabase.com/dashboard/project/bhsofudngyukxkkialwi/storage/buckets
   ```

2. **Click the green "New bucket" button** (top right)

3. **Fill in the form:**
   ```
   Name: avatars
   Public bucket: ✅ CHECK THIS BOX (IMPORTANT!)
   File size limit: 5242880 (5MB - default is fine)
   Allowed MIME types: Leave empty (allows all image types)
   ```

4. **Click "Create bucket"**

5. **Verify:** You should see `avatars` in the bucket list

---

### STEP 2: Set Storage Policies (3 minutes)

1. **Click on the `avatars` bucket** you just created

2. **Go to the "Policies" tab** (top menu)

3. **Click "New Policy"** button

4. **Create Policy 1: Public Read Access**
   - Click **"For full customization"**
   - Policy name: `Public Access`
   - Allowed operation: **SELECT** (check this box)
   - Target roles: **public** (check this box)
   - USING expression:
     ```sql
     bucket_id = 'avatars'
     ```
   - Click **"Review"** → **"Save policy"**

5. **Create Policy 2: Authenticated Upload**
   - Click **"New Policy"** again
   - Click **"For full customization"**
   - Policy name: `Authenticated users can upload`
   - Allowed operation: **INSERT** (check this box)
   - Target roles: **authenticated** (check this box)
   - WITH CHECK expression:
     ```sql
     bucket_id = 'avatars' AND auth.role() = 'authenticated'
     ```
   - Click **"Review"** → **"Save policy"**

6. **Create Policy 3: Service Role Full Access**
   - Click **"New Policy"** again
   - Click **"For full customization"**
   - Policy name: `Service role full access`
   - Allowed operation: **ALL** (check all boxes: SELECT, INSERT, UPDATE, DELETE)
   - Target roles: **service_role** (check this box)
   - USING expression:
     ```sql
     bucket_id = 'avatars'
     ```
   - Click **"Review"** → **"Save policy"**

7. **Verify:** You should see 3 policies listed under the Policies tab

---

## ✅ Verification

### Check Bucket Settings:
1. Go to Storage → avatars → Settings
2. Verify:
   - ✅ **Public bucket:** ON (toggle should be green)
   - ✅ **File size limit:** 5242880 bytes (5MB)

### Check Policies:
1. Go to Storage → avatars → Policies
2. You should see:
   - ✅ `Public Access` (SELECT)
   - ✅ `Authenticated users can upload` (INSERT)
   - ✅ `Service role full access` (ALL)

---

## 🧪 Test the Setup

### Option 1: Test via Supabase UI
1. Go to Storage → avatars
2. Click **"Upload file"**
3. Select any image file
4. Create folder: `profile-pictures`
5. Upload the file
6. Click on the uploaded file
7. Copy the **"Public URL"**
8. Paste URL in browser - image should load ✅

### Option 2: Test via Your App
1. Go to: https://cylix-parking-slot.onrender.com/account
2. Click the **"+"** button on avatar
3. Select an image
4. Upload should succeed
5. Image should display immediately
6. Check browser DevTools → Network → Response should show Supabase URL

---

## 🔧 Alternative: SQL Script Method

If you prefer SQL, run this in **Supabase SQL Editor:**

```sql
-- Create storage bucket (if not exists)
INSERT INTO storage.buckets (id, name, public)
VALUES ('avatars', 'avatars', true)
ON CONFLICT (id) DO NOTHING;

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

---

## ❌ Common Mistakes

### Mistake 1: Forgot to make bucket public
**Symptom:** Images upload but don't load (403 error)  
**Fix:** Storage → avatars → Settings → Enable "Public bucket"

### Mistake 2: Missing policies
**Symptom:** Upload fails with 403 Forbidden  
**Fix:** Add all 3 policies (especially Policy 3 for service role)

### Mistake 3: Wrong bucket name
**Symptom:** Upload fails with 404 Not Found  
**Fix:** Bucket MUST be named exactly `avatars` (lowercase, plural)

### Mistake 4: Policies have wrong bucket_id
**Symptom:** Policies exist but upload still fails  
**Fix:** Check USING/WITH CHECK expressions - must say `bucket_id = 'avatars'`

---

## 📞 Need Help?

### Check Supabase Logs:
1. Go to: https://supabase.com/dashboard/project/bhsofudngyukxkkialwi/logs/explorer
2. Filter by: `storage`
3. Look for error messages

### Check Render Logs:
1. Go to: https://dashboard.render.com
2. Select your service
3. Click **"Logs"** tab
4. Look for "Supabase storage upload failed" messages

---

## 🎉 Success Indicators

When setup is complete, you should see:

✅ Bucket `avatars` exists and is public  
✅ 3 policies are active  
✅ Upload succeeds with 200/201 status  
✅ Image URL format:
```
https://bhsofudngyukxkkialwi.supabase.co/storage/v1/object/public/avatars/profile-pictures/admin_1_1234567890.jpg
```
✅ Image loads in browser  
✅ Image persists after Render restart  

---

**Ready to test?** Go to: https://cylix-parking-slot.onrender.com/account 🚀
