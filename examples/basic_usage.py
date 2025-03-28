import cv2
from robotic_hand.hand_controller import HandController

def main():
    # Initialize the HandController
    controller = HandController(com_port="COM5")

    # Start capturing video
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process the frame to get hand landmarks and control the robotic hand
        controller.process_frame(frame)

        # Display the processed frame
        cv2.imshow("Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    controller.close()

if __name__ == "__main__":
    main()