# Analytics Page - User Guide

**Version**: 2.0  
**Status**: ✅ Production Ready  
**Last Updated**: May 2, 2026

---

## Quick Start

### Accessing the Analytics Page
1. Navigate to `http://localhost:5000/analytics`
2. Page loads with "Today" filter selected by default
3. All charts and statistics display immediately

### Understanding the Dashboard

#### Overview Cards (Top Section)
- **Total Sessions Completed**: Number of completed parking sessions
- **Avg. Parking Duration**: Average time vehicles stayed parked
- **Available Parking Slots**: Current available vs total slots
- **Active Sessions**: Number of currently parked vehicles

#### Occupancy Rate Chart (24h)
- Shows parking occupancy percentage for each hour
- X-axis: Hours (12am to 11pm)
- Y-axis: Occupancy percentage (0-100%)
- Green line indicates occupancy trend
- Based on real data: (occupied slots / total slots) × 100

#### Peak Hours Chart
- Shows the 3 busiest hours of the day
- Displays hour and occupancy percentage
- Automatically calculated from actual data
- Updates when you change the filter

---

## Using Filters

### Available Filters
1. **Today** (Default)
   - Shows data from current day
   - Updates in real-time

2. **Yesterday**
   - Shows data from previous day
   - Useful for comparing daily patterns

3. **This Week**
   - Shows data from last 7 days
   - Identifies weekly trends

4. **1 Month**
   - Shows data from last 30 days
   - Long-term analysis

### How to Change Filter
1. Click the filter dropdown (top right)
2. Select desired time period
3. Analytics update automatically
4. Charts refresh with new data

---

## Generating Reports

### Print Analytics Report
1. Click "📄 Print Report" button
2. Professional PDF opens in new window
3. Report includes:
   - Executive summary
   - Key metrics
   - Parking history table (last 10 records)
   - Date and time stamps

### Printing to PDF
1. In the print window, press `Ctrl+P` (or `Cmd+P` on Mac)
2. Select "Save as PDF"
3. Choose location and save

### Report Contents
- **Header**: ParkSlot logo, date, time
- **Executive Summary**: Overview of parking activity
- **Key Metrics**: Total sessions, average duration, active sessions, available slots
- **Parking History**: Recent parking records with check-in/out times
- **Footer**: Copyright and system information

---

## Understanding the Data

### Occupancy Rate Calculation
```
Occupancy % = (Number of Occupied Slots / Total Slots) × 100
```

Example:
- Total Slots: 3
- Occupied Slots: 2
- Occupancy Rate: (2 / 3) × 100 = 66.67%

### Average Duration Calculation
```
Average Duration = Sum of All Durations / Number of Sessions
```

Example:
- Session 1: 2 hours
- Session 2: 1.5 hours
- Session 3: 3 hours
- Average: (2 + 1.5 + 3) / 3 = 2.17 hours = 2h 10m

### Peak Hours
- Calculated from hourly occupancy data
- Shows the 3 hours with highest occupancy
- Helps identify busy times

---

## Features

### Real-Time Updates
- Analytics refresh every 30 seconds
- Charts update automatically
- No manual refresh needed

### Responsive Design
- Works on desktop, tablet, mobile
- Charts scale to screen size
- Touch-friendly on mobile devices

### Error Handling
- Graceful handling of missing data
- No crashes or errors
- Clear error messages if issues occur

### Data Validation
- All values checked for accuracy
- Null values handled properly
- Type conversions done safely

---

## Troubleshooting

### Issue: Charts Not Loading
**Solution**:
1. Refresh the page (F5)
2. Check browser console (F12) for errors
3. Verify database connection
4. Try different filter

### Issue: No Data Showing
**Solution**:
1. Ensure parking sessions exist in database
2. Check if data is within selected time period
3. Try "This Week" or "1 Month" filter
4. Verify parking_history table has records

### Issue: Print Report Not Opening
**Solution**:
1. Disable popup blocker
2. Check browser console for errors
3. Try different browser
4. Ensure JavaScript is enabled

### Issue: Slow Performance
**Solution**:
1. Close other browser tabs
2. Clear browser cache
3. Reduce number of open applications
4. Try different browser

---

## Tips & Best Practices

### For Daily Monitoring
1. Check analytics first thing in the morning
2. Use "Today" filter for current status
3. Monitor peak hours for capacity planning
4. Track average duration trends

### For Weekly Analysis
1. Use "This Week" filter on Fridays
2. Compare with previous weeks
3. Identify patterns and trends
4. Plan staffing accordingly

### For Monthly Reports
1. Use "1 Month" filter for comprehensive view
2. Generate PDF report for documentation
3. Compare with previous months
4. Identify seasonal patterns

### For Presentations
1. Generate PDF report
2. Print to high-quality paper
3. Include in presentations
4. Share with stakeholders

---

## Data Interpretation

### High Occupancy Rate
- Indicates busy parking facility
- May need additional capacity
- Consider peak hour management

### Low Occupancy Rate
- Indicates available capacity
- Good for customer experience
- May indicate off-peak hours

### Peak Hours
- Plan staffing for these times
- Implement traffic management
- Consider dynamic pricing

### Average Duration
- Longer duration = higher turnover time
- Shorter duration = quick parking
- Use for capacity planning

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| F5 | Refresh page |
| F12 | Open developer console |
| Ctrl+P | Print page |
| Ctrl+S | Save page |
| Esc | Close dialogs |

---

## Browser Support

✅ Chrome/Edge (latest)  
✅ Firefox (latest)  
✅ Safari (latest)  
✅ Mobile browsers  

---

## Performance

- **Page Load**: < 500ms
- **Chart Render**: < 200ms
- **API Response**: < 100ms
- **Auto-Refresh**: Every 30 seconds

---

## Security

- Authentication required (login)
- Session-based access control
- Data encrypted in transit
- No sensitive data in URLs

---

## Support

### For Issues
1. Check this guide
2. Review troubleshooting section
3. Check browser console (F12)
4. Contact system administrator

### For Feature Requests
1. Document the request
2. Explain use case
3. Submit to development team

---

## FAQ

**Q: How often does the data update?**  
A: Every 30 seconds automatically. You can also refresh manually.

**Q: Can I export data to Excel?**  
A: Currently, you can print to PDF. Excel export coming soon.

**Q: How far back does the data go?**  
A: Data is stored indefinitely. Use filters to view specific periods.

**Q: Can I customize the report?**  
A: Currently, the report format is fixed. Customization coming soon.

**Q: What if I see an error?**  
A: Check the troubleshooting section or contact support.

**Q: Is the data real-time?**  
A: Yes, data updates every 30 seconds from the database.

**Q: Can multiple users view analytics simultaneously?**  
A: Yes, multiple users can access the analytics page.

**Q: Is there a mobile app?**  
A: Currently web-based only. Mobile app coming soon.

---

## Glossary

| Term | Definition |
|------|-----------|
| Occupancy Rate | Percentage of slots currently occupied |
| Peak Hours | Hours with highest parking activity |
| Session | One parking event (check-in to check-out) |
| Duration | Time between check-in and check-out |
| Active Session | Currently parked vehicle |
| Completed Session | Vehicle has checked out |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | May 2, 2026 | All fixes implemented |
| 1.0 | April 2026 | Initial release |

---

## Contact

For support or questions, contact the system administrator.

---

**Last Updated**: May 2, 2026  
**Status**: ✅ Production Ready  
**Version**: 2.0
