# 2FA Login Flow Diagram

## Complete Authentication Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Admin Login Process                             │
└─────────────────────────────────────────────────────────────────────────┘

                              START
                                │
                                ▼
                    ┌─────────────────────┐
                    │  Enter Email &      │
                    │  Password Form      │
                    └─────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │ Credentials Valid?  │
                    └────┬───────────┬────┘
                         │           │
                      NO │           │ YES
                         ▼           ▼
                    ERROR MSG   ┌──────────────┐
                    SHOWN       │ Check Access │
                    FORM RESET  │ Level        │
                                └──┬───────┬───┘
                                   │       │
                        ADMIN/SUPER│       │OTHER
                           ADMIN   │       │
                                   ▼       ▼
                         ┌──────────────────┐
                         │ Generate 6-Digit │
                         │ Verification Code│
                         └────┬─────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │ Send Code via Email │
                    │ (SMTP/SendGrid)     │
                    └────┬────────────────┘
                         │
                    SUCCESS?
                    ┌──┴──┐
                 YES│     │NO
                    ▼     ▼
              SHOW   ERROR
              VERIFY  MSG
              FORM    SHOWN
                │
                ▼
    ┌───────────────────────────────┐
    │  Enter 6-Digit Code Form      │
    │  • 6 input fields (auto-tab)  │
    │  • Timer (5 minutes)          │
    │  • Resend button              │
    └───────────────────────────────┘
                │
                ▼
    ┌───────────────────────────────┐
    │ Code Format Valid?            │
    │ (6 digits only)               │
    └─────┬──────────────┬──────────┘
          │              │
       YES│              │NO
          ▼              ▼
    SUBMIT TO   ERROR MSG
    BACKEND     SHOWN
          │
          ▼
    ┌─────────────────────────────┐
    │ /api/verify-code endpoint   │
    │ • Verify code matches       │
    │ • Check expiration          │
    │ • Check failed attempts     │
    └─────┬──────────────┬────────┘
          │              │
        YES│             │NO
          ▼              ▼
    ┌──────────────┐   ┌──────────┐
    │ Code Valid   │   │ Increment│
    │ Create       │   │ Failed   │
    │ Session      │   │ Attempts │
    │ Set Cookies  │   └──────────┘
    └─────┬────────┘        │
          │                 ▼
          │         ┌──────────────────┐
          │         │ Attempts >= 5?   │
          │         └──┬──┬────────────┘
          │            │  │
          │         YES│  │NO
          │            ▼  ▼
          │         DISABLE  ERROR MSG
          │         INPUTS   SHOWN
          │                  │
          │                  ▼
          │         RESEND OR
          │         BACK
          │
          ▼
    ┌─────────────────────────┐
    │ Redirect to Dashboard   │
    │ /home                   │
    └─────────────────────────┘
                │
                ▼
            SUCCESS!
```

## State Transitions

```
┌──────────────┐
│ LOGIN_FORM   │◄─────┐
│              │      │
└──────┬───────┘      │
       │              │
       │ Valid Creds  │ Back to Login
       │ + 2FA Needed │ or Error
       ▼              │
┌──────────────┐      │
│ VERIFICATION │      │
│ FORM         │      │
└──────┬───────┘      │
       │              │
       │ Valid Code   │
       │              │
       ▼              │
┌──────────────┐      │
│ DASHBOARD    │      │
└──────────────┘      │
       │              │
       │ Logout or    │
       │ Session      │
       │ Expiry       │
       └──────────────┘
```

## Security Checkpoint Diagram

```
AUTHENTICATION FLOW WITH SECURITY CHECKS

