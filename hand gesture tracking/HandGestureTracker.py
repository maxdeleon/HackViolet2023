# TechVidvan hand Gesture Recognizer

# import necessary packages

import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model

import threading
import time


def main():

    open("data/hand_data.txt", "w").close()
    data_file = open("data/hand_data.txt", "w")
    data_file.flush()

    # initialize mediapipe
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.6)
    mpDraw = mp.solutions.drawing_utils

    # Load the gesture recognizer model
    model = load_model('mp_hand_gesture')

    # Load class names
    f = open('gesture.names', 'r')
    classNames = f.read().split('\n')
    f.close()


    # Initialize the webcam
    cap = cv2.VideoCapture(0)


    #data_file.close() # this will erease contents of last time this was run
    #data_file = open("data/hand_data.txt", "w")

    while True:
        # Read each frame from the webcam
        _, frame = cap.read()

        x, y, c = frame.shape

        # Flip the frame vertically
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get hand landmark prediction
        result = hands.process(framergb)

        #print(result)

        className = ''
        x_0 = 0
        y_0 = 0
        gesture_0 = ''
        # post process the result
        landmarks_0 = []
        if result.multi_hand_landmarks:
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    # print(id, lm)
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)
                    #print("x " + str(lmx) + " y " + str(lmy))
                    landmarks.append([lmx, lmy])
                    x_0 = lmx
                    y_0 = lmy
                    #for a in range(len(landmarks)):
                        #print(str(a) + " " + str(landmarks[a]))
                    #print("---------------")
                    landmarks_0 = landmarks
                # Drawing landmarks on frames
                mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

                # Predict gesture
                prediction = model.predict([landmarks])
                # print(prediction)
                classID = np.argmax(prediction)
                className = classNames[classID]

                gesture_0 = className
                data_file.write(str(x_0) + ", " + str(y_0) + ", " + str(gesture_0) + "\n")
                data_file.flush()

                # start



                # end

        # show the prediction on the frame
        cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                       1, (0,0,255), 2, cv2.LINE_AA)

        #rect_frame = cv2.rectangle(frame, (x_0,y_0), (x_0+ 5, y_0 + 5), (0,255,0), 2)
        rect_frame = frame
        for i in range(len(landmarks_0)):
            x1 = landmarks_0[i][0]
            y1 = landmarks_0[i][1]
            rect_frame = cv2.rectangle(rect_frame, (x1, y1), (x1 + 5, y1 + 5), (0, 0, (255*i)/ 20), 2)

        # Show the final output
        cv2.imshow("Output", rect_frame)

        if cv2.waitKey(1) == ord('q'):
            break

    # release the webcam and destroy all active windows
    cap.release()

    cv2.destroyAllWindows()

    data_file.close()
    # in the format x,y,gesture


def app_runner():
    data_file = open("data/hand_data.txt", "r")
    data_file.flush()
    lines = []
    while True:
        line = data_file.readline()
        if not line == "":
            lines.append(line)
            time.sleep(0.1)
        if len(lines) > 0:
            print("L: " + lines[len(lines)-1])






thread_1 = threading.Thread(target=main, daemon=True)
thread_2 = threading.Thread(target=app_runner, daemon=False)


thread_1.start()
thread_2.start()


thread_1.join()
thread_2.join()

