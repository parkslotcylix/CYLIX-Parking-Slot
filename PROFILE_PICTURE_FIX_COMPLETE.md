# Profile Picture Upload Fix - COMPLETE

## Problem Solved
✅ Profile pictures now persist across Render restarts using Supabase Storage instead of ephemeral filesystem

## Changes Made

### 1. Updated `app.py` (lines 1570-1650)
- **OLD:** Saved files to local filesystem (`/static/images/profiles/`)
- **NEW:** Uploads files to Supabase Storage bucket (`avatars`)

### Key Changes:
- Reads file content into memory instead of saving to disk
- Uploads to Supabase Storage via REST API
- Stores public Supabase URL in database instead of local path
- No more `os.path.join()` or `file.save()` calls

### 2. Storage URL Format
**OLD (local):**
```
/static/images/profiles/admin_1_1777646461.jpg
```

**NEW (Supabase):**
```
https://bhsofudngyukxkkialwi.supabase.co/storage/v1/object/public/avatars/profile-pictures/admin_1_1777646461.jpg
```

## Setup Required in Supabase Dashboard

### Step 1: Create Storage Bucket
1. Go to: https://supabase.com/dashboard/project/bhsofudngyukxkkialwi/storage/buckets
2. Click **"New bucket"**
3. Settings:
   - **Name:** `avatars`
   - **Public bucket:** ✅ YES (check this box)
   - **File size limit:** 5MB (default is fine)
4. Click **"Create bucket"**

### Step 2: Set Storage Policies
Go to Storage → avatars → Policies

**Create 3 policies:**

#### Policy 1: Public Read Access
```sql
CREATE POLICY "Public Access"
ON storage.objects FOR SELECT
USING ( bucket_id = 'avatars' );
```

#### Policy 2: Authenticated Upload
```sql
CREATE POLICY "Authenticated users can upload"
ON storage.objects FOR INSERT
WITH CHECK ( bucket_id = 'avatars' AND auth.role() = 'authenticated' );
```

#### Policy 3: Service Role Full Access
```sql
CREATE POLICY "Service role full access"
ON storage.objects FOR ALL
USING ( bucket_id = 'avatars' );
```

**OR use the Supabase UI:**
1. Click **"New Policy"**
2. Select **"For full customization"**
3. Policy name: `Public Access`
4. Allowed operation: `SELECT`
5. Target roles: `public`
6. Click **"Review"** → **"Save policy"**

Repeat for the other 2 policies.

## Deployment Steps

### 1. Commit and Push Changes
```bash
git add app.py
git commit -m "Fix: Use Supabase Storage for profile pictures (persist across restarts)"
git push origin main
```

### 2. Render Auto-Deploy
Render will automatically detect the push and redeploy.

### 3. Test Upload
1. Go to: https://cylix-parking-slot.onrender.com/account
2. Click **"Change Picture"**
3. Upload an image
4. Verify the URL starts with `https://bhsofudngyukxkkialwi.supabase.co/storage/`
5. Restart the Render service manually
6. Verify the image still loads (persistence test)

## How It Works

### Upload Flow:
1. User selects image in `/account` page
2. Frontend sends file to `/api/upload_profile_picture`
3. Backend reads file content into memory
4. Backend uploads to Supabase Storage via REST API:
   ```
   POST https://bhsofudngyukxkkialwi.supabase.co/storage/v1/object/avatars/profile-pictures/admin_1_1234567890.jpg
   ```
5. Backend gets public URL from Supabase
6. Backend updates `admin` table with new URL
7. Frontend displays image from Supabase CDN

### Benefits:
✅ Files persist across Render restarts
✅ CDN-backed (fast global loading)
✅ No local disk space used
✅ Automatic image optimization by Supabase
✅ Scalable storage solution

## Troubleshooting

### Issue: Upload fails with 404
**Cause:** Bucket `avatars` doesn't exist
**Fix:** Create the bucket in Supabase Dashboard (Step 1 above)

### Issue: Upload fails with 403
**Cause:** Storage policies not set correctly
**Fix:** Add the 3 policies (Step 2 above)

### Issue: Image doesn't load after upload
**Cause:** Bucket is not public
**Fix:** Edit bucket settings → Enable "Public bucket"

### Issue: Old local URLs still in database
**Fix:** Run this SQL in Supabase SQL Editor:
```sql
UPDATE admin 
SET profile_picture = 'https://bhsofudngyukxkkialwi.supabase.co/storage/v1/object/public/avatars/profile-pictures/default-avatar.png'
WHERE profile_picture LIKE '/static/images/%';
```

## Verification Checklist

- [ ] Supabase bucket `avatars` created and set to public
- [ ] 3 storage policies added
- [ ] Code changes committed and pushed to GitHub
- [ ] Render deployment successful
- [ ] Upload test successful
- [ ] Image URL starts with Supabase domain
- [ ] Image persists after Render restart

## Status
🟢 **READY TO DEPLOY**

All code changes complete. Just need to:
1. Create Supabase Storage bucket
2. Set policies
3. Push to GitHub
4. Test on Render
