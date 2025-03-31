import cv2
import asyncio  # Import asyncio for handling async functions
from robotic_hand_PNT.robotic_hand.hand_controller import HandController

def main():
    controller = HandController(com_port="COM3", resolution=(1080, 720))


    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open the camera.")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            processed_frame = controller.process_hand_data(frame)

            cv2.imshow("Hand Tracking", processed_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        # controller.close()  # Uncomment if a close method is implemented


    

if __name__ == "__main__":
    main()
