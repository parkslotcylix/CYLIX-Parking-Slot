-- Fix admin table schema
-- This script updates the admin table structure

-- Drop existing table if you want to recreate (WARNING: This deletes all data!)
-- DROP TABLE IF EXISTS public.admin CASCADE;

-- Create admin table with proper structure
CREATE TABLE IF NOT EXISTS public.admin (
    admin_id SERIAL PRIMARY KEY,
    admin_name VARCHAR(100) NOT NULL,
    admin_email VARCHAR(100) NOT NULL UNIQUE,
    profile_picture VARCHAR(500) DEFAULT '/static/images/default-profile.png',
    admin_password VARCHAR(255) NOT NULL,
    access_level VARCHAR(20) DEFAULT 'admin' CHECK (access_level IN ('super_admin', 'admin', 'manager')),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'suspended')),
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on email for faster lookups
CREATE INDEX IF NOT EXISTS idx_admin_email ON public.admin(admin_email);

-- Create index on status for filtering
CREATE INDEX IF NOT EXISTS idx_admin_status ON public.admin(status);

-- Insert default admin user if not exists
INSERT INTO public.admin (admin_name, admin_email, admin_password, access_level, status)
VALUES ('Admin', 'admin@parkslot.com', 'admin123', 'super_admin', 'active')
ON CONFLICT (admin_email) DO NOTHING;

-- Create trigger to auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Drop trigger if exists and recreate
DROP TRIGGER IF EXISTS update_admin_updated_at ON public.admin;
CREATE TRIGGER update_admin_updated_at
    BEFORE UPDATE ON public.admin
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions (adjust as needed)
-- GRANT ALL ON public.admin TO your_user;
-- GRANT USAGE, SELECT ON SEQUENCE admin_admin_id_seq TO your_user;

-- Verify table structure
SELECT 
    column_name, 
    data_type, 
    character_maximum_length,
    column_default,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'public' 
  AND table_name = 'admin'
ORDER BY ordinal_position;
