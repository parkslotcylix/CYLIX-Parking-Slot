-- ============================================
-- ADMIN MANAGEMENT DATABASE UPDATES
-- ============================================
-- Run this in Supabase SQL Editor
-- ============================================

-- Add tracking fields to admin table
ALTER TABLE admin ADD COLUMN IF NOT EXISTS created_by INTEGER REFERENCES admin(admin_id);
ALTER TABLE admin ADD COLUMN IF NOT EXISTS invite_token VARCHAR(255);
ALTER TABLE admin ADD COLUMN IF NOT EXISTS invite_expires_at TIMESTAMPTZ;

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_admin_created_by ON admin(created_by);
CREATE INDEX IF NOT EXISTS idx_admin_access_level ON admin(access_level);

-- Update existing admin to be created by themselves (bootstrap)
UPDATE admin 
SET created_by = admin_id 
WHERE created_by IS NULL AND access_level = 'super_admin';

-- Verify changes
SELECT 
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'admin'
ORDER BY ordinal_position;

-- Show current admins
SELECT 
    admin_id,
    admin_name,
    admin_email,
    access_level,
    status,
    created_by,
    created_at
FROM admin
ORDER BY admin_id;
