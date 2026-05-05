-- Reset all profile pictures to default
-- Run this in Supabase SQL Editor to fix 404 errors

-- Update all admin profile pictures to use default
UPDATE public.admin
SET profile_picture = '/static/images/default-profile.png'
WHERE profile_picture IS NOT NULL 
  AND profile_picture != '/static/images/default-profile.png';

-- Or reset specific admin by ID
-- UPDATE public.admin
-- SET profile_picture = '/static/images/default-profile.png'
-- WHERE admin_id = 1;

-- Verify the update
SELECT admin_id, admin_name, admin_email, profile_picture
FROM public.admin;
