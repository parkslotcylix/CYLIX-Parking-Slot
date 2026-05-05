-- Supabase Admin Table Setup
-- Run this in Supabase SQL Editor

-- Create admin table
CREATE TABLE IF NOT EXISTS public.admin (
    admin_id SERIAL PRIMARY KEY,
    admin_name VARCHAR(100) NOT NULL,
    admin_email VARCHAR(100) NOT NULL UNIQUE,
    profile_picture VARCHAR(500) DEFAULT '/static/images/default-profile.png',
    admin_password VARCHAR(255) NOT NULL,
    access_level VARCHAR(20) DEFAULT 'admin',
    status VARCHAR(20) DEFAULT 'active',
    last_login TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT admin_access_level_check CHECK (access_level IN ('super_admin', 'admin', 'manager')),
    CONSTRAINT admin_status_check CHECK (status IN ('active', 'inactive', 'suspended'))
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_admin_email ON public.admin(admin_email);
CREATE INDEX IF NOT EXISTS idx_admin_status ON public.admin(status);

-- Enable Row Level Security (RLS)
ALTER TABLE public.admin ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
CREATE POLICY "Allow authenticated users to read admin"
    ON public.admin FOR SELECT
    USING (auth.role() = 'authenticated');

CREATE POLICY "Allow service role full access to admin"
    ON public.admin FOR ALL
    USING (auth.role() = 'service_role');

-- Insert default admin (change password after first login!)
INSERT INTO public.admin (admin_name, admin_email, admin_password, access_level, status)
VALUES 
    ('Super Admin', 'admin@parkslot.com', 'admin123', 'super_admin', 'active'),
    ('Manager', 'manager@parkslot.com', 'manager123', 'manager', 'active')
ON CONFLICT (admin_email) DO NOTHING;

-- Create function to update updated_at
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger
DROP TRIGGER IF EXISTS set_updated_at ON public.admin;
CREATE TRIGGER set_updated_at
    BEFORE UPDATE ON public.admin
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_updated_at();

-- Verify setup
SELECT 
    admin_id,
    admin_name,
    admin_email,
    access_level,
    status,
    created_at
FROM public.admin
ORDER BY admin_id;
