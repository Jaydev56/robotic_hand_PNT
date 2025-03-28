import mediapipe as mp
import cv2
import numpy as np
import serial
import time

class HandController:
    def __init__(self, com_port):
        self.arduino = self.connect_arduino(com_port)
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils

    def connect_arduino(self, com):
        try:
            arduino = serial.Serial(port=com, baudrate=9600, timeout=1)
            time.sleep(2)
            return arduino
        except serial.SerialException as e:
            print(e)
            return None

    def get_finger_angles(self, landmarks, width, height):
        fingers = [(4, 3, 2), (8, 6, 5), (12, 10, 9), (16, 14, 13), (20, 18, 17)]
        angles = []
        for tip, mid, base in fingers:
            x1, y1 = int(landmarks.landmark[tip].x * width), int(landmarks.landmark[tip].y * height)
            x2, y2 = int(landmarks.landmark[mid].x * width), int(landmarks.landmark[mid].y * height)
            x3, y3 = int(landmarks.landmark[base].x * width), int(landmarks.landmark[base].y * height)
            vec1 = np.array([x1 - x2, y1 - y2])
            vec2 = np.array([x3 - x2, y3 - y2])
            dot_product = np.dot(vec1, vec2)
            magnitude_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
            angle_deg = np.degrees(np.arccos(np.clip(dot_product / magnitude_product, -1.0, 1.0))) if magnitude_product != 0 else 0
            angles.append(int(np.clip(angle_deg, 0, 180)))
        return angles

    def calculate_thumb_angle(self, landmarks, width, height):
        joint_0 = np.array([landmarks.landmark[0].x * width, landmarks.landmark[0].y * height])
        joint_1 = np.array([landmarks.landmark[1].x * width, landmarks.landmark[1].y * height])
        joint_2 = np.array([landmarks.landmark[2].x * width, landmarks.landmark[2].y * height])
        joint_3 = np.array([landmarks.landmark[3].x * width, landmarks.landmark[3].y * height])
        joint_4 = np.array([landmarks.landmark[4].x * width, landmarks.landmark[4].y * height])

        res_vec1 = joint_2 - joint_4
        res_vec2 = joint_2 - joint_0

        dot_product = np.dot(res_vec1, res_vec2)
        magnitude_product = np.linalg.norm(res_vec1) * np.linalg.norm(res_vec2)
        angle = np.degrees(np.arccos(np.clip(dot_product / magnitude_product, -1.0, 1.0))) if magnitude_product != 0 else 0
        servo_angle = np.interp(angle, [0, 180], [0, 90])
        return int(np.clip(servo_angle - 20, 0, 90))

    def process_hand_data(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5).process(frame_rgb)
        height, width = frame.shape[:2]
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                angles = self.get_finger_angles(hand_landmarks, width, height)
                thumb_servo_angle = self.calculate_thumb_angle(hand_landmarks, width, height)
                if self.arduino:
                    try:
                        data = ",".join(map(str, angles)) + f",{int(thumb_servo_angle)}\n"
                        self.arduino.write(data.encode())
                        time.sleep(0.1)
                        while self.arduino.in_waiting:
                            received = self.arduino.readline().decode().strip()
                    except:
                        pass
        return frame