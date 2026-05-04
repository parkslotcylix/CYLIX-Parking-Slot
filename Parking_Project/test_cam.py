import cv2
import pickle
import requests
import time
#julie run mo muna ung directory "cd C:\Users\Christine\OneDrive\Documents\Parking_Project" sa terminal 
# then run mo ung "python test_cam.py" para ma calibrate mo yung camera at ma set mo yung slot positions, once na save na yung slot positions sa "slot_coords.pkl" file, run mo na ung "python master_script.py" para mag start na ung monitoring ng parking slots.
# then julie test mo na ung "python master_script.py" para ma start na ung monitoring ng parking slots, make sure na naka on yung camera web server at naka flash yung led para ma detect ng camera yung slot positions, once na detect na ng camera yung slot positions, you can start testing by placing objects in the slots and see if it detects them as full or empty.

# --- SETTINGS ---
url = "http://192.168.68.146:81/stream"
ip_addr = "192.168.68.146"

def set_led(state):
    """Turns the ESP32-CAM Flash LED On (1) or Off (0)"""
    val = 255 if state == 1 else 0
    try:
        requests.get(f"http://{ip_addr}/control?var=led_intensity&val={val}", timeout=1)
    except:
        print("Could not toggle LED. Check if CameraWebServer is running.")

def main():
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        print("Error: Could not connect to ESP32-CAM.")
        return
    #naglagy nalng ako instructios pasunod nalng 
    print("\n--- STEP 1: ADJUST PLACEMENT (LIGHTS OFF) ---")
    print("1. Move the camera until the 3 slots are centered.")
    print("2. Press 's' to FLASH LIGHT and SNAP the setup.")

    while True:
        ret, frame = cap.read()
        if not ret: continue

        cv2.imshow("Adjust Placement - Press 's' to Flash & Snap", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            print("\nFlashing LED...")
            set_led(1)       
            time.sleep(0.5)  
            for _ in range(5): cap.read() 
            ret, snap_frame = cap.read()
            
            set_led(0)     
            print("Snap taken! LED Off.")
            break
        elif key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return

    print("\n--- STEP 2: DRAW THE SLOTS ON THE BRIGHT IMAGE ---")
    s1 = cv2.selectROI("Draw Slot 1", snap_frame, fromCenter=False)
    s2 = cv2.selectROI("Draw Slot 2", snap_frame, fromCenter=False)
    s3 = cv2.selectROI("Draw Slot 3", snap_frame, fromCenter=False)

    slot_positions = [s1, s2, s3]
    with open("slot_coords.pkl", "wb") as f:
        pickle.dump(slot_positions, f)

    print("\n--- SUCCESS! ---")
    print("Coordinates saved with bright exposure.")
    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    main()