-- ============================================
-- RUN THIS IN SUPABASE SQL EDITOR
-- ============================================
-- This creates the 2 remaining storage policies
-- (Policy 1 already exists, so we skip it)
-- ============================================

-- Policy 2: Authenticated users can upload
CREATE POLICY "Authenticated users can upload"
ON storage.objects FOR INSERT
WITH CHECK ( bucket_id = 'avatars' AND auth.role() = 'authenticated' );

-- Policy 3: Service role full access
CREATE POLICY "Service role full access"
ON storage.objects FOR ALL
USING ( bucket_id = 'avatars' );

-- ============================================
-- VERIFY: Check all policies are created
-- ============================================
SELECT 
    policyname,
    cmd as operation
FROM pg_policies 
WHERE schemaname = 'storage' 
AND tablename = 'objects'
AND bucket_id = 'avatars'
ORDER BY policyname;

-- Should return 3 rows:
-- 1. Authenticated users can upload (INSERT)
-- 2. Public Access (SELECT)
-- 3. Service role full access (ALL)
