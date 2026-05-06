-- Safe storage policy creation - handles existing policies
-- This script will only create policies that don't already exist

-- Drop existing policies if you want to recreate them (optional)
-- Uncomment these lines if you need to start fresh:
-- DROP POLICY IF EXISTS "Public Access" ON storage.objects;
-- DROP POLICY IF EXISTS "Authenticated users can upload" ON storage.objects;
-- DROP POLICY IF EXISTS "Service role full access" ON storage.objects;

-- Policy 1: Public read access
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'storage' 
        AND tablename = 'objects' 
        AND policyname = 'Public Access'
    ) THEN
        CREATE POLICY "Public Access"
        ON storage.objects FOR SELECT
        USING ( bucket_id = 'avatars' );
        RAISE NOTICE 'Created policy: Public Access';
    ELSE
        RAISE NOTICE 'Policy already exists: Public Access';
    END IF;
END $$;

-- Policy 2: Authenticated upload
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'storage' 
        AND tablename = 'objects' 
        AND policyname = 'Authenticated users can upload'
    ) THEN
        CREATE POLICY "Authenticated users can upload"
        ON storage.objects FOR INSERT
        WITH CHECK ( bucket_id = 'avatars' AND auth.role() = 'authenticated' );
        RAISE NOTICE 'Created policy: Authenticated users can upload';
    ELSE
        RAISE NOTICE 'Policy already exists: Authenticated users can upload';
    END IF;
END $$;

-- Policy 3: Service role full access
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'storage' 
        AND tablename = 'objects' 
        AND policyname = 'Service role full access'
    ) THEN
        CREATE POLICY "Service role full access"
        ON storage.objects FOR ALL
        USING ( bucket_id = 'avatars' );
        RAISE NOTICE 'Created policy: Service role full access';
    ELSE
        RAISE NOTICE 'Policy already exists: Service role full access';
    END IF;
END $$;

-- Verify all policies are created
SELECT 
    schemaname,
    tablename,
    policyname,
    cmd as operation,
    roles
FROM pg_policies 
WHERE schemaname = 'storage' 
AND tablename = 'objects'
AND policyname IN ('Public Access', 'Authenticated users can upload', 'Service role full access')
ORDER BY policyname;
