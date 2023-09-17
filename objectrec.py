import cv2
import numpy as np
  
cap1 = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(2)
  
while 1:
    ret1,frame1 =cap1.read()
    ret2,frame2 =cap2.read()
    # ret will return a true value if the frame exists otherwise False
    into_hsv1 =cv2.cvtColor(frame1,cv2.COLOR_BGR2HSV)
    into_hsv2 =cv2.cvtColor(frame2,cv2.COLOR_BGR2HSV)
    # changing the color format from BGr to HSV 
    # This will be used to create the mask
    blue_L_limit=np.array([98,50,50]) # setting the blue lower limit
    blue_U_limit=np.array([139,255,255]) # setting the blue upper limit

    yellow_L_limit=np.array([20, 100, 100]) # setting the yellow lower limit
    yellow_U_limit=np.array([30, 255, 255]) # setting the yellow upper limit

    red_L_limit=np.array([0, 100, 20]) # setting the red lower limit
    red_U_limit=np.array([10, 255, 255]) # setting the red upper limit

    b_mask=cv2.inRange(into_hsv1,blue_L_limit, blue_U_limit)
    y_mask=cv2.inRange(into_hsv1,yellow_L_limit, yellow_U_limit)
    r_mask=cv2.inRange(into_hsv2,red_L_limit, red_U_limit)
    # creating the mask using inRange() function
    # this will produce an image where the color of the objects
    # falling in the range will turn white and rest will be black
    blue=cv2.bitwise_and(frame1,frame1,mask=b_mask)
    yellow=cv2.bitwise_and(frame1,frame1,mask=y_mask)
    red=cv2.bitwise_and(frame2,frame2,mask=r_mask)
    # this will give the color to mask.
    #cv2.imshow('Original',frame) # to display the original frame
    cv2.imshow('Blue Detector',blue) # to display the blue object output
    cv2.imshow('Red Detector',red) # to display the blue object output
    #cv2.imshow('Yellow Detector',yellow) # to display the blue object output
  
    if cv2.waitKey(1)==27:
        break
    # this function will be triggered when the ESC key is pressed
    # and the while loop will terminate and so will the program
cap.release()
  
cv2.destroyAllWindows()
