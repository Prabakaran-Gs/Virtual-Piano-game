import cv2
import mediapipe as mp
import pygame
import random
import time
import numpy as np

pygame.init()
pygame.mixer.init()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)

# songs =[
#     [4,4,3,4,1,2,4,4,3,4,2,1,4,4,5,3,1,2,3,4,4,3,1,2,1], #happy birthday
#     [3,2,1,2,3,3,3, 2,2,2,3,3,3 ,3,2,1,2,3,3,3, 3,2,2,3,2,1], #mary lamb
#     [1,1,5,5,5,5,5,4,4,3,3,2,2,1,5,5,4,4,3,3,2,1,1,5,5,5,5,5,4,4,3,3,2,2,1], #twinkle star
#     [1,2,3,1,1,2,3,1,3,4,5,3,4,5,4,5,4,3,2,1,4,5,4,3,2,1,4,5,4,3,2,1,1,1]
# ]


sound_files = ["C4.mp3", "D4.mp3", "E4.mp3", "F4.mp3", "G4.mp3", "A4.mp3", "B4.mp3"]
sounds = [pygame.mixer.Sound(file) for file in sound_files]
buz = pygame.mixer.Sound('wrong.mp3')
st = pygame.mixer.Sound('start.mp3')

piano_keys = [
    (0, 180, 91, 480),    # C
    (91, 180, 91, 480),   # D
    (182, 180, 91, 480),   # E
    (273, 180, 91, 480),   # F
    (364, 180, 91, 480),   # G
    (455, 180, 91, 480),   # A
    (546, 180, 91, 480)   # B
]

# Get screen resolution
screen_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
screen_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

def create_white_bg():
    return np.ones((int(screen_height), int(screen_width), 3), np.uint8) * 255

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

def start_game():
    start_time = time.time()
    total_time = 30
    score = 0

    # choice = random.randint(0, 3)
    # song = songs[choice]
    # ind = 0
    key_to_press = random.randint(1, 7)

    cv2.namedWindow("Game Info", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Game Info", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    pre = -1
    while time.time() - start_time < total_time:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 0)
        frame = cv2.flip(frame, 0)

        white_bg = create_white_bg()
        frame, flag, x, y = detect_hand(frame)
        draw_piano(frame, piano_keys)

        # Draw key to be pressed in the center of the window
        key_text = f"{key_to_press}"
        key_text_size = cv2.getTextSize(key_text, cv2.FONT_HERSHEY_SIMPLEX, 10, 20)[0]
        key_text_position = ((int(screen_width) - key_text_size[0]) // 2, (int(screen_height) + key_text_size[1]) // 2)
        cv2.putText(white_bg, key_text, key_text_position, cv2.FONT_HERSHEY_SIMPLEX, 10, (0, 0, 225), 20)

        cv2.putText(white_bg, f"Score: {score}", (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 225), 2)

        # Draw remaining time on the white background
        remaining_time = int(total_time - (time.time() - start_time))
        time_text = f"Time Left: {remaining_time} seconds"
        time_text_size = cv2.getTextSize(time_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        time_text_position = ((int(screen_width) - time_text_size[0]) // 2, 50)
        cv2.putText(white_bg, time_text, time_text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 225), 2)

        cv2.imshow('Hand Tracking', frame)
        cv2.imshow("Game Info", white_bg)
        if flag:
            key_index = get_piano_key(x, y, piano_keys)
            if key_index != -1 and key_index + 1 == key_to_press:
                # pre = key_index
                sounds[key_index].play()
                score += 1
                key_to_press = random.randint(1,7)
                # ind +=1 
                # if ind == len(song):
                #     ind = 0
            # elif key_index != pre and key_index != -1 and key_index+1 != key:
            #     buz.play()
                

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print(f"Game Over! Your Score: {score}")
    cv2.destroyWindow("Game Info")
    return score

while True:
    
    start = int(input("Press 1 to start a new game and 0 to exit: "))

    if start == 1:
        print("Starting new round...")
        time.sleep(5)  # Wait for 5 seconds before starting a new round
        
        print("GAME STARTED")
        st.play()
        score = start_game()
        buz.play()

    else:
        print("Bye .........")
        break
