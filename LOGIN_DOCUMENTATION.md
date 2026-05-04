# Login System Documentation - Smart Parking Slot

## 🔐 Login Overview

A secure authentication system has been implemented for the Smart Parking Slot system. All users must login before accessing the dashboard.

## 📋 Login Flow

```
index.html (root)
    ↓
    Checks sessionStorage for user_email
    ↓
    YES → templates/home.html (Dashboard)
    NO  → templates/login.html (Login Page)
```

## 🚀 Getting Started

### Access the System
1. Start PHP server: `php -S localhost:8000`
2. Visit: `http://localhost:8000/` or `http://localhost:8000/index.html`
3. You'll be redirected to login page

### Default Test Credentials

```
Email:    admin@smartparking.com
Password: admin123
```

## 📝 Login Page Features

### Design Elements (From Picture)
- ✅ **Left Section**: Clean login form with email/password fields
- ✅ **Center Section**: Animated car illustration
- ✅ **Right Section**: "Smart Parking Made Simple" headline with description
- ✅ **Top Left**: PARKSLOT logo and branding

### Form Features
- Email validation
- Password requirement
- "Forgot Password?" link (placeholder)
- Error/Success messages
- Loading state during login
- Responsive design

## 🔄 Authentication System

### Login Process
1. User enters email and password
2. Validates against default admin credentials
3. On success:
   - Stores in `sessionStorage`:
     - `user_email`: User's email
     - `user_id`: User ID (1 for admin)
     - `access_level`: User's access level
   - Redirects to dashboard (home.html)
4. On failure:
   - Displays error message
   - Clears password field
   - Shows hint for test credentials

### Session Management
- **Storage**: Browser's `sessionStorage` (cleared when tab closes)
- **Duration**: Session-based (not persistent after browser restart)
- **Security**: For development only

## 🚪 Protected Pages

All template pages now require authentication:
- ✅ `templates/home.html`
- ✅ `templates/parking.html`
- ✅ `templates/analytics.html`
- ✅ `templates/account.html`

### Accessing Protected Pages
- Unauthorized users are automatically redirected to login

## 🔑 Logout Feature

### Logout Button
- Located in navbar on all pages
- Styled with 🔒 emoji
- Separated with visual divider

### Logout Process
1. Click "🔒 Logout" in navbar
2. Confirmation dialog appears
3. On confirm:
   - Clears all session data
   - Redirects to login page

## 💾 Session Storage Details

### Stored Information
```javascript
sessionStorage.setItem('user_email', 'admin@smartparking.com');
sessionStorage.setItem('user_id', '1');
sessionStorage.setItem('access_level', 'super_admin');
```

### Checking Authentication
```javascript
const userEmail = sessionStorage.getItem('user_email');
if (!userEmail) {
  // User not logged in - redirect to login
  window.location.href = 'login.html';
}
```

## 🎨 Login Page UI Components

### Left Section - Login Form
- Logo: 🅿 PARKSLOT
- Heading: "LOGIN"
- Subheading: "Welcome to ParkSlot"
- Email input field
- Password input field
- "Forgot Password?" link
- LOGIN button (brown gradient)
- Error/Success messages

### Center Section - Car Image
- SVG car illustration (gradient brown/orange)
- Floating animation
- Drop shadow effect

### Right Section - Information
- Main heading: "SMART PARKING MADE SIMPLE"
- Description text about IoT and parking benefits
- White text on semi-transparent background

## 🎯 Navigation Bar Updates

All pages now have consistent navbar with:
- Navigation links (Home, Analytics, Parking, Account)
- Active page indicator
- Logout button (right side, pink color)
- Visual separator between nav items and logout

## 📱 Responsive Design

### Breakpoints
- **Desktop** (>1200px): 3-column layout
- **Tablet** (768-1200px): Stacked layout
- **Mobile** (<768px): Full-width form

### Mobile Features
- Adjusted font sizes
- Resized car image
- Responsive form fields
- Touch-friendly buttons

## 🔐 Security Notes

### Current Implementation (Development)
- ⚠️ Hardcoded credentials (admin123)
- ⚠️ No password hashing
- ⚠️ Client-side validation only
- ⚠️ Session storage (not secure)

