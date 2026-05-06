# Bucket 404 Error - Diagnostic & Fix

## Error
```
Storage upload failed: {"statusCode":"404","error":"Bucket not found","message":"Bucket not found"}
```

## Possible Causes

1. **Bucket name mismatch** - Bucket might have different name
2. **Wrong Supabase project** - Bucket created in different project
3. **Bucket not fully created** - Creation didn't complete
4. **API key permissions** - Service role key doesn't have access

---

## 🔍 Step 1: Verify Bucket Exists

### Check in Supabase Dashboard:

1. Go to: https://supabase.com/dashboard/project/bhsofudngyukxkkialwi/storage/buckets

2. **Look for a bucket named `avatars`**

3. **Check the exact name** - must be exactly `avatars` (lowercase, plural)

---

## 🔧 Step 2: Verify Bucket is Public

If bucket exists:

1. Click on the `avatars` bucket
2. Go to **Settings** tab
3. **Public bucket** toggle should be **ON** (green)
4. If OFF, turn it ON and save

---

## 🔧 Step 3: Check Bucket Name in Code

The code expects bucket name: `avatars`

If your bucket has a different name, we need to update the code.

### To check what buckets exist, run this SQL:

```sql
SELECT 
    id,
    name,
    public
FROM storage.buckets
ORDER BY name;
```

This will show all buckets in your project.

---

## 🛠️ Fix Option 1: Recreate Bucket with Correct Name

If bucket doesn't exist or has wrong name:

### Delete old bucket (if exists):
```sql
DELETE FROM storage.buckets WHERE name = 'avatars';
```

### Create new bucket:
```sql
INSERT INTO storage.buckets (id, name, public)
VALUES ('avatars', 'avatars', true);
```

### Then recreate policies:
```sql
-- Policy 1
CREATE POLICY "Public Access"
ON storage.objects FOR SELECT
USING ( bucket_id = 'avatars' );

-- Policy 2
CREATE POLICY "Authenticated users can upload"
ON storage.objects FOR INSERT
WITH CHECK ( bucket_id = 'avatars' AND auth.role() = 'authenticated' );

-- Policy 3
CREATE POLICY "Service role full access"
ON storage.objects FOR ALL
USING ( bucket_id = 'avatars' );
```

---

## 🛠️ Fix Option 2: Use Supabase UI to Create Bucket

1. Go to: https://supabase.com/dashboard/project/bhsofudngyukxkkialwi/storage/buckets

2. Click **"New bucket"**

3. **IMPORTANT:** Fill in exactly:
   - **Name:** `avatars` (lowercase, no spaces)
   - **Public bucket:** ✅ **CHECK THIS BOX**
   - Click **"Create bucket"**

4. Verify bucket appears in list

5. Recreate the 3 policies (see Fix Option 1 above)

---

## 🔍 Step 4: Test Storage Endpoint

After fixing, test the storage connection:

```
https://cylix-parking-slot.onrender.com/api/test_storage
```

**Expected response:**
```json
{
  "success": true,
  "message": "Supabase Storage bucket 'avatars' is accessible",
  "bucket_exists": true
}
```

**If still 404:**
```json
{
  "success": false,
  "message": "Storage bucket 'avatars' not found",
  "bucket_exists": false
}
```

---

## 🔍 Step 5: Verify API Key

Make sure your Supabase API key has storage permissions:

1. Go to: https://supabase.com/dashboard/project/bhsofudngyukxkkialwi/settings/api

2. Copy the **service_role** key (not anon key!)

3. Check your Render environment variables:
   - `SUPABASE_API_KEY` should be the **service_role** key
   - Not the **anon** key

4. If wrong, update in Render:
   - Dashboard → Your Service → Environment
   - Update `SUPABASE_API_KEY`
   - Redeploy

---

## 🐛 Common Issues

### Issue: Bucket exists but still 404
**Cause:** Bucket ID doesn't match bucket name  
**Fix:** Delete and recreate bucket using SQL (Fix Option 1)

### Issue: Policies exist but upload fails
**Cause:** Bucket not public  
**Fix:** Storage → avatars → Settings → Enable "Public bucket"

### Issue: Test endpoint works but upload fails
**Cause:** Different API keys or permissions  
**Fix:** Verify service_role key in Render environment

---

## 📋 Quick Checklist

Run through this checklist:

- [ ] Bucket named exactly `avatars` exists in Supabase
- [ ] Bucket is set to **public** (toggle ON)
- [ ] All 3 policies exist (run verification query)
- [ ] Render has correct `SUPABASE_API_KEY` (service_role key)
- [ ] Test endpoint returns success
- [ ] Try upload again

---

## 🔧 Nuclear Option: Start Fresh

If nothing works, start completely fresh:

### 1. Delete everything:
```sql
-- Delete policies
DROP POLICY IF EXISTS "Public Access" ON storage.objects;
DROP POLICY IF EXISTS "Authenticated users can upload" ON storage.objects;
DROP POLICY IF EXISTS "Service role full access" ON storage.objects;

-- Delete bucket
DELETE FROM storage.buckets WHERE name = 'avatars';
```

### 2. Create bucket via UI:
- Go to Storage → New bucket
- Name: `avatars`
- Public: ✅ YES
- Create

### 3. Create policies:
```sql
CREATE POLICY "Public Access"
ON storage.objects FOR SELECT
USING ( bucket_id = 'avatars' );

CREATE POLICY "Authenticated users can upload"
ON storage.objects FOR INSERT
WITH CHECK ( bucket_id = 'avatars' AND auth.role() = 'authenticated' );

CREATE POLICY "Service role full access"
ON storage.objects FOR ALL
USING ( bucket_id = 'avatars' );
```

### 4. Test again

---

## 📞 Next Steps

1. **Check if bucket exists** (Step 1)
2. **Verify bucket name is exactly `avatars`** (Step 3)
3. **Recreate bucket if needed** (Fix Option 2)
4. **Test storage endpoint** (Step 4)
5. **Try upload again**

---

**Start here:** Check if bucket exists in Supabase Dashboard
