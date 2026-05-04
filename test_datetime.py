#!/usr/bin/env python3
from datetime import datetime

# Test timestamp parsing
check_in_str = "2026-05-04T18:13:31"
check_out_str = "2026-05-04T18:14:53"

print(f"Original strings:")
print(f"  check_in:  {check_in_str}")
print(f"  check_out: {check_out_str}")

# Try ISO format with timezone removal
try:
    check_in_clean = check_in_str.replace('Z', '').replace('+00:00', '')
    check_out_clean = check_out_str.replace('Z', '').replace('+00:00', '')
    print(f"\nCleaned strings:")
    print(f"  check_in:  {check_in_clean}")
    print(f"  check_out: {check_out_clean}")
    
    check_in = datetime.fromisoformat(check_in_clean)
    check_out = datetime.fromisoformat(check_out_clean)
    print(f"\nParsed datetimes:")
    print(f"  check_in:  {check_in}")
    print(f"  check_out: {check_out}")
    
    calculated_duration = (check_out - check_in).total_seconds() / 3600
    print(f"\nDuration calculation:")
    print(f"  seconds: {(check_out - check_in).total_seconds()}")
    print(f"  hours: {calculated_duration}")
    print(f"  rounded: {round(calculated_duration, 2)}")
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
