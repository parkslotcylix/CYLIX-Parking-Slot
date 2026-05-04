# Testing Checklist - Smart Parking Slot System

## Pre-Setup Tests

### Database Connection
- [ ] MySQL/MariaDB is running
- [ ] Database `parkingslot` exists
- [ ] All tables created successfully
- [ ] Sample data inserted
- [ ] User has proper permissions

### File Structure
- [ ] `config/db.php` exists
- [ ] `api/parking.php` exists
- [ ] `templates/` folder has 4 HTML files
- [ ] `static/images/` has green.png, orange.png, red.png

### Configuration
- [ ] Database credentials updated in `config/db.php`
- [ ] Database host is correct
- [ ] Database user exists
- [ ] Database password is correct

---

## Functionality Tests

### Home Page (`http://localhost:8000/templates/home.html`)

**Visual Tests:**
- [ ] Page loads without errors
- [ ] Navigation bar displays correctly
- [ ] Dashboard widget visible
- [ ] Logo and title display

**Data Tests:**
- [ ] Dashboard shows "Available: 2"
- [ ] Dashboard shows "Occupied: 1"
- [ ] Occupancy percentage shows "33%"
- [ ] Slot 1 shows green dot (Available)
- [ ] Slot 2 shows red dot (Occupied)
- [ ] Slot 3 shows green dot (Available)
- [ ] "Live Monitoring Active" badge displays
- [ ] "1 Spot Free!" message shows

**Real-time Tests:**
- [ ] Dashboard auto-refreshes every 5 seconds
- [ ] After toggling slot in parking page, home updates within 5 seconds
- [ ] Numbers update without page reload

### Parking Page (`http://localhost:8000/templates/parking.html`)

**Visual Tests:**
- [ ] Page loads without errors
- [ ] 3 slot cards display
- [ ] Car images visible (green, orange, red)
- [ ] Camera feed displays with sonar animation

**Slot Status Tests:**
- [ ] Slot 1: Green background, "AVAILABLE" badge
- [ ] Slot 2: Red background, "OCCUPIED" badge, timestamp visible
- [ ] Slot 3: Green background, "AVAILABLE" badge

**Timestamp Tests:**
- [ ] Slot 2 shows "Occupied Since" with time
- [ ] Time format is HH:MM MM/DD
- [ ] Slot 1 and 3 don't show timestamp

**Toggle Functionality:**
- [ ] Click Slot 1 → Changes to occupied (red bg, red badge)
- [ ] Timestamp appears for Slot 1
- [ ] Footer updates: Available becomes 1, Occupied becomes 2
- [ ] Click Slot 1 again → Changes to available
- [ ] Timestamp disappears
- [ ] Footer updates correctly
- [ ] Car image appears/disappears with status

**Reset Button:**
- [ ] Click RESET button
- [ ] Confirmation dialog appears
- [ ] All slots become available
- [ ] All timestamps disappear
- [ ] Car images hide
- [ ] Footer shows correct counts

**Auto-refresh:**
- [ ] Parking page auto-refreshes every 5 seconds
- [ ] Changes from other browser tabs sync in real-time

### Analytics Page (`http://localhost:8000/templates/analytics.html`)

**Visual Tests:**
- [ ] Page loads without errors
- [ ] Analytics header displays
- [ ] 3 statistics cards visible
- [ ] Chart canvas displays

**Data Tests:**
- [ ] "Available Parking Slots" shows "2/3" (matches database)
- [ ] "Total Vehicles Today" shows "156"
- [ ] "Avg. Parking Duration" shows "45m"
- [ ] Chart displays with data points
- [ ] Peak Hours section shows bars

**Real-time Tests:**
- [ ] Analytics updates every 10 seconds
- [ ] After changing slots in parking page, analytics updates
- [ ] Slot count updated correctly

### Account Page (`http://localhost:8000/templates/account.html`)

