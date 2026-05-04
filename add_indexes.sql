-- ============================================
-- Parking Slot System - Performance Indexes
-- ============================================
-- Run this in your Supabase SQL editor to add
-- missing indexes for optimal performance

-- Index on parking_slots.updated_at for recent changes
CREATE INDEX IF NOT EXISTS idx_parking_slots_updated_at 
  ON public.parking_slots USING btree (updated_at DESC);

-- Index on parking_history.status for filtering
CREATE INDEX IF NOT EXISTS idx_parking_history_status 
  ON public.parking_history USING btree (status);

-- Index on parking_history.created_at for time-based queries
CREATE INDEX IF NOT EXISTS idx_parking_history_created_at 
  ON public.parking_history USING btree (created_at DESC);

-- Index on admin_logs.created_at for audit trails
CREATE INDEX IF NOT EXISTS idx_admin_logs_created_at 
  ON public.admin_logs USING btree (created_at DESC);

-- Composite index for common queries (slot + status)
CREATE INDEX IF NOT EXISTS idx_parking_history_slot_status 
  ON public.parking_history USING btree (slot_id, status);

-- Index on parking_slots.slot_status for occupancy queries
CREATE INDEX IF NOT EXISTS idx_parking_slots_status_updated 
  ON public.parking_slots USING btree (slot_status, updated_at DESC);

-- Index on parking_history.vehicle_reg_number for vehicle tracking
CREATE INDEX IF NOT EXISTS idx_parking_history_vehicle_checkin 
  ON public.parking_history USING btree (vehicle_reg_number, check_in_time DESC);

-- Verify indexes were created
SELECT 
    schemaname,
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public' 
  AND (tablename IN ('parking_slots', 'parking_history', 'admin_logs'))
ORDER BY tablename, indexname;
