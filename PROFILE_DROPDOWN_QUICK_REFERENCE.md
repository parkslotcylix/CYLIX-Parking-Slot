# Profile Dropdown - Quick Reference Guide

## 🎯 Quick Overview

The profile dropdown replaces the old "🔒 Logout" link with a modern, feature-rich component showing:
- **Avatar** (profile picture or initials)
- **Admin Name**
- **Role Badge** (Super Admin / Admin / Manager)
- **Status Badge** (Active / Inactive / Suspended)
- **Dropdown Menu** (Account links + Logout)

---

## 📍 Location

**Top-right corner of navbar** on all pages:
- Home (`/home`)
- Parking (`/parking`)
- Analytics (`/analytics`)
- Account (`/account`)
- Admin Management (`/admin-management`)

---

## 🎨 Visual Components

### Profile Trigger (Always Visible)
```
┌─────────────────────────────────┐
│  [Avatar] Admin Name ▼          │
└─────────────────────────────────┘
```

**Desktop**: Avatar + Name + Arrow  
**Tablet**: Avatar + Arrow (name hidden)  
**Mobile**: Avatar only

### Dropdown Menu (Click to Open)
```
┌─────────────────────────────────┐
│  ╔═══════════════════════════╗  │
│  ║  John Doe                 ║  │ ← Gradient Header
│  ║  admin@example.com        ║  │
│  ║  ⭐ Super Admin  🟢 Active ║  │
│  ╚═══════════════════════════╝  │
│  ─────────────────────────────  │
│  👤 My Account                  │
│  ⚙️ Account Settings            │
│  ─────────────────────────────  │
│  🚪 Logout                      │ ← Red color
└─────────────────────────────────┘
```

---

## 🏷️ Role Badges

| Role | Badge | Color | Access |
|------|-------|-------|--------|
| **Super Admin** | ⭐ Super Admin | 🟡 Gold | All pages + Admin Management |
| **Admin** | 🔐 Admin | 🟢 Green | All pages except Admin Management |
| **Manager** | 📋 Manager | 🔵 Blue | All pages except Admin Management |

---

## 🚦 Status Badges

| Status | Badge | Color | Animation | Login |
|--------|-------|-------|-----------|-------|
| **Active** | 🟢 Active | Green | Pulsing dot | ✅ Allowed |
| **Inactive** | ⚪ Inactive | Gray | Static | ❌ Blocked (403) |
| **Suspended** | 🔴 Suspended | Red | Static | ❌ Blocked (403) |

---

## 🔒 Access Control Matrix

| Page | Super Admin | Admin | Manager |
|------|-------------|-------|---------|
| Home | ✅ | ✅ | ✅ |
| Parking | ✅ | ✅ | ✅ |
| Analytics | ✅ | ✅ | ✅ |
| Account | ✅ | ✅ | ✅ |
| **Admin Management** | ✅ | ❌ Redirect | ❌ Redirect |

**Admin Management Link Visibility**:
- Super Admin: ✅ Visible
- Admin: ❌ Hidden
- Manager: ❌ Hidden

---

## 🖱️ User Interactions

### Opening Dropdown
1. Click on profile trigger (avatar/name area)
2. Dropdown menu appears below
3. Smooth fade-in and slide-down animation

### Closing Dropdown
- Click outside the dropdown
- Click on a menu item
- Press ESC key (optional)

### Menu Actions
- **My Account** → Navigate to `/account`
- **Account Settings** → Navigate to `/account`
- **Logout** → Confirm dialog → Clear session → Redirect to `/`

---

## 📱 Responsive Behavior

### Desktop (> 768px)
```
[Avatar] Admin Name ▼
```
- Full display
- Dropdown below trigger
- Hover effects

### Tablet (768px - 480px)
```
[Avatar] ▼
```
- Name hidden
- Avatar and arrow visible
- Dropdown slightly narrower

### Mobile (< 480px)
```
[Avatar]
```
- Only avatar visible
- Dropdown becomes full-width bottom sheet
- Slides up from bottom

---

## 🎭 Avatar Display Logic

### Priority Order:
1. **Profile Picture** (from database)
   - If URL exists and loads successfully
   - Displayed as circular image

2. **Initials Fallback** (auto-generated)
   - If no profile picture or image fails to load
   - First letter of first name + first letter of last name
   - Example: "John Doe" → "JD"
   - Gradient background

3. **Default** (last resort)
   - Single letter "A"
   - Gradient background

---

## 🔐 Session Data

