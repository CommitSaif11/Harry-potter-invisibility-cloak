import cv2
'''if the code could not access the camera run this code and check 
whether it is accessible or not'''
cap = cv2.VideoCapture(0)  # Open webcam
if not cap.isOpened():
    print("Error: Could not access the webcam.")
else:
    print("Webcam is working.")
    cap.release()