**Visual Tests:**
- [ ] Page loads without errors
- [ ] Avatar displays
- [ ] Admin Dashboard title shows
- [ ] Information sections display

**Data Tests:**
- [ ] "Admin Name" shows "Administrator"
- [ ] "Admin Email" shows "admin@smartparking.com"
- [ ] "Access Level" shows "🔒 Super Admin"
- [ ] All fields load from database

**Button Tests:**
- [ ] "VIEW FULL REPORT" button visible and clickable
- [ ] "LOGOUT" button visible and clickable

---

## Database Operation Tests

### Slot Toggle Operations
- [ ] Toggling updates `parking_slots` table
- [ ] `check_in_time` populated when toggled to occupied
- [ ] `check_out_time` populated when toggled to available
- [ ] Status changes between 'Available' and 'Occupied'

### Admin Logging
- [ ] Admin logs table populated on slot changes
- [ ] Action descriptions recorded
- [ ] Timestamps recorded correctly

### Data Consistency
- [ ] Frontend data matches database data
- [ ] No data loss during updates
- [ ] Timestamps are accurate

---

## API Tests (Using Postman or curl)

### Test get_slots
```bash
curl "http://localhost:8000/api/parking.php?action=get_slots"
```
- [ ] Returns JSON array
- [ ] Contains all 3 slots
- [ ] Has slot_id, slot_number, slot_status, check_in_time, etc.
- [ ] Slot 2 shows 'Occupied', others show 'Available'

### Test toggle_slot
```bash
curl -X POST "http://localhost:8000/api/parking.php?action=toggle_slot" \
  -H "Content-Type: application/json" \
  -d '{"slot_id": 1}'
```
- [ ] Returns success: true
- [ ] Returns new_status
- [ ] Database updates accordingly

### Test get_summary
```bash
curl "http://localhost:8000/api/parking.php?action=get_summary"
```
- [ ] Returns available count
- [ ] Returns occupied count
- [ ] Returns total count
- [ ] Returns occupancy_percent

### Test reset_slots
```bash
curl -X POST "http://localhost:8000/api/parking.php?action=reset_slots"
```
- [ ] Returns success: true
- [ ] All slots become 'Available'
- [ ] All check times reset to NULL

### Test get_admin
```bash
curl "http://localhost:8000/api/parking.php?action=get_admin"
```
- [ ] Returns admin information
- [ ] Returns correct email
- [ ] Returns correct access level

---

## Browser Compatibility Tests

- [ ] Chrome/Edge (Latest)
- [ ] Firefox (Latest)
- [ ] Safari (Latest)
- [ ] Mobile browsers

---

## Performance Tests

- [ ] Page load time < 2 seconds
- [ ] API responses < 500ms
- [ ] No console errors
- [ ] Auto-refresh doesn't cause lag
- [ ] Multiple rapid clicks handled correctly

---

## Error Handling Tests

### Database Connection Error
- [ ] Change db credentials in `config/db.php`
- [ ] Verify error message displays gracefully

### Invalid Action
```bash
curl "http://localhost:8000/api/parking.php?action=invalid"
```
- [ ] Returns error JSON

### Missing Parameters
```bash
curl -X POST "http://localhost:8000/api/parking.php?action=toggle_slot" \
  -H "Content-Type: application/json" \
  -d '{}'
```
- [ ] Handles gracefully

---

## Cross-Browser Navigation Tests

- [ ] Click links to navigate between pages
- [ ] Back button works
- [ ] Forward button works
- [ ] Refresh maintains data

---

## Final Verification

- [ ] All pages load without errors
- [ ] All features work as expected
- [ ] Database stays consistent
- [ ] Real-time updates work
- [ ] No console errors
- [ ] Responsive on different screens
- [ ] API responses are fast

---

## Sign-Off

- **Tested By**: __________________
- **Date**: __________________
- **Status**: [ ] PASS [ ] FAIL

**Notes:**
_________________________________
_________________________________
_________________________________

