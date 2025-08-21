import cv2

# Initialize camera (0 is default camera)
cap = cv2.VideoCapture(0)

while True:
    # Read frame from camera
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Display the frame
    cv2.imshow('Camera', frame)
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Camera', cv2.WND_PROP_VISIBLE) < 1:
       break

# Release camera and close windows
cap.release()
cv2.destroyAllWindows()