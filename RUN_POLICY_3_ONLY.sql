-- ============================================
-- CREATE POLICY 3 ONLY
-- ============================================
-- Policies 1 and 2 already exist, so just create Policy 3
-- ============================================

-- Policy 3: Service role full access
CREATE POLICY "Service role full access"
ON storage.objects FOR ALL
USING ( bucket_id = 'avatars' );

-- ============================================
-- VERIFY: All 3 policies should now exist
-- ============================================
SELECT 
    policyname,
    cmd as operation
FROM pg_policies 
WHERE schemaname = 'storage' 
AND tablename = 'objects'
AND policyname IN ('Public Access', 'Authenticated users can upload', 'Service role full access')
ORDER BY policyname;

-- Should return 3 rows
