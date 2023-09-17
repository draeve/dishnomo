import cv2
import numpy as np

# Initialize the video capture device (0 for default camera, or provide the video file path)
cap = cv2.VideoCapture(1)

dish_status = [False, False, False]
cnt = 0
while True:
    if cnt % 5 == 0:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to the HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define the lower and upper bounds for the red color in HSV
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])

        # Create a mask to isolate red pixels
        mask1 = cv2.inRange(hsv, lower_red, upper_red)

        # Define the lower and upper bounds for the red color (wrap-around hue) in HSV
        lower_red = np.array([160, 100, 100])
        upper_red = np.array([180, 255, 255])

        # Create a mask to isolate red pixels (wrap-around hue)
        mask2 = cv2.inRange(hsv, lower_red, upper_red)

        # Combine the masks to detect red in both ranges
        mask = mask1 + mask2

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Initialize variables to track the largest red object
        largest_area = 0
        largest_contour = None

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > largest_area and area > 50000:
                largest_area = area
                largest_contour = contour



    print(dish_status)
    cv2.imshow("Largest Red Object Detection", frame)
    cnt += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture device and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
