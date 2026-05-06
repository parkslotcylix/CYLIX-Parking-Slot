# Supabase Storage Setup for Profile Pictures

## Problem
Render's free tier has ephemeral filesystem - uploaded files are deleted on restart.

## Solution
Use Supabase Storage to persist profile pictures.

## Setup Steps

### 1. Create Storage Bucket in Supabase

Go to Supabase Dashboard → Storage → Create Bucket:
- **Name:** `avatars`
- **Public:** Yes (check "Public bucket")
- Click **Create bucket**

### 2. Set Bucket Policies

Go to Storage → avatars → Policies → New Policy:

**Policy 1: Allow public read**
```sql
CREATE POLICY "Public Access"
ON storage.objects FOR SELECT
USING ( bucket_id = 'avatars' );
```

**Policy 2: Allow authenticated upload**
```sql
CREATE POLICY "Authenticated users can upload"
ON storage.objects FOR INSERT
WITH CHECK ( bucket_id = 'avatars' AND auth.role() = 'authenticated' );
```

**Policy 3: Allow service role full access**
```sql
CREATE POLICY "Service role full access"
ON storage.objects FOR ALL
USING ( bucket_id = 'avatars' AND auth.role() = 'service_role' );
```

### 3. Update app.py

Replace the `upload_profile_picture` function with Supabase Storage upload.

The new code:
- Reads file content into memory
- Uploads to Supabase Storage via REST API
- Gets public URL from Supabase
- Updates database with new URL

### 4. Test

1. Deploy to Render
2. Go to /account page
3. Upload a profile picture
4. Picture should persist across restarts

## Storage URL Format

```
https://bhsofudngyukxkkialwi.supabase.co/storage/v1/object/public/avatars/profile-pictures/admin_1_1777646461.jpg
```

## Benefits

✅ Files persist across Render restarts
✅ CDN-backed (fast loading)
✅ Automatic image optimization
✅ No local disk space needed
