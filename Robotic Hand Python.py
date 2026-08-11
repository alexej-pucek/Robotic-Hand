

#                _  _   _   _  _ ___     _____ ___   _   ___ _  _____ _  _  ___ 
#               | || | /_\ | \| |   \   |_   _| _ \ /_\ / __| |/ /_ _| \| |/ __|
#               | __ |/ _ \| .` | |) |    | | |   // _ \ (__| ' < | || .` | (_ |
#               |_||_/_/ \_\_|\_|___/     |_| |_|_/_/ \_\___|_|\_\___|_|\_|\___|          


#                          _          _____ _               _    _____             _   
#                         | |_ _ _   |  _  | |___ _ _ ___  |_|  |  _  |_ _ ___ ___| |_ 
#                         | . | | |  |     | | -_|_|_| -_| | |  |   __| | |  _| -_| '_|
#                         |___|_  |  |__|__|_|___|_|_|___|_| |  |__|  |___|___|___|_|_|
#                             |___|                      |___|                         

# DATE: 2026
# LICENSE: Licensed under the MIT License
# REQIREMENTS: pip install opencv-python, mediapipe, numpy, pyserial

# USAGE: 
#   1. Connect ESP32 via USB port and check your COM port (update COM_PORT bellow).
#   2. Run script: py -3.12 "Robotic Hand Python.py".
#   3. If you wish to leave the application, press the ESC key.


# !!IMPORTANT NOTICE!!

# This is only the one half of the project, the other half is in Arduino IDE, where is the code for actually controlling the Hardware.
# This code only reads the input, and sends the finger angles to the port you selected.


#required libraries

import cv2 
import mediapipe as mp
import math
import numpy as np
import serial
import time

# ALL MODIFIABLE VALUES FOR FINE TUNING (KEEP ALL OTHER VALUES AS THEY ARE IF YOU AREN'T FAMILIAR WITH THE CODE)

HAND_COMPLEXITY = 1   # complexity of the tracking points, keep on 1 for the program to work

NUM_CAMERA = 0   # number of camera you want to use, default camera is usually on number 0

ANGLE_SMOOTHENING = 2   # the difference between angle of the previous frame to the current frame, lower the value, the smoother the movements will be, but there will also be more jitters

COM_PORT = 'COM3'   # COM port on your computer on which is connected you microcontroler with the arm, if you only want to use the software, not the hardware, this doesn´t matter

BAUDRATE = 115200   # the number of times data is send per second, ESP32 usually communicates at 115200, but you can change it !must be the same as in the Arduino IDE code!

TIMEOUT = 0   # timeout in seconds, how frequently will the data be sent (if set to 0, the data will be returned immediately, recommended)

MAX_NUM_OF_HANDS = 1   # the max number of hands on screen that will be tracked, keep on 1 to have the programm running correctly

DETECTION_CONFIDENCE = 0.9 # the minimal confidence of the hand detection model that it sees a hand on the screen (values from 0.0 to 1.0)

TRACKING_CONFIDENCE = 0.8   # the minimal confidence of the landmark tracking model that it recognized the hand landmarks (values from 0.0 to 1.0)

THUMB_LIMITS  = [120, 160]   # the angles for when the thumb is open, and when it is closed [CLOSED, OPEN]

INDEX_LIMITS  = [112, 145]   # the angles for when the index finger is open, and when it is closed [CLOSED, OPEN]

MIDDLE_LIMITS = [100, 145]   # the angles for when the middle finger is open, and when it is closed [CLOSED, OPEN]

RING_LIMITS   = [95, 150]   # the angles for when the ring finger is open, and when it is closed [CLOSED, OPEN]

PINKY_LIMITS  = [95, 155]   # the angles for when the pinky is open, and when it is closed [CLOSED, OPEN]

TEXT_Y = 20   # X position of the first line of the angles printed on the screen (Bottom-left of the first line)

TEXT_X = 10   # Y position of the first line of the angles printed on the screen (Bottom-left of the first line)

LINE_SPACING = 15   # the spacing between the lines of the angles printed on the screen

TEXT_COLOR = [0, 255, 0]   # text color of the angles printed on the screen (in BGR)

TEXT_SIZE = 0.5   # the size multiplier for the font

