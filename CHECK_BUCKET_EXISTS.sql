-- ============================================
-- CHECK IF BUCKET EXISTS
-- ============================================
-- Run this to see all storage buckets in your project
-- ============================================

SELECT 
    id,
    name,
    public,
    created_at
FROM storage.buckets
ORDER BY name;

-- ============================================
-- Expected result: Should see 'avatars' bucket
-- ============================================
-- If you see 'avatars' with public = true, bucket exists correctly
-- If you don't see 'avatars', bucket doesn't exist - create it
-- If you see different name, we need to update the code or recreate bucket
-- ============================================
