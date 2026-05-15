# Email Domain Validation - Visual Guide 🎨

## Email Input Field

### Before (Any Email Allowed):
```
┌─────────────────────────────────────────┐
│ Email Address *                         │
│ ┌─────────────────────────────────────┐ │
│ │ Enter email address                 │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### After (Only @umak.edu.ph):
```
┌─────────────────────────────────────────┐
│ Email Address *                         │
│ ┌─────────────────────────────────────┐ │
│ │ example@umak.edu.ph                 │ │
│ └─────────────────────────────────────┘ │
│ Only @umak.edu.ph emails are accepted  │
└─────────────────────────────────────────┘
```

---

## Validation Flow

### Valid Email Flow:
```
User enters: admin@umak.edu.ph
         ↓
┌────────────────────┐
│ HTML5 Validation   │ ✅ PASS
└────────┬───────────┘
         ↓
┌────────────────────┐
│ JavaScript Check   │ ✅ PASS
└────────┬───────────┘
         ↓
┌────────────────────┐
│ Backend Validation │ ✅ PASS
└────────┬───────────┘
         ↓
┌────────────────────┐
│ Admin Created! 🎉  │
└────────────────────┘
```

### Invalid Email Flow:
```
User enters: admin@gmail.com
         ↓
┌────────────────────┐
│ HTML5 Validation   │ ❌ FAIL
└────────┬───────────┘
         ↓
┌────────────────────────────────────────┐
│ 🔴 Red border on input field           │
│ 💬 Tooltip: "Only University of        │
│    Makati email addresses              │
│    (@umak.edu.ph) are allowed"         │
└────────────────────────────────────────┘
         ↓
    Form blocked
```

---

## Error Messages

### Browser Tooltip (HTML5):
```
┌─────────────────────────────────────────────┐
│ ⚠️  Only University of Makati email        │
│     addresses (@umak.edu.ph) are allowed   │
└─────────────────────────────────────────────┘
```

### Notification Popup (JavaScript):
```
┌─────────────────────────────────────────────┐
│ ❌ Only University of Makati email          │
│    addresses (@umak.edu.ph) are allowed    │
└─────────────────────────────────────────────┘
```

### Backend Error (API Response):
```json
{
  "success": false,
  "error": "Only University of Makati email addresses (@umak.edu.ph) are allowed"
}
```

---

## Add Admin Modal

### Complete Modal View:
```
┌──────────────────────────────────────────────────────┐
│  Add New Admin                                    ✕  │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Full Name *                    Email Address *      │
│  ┌────────────────────┐         ┌─────────────────┐ │
│  │ John Doe           │         │ john@umak.edu.ph│ │
│  └────────────────────┘         └─────────────────┘ │
│                                  Only @umak.edu.ph  │
│                                  emails are accepted│
│                                                      │
│  Password *                                          │
│  ┌──────────────────────────────────────────────┐  │
│  │ ••••••••••••                              👁  │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  Access Level *                 Status *             │
│  ┌────────────────────┐         ┌─────────────────┐ │
│  │ Admin          ▼   │         │ Active      ▼   │ │
│  └────────────────────┘         └─────────────────┘ │
│                                                      │
│                          ┌────────┐  ┌────────────┐ │
│                          │ Cancel │  │ Save Admin │ │
│                          └────────┘  └────────────┘ │
└──────────────────────────────────────────────────────┘
```

---

## Validation States

### State 1: Empty Field
```
┌─────────────────────────────────────┐
│ Email Address *                     │
│ ┌─────────────────────────────────┐ │
│ │ example@umak.edu.ph             │ │ ← Gray placeholder
│ └─────────────────────────────────┘ │
│ Only @umak.edu.ph emails accepted  │ ← Gray helper text
└─────────────────────────────────────┘
```

### State 2: Valid Input
```
┌─────────────────────────────────────┐
│ Email Address *                     │
│ ┌─────────────────────────────────┐ │
│ │ admin@umak.edu.ph               │ │ ← Green border ✅
│ └─────────────────────────────────┘ │
│ Only @umak.edu.ph emails accepted  │
└─────────────────────────────────────┘
```

### State 3: Invalid Input
```
┌─────────────────────────────────────┐
│ Email Address *                     │
│ ┌─────────────────────────────────┐ │
│ │ admin@gmail.com                 │ │ ← Red border ❌
│ └─────────────────────────────────┘ │
│ ⚠️  Only @umak.edu.ph emails allowed│ ← Red error text
└─────────────────────────────────────┘
```

---

## Valid Email Examples

### ✅ Accepted Formats:
```
student@umak.edu.ph
john.doe@umak.edu.ph
admin123@umak.edu.ph
faculty_member@umak.edu.ph
ADMIN@UMAK.EDU.PH
Admin@Umak.Edu.Ph
```

### ❌ Rejected Formats:
```
admin@gmail.com          → Wrong domain
user@yahoo.com           → Wrong domain
sample@umak.com          → Missing .edu.ph
test@umak.edu            → Missing .ph
admin@umakedu.ph         → Missing dots
admin@umak.edu.com       → Wrong TLD
```

---

## User Journey

### Journey 1: Successful Admin Creation

```
Step 1: Click "Add New Admin"
┌────────────────────────────────┐
│ 🟢 Add New Admin               │
└────────────────────────────────┘

