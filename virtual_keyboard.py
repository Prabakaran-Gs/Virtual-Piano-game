import cv2
import mediapipe as mp
import pygame

pygame.init()
pygame.mixer.init()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)  

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
sound_files = ["C4.mp3", "D4.mp3", "E4.mp3", "F4.mp3", "G4.mp3", "A4.mp3", "B4.mp3"]

sounds = [pygame.mixer.Sound(file) for file in sound_files]

# Define the piano key positions (x, y, width, height)
piano_keys = [
    (0, 180, 91, 480),    # C
    (91, 180, 91, 480),   # D
    (182, 180, 91, 480),   # E
    (273, 180, 91, 480),   # F
    (364, 180, 91, 480),   # G
    (455, 180, 91, 480),   # A
    (546, 180, 91, 480)   # B
]

def draw_piano(image, piano_keys):
    for key in piano_keys:
        x, y, w, h = key
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

def detect_hand(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    sound_flag = False
    x, y = 0, 0

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            point_9 = hand_landmarks.landmark[9]
            point_0 = hand_landmarks.landmark[0]
            frame, x, y = draw_circle(frame, point_9, point_0)
            sound_flag = True

    return frame, sound_flag, x, y

def draw_circle(image, point_9, point_0):
    mean_x = int((point_9.x + point_0.x) / 2 * image.shape[1])
    mean_y = int((point_9.y + point_0.y) / 2 * image.shape[0])
    cv2.circle(image, (mean_x, mean_y), 10, (0, 255, 0), -1)
    return image, mean_x, mean_y

def get_piano_key(x, y, piano_keys):
    for i, key in enumerate(piano_keys):
        key_x, key_y, key_w, key_h = key
        if key_x <= x <= key_x + key_w and key_y <= y <= key_y + key_h:
            return i
    return -1

pre = -1
while cap.isOpened():
    # Read a frame from the camera
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    frame = cv2.flip(frame,0)
    if not ret:
        break

    frame, flag, x, y = detect_hand(frame)
    draw_piano(frame, piano_keys)

    # Display the frame
    cv2.imshow('Hand Tracking', frame)

    if flag :
        key_index = get_piano_key(x, y, piano_keys)
        if key_index != -1 and pre != key_index:
            sounds[key_index].play()
        pre = key_index
    else:
        pre = -1
    

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
