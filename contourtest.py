import cv2
import numpy as np

# Initialize the video capture device (0 for default camera, or provide the video file path)
cap = cv2.VideoCapture(1)
previous_state = ["", 0] # [ dish region (left or right), largest_contour ]

while True:
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

    if( previous_state[0] == "left" and previous_state[1] is not None ):
        print("dish was WASHED (left)")
    elif (previous_state[1] == "right" and previous_state[1] is None):
        print("dish was PLACED (right)")

    if largest_contour is not None:
        print(cv2.contourArea(largest_contour))
        # Get the bounding rectangle for the largest red object
        x, y, w, h = cv2.boundingRect(largest_contour)
        center_x = x + w // 2

        # Draw a bounding box around the object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Indicate the direction (left or right) of the object
        frame_width = frame.shape[1]
        if center_x < frame_width // 2:
            previous_state = [ "left", largest_contour]
        else:
            previous_state = [ "right", largest_contour]
            #cv2.putText(frame, direction_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame with bounding box and direction
    cv2.imshow("Largest Red Object Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture device and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