Step 2: Fill in details
┌────────────────────────────────┐
│ Name: John Doe                 │
│ Email: john@umak.edu.ph ✅     │
│ Password: SecurePass123!       │
│ Role: Admin                    │
└────────────────────────────────┘

Step 3: Click "Save Admin"
┌────────────────────────────────┐
│ ⏳ Saving...                   │
└────────────────────────────────┘

Step 4: Success!
┌────────────────────────────────┐
│ ✅ Admin created successfully! │
└────────────────────────────────┘
```

### Journey 2: Failed Admin Creation (Invalid Email)

```
Step 1: Click "Add New Admin"
┌────────────────────────────────┐
│ 🟢 Add New Admin               │
└────────────────────────────────┘

Step 2: Fill in details
┌────────────────────────────────┐
│ Name: John Doe                 │
│ Email: john@gmail.com ❌       │
│ Password: SecurePass123!       │
│ Role: Admin                    │
└────────────────────────────────┘

Step 3: Click "Save Admin"
┌────────────────────────────────┐
│ 🔴 Validation Error            │
│ Only @umak.edu.ph emails       │
│ are allowed                    │
└────────────────────────────────┘

Step 4: Fix email
┌────────────────────────────────┐
│ Email: john@umak.edu.ph ✅     │
└────────────────────────────────┘

Step 5: Success!
┌────────────────────────────────┐
│ ✅ Admin created successfully! │
└────────────────────────────────┘
```

---

## Notification Styles

### Success Notification:
```
┌──────────────────────────────────────┐
│ ✅ Admin created successfully!       │
└──────────────────────────────────────┘
  Green background, white text
  Auto-dismiss after 3 seconds
```

### Error Notification:
```
┌──────────────────────────────────────┐
│ ❌ Only University of Makati email   │
│    addresses (@umak.edu.ph) are      │
│    allowed                           │
└──────────────────────────────────────┘
  Red background, white text
  Auto-dismiss after 6 seconds
```

---

## Mobile View

### Mobile Modal (< 768px):
```
┌─────────────────────────┐
│ Add New Admin        ✕  │
├─────────────────────────┤
│                         │
│ Full Name *             │
│ ┌─────────────────────┐ │
│ │ John Doe            │ │
│ └─────────────────────┘ │
│                         │
│ Email Address *         │
│ ┌─────────────────────┐ │
│ │ john@umak.edu.ph    │ │
│ └─────────────────────┘ │
│ Only @umak.edu.ph      │
│ emails accepted        │
│                         │
│ Password *              │
│ ┌─────────────────────┐ │
│ │ ••••••••••••     👁 │ │
│ └─────────────────────┘ │
│                         │
│ Access Level *          │
│ ┌─────────────────────┐ │
│ │ Admin           ▼   │ │
│ └─────────────────────┘ │
│                         │
│ Status *                │
│ ┌─────────────────────┐ │
│ │ Active          ▼   │ │
│ └─────────────────────┘ │
│                         │
│ ┌─────────┐ ┌─────────┐│
│ │ Cancel  │ │  Save   ││
│ └─────────┘ └─────────┘│
└─────────────────────────┘
```

---

## Color Scheme

### Input States:
```
Default:    Border: #c8e6c9 (Light green)
Focus:      Border: #2d6a4f (Medium green)
Valid:      Border: #4caf50 (Green) ✅
Invalid:    Border: #e05252 (Red) ❌
```

### Text Colors:
```
Label:      #5a7a6a (Muted green)
Input:      #1a3a2a (Dark green)
Helper:     #666666 (Gray)
Error:      #e05252 (Red)
```

### Notification Colors:
```
Success BG: #e8f5e9 (Light green)
Success Text: #2e7d32 (Dark green)
Error BG:   #fce4ec (Light red)
Error Text: #c62828 (Dark red)
```

---

## Accessibility

### Screen Reader Announcements:
```
"Email Address, required field"
"Only University of Makati email addresses at umak dot edu dot ph are allowed"
"Invalid email format. Only University of Makati email addresses are allowed"
```

### Keyboard Navigation:
```
Tab       → Move to email field
Type      → Enter email
Tab       → Move to next field
Shift+Tab → Move back to email field
```

### ARIA Labels:
```html
<input 
  type="email"
  aria-label="Email Address"
  aria-required="true"
  aria-invalid="false"
  aria-describedby="email-helper-text"
/>
<small id="email-helper-text">
  Only @umak.edu.ph emails are accepted
</small>
```

---

## Browser Compatibility

### Tested Browsers:
```
✅ Chrome 120+    → Full support
✅ Firefox 120+   → Full support
✅ Safari 17+     → Full support
✅ Edge 120+      → Full support
✅ Mobile Safari  → Full support
✅ Chrome Mobile  → Full support
```

### Pattern Support:
```
✅ HTML5 pattern attribute supported
✅ JavaScript validation as fallback
✅ Backend validation always enforced
```

---

**Visual guide complete!** 🎨✅
