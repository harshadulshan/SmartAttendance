import cv2
import os

# ─────────────────────────────────────────
# FACE REGISTRATION
# ─────────────────────────────────────────

def register_face():
    # Create dataset folder if not exists
    if not os.path.exists('dataset'):
        os.makedirs('dataset')

    # Get student/employee name
    name = input("Enter the person's name: ").strip()
    if not name:
        print("Name cannot be empty!")
        return

    # Create folder for this person
    person_folder = f'dataset/{name}'
    if not os.path.exists(person_folder):
        os.makedirs(person_folder)

    # Start webcam
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    count = 0
    total_samples = 50  # capture 50 face samples
    print(f"\n📸 Capturing {total_samples} face samples for {name}...")
    print("Please look at the camera and slowly move your head slightly!")

    while count < total_samples:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5
        )

        for (x, y, w, h) in faces:
            count += 1
            # Save face image
            face_img = gray[y:y+h, x:x+w]
            cv2.imwrite(f'{person_folder}/{count}.jpg', face_img)
            cv2.waitKey(100)  # 100ms delay between each capture

            # Draw rectangle and counter
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f'Capturing: {count}/{total_samples}',
                       (x, y-10), cv2.FONT_HERSHEY_SIMPLEX,
                       0.7, (0, 255, 0), 2)

        # Progress bar on screen
        progress = int((count / total_samples) * 400)
        cv2.rectangle(frame, (10, 30), (410, 60), (50, 50, 50), -1)
        cv2.rectangle(frame, (10, 30), (10 + progress, 60), (0, 255, 0), -1)
        cv2.putText(frame, f'Progress: {count}/{total_samples}',
                   (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(frame, f'Registering: {name}',
                   (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        cv2.putText(frame, 'Press Q to cancel',
                   (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        cv2.imshow('Face Registration', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if count >= total_samples:
        print(f"\n✅ Successfully registered {name} with {count} samples!")
        print("📚 Training the model now...")
        train_model()
    else:
        print(f"\n⚠️ Only captured {count} samples. Please try again!")

def train_model():
    """Train the face recognizer with all registered faces."""
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    faces = []
    labels = []
    label_map = {}
    label_id = 0

    # Load all registered faces
    for person_name in os.listdir('dataset'):
        person_folder = f'dataset/{person_name}'
        if not os.path.isdir(person_folder):
            continue

        label_map[label_id] = person_name
        for img_file in os.listdir(person_folder):
            img_path = f'{person_folder}/{img_file}'
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                faces.append(img)
                labels.append(label_id)
        label_id += 1

    if len(faces) == 0:
        print("❌ No faces found to train!")
        return

    # Train and save model
    recognizer.train(faces, __import__('numpy').array(labels))
    recognizer.write('face_model.yml')

    # Save label map
    import json
    with open('label_map.json', 'w') as f:
        json.dump(label_map, f)

    print(f"✅ Model trained successfully with {len(set(labels))} people!")
    print("🎯 You can now run attendance.py")

if __name__ == '__main__':
    print("=" * 40)
    print("   👤 FACE REGISTRATION SYSTEM")
    print("=" * 40)
    while True:
        print("\n1. Register new person")
        print("2. Retrain model only")
        print("3. Exit")
        choice = input("\nEnter choice (1/2/3): ").strip()

        if choice == '1':
            register_face()
        elif choice == '2':
            train_model()
        elif choice == '3':
            break
        else:
            print("Invalid choice!")