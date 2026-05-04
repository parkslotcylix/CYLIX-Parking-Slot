import cv2
import pickle
import requests
import serial
import numpy as np
import time
from urllib.request import urlopen
import threading

# --- CONFIG ---
CAM_URL = "http://192.168.68.146:81/stream"
CAM_IP = "192.168.68.146"
COM_PORT = 'COM7' #Julie palitan mo to depende sa port nung LOLin mo or ung esp8266 mow check mo sa ide
SENSITIVITY = 3500  # Total pixel change required to trigger "Full": adjust low (0 - 5000) means more sensitive, high (5000 and beyond ewan HDSAHDAH) means less sensitive 
FLASK_API = "https://cylix-parking-slot.onrender.com/api/update_slot_from_hardware"  # Backend API endpoint

# Track previous slot states to detect changes
previous_results = [None, None, None]
last_api_update_time = {}  # Throttle API updates
state_change_counts = [0, 0, 0]  # Count consecutive changes before confirming
DEBOUNCE_FRAMES = 5  # Require 5 consecutive frames of same state before accepting change

ser = serial.Serial(COM_PORT, 115200, timeout=0.1)
with open("slot_coords.pkl", "rb") as f:
    slot_positions = pickle.load(f)

# Better MJPEG stream handling
def get_mjpeg_frame(url):
    """Extract frames from MJPEG stream with proper boundary handling"""
    try:
        stream = urlopen(url, timeout=5)
        bytes_data = b''
        
        while True:
            bytes_data += stream.read(1024)
            a = bytes_data.find(b'\xff\xd8')  # JPEG start
            b = bytes_data.find(b'\xff\xd9')  # JPEG end
            
            if a != -1 and b != -1:
                jpg = bytes_data[a:b+2]
                bytes_data = bytes_data[b+2:]
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                if frame is not None:
                    return frame
    except Exception as e:
        print(f"Stream error: {e}")
        return None

# Initialize camera with retry logic
cap = None
retry_count = 0
max_retries = 5

while cap is None and retry_count < max_retries:
    try:
        cap = cv2.VideoCapture(CAM_URL)
        if cap.isOpened():
            print("Camera connected successfully")
            break
        else:
            retry_count += 1
            print(f"Camera connection attempt {retry_count}/{max_retries} failed, retrying...")
            time.sleep(2)
    except Exception as e:
        retry_count += 1
        print(f"Camera error (attempt {retry_count}/{max_retries}): {e}")
        time.sleep(2)

if cap is None:
    print("Failed to connect to camera after retries")
    exit(1)

try:
    requests.get(f"http://{CAM_IP}/control?var=led_intensity&val=255", timeout=3)
except:
    print("Warning: Could not set LED intensity")

print("--- CALIBRATION ---")
print("Make sure all 3 slots are EMPTY. Press 'c' to capture the EMPTY reference.")

empty_reference = None
while empty_reference is None:
    ret, frame = cap.read()
    if not ret:
        frame = get_mjpeg_frame(CAM_URL)
    
    if frame is not None:
        cv2.imshow("Calibration - CLEAR ALL SLOTS", frame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            empty_reference = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            empty_reference = cv2.GaussianBlur(empty_reference, (21, 21), 0)
            print("Empty state saved!")
    else:
        print("Waiting for camera frame...")
        time.sleep(1)

print("Running Detection...")

def send_slot_to_backend(slot_id, status):
    """Send slot status to Flask backend API"""
    try:
        response = requests.post(
            FLASK_API,
            json={'slot_id': slot_id, 'status': status},
            timeout=5
        )
        if response.status_code == 200:
            print(f"✓ Slot {slot_id} updated to backend: {status}")
        else:
            print(f"✗ Backend error for Slot {slot_id}: {response.status_code}")
    except requests.exceptions.Timeout:
        print(f"⚠ Backend timeout for Slot {slot_id}")
    except requests.exceptions.ConnectionError:
        print(f"⚠ Backend unreachable for Slot {slot_id} - Check Render deployment")
    except Exception as e:
        print(f"✗ Error sending Slot {slot_id}: {str(e)}")

print(f"Slot positions loaded: {slot_positions}")
print(f"Sensitivity threshold: {SENSITIVITY}")
print(f"Debounce frames: {DEBOUNCE_FRAMES}")
print("Running Detection...")

frame_count = 0
while True:
    try:
        ret, frame = cap.read()
        if not ret:
            frame = get_mjpeg_frame(CAM_URL)
        
        if frame is None:
            print("No frame received, retrying...")
            time.sleep(0.5)
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        frame_delta = cv2.absdiff(empty_reference, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

        results = []
        frame_count += 1
        debug_output = ""
        
        for i, (x, y, w, h) in enumerate(slot_positions):
            slot_roi = thresh[y:y+h, x:x+w]
            change_count = cv2.countNonZero(slot_roi)
            
            status = 1 if change_count > SENSITIVITY else 0
            results.append(status)
            
            slot_id = i + 1
            if status == previous_results[i]:
                state_change_counts[i] = 0
            else:
                state_change_counts[i] += 1
                
                if state_change_counts[i] >= DEBOUNCE_FRAMES:
                    print(f"[Frame {frame_count}] Slot {slot_id} CONFIRMED changed: {previous_results[i]} → {status} (pixels: {change_count})")
                    send_slot_to_backend(slot_id, status)
                    previous_results[i] = status
                    state_change_counts[i] = 0
                else:
                    print(f"[Frame {frame_count}] Slot {slot_id} pending change ({state_change_counts[i]}/{DEBOUNCE_FRAMES}): {previous_results[i]} → {status} (pixels: {change_count})")
            
            debug_output += f"S{slot_id}:{change_count}({'✓' if status == 1 else '○'}) "
            
            color = (0, 0, 255) if status == 1 else (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, str(change_count), (x, y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
        
        if frame_count % 30 == 0:
            print(f"[Frame {frame_count}] {debug_output}")

        try:
            ser.write(f"{results[0]},{results[1]},{results[2]}\n".encode())
        except:
            print("Warning: Serial write failed")
        
        cv2.imshow("Parking Area", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    except Exception as e:
        print(f"Error in main loop: {e}")
        time.sleep(1)
        continue

try:
    requests.get(f"http://{CAM_IP}/control?var=led_intensity&val=0", timeout=3)
except:
    pass

cap.release()
ser.close()
cv2.destroyAllWindows()
print("Script ended")