TEXT_THICKNESS = 2   # the font thickness of the the angles printed on the screen


#  CODE

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles  = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

try:
    port = serial.Serial(COM_PORT, BAUDRATE, timeout = TIMEOUT)
    time.sleep(2)
    print("ESP32 Connected Succesfully!")

except:
    port = None
    print("Unable to connect to ESP32, camera mode only!")


FINGERS = {
    "Thumb":[1, 2, 4],
    "Index":[5, 6, 8],
    "Middle":[9, 10, 12],
    "Ring":[13, 14, 16],
    "Pinky":[17, 18, 20],
}

ANGLES = {
    "Thumb": 0,
    "Index": 0,
    "Middle": 0,
    "Ring": 0,
    "Pinky": 0,
}

LAST_ANGLES = {
    "Thumb": 0,
    "Index": 0,
    "Middle": 0,
    "Ring": 0,
    "Pinky": 0,
}

FINGER_STATES = {
    "Thumb":THUMB_LIMITS,
    "Index":INDEX_LIMITS,
    "Middle":MIDDLE_LIMITS,
    "Ring":RING_LIMITS,
    "Pinky":PINKY_LIMITS,
}
camera = cv2.VideoCapture(NUM_CAMERA)
with mp_hands.Hands(
    max_num_hands = MAX_NUM_OF_HANDS,
    model_complexity = HAND_COMPLEXITY, 
    min_detection_confidence = DETECTION_CONFIDENCE, 
    min_tracking_confidence = TRACKING_CONFIDENCE) as hands: 
    while camera.isOpened():
        success, image = camera.read()
        if not success:
            print("Empty Frame")
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
                if results.multi_hand_world_landmarks:
                    hand = results.multi_hand_world_landmarks[0]

                
                for finger_name, id in FINGERS.items():
                    
                    id_1 = id[0]
                    id_2 = id[1]
                    id_3 = id[2]

                    joint_1 = hand.landmark[id_1]
                    joint_2 = hand.landmark[id_2]
                    joint_3 = hand.landmark[id_3]

                    v_x = joint_1.x - joint_2.x
                    v_y = joint_1.y - joint_2.y
                    v_z = joint_1.z - joint_2.z

                    u_x = joint_3.x - joint_2.x
                    u_y = joint_3.y - joint_2.y
                    u_z = joint_3.z - joint_2.z

                    lenght_1 = math.sqrt(v_x**2 + v_y**2 + v_z**2)
                    lenght_2 = math.sqrt(u_x**2 + u_y**2 + u_z**2)

                    dot_product = (v_x * u_x) + (v_y * u_y) + (v_z * u_z)

                    cos_angle = dot_product / (lenght_1 * lenght_2) 
                    cos_angle = max(-1.0,min(1.0,cos_angle))

                    angle = math.degrees(math.acos(cos_angle))
                    angle = max(FINGER_STATES[finger_name][0],min(angle,FINGER_STATES[finger_name][1]))

                    ANGLES[finger_name] = int(angle)

                    if(np.abs(ANGLES[finger_name] - LAST_ANGLES[finger_name] ) < ANGLE_SMOOTHENING):
                        ANGLES[finger_name] = LAST_ANGLES[finger_name]
                    else:
                        LAST_ANGLES[finger_name] = ANGLES[finger_name]


                information = ",".join(str(ANGLES[f]) for f in ["Thumb", "Index", "Middle", "Ring", "Pinky"]) + "\n"
                if port is not None:
                    port.write(information.encode('utf-8'))
                    

        image = cv2.flip(image,1)
        y_offset = TEXT_Y
        for finger_name, angle_val in ANGLES.items():
            cv2.putText(image,f"{finger_name}: {angle_val} deg",(TEXT_X, y_offset), cv2.FONT_HERSHEY_SIMPLEX, TEXT_SIZE, (TEXT_COLOR[0], TEXT_COLOR[1], TEXT_COLOR[2]), TEXT_THICKNESS )
            y_offset += LINE_SPACING

        cv2.imshow('MediaPipe Hands', image)

        if cv2.waitKey(1) &0xFF == 27:
            break

        
camera.release()
if port is not None:
    port.close()
cv2.destroyAllWindows()