### Stored in sessionStorage:
```javascript
{
  user_email: "admin@example.com",
  user_id: 1,
  user_name: "John Doe",
  access_level: "super_admin",
  status: "active",
  profile_picture: "/static/images/default-profile.png"
}
```

### Checked on Every Page Load:
- If `user_email` missing → Redirect to login
- If `access_level` not super_admin + page is admin-management → Redirect to home

---

## 🚪 Logout Flow

```
1. Click "🚪 Logout"
   ↓
2. Confirm dialog: "Are you sure you want to logout?"
   ↓
3. POST /api/logout (clear server session)
   ↓
4. Clear sessionStorage (clear client data)
   ↓
5. Redirect to / (login page)
```

**Result**: User fully logged out, cannot access protected pages

---

## 🎨 Color Scheme

### Role Badge Colors
- **Super Admin**: `#FFD700` (Gold) on `rgba(255, 215, 0, 0.3)` background
- **Admin**: `#4CAF50` (Green) on `rgba(76, 175, 80, 0.3)` background
- **Manager**: `#2196F3` (Blue) on `rgba(33, 150, 243, 0.3)` background

### Status Badge Colors
- **Active**: `#4CAF50` (Green) with pulsing animation
- **Inactive**: `#9E9E9E` (Gray) static
- **Suspended**: `#F44336` (Red) static

### Dropdown Colors
- **Header**: Purple gradient (`#667eea` to `#764ba2`)
- **Body**: White (`#FFFFFF`)
- **Hover**: Light gray (`#F5F5F5`)
- **Logout Hover**: Light red (`#FFEBEE`)

---

## 🧪 Quick Test Checklist

### Visual Tests
- [ ] Avatar displays correctly
- [ ] Admin name shows next to avatar
- [ ] Role badge has correct icon and color
- [ ] Status badge shows with correct color
- [ ] Dropdown opens on click
- [ ] Dropdown closes when clicking outside

### Functional Tests
- [ ] "My Account" link works
- [ ] "Logout" button works
- [ ] Session cleared after logout
- [ ] Cannot access pages after logout

### Role Tests
- [ ] Super admin sees Admin Management link
- [ ] Admin does NOT see Admin Management link
- [ ] Manager does NOT see Admin Management link
- [ ] Non-super admins redirected from /admin-management

### Responsive Tests
- [ ] Desktop: Full display
- [ ] Tablet: Name hidden
- [ ] Mobile: Only avatar, bottom sheet dropdown

---

## 🐛 Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Avatar not showing | Image URL invalid | Check Supabase Storage URL |
| Initials not showing | Name missing | Check sessionStorage.user_name |
| Role badge wrong color | access_level incorrect | Verify login response |
| Dropdown not opening | JS not loaded | Check profile_dropdown.js |
| Admin Management visible | Role check failed | Clear cache and re-login |
| Logout not working | Backend error | Check /api/logout endpoint |

---

## 📂 File Locations

### Frontend Assets
- **JavaScript**: `static/js/profile_dropdown.js`
- **CSS**: `static/css/profile_dropdown.css`

### Templates (All include dropdown)
- `templates/home.html`
- `templates/parking.html`
- `templates/analytics.html`
- `templates/account.html`
- `templates/admin_management.html`

### Backend
- **Login**: `app.py` → `/api/login` endpoint
- **Session Check**: `app.py` → `/api/check_session` endpoint
- **Logout**: `app.py` → `/api/logout` endpoint

---

## 🔧 Customization

### Change Role Badge Text
Edit `static/js/profile_dropdown.js`:
```javascript
function getRoleBadge(accessLevel) {
  const badges = {
    'super_admin': '<span class="role-badge super-admin">⭐ Super Admin</span>',
    'admin': '<span class="role-badge admin">🔐 Admin</span>',
    'manager': '<span class="role-badge manager">📋 Manager</span>'
  };
  return badges[accessLevel] || badges['admin'];
}
```

### Change Colors
Edit `static/css/profile_dropdown.css`:
```css
.role-badge.super-admin {
  background: rgba(255, 215, 0, 0.3);
  color: #ffd700;
}
```

### Add New Menu Item
Edit each template's dropdown-body section:
```html
<a href="/new-page" class="dropdown-item">
  <span>🆕</span>
  <span>New Feature</span>
</a>
```

---

## 📞 Support

**Documentation**: `PROFILE_DROPDOWN_COMPLETE.md`  
**Deployment**: `PROFILE_DROPDOWN_DEPLOYED.md`  
**This Guide**: `PROFILE_DROPDOWN_QUICK_REFERENCE.md`

---

**Last Updated**: May 5, 2026  
**Version**: 1.0  
**Status**: ✅ Deployed
