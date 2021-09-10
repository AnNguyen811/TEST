import cv2
import os
import pickle

if not os.path.exists('./calibration.pckl'):
    print('you need to calibrate')
    exit()
else:
    f = open('calibration.pckl', 'rb')
    cameraMatrix ,  distCoeffs = pickle.load(f)
    f.close()
    if cameraMatrix is None or distCoeffs is None:
        print(" calibration issue. remove")
        exit()
aruco_dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_7X7_250)
parameters = cv2.aruco.DetectorParameters_create()

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgpoints = cv2.aruco.detectMarkers(gray_frame, aruco_dictionary, parameters=parameters)
    frame = cv2.aruco.drawDetectedMarkers(image=frame, corners=corners,ids= ids, borderColor=(0,255,0))
    frame = cv2.aruco.drawDetectedMarkers(image= frame, corners= rejectedImgpoints, borderColor=(0,0,255))
    if ids is not None:
        rvecs, tvecs, _ =cv2.aruco.estimatePoseSingleMarkers(corners, 1 , cameraMatrix, distCoeffs)
        for rvec, tvec in zip(rvecs, tvecs):
            cv2.aruco.drawAxis(frame, cameraMatrix, distCoeffs, rvec, tvec, 1)
    cv2.imshow('frame', frame)
    cv2.waitKey(10)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.waitKey()
cv2.destroyAllwindows()
            
