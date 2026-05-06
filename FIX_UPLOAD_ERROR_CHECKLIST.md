# Fix Upload Error - Simple Checklist ✅

## Current Error
```
POST https://cylix-parking-slot.onrender.com/api/upload_profile_picture 500 (Internal Server Error)
```

**Cause:** Supabase Storage bucket not created yet

---

## ✅ Checklist (5 minutes total)

### [ ] Step 1: Wait for Render Deployment (2-3 minutes)
- Render is deploying improved error messages
- Check: https://dashboard.render.com
- Wait for "Live" status

### [ ] Step 2: Test Storage Connection (30 seconds)
Open this URL in browser:
```
https://cylix-parking-slot.onrender.com/api/test_storage
```

**If you see 404 error** → Bucket doesn't exist, continue to Step 3  
**If you see 403 error** → Bucket exists but policies missing, skip to Step 4  
**If you see 200 success** → Storage ready! Skip to Step 5

### [ ] Step 3: Create Storage Bucket (2 minutes)

1. Go to: https://supabase.com/dashboard/project/bhsofudngyukxkkialwi/storage/buckets
2. Click **"New bucket"** button
3. Fill in:
   - Name: `avatars`
   - Public bucket: ✅ **CHECK THIS**
4. Click **"Create bucket"**

### [ ] Step 4: Set Storage Policies (2 minutes)

**Option A: SQL (Fastest)**
1. Go to: https://supabase.com/dashboard/project/bhsofudngyukxkkialwi/sql/new
2. Paste and run:
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

**Option B: UI (Manual)**
- Go to: Storage → avatars → Policies
- Click "New Policy" 3 times
- See `SUPABASE_SETUP_QUICK_GUIDE.md` for details

### [ ] Step 5: Test Upload (30 seconds)

1. Go to: https://cylix-parking-slot.onrender.com/account
2. Click the **"+"** button on avatar
3. Select an image file
4. Upload should succeed! ✅

### [ ] Step 6: Verify Persistence (Optional)

1. Restart Render service
2. Go back to `/account` page
3. Profile picture should still be visible ✅

---

## 🎯 Quick Summary

| Step | Time | Action |
|------|------|--------|
| 1 | 2-3 min | Wait for Render deployment |
| 2 | 30 sec | Test storage endpoint |
| 3 | 2 min | Create bucket `avatars` (public) |
| 4 | 2 min | Set 3 storage policies |
| 5 | 30 sec | Test upload |

**Total:** ~5-7 minutes

---

## 🆘 If Something Goes Wrong

### Upload still fails after setup
- Wait 1 minute and try again (cache)
- Check Render logs for specific error
- Test storage endpoint again

### Test endpoint returns error
- 404 = Bucket name wrong (must be exactly `avatars`)
- 403 = Policies missing (run SQL script)
- 500 = Connection issue (check Supabase status)

### Image uploads but doesn't display
- Bucket not public (edit bucket settings)
- Check browser console for CORS errors

---

## 📖 More Help

- **Detailed guide:** `STORAGE_ERROR_DIAGNOSTIC.md`
- **Setup instructions:** `SUPABASE_SETUP_QUICK_GUIDE.md`
- **Full documentation:** `PROFILE_PICTURE_FIX_COMPLETE.md`

---

**Status:** 🟡 Waiting for Render deployment, then ready to set up Supabase Storage
