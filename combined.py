import face_recognition
import cv2
import numpy as np

# Get a reference to webcam #0 (the default one)
c1 = cv2.VideoCapture(1)  # facial
c2 = cv2.VideoCapture(0)  # object

# FACIAL RECOGNITION VARIABLES ===============
yuxi_image = face_recognition.load_image_file("yuxi.jpg")
yuxi_face_encoding = face_recognition.face_encodings(yuxi_image)[0]

fei_image = face_recognition.load_image_file("fei.jpg")
fei_face_encoding = face_recognition.face_encodings(fei_image)[0]

known_face_encodings = [yuxi_face_encoding, fei_face_encoding]
known_face_names = ["Yuxi Qin", "Fei Xe"]

face_locations = []
face_encodings = []
face_names = []

# VARIABLES FOR DISH TRACKING ====================
# dish_status = [False, False, False]
user_dishes = [{}, {}]
cnt = 0
user = -1


def get_contours(frame):
    global user_dishes, user
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convert the frame to the HSV color space

    lower_red = np.array([0, 100, 20])
    upper_red = np.array([10, 255, 255])
    lower_blue = np.array([98, 50, 50])
    upper_blue = np.array([140, 255, 255])
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    # Create masks for each color
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    combined_mask = cv2.bitwise_or(mask_red, cv2.bitwise_or(mask_blue, mask_yellow))
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    big_contour = None
    largest_area = 0
    object_colour = None

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > largest_area:
            largest_area = area
            big_contour = contour
            if np.max(mask_red[contour[:, :, 1], contour[:, :, 0]]) == 255:
                object_colour = "red"
            elif np.max(mask_blue[contour[:, :, 1], contour[:, :, 0]]) == 255:
                object_colour = "blue"
            elif np.max(mask_yellow[contour[:, :, 1], contour[:, :, 0]]) == 255:
                object_colour = "yellow"

    if big_contour is not None:
        # Get the bounding rectangle for the largest red object
        x, y, w, h = cv2.boundingRect(big_contour)
        center_x = x + w // 2

        # Draw a bounding box around the object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Indicate the direction (left or right) of the object
        frame_width = frame.shape[1]

        if center_x > frame_width // 2:
            if user_dishes[user].get(object_colour) is not None:
                user_dishes[user][object_colour][2] = True
            else:
                user_dishes[user][object_colour] = [False, False, True]
                print(known_face_names[user], "placed the dirty", object_colour, "dish in the sink")
        else:
            if user_dishes[user].get(object_colour) is not None:
                user_dishes[user][object_colour][1] = True
            else:
                user_dishes[user][object_colour] = [False, True, False]

    if big_contour is None:
        x, y, w, h = cv2.boundingRect(big_contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        for dish_colour in user_dishes[user]:
            if user_dishes[user][dish_colour] == [False, True, True]:
                user_dishes[user][dish_colour] = [True, True, True]
                print("the", object_colour, "dish was washed by", known_face_names[user])

    cv2.imshow('Largest Contour Detection', frame)
    return


def get_user(frame):
    global face_locations, face_encodings, user

    small_frame = cv2.resize(frame, (1280, 720))
    rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])  # convert from bgr to rgb

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        # see if there are any matches
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # just use the first match that you find
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            user = first_match_index
            print("we see", name)
    return


while True:
    ret1, frame1 = c1.read()
    ret2, frame2 = c2.read()

    if not ret1 or not ret2:
        break

    # Only process every other frame of video to save time
    if cnt % 5 == 0:
        get_user(frame2)
        get_contours(frame1)

    cnt += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):  # q to exit
        break

c1.release()
c2.release()
cv2.destroyAllWindows()