### Production Recommendations
1. **Backend Authentication**
   - Implement secure API endpoint
   - Use password hashing (bcrypt, argon2)
   - Validate credentials server-side
   - Return authentication tokens

2. **Secure Session Management**
   - Use JWT tokens
   - HTTP-only cookies
   - Proper token expiration
   - CSRF protection

3. **HTTPS**
   - Always use HTTPS
   - Secure cookies

4. **API Protection**
   - Token verification on all endpoints
   - Rate limiting
   - Input validation

## 🧪 Testing

### Test Scenarios

**Successful Login**
- Email: `admin@smartparking.com`
- Password: `admin123`
- Expected: Redirects to home.html

**Invalid Email**
- Email: `wrong@email.com`
- Password: `admin123`
- Expected: Error message

**Invalid Password**
- Email: `admin@smartparking.com`
- Password: `wrongpassword`
- Expected: Error message

**Empty Fields**
- Leave email or password empty
- Click Login
- Expected: HTML5 validation error

**Logout**
- Click 🔒 Logout button
- Confirm logout
- Expected: Redirects to login

**Direct URL Access**
- Not logged in
- Visit: `/templates/home.html`
- Expected: Redirects to login

## 📁 File Structure

```
ParkSlot/
├── index.html                 # Entry point (redirects)
├── templates/
│   ├── login.html            # Login page
│   ├── home.html             # Dashboard (protected)
│   ├── parking.html          # Parking page (protected)
│   ├── analytics.html        # Analytics page (protected)
│   └── account.html          # Account page (protected)
├── api/
│   └── parking.php           # API endpoints
├── config/
│   └── db.php                # Database config
└── static/
    └── images/
        ├── green.png
        ├── orange.png
        └── red.png
```

## 🔗 Quick Links

- Login: `http://localhost:8000/templates/login.html`
- Dashboard: `http://localhost:8000/templates/home.html`
- Parking: `http://localhost:8000/templates/parking.html`
- Analytics: `http://localhost:8000/templates/analytics.html`
- Account: `http://localhost:8000/templates/account.html`

## 🎓 Example Code

### Check if User is Logged In
```javascript
function checkAuthentication() {
  const userEmail = sessionStorage.getItem('user_email');
  if (!userEmail) {
    window.location.href = 'login.html';
  }
}

// Call on page load
document.addEventListener('DOMContentLoaded', checkAuthentication);
```

### Get User Information
```javascript
const userEmail = sessionStorage.getItem('user_email');
const userId = sessionStorage.getItem('user_id');
const accessLevel = sessionStorage.getItem('access_level');

console.log(`Logged in as: ${userEmail}`);
console.log(`Access Level: ${accessLevel}`);
```

### Logout Function
```javascript
function handleLogout(event) {
  event.preventDefault();
  if (confirm('Are you sure?')) {
    // Clear session
    sessionStorage.removeItem('user_email');
    sessionStorage.removeItem('user_id');
    sessionStorage.removeItem('access_level');
    
    // Redirect to login
    window.location.href = 'login.html';
  }
}
```

## 🐛 Troubleshooting

### "Not Logged In" Redirect Loop
- **Problem**: Always redirects to login even after entering credentials
- **Solution**: Check browser's SessionStorage (DevTools → Application → Session Storage)
- **Verify**: `sessionStorage.getItem('user_email')` should have value

### Logout Not Working
- **Problem**: Clicking logout doesn't work
- **Solution**: Ensure JavaScript is enabled
- **Verify**: Check console for errors (F12 → Console tab)

### Login Button Disabled
- **Problem**: Login button stays disabled after attempt
- **Solution**: Wait for page to finish loading or refresh
- **Verify**: Check network tab for API delays

### Session Lost on Page Refresh
- **Problem**: Session clears when page is refreshed
- **Solution**: This is normal for sessionStorage; consider using localStorage or HTTP cookies for persistence

## 📞 Support

For issues or feature requests related to login:
1. Check this documentation first
2. Review browser console for errors (F12)
3. Verify sessionStorage is enabled
4. Test with default credentials
5. Check PHP/API logs if login fails

---

**Status**: ✅ Login system fully implemented and integrated
**Last Updated**: April 17, 2026
