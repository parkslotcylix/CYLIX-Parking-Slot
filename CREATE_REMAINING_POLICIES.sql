-- Create remaining storage policies for avatars bucket
-- Run these one at a time if you get "already exists" errors

-- Policy 2: Authenticated users can upload
CREATE POLICY "Authenticated users can upload"
ON storage.objects FOR INSERT
WITH CHECK ( bucket_id = 'avatars' AND auth.role() = 'authenticated' );

-- Policy 3: Service role full access
CREATE POLICY "Service role full access"
ON storage.objects FOR ALL
USING ( bucket_id = 'avatars' );
