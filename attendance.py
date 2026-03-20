import cv2
import numpy as np
import pandas as pd
import json
import os
from datetime import datetime

# ─────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────
LATE_ARRIVAL_HOUR   = 9   # After 9:00 AM = Late
LATE_ARRIVAL_MINUTE = 0
CONFIDENCE_THRESHOLD = 70
SNAPSHOT_FOLDER = 'snapshots'
UNKNOWN_FOLDER  = 'unknown_faces'

# Create folders
for folder in ['attendance', SNAPSHOT_FOLDER, UNKNOWN_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# ─────────────────────────────────────────
# CHECK MODEL EXISTS
# ─────────────────────────────────────────
if not os.path.exists('face_model.yml'):
    print("❌ No trained model found!")
    print("Please run register.py first!")
    exit()

if not os.path.exists('label_map.json'):
    print("❌ No label map found!")
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
# ATTENDANCE SETUP
# ─────────────────────────────────────────
today            = datetime.now().strftime('%Y-%m-%d')
attendance_file  = f'attendance/attendance_{today}.csv'

if os.path.exists(attendance_file):
    df = pd.read_csv(attendance_file)
else:
    df = pd.DataFrame(columns=[
        'Name', 'Date', 'Time', 'Status', 'Arrival'
    ])

marked_today    = set(df['Name'].tolist())
unknown_log     = []
unknown_counter = 0

print(f"📋 Attendance System Started — {today}")
print(f"⏰ Late arrival after: {LATE_ARRIVAL_HOUR:02d}:{LATE_ARRIVAL_MINUTE:02d}")
print(f"✅ Already marked: {len(marked_today)} people")
print("Press Q to quit\n")

# ─────────────────────────────────────────
# WEBCAM
# ─────────────────────────────────────────
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Colors
GREEN  = (0, 255, 0)
RED    = (0, 0, 255)
YELLOW = (0, 255, 255)
ORANGE = (0, 165, 255)
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)

def is_late():
    """Check if current time is past late threshold."""
    now = datetime.now()
    return (now.hour > LATE_ARRIVAL_HOUR or
           (now.hour == LATE_ARRIVAL_HOUR and
            now.minute >= LATE_ARRIVAL_MINUTE))

def mark_attendance(name, frame, x, y, w, h):
    """Mark attendance and save snapshot."""
    global df, marked_today
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
        timestamp   = now.strftime('%H%M%S')
        snapshot    = frame.copy()
        snap_path   = f'{SNAPSHOT_FOLDER}/{name}_{today}_{timestamp}.jpg'
        cv2.imwrite(snap_path, snapshot)

        print(f"✅ {name} marked — {arrival} at {now.strftime('%H:%M:%S')}")
        return True, arrival
    return False, None

def save_unknown_face(frame, x, y, w, h):
    """Save unknown face snapshot and log it."""
    global unknown_counter
    unknown_counter += 1
    now       = datetime.now()
    timestamp = now.strftime('%H%M%S')
    face_img  = frame[y:y+h, x:x+w]
    path      = f'{UNKNOWN_FOLDER}/unknown_{today}_{timestamp}.jpg'
    cv2.imwrite(path, face_img)

    unknown_log.append({
        'Date'     : today,
        'Time'     : now.strftime('%H:%M:%S'),
        'Snapshot' : path
    })

    # Save unknown log
    unknown_df = pd.DataFrame(unknown_log)
    unknown_df.to_csv(f'attendance/unknown_log_{today}.csv',
                     index=False)
    print(f"⚠️  Unknown face detected and saved! ({unknown_counter} today)")

# Track unknown face timer to avoid spam saving
last_unknown_save = {}

# ─────────────────────────────────────────
# MAIN LOOP
# ─────────────────────────────────────────
while True:
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
            # ── Known Person ──
            name  = label_map[str(label_id)]
            color = GREEN

            just_marked, arrival = mark_attendance(
                name, frame, x, y, w, h
            )

            if name in marked_today:
                late_tag = ""
                if not df.empty:
                    person_row = df[df['Name'] == name]
                    if not person_row.empty:
                        late_tag = person_row.iloc[-1]['Arrival']

                status = f"✅ {late_tag}"
                color  = ORANGE if "Late" in late_tag else GREEN
            else:
                status = "Marking..."

        else:
            # ── Unknown Person ──
            name   = "Unknown"
            status = "❌ Not Registered"
            color  = RED

            # Save unknown face (max once per 10 seconds)
            current_time = datetime.now().timestamp()
            last_save    = last_unknown_save.get('time', 0)
            if current_time - last_save > 10:
                save_unknown_face(frame, x, y, w, h)
                last_unknown_save['time'] = current_time

        # Draw face box
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

        # Name tag background
        cv2.rectangle(frame, (x, y-75), (x+w, y), color, -1)
        cv2.putText(frame, name,
                   (x+5, y-50),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, WHITE, 2)
        cv2.putText(frame, f"Confidence: {confidence_pct}%",
                   (x+5, y-28),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 1)
        cv2.putText(frame, status,
                   (x+5, y-8),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 1)

    # ── INFO PANEL ──
    late_now = is_late()
    time_color = RED if late_now else GREEN
    time_status = "🔴 LATE PERIOD" if late_now else "🟢 ON TIME PERIOD"

    cv2.rectangle(frame, (0, 0), (450, 110), (20, 20, 20), -1)
    cv2.putText(frame, '🎯 Smart Attendance System',
               (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, YELLOW, 2)
    cv2.putText(frame, f'Date: {today}  |  {datetime.now().strftime("%H:%M:%S")}',
               (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.55, WHITE, 1)
    cv2.putText(frame, f'Marked: {len(marked_today)}  |  Unknown: {unknown_counter}  |  {time_status}',
               (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, time_color, 1)
    cv2.putText(frame, 'Press Q to quit',
               (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, RED, 1)

    cv2.imshow('Smart Attendance System', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print(f"\n📊 Session Summary for {today}:")
print(f"✅ Total Present  : {len(marked_today)}")
print(f"⚠️  Unknown Faces  : {unknown_counter}")
print(f"📁 Saved to       : {attendance_file}")
print("\nRun dashboard.py to see full report! 🚀")