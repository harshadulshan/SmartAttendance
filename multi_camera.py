import cv2
import numpy as np
import pandas as pd
import json
import os
import threading
from datetime import datetime

# ─────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────
CAMERAS = [0,1]              # ← Camera indexes (0=built-in, 1=external)
CONFIDENCE_THRESHOLD = 70
LATE_ARRIVAL_HOUR    = 9
LATE_ARRIVAL_MINUTE  = 0

# Create folders
for folder in ['attendance', 'snapshots', 'unknown_faces']:
    if not os.path.exists(folder):
        os.makedirs(folder)

# ─────────────────────────────────────────
# CHECK MODEL
# ─────────────────────────────────────────
if not os.path.exists('face_model.yml'):
    print("❌ No trained model found!")
    print("Please run register.py first!")
    exit()

# ─────────────────────────────────────────
# LOAD MODEL
# ─────────────────────────────────────────
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('face_model.yml')

with open('label_map.json', 'r') as f:
    label_map = json.load(f)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# ─────────────────────────────────────────
# SHARED STATE
# ─────────────────────────────────────────
today           = datetime.now().strftime('%Y-%m-%d')
attendance_file = f'attendance/attendance_{today}.csv'

if os.path.exists(attendance_file):
    df = pd.read_csv(attendance_file)
    if 'Arrival' not in df.columns:
        df['Arrival'] = 'On Time 🟢'
else:
    df = pd.DataFrame(columns=[
        'Name', 'Date', 'Time', 'Status', 'Arrival'
    ])

marked_today     = set(df['Name'].tolist())
unknown_counters = {}
lock             = threading.Lock()

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
def is_late():
    now = datetime.now()
    return (now.hour > LATE_ARRIVAL_HOUR or
           (now.hour == LATE_ARRIVAL_HOUR and
            now.minute >= LATE_ARRIVAL_MINUTE))

def mark_attendance(name, frame, cam_id):
    global df, marked_today
    with lock:
        if name not in marked_today:
            now     = datetime.now()
            arrival = "Late 🔴" if is_late() else "On Time 🟢"
            new_row = {
                'Name'   : name,
                'Date'   : now.strftime('%Y-%m-%d'),
                'Time'   : now.strftime('%H:%M:%S'),
                'Status' : 'Present',
                'Arrival': arrival
            }
            df = pd.concat([df, pd.DataFrame([new_row])],
                          ignore_index=True)
            df.to_csv(attendance_file, index=False)
            marked_today.add(name)

            # Save snapshot
            timestamp = now.strftime('%H%M%S')
            cv2.imwrite(
                f'snapshots/{name}_{today}_{timestamp}_cam{cam_id}.jpg',
                frame
            )
            print(f"✅ [{cam_id}] {name} — {arrival} at {now.strftime('%H:%M:%S')}")
            return True, arrival
    return False, None

last_unknown_save = {}

def save_unknown(frame, x, y, w, h, cam_id):
    current_time = datetime.now().timestamp()
    key          = f'cam{cam_id}'
    last_save    = last_unknown_save.get(key, 0)

    if current_time - last_save > 10:
        now       = datetime.now()
        timestamp = now.strftime('%H%M%S')
        face_img  = frame[y:y+h, x:x+w]
        cv2.imwrite(
            f'unknown_faces/unknown_{today}_{timestamp}_cam{cam_id}.jpg',
            face_img
        )
        last_unknown_save[key] = current_time
        unknown_counters[key]  = unknown_counters.get(key, 0) + 1
        print(f"⚠️  [{cam_id}] Unknown face detected!")

# ─────────────────────────────────────────
# CAMERA THREAD
# ─────────────────────────────────────────
class CameraThread(threading.Thread):
    def __init__(self, cam_id):
        super().__init__()
        self.cam_id  = cam_id
        self.running = True
        self.frame   = None

    def run(self):
        cap = cv2.VideoCapture(self.cam_id)

        if not cap.isOpened():
            print(f"❌ Camera {self.cam_id} not found!")
            self.running = False
            return

        cap.set(3, 640)
        cap.set(4, 480)
        print(f"✅ Camera {self.cam_id} started!")

        # Colors
        GREEN  = (0, 255, 0)
        RED    = (0, 0, 255)
        YELLOW = (0, 255, 255)
        ORANGE = (0, 165, 255)
        WHITE  = (255, 255, 255)

        while self.running:
            success, frame = cap.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)
            gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.3, minNeighbors=5
            )

            for (x, y, w, h) in faces:
                face_roi             = gray[y:y+h, x:x+w]
                label_id, confidence = recognizer.predict(face_roi)
                confidence_pct       = round(100 - confidence, 2)

                if confidence < CONFIDENCE_THRESHOLD:
                    name  = label_map[str(label_id)]
                    color = GREEN

                    just_marked, arrival = mark_attendance(
                        name, frame, self.cam_id
                    )

                    late_tag = ""
                    with lock:
                        if not df.empty:
                            person_row = df[df['Name'] == name]
                            if not person_row.empty:
                                late_tag = person_row.iloc[-1]['Arrival']

                    color  = ORANGE if "Late" in late_tag else GREEN
                    status = f"✅ {late_tag}"
                else:
                    name   = "Unknown"
                    status = "❌ Not Registered"
                    color  = RED
                    save_unknown(frame, x, y, w, h, self.cam_id)

                # Draw
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.rectangle(frame, (x, y-75), (x+w, y), color, -1)
                cv2.putText(frame, name,
                           (x+5, y-50),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, WHITE, 2)
                cv2.putText(frame, f"Conf: {confidence_pct}%",
                           (x+5, y-28),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 1)
                cv2.putText(frame, status,
                           (x+5, y-8),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 1)

            # Info panel
            unk_count = unknown_counters.get(f'cam{self.cam_id}', 0)
            cv2.rectangle(frame, (0, 0), (400, 85), (20, 20, 20), -1)
            cv2.putText(frame, f'Camera {self.cam_id} — Smart Attendance',
                       (10, 22), cv2.FONT_HERSHEY_SIMPLEX,
                       0.6, YELLOW, 2)
            cv2.putText(frame,
                       f'Marked: {len(marked_today)} | Unknown: {unk_count}',
                       (10, 47), cv2.FONT_HERSHEY_SIMPLEX,
                       0.55, GREEN, 1)
            cv2.putText(frame,
                       f'{datetime.now().strftime("%H:%M:%S")} | Press Q to quit',
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX,
                       0.5, WHITE, 1)

            self.frame = frame
            cv2.imshow(f'Camera {self.cam_id}', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False
                break

        cap.release()
        cv2.destroyWindow(f'Camera {self.cam_id}')
        print(f"📷 Camera {self.cam_id} stopped!")

    def stop(self):
        self.running = False

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 45)
    print("  📷 MULTI-CAMERA ATTENDANCE SYSTEM")
    print("=" * 45)
    print(f"\n🎥 Starting {len(CAMERAS)} cameras...")
    print("Press Q in any camera window to quit\n")

    # Start camera threads
    threads = []
    for cam_id in CAMERAS:
        t = CameraThread(cam_id)
        t.start()
        threads.append(t)

    # Wait for all threads
    for t in threads:
        t.join()

    print(f"\n📊 Final Summary:")
    print(f"✅ Total Present : {len(marked_today)}")
    print(f"📁 Saved to      : {attendance_file}")
    print("\nRun dashboard.py to see full report! 🚀")