┌─────────────────────────────────────────────┐
│ 1. PASSWORD VALIDATION                      │
│    ✓ Check password against database        │
│    ✓ Verify account status (active)         │
│    ✓ Check access level (admin/super admin) │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│ 2. CODE GENERATION & DELIVERY               │
│    ✓ Generate random 6-digit code           │
│    ✓ Set expiration (5 minutes)             │
│    ✓ Store in memory with timestamp         │
│    ✓ Send via encrypted SMTP/SendGrid       │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│ 3. CODE VERIFICATION (Backend)              │
│    ✓ Check code hasn't expired              │
│    ✓ Verify code matches stored code        │
│    ✓ Track failed attempts                  │
│    ✓ Enforce max 5 failed attempts          │
│    ✓ Delete code after verification         │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│ 4. SESSION CREATION                         │
│    ✓ Create secure session                  │
│    ✓ Store user data in session             │
│    ✓ Set session cookies                    │
│    ✓ Log login event                        │
└──────────────┬──────────────────────────────┘
               │
               ▼
         ✓ ACCESS GRANTED
```

## Code Lifecycle

```
CODE GENERATION
       │
       ▼
GENERATED (00:00)
       │
       ├─► SENT VIA EMAIL
       │
       ▼
VALID (00:00 - 04:59)
       │
       ├─► CORRECT CODE ENTERED ──► DELETED ──► VERIFIED
       │
       └─► INCORRECT CODE ENTERED ──► INCREMENT ATTEMPTS
           ├─► Attempts < 5? ──► REMAIN VALID
           └─► Attempts = 5? ──► DELETED ──► EXPIRED (lockout)
       │
       ▼
EXPIRED (05:00+)
       │
       └─► MUST RESEND CODE
           │
           ▼
       NEW CODE GENERATED
```

## Token Format

```
VERIFICATION CODE STRUCTURE

┌─────────────────┐
│   6 Digits      │
│   Random        │
│   Numeric       │
│   Format: XXXXXX│
│   Example: 382951│
└─────────────────┘

STORAGE FORMAT (Server-side)

{
  email: {
    code: "382951",
    expires_at: 1747298134 (Unix timestamp),
    failed_attempts: 0
  }
}
```

## Error Handling Flow

```
VERIFICATION ERRORS

Code Validation
├─ Invalid Format (not 6 digits)
│  └─ Show: "Please enter all 6 digits"
│
├─ Code Mismatch
│  └─ Show: "Invalid verification code. (X/5)"
│  └─ Increment failed attempts counter
│
├─ Code Expired
│  └─ Show: "Verification code expired. Please request a new one."
│  └─ Delete code from storage
│  └─ Offer resend button
│
└─ Too Many Attempts
   └─ Show: "Too many failed attempts. Please request a new code."
   └─ Disable all inputs
   └─ Force resend
```

## Timeline Example

```
Timeline of a Login Session

T+0s    | Admin enters credentials
        | Form submitted to /api/login
        │
T+1s    | Credentials validated
        | Code generated: 382951
        │
T+2s    | Email sent to admin@example.com
        │
T+3s    | Verification form displayed
        | Timer shows: 4:57
        │
T+5s    | Admin receives email
        | Admin enters code: 3829
        │
T+8s    | Admin enters remaining digits: 51
        │
T+10s   | Admin clicks "Verify Code"
        │
T+11s   | /api/verify-code request sent
        │
T+12s   | Code verified successfully
        │
T+13s   | Session created
        | Redirecting to dashboard...
        │
T+15s   | Dashboard loaded
        | Admin has access!
```

## Resend Code Scenario

```
RESEND CODE FLOW

Initial Code Sent
       │ (5:00 timer starts)
       │
       ├─► 3:30 elapsed
       │   Admin didn't receive email
       │
       ▼
Admin Clicks "Resend Code"
       │
       ▼
New Code Generated (different code)
       │ └─ Old code invalidated
       │ └─ Failed attempts reset
       │
       ▼
New Email Sent
       │
       ▼
Timer Resets (5:00)
       │
       ▼
Admin Enters New Code
       │
       ▼
Verification Complete
```

---

**Diagram Version:** 1.0  
**Last Updated:** May 15, 2026
