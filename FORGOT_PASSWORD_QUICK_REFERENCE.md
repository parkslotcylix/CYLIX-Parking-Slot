# Forgot Password - Quick Reference

## How It Works Now

### User Flow
1. User enters email on forgot password page
2. System queries database for that email
3. If found, fetches complete user record
4. Uses SAME record for email recipient and greeting name
5. Sends reset email with correct name

---

## Key Fix

### Before ❌
```python
# Mixed sources
admin_name = result['admin_name']  # From database
send_email(email, ...)             # From user input
```

**Problem:** Email from input, name from database (potential mismatch)

---

### After ✅
```python
# Single source
user = users[0]
admin_email = user['admin_email']  # From database
admin_name = user['admin_name']    # From database
send_email(admin_email, ...)       # From database
```

**Solution:** Everything from the same database record

---

## Data Source

### What We Use
- ✅ `user['admin_email']` - Email from database
- ✅ `user['admin_name']` - Name from database
- ✅ `user['admin_id']` - ID from database

### What We DON'T Use
- ❌ Session data
- ❌ Logged-in user data
- ❌ Cached variables
- ❌ Fallback defaults
- ❌ User input (except for lookup)

---

## Example

### Julie's Email
**Input:** `julie@example.com`

**Database Query:**
```python
response = requests.get(
    f"{SUPABASE_URL}/rest/v1/admin",
    params={'admin_email': 'eq.julie@example.com'}
)
```

**Database Returns:**
```json
{
  "admin_id": 5,
  "admin_email": "julie@example.com",
  "admin_name": "Julie"
}
```

**Email Sent:**
- **To:** `julie@example.com` ✅
- **Greeting:** "Hello **Julie**" ✅

---

## Code Structure

```python
# 1. Fetch user from database
response = requests.get(
    f"{SUPABASE_URL}/rest/v1/admin",
    params={'admin_email': f'eq.{email}'}
)

# 2. Get single user object
user = response.json()[0]

# 3. Extract data from SAME object
admin_id = user['admin_id']
admin_email = user['admin_email']
admin_name = user['admin_name']

# 4. Use in email template
html_content = f"Hello <strong>{admin_name}</strong>"

# 5. Send to database email
send_email(admin_email, subject, html_content)
```

---

## Security

### Email Enumeration Protection
```python
if not users:
    return jsonify({
        'success': True,
        'message': 'If an account exists with this email, a password reset link will be sent'
    })
```

**Purpose:** Don't reveal if email exists

---

### Token Expiration
```python
expiration_time = datetime.now(timezone.utc) + timedelta(minutes=30)
```

**Purpose:** Links expire after 30 minutes

---

## Debugging

### Console Output
```
✅ Reset token stored: abc123... for admin_id: 5, name: Julie
📧 Sending reset email to: julie@example.com for user: Julie
📧 Reset link: http://localhost:5000/reset-password?token=abc123...
```

**Purpose:** Verify correct user matching

---

## Testing

### Test Case 1: Valid Email
```
Input: julie@example.com
Expected: Email sent to julie@example.com with "Hello Julie"
Result: ✅ Pass
```

### Test Case 2: Different User
```
Input: john@example.com
Expected: Email sent to john@example.com with "Hello John Doe"
Result: ✅ Pass
```

### Test Case 3: Invalid Email
```
Input: invalid@example.com
Expected: Generic success message, no email sent
Result: ✅ Pass
```

---

## Status
✅ Fixed - Email and name always match the correct user!
