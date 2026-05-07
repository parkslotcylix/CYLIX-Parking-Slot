# Password Requirements - Visual Guide

## "Add New Admin" Modal - With Password Requirements

```
┌─────────────────────────────────────────────────────────────┐
│ Add New Admin                                            ✕   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ FULL NAME *                                                  │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ John Doe                                                 │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ EMAIL ADDRESS *                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ john@example.com                                         │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ PASSWORD *                                                   │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ SecurePass123!                                      👁️   │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Password Requirements:                                   │ │
│ │ ✅ At least 8 characters                                 │ │
│ │ ✅ At least one uppercase letter (A-Z)                  │ │
│ │ ✅ At least one lowercase letter (a-z)                  │ │
│ │ ✅ At least one number (0-9)                            │ │
│ │ ✅ At least one special character (!@#$%^&*)            │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ ACCESS LEVEL *                                               │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Admin                                                  ▼ │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ STATUS *                                                     │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Active                                                 ▼ │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│                                                              │
│                          [Cancel]  [Save Admin]             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Requirements Box States

**Empty Password** (requirements hidden):
```
PASSWORD *
┌──────────────────────────────────────────────────────────┐
│                                                          │
│ └──────────────────────────────────────────────────────┘
```

**Weak Password** (requirements shown with ❌):
```
PASSWORD *
┌──────────────────────────────────────────────────────────┐
│ Pass                                                 👁️  │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ Password Requirements:                                   │
│ ❌ At least 8 characters                                 │
│ ❌ At least one uppercase letter (A-Z)                  │
│ ❌ At least one lowercase letter (a-z)                  │
│ ❌ At least one number (0-9)                            │
│ ❌ At least one special character (!@#$%^&*)            │
└──────────────────────────────────────────────────────────┘
```

**Partially Met** (some ✅, some ❌):
```
PASSWORD *
┌──────────────────────────────────────────────────────────┐
│ Password123                                          👁️  │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ Password Requirements:                                   │
│ ✅ At least 8 characters                                 │
│ ❌ At least one uppercase letter (A-Z)                  │
│ ✅ At least one lowercase letter (a-z)                  │
│ ✅ At least one number (0-9)                            │
│ ❌ At least one special character (!@#$%^&*)            │
└──────────────────────────────────────────────────────────┘
```

**All Requirements Met** (all ✅):
```
PASSWORD *
┌──────────────────────────────────────────────────────────┐
│ SecurePass123!                                     👁️  │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ Password Requirements:                                   │
│ ✅ At least 8 characters                                 │
│ ✅ At least one uppercase letter (A-Z)                  │
│ ✅ At least one lowercase letter (a-z)                  │
│ ✅ At least one number (0-9)                            │
│ ✅ At least one special character (!@#$%^&*)            │
└──────────────────────────────────────────────────────────┘
```

---

## "Edit Profile" Modal - With Optional Password

```
┌─────────────────────────────────────────────────────────────┐
│ Edit Profile - John Doe                              ✕   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ PROFILE PICTURE                                              │
│ ┌──────────────┐                                             │
│ │              │  [Choose Picture]                          │
│ │   JD         │                                             │
│ │              │                                             │
│ └──────────────┘                                             │
│                                                              │
│ FULL NAME *                                                  │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ John Doe                                                 │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ EMAIL ADDRESS *                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ john@example.com                                         │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ PASSWORD (Optional - leave blank to keep current)            │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │                                                      👁️  │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ (Requirements box appears when user starts typing)           │
│                                                              │
│ ACCESS LEVEL *                                               │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Super Admin                                            ▼ │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ STATUS *                                                     │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Active                                                 ▼ │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│                                                              │
│                       [Cancel]  [Update Profile]            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Edit Profile Password States

**Empty Password** (requirements hidden):
```
PASSWORD (Optional - leave blank to keep current)
┌──────────────────────────────────────────────────────────┐
│                                                      👁️  │
└──────────────────────────────────────────────────────────┘
```

**User Typing New Password** (requirements shown):
```
PASSWORD (Optional - leave blank to keep current)
┌──────────────────────────────────────────────────────────┐
│ NewPass123!                                         👁️  │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ Password Requirements:                                   │
│ ✅ At least 8 characters                                 │
│ ✅ At least one uppercase letter (A-Z)                  │
│ ✅ At least one lowercase letter (a-z)                  │
│ ✅ At least one number (0-9)                            │
│ ✅ At least one special character (!@#$%^&*)            │
└──────────────────────────────────────────────────────────┘
```

---

## Eye Icon Toggle Behavior

### Password Hidden (Default)
```
PASSWORD *
┌──────────────────────────────────────────────────────────┐
│ ••••••••••••••••••                                  👁️  │
└──────────────────────────────────────────────────────────┘
```

### Password Visible (After Clicking Eye)
```
PASSWORD *
┌──────────────────────────────────────────────────────────┐
│ SecurePass123!                                     👁️‍🗨️ │
└──────────────────────────────────────────────────────────┘
```

---

## Color Scheme

### Requirements Box
- **Background**: Light Orange (#fff3e0)
- **Border Left**: Orange (#ff9800) - 4px
- **Text**: Dark Orange (#e65100)
- **Header Font Weight**: 700 (bold)
- **Header Font Size**: 0.8rem
- **Item Font Size**: 0.75rem

### Icons
- **Not Met**: ❌ (red X)
- **Met**: ✅ (green checkmark)
- **Eye Icon**: Gray (#999) - changes to darker on hover

---

## Interaction Flow

### "Add New Admin" Flow
1. User clicks "Add New Admin" button
2. Modal opens with empty password field
3. Requirements box is hidden
4. User starts typing password
5. Requirements box appears
6. Icons update in real-time as user types
7. When all requirements met, user can submit
8. If requirements not met, form submission blocked with error

### "Edit Profile" Flow
1. User clicks "Edit Profile" button
2. Modal opens with profile picture and optional password field
3. Password field is empty, requirements box is hidden
4. User can edit name, email, access level, status
5. If user wants to change password:
   - Clicks in password field
   - Types new password
   - Requirements box appears
   - Icons update in real-time
6. User can submit with or without password change
7. If password entered but requirements not met, form submission blocked

---

## Accessibility Features

- **Clear Labels**: Each requirement is clearly labeled
- **Visual Indicators**: ❌ and ✅ icons are easy to see
- **Color + Icons**: Not relying on color alone
- **Real-time Feedback**: Users know status immediately
- **Optional Field**: Edit profile password is optional
- **Eye Icon**: Clear toggle for password visibility

---

## Browser Compatibility

- Works in all modern browsers (Chrome, Firefox, Safari, Edge)
- Uses standard HTML5 input types
- CSS Grid and Flexbox for layout
- SVG icons for eye toggle
- JavaScript ES6 compatible

---

**Visual Guide Complete** ✅  
**Ready for User Testing** ✅
