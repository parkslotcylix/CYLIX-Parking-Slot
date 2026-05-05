-- Check and fix profile pictures in admin table

-- Step 1: Check current profile pictures
SELECT 
    admin_id, 
    admin_name, 
    admin_email, 
    profile_picture,
    CASE 
        WHEN profile_picture IS NULL THEN 'NULL'
        WHEN profile_picture = '' THEN 'EMPTY'
        WHEN profile_picture = '/static/images/default-profile.png' THEN 'DEFAULT'
        ELSE 'CUSTOM'
    END as picture_status
FROM public.admin
ORDER BY admin_id;

-- Step 2: Update ALL profile pictures to default (including NULL and empty)
UPDATE public.admin
SET profile_picture = '/static/images/default-profile.png'
WHERE profile_picture IS NULL 
   OR profile_picture = '' 
   OR profile_picture NOT LIKE '/static/images/default-profile.png';

-- Step 3: Verify the update
SELECT 
    admin_id, 
    admin_name, 
    admin_email, 
    profile_picture
FROM public.admin
ORDER BY admin_id;

-- Step 4: If you want to reset a specific admin by email
-- UPDATE public.admin
-- SET profile_picture = '/static/images/default-profile.png'
-- WHERE admin_email = 'your-email@example.com';
