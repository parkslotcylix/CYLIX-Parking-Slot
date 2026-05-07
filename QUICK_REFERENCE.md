# ParkSlot - Quick Reference Guide

## 🎯 What's Been Implemented

### ✅ All Features Complete and Working

---

## 🔐 Password Requirements

When creating or editing admin accounts, passwords must meet these requirements:

- **Minimum 8 characters**
- **At least one uppercase letter** (A-Z)
- **At least one lowercase letter** (a-z)
- **At least one number** (0-9)
- **At least one special character** (!@#$%^&*)

**Example of valid password**: `SecurePass123!`

---

## 👥 Admin Management Features

### Create New Admin
1. Click "Add New Admin" button
2. Fill in name, email, password
3. Select access level (Super Admin, Admin, Manager)
4. Select status (Active, Inactive, Suspended)
5. Password field has eye icon to show/hide
6. Click "Save Admin"

### Edit Admin Profile
1. Click "Edit Profile" button on admin row
2. Update name, email, access level, status
3. Optionally upload new profile picture
4. Optionally change password (optional field)
5. Click "Update Profile"

### Deactivate/Activate Admin
1. Click "Deactivate" or "Activate" button
2. Confirm action
3. Admin status updates immediately

### Delete Admin
1. Click "Delete" button
2. Confirm deletion
3. Admin is permanently removed

---

## 📊 Analytics Features

### View Analytics
1. Go to Analytics page
2. Select time period:
   - Today
   - Yesterday
   - This Week (Last 7 Days)
   - 1 Month (Last 30 Days)

### Metrics Displayed
- **Total Sessions Completed**: Number of completed parking sessions
- **Average Parking Duration**: Average time vehicles stayed
- **Available Parking Slots**: Current available/total slots
- **Active Sessions**: Currently occupied slots

### Charts
- **Occupancy Rate (24h)**: Line chart showing hourly occupancy
- **Peak Hours**: Top 3 busiest hours with percentage bars

### Print Report
1. Click "📄 Print Report" button
2. New window opens with formatted report
3. Report includes:
   - Header with period
   - Generated timestamp
   - All metrics
   - Summary section
   - Professional footer
4. Click "🖨️ Print This Report" to print
5. Click "✕ Close" to close window

---

## 🚪 Logout & Session Management

### Logout
1. Click profile dropdown (top right)
2. Click "Logout"
3. Session is cleared
4. Logout action is logged to database
5. Redirected to login page

### Session Validation
- Session is checked on every page load
- Inactive accounts are automatically logged out
- Session expires when browser closes

---

## 🎨 UI Features

### Navbar
- Logo on left
- Navigation links on right (Home, Report, Parking, Admin Management)
- Profile dropdown with user name
- Role-based visibility:
  - Super Admin: sees all modules
  - Admin/Manager: cannot see Admin Management

### Profile Pictures
- Shows user initials in colored circle when no picture
- Gradient background for visual appeal
- Upload new picture in profile edit modal
- Supports: PNG, JPG, JPEG, GIF, WebP
- Max size: 5MB

### Buttons
- "Save Information" and "Logout" buttons aligned on bottom right
- Responsive sizing for different screen sizes
- Smooth hover effects

---

## 🔒 Security Features

### Access Control
- Super Admin: Full access to all features
- Admin: Can manage parking, view analytics
- Manager: Can view parking, view analytics
- Only Super Admin can access Admin Management

### Password Security
- Strong password requirements enforced
- Passwords validated on both frontend and backend
- Show/hide eye icon for password visibility
- No password hashing in current version (add for production)

### Session Security
- Flask session management
- Automatic logout on inactive accounts
- Session cleared on logout
- Client-side storage cleared

### Audit Logging
- All logout actions logged to database
- Admin actions tracked in admin_logs table
- Terminal logging for debugging

---

## 📱 Responsive Design

### Desktop (1200px+)
- Full layout with all features visible
- Comfortable spacing and padding
- Large buttons and inputs

### Tablet (768px - 1199px)
- Adjusted spacing
- Responsive button sizes
- Optimized for touch

### Mobile (< 768px)
- Stacked layout
- Smaller buttons
- Touch-friendly inputs
- Optimized for small screens

---

## 🐛 Troubleshooting

### Password Validation Fails
- Check all requirements are met
- Ensure at least 8 characters
- Include uppercase, lowercase, number, special character
- Example: `MyPass123!`

### Profile Picture Not Showing
- Check file format (PNG, JPG, JPEG, GIF, WebP)
- Check file size (max 5MB)
- Ensure file is valid image
- Fallback shows initials

### Analytics Not Loading
- Check internet connection
- Verify parking_history table exists
- Check date filter selection
- Try refreshing page

### Logout Not Working
- Check browser console for errors
- Verify session is active
- Try clearing browser cache
- Check network tab for API calls

---

## 📋 Database Tables

### parking_history
Stores all parking session records:
- history_id (unique identifier)
- slot_id (which parking slot)
- vehicle_reg_number (license plate)
- check_in_time (when vehicle entered)
- check_out_time (when vehicle left)
- duration_hours (how long parked)
- parking_fee (cost of parking)
- status (active/completed/cancelled)
- notes (additional information)

### admin
Stores admin user accounts:
- admin_id (unique identifier)
- admin_name (full name)
- admin_email (email address)
- admin_password (password)
- access_level (super_admin/admin/manager)
- status (active/inactive/suspended)
- profile_picture (path to image)
- last_login (when last logged in)

---

## 🚀 Getting Started

1. **Login**: Use admin credentials
2. **View Dashboard**: See parking overview
3. **Manage Admins**: Create/edit/delete admin accounts (Super Admin only)
4. **View Analytics**: Check parking statistics
5. **Print Reports**: Generate professional reports
6. **Logout**: Safely exit the system

---

## 📞 Support

For issues or questions:
1. Check browser console for errors
2. Review network tab for API calls
3. Check server logs for backend errors
4. Verify database connection
5. Ensure all tables exist

---

**Last Updated**: May 7, 2026  
**Version**: 1.0.0  
**Status**: Production Ready ✅
