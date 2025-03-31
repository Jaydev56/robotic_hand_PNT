import os
import logging
import time
import serial
import asyncio
import numpy as np
import cv2
import mediapipe as mp
import socket


# Suppress TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('absl').setLevel(logging.ERROR)

class HandController:
    def __init__(self, com_port, resolution=(1080, 720), socket_host="127.0.0.1", socket_port=12345):
        self.resolution = resolution
        self.socket_host = socket_host
        self.socket_port = socket_port
        self.arduino = self.connect_arduino(com_port)

        # Initialize Mediapipe Hand Tracking
        self.mp_hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def connect_arduino(self, com):
        """Connect to Arduino via Serial."""
        try:
            arduino = serial.Serial(port=com, baudrate=9600, timeout=1)
            time.sleep(2)
            print(f"Connected to Arduino on {com}")
            return arduino
        except serial.SerialException as e:
            print(f"Error connecting to Arduino: {e}")
            return None

    def get_finger_angles(self, landmarks, width, height):
        """Calculate angles for fingers."""
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

    def process_hand_data(self, frame):
        """Detect hand and calculate angles."""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.mp_hands.process(frame_rgb)
        height, width = self.resolution

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
                angles = self.get_finger_angles(hand_landmarks, width, height)

                if self.arduino:
                    try:
                        data = ",".join(map(str, angles)) + "\n"
                        self.arduino.write(data.encode())
                        time.sleep(0.1)
                    except Exception as e:
                        print(f"Error communicating with Arduino: {e}")

        return cv2.resize(frame, self.resolution)

    def receive_ble_data(self):
        """Receive BLE data via socket."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.socket_host, self.socket_port))
            print(f"Connected to BLE data socket at {self.socket_host}:{self.socket_port}")
            while True:
                data = s.recv(1024).decode()
                if data:
                    print(f"Received BLE data: {data}")
                    try:
                        # Parse sensor values
                        sensor_values = list(map(float, data.split(',')))
                        print(f"Parsed Sensor Values: {sensor_values}")
                    except ValueError:
                        print("Error parsing sensor values.")

    def run(self):
        """Main loop to capture video and process hand tracking."""
        cap = cv2.VideoCapture(0)
        cap.set(3, self.resolution[0])
        cap.set(4, self.resolution[1])

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            processed_frame = self.process_hand_data(frame)
            cv2.imshow("Hand Tracking", processed_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

# Example Usage
if __name__ == "__main__":
    controller = HandController(com_port="COM3")
    controller.run()
