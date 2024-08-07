# import cv2
# import numpy as np

# def selective_image_extraction(frame):
#     # Convert the frame to grayscale
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Apply a threshold to obtain a binary image
#     _, binary_mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

#     # Apply morphological operations to remove small noise
#     kernel = np.ones((5, 5), np.uint8)
#     opening = cv2.morphologyEx(binary_mask, cv2.MORPH_OPEN, kernel, iterations=2)

#     # Invert the binary mask to get the background
#     background = cv2.bitwise_not(opening)

#     # Extract the user by bitwise AND operation with the original frame
#     result = cv2.bitwise_and(frame, frame, mask=background)

#     return result

# def capture_and_process_video():
#     # Open the camera
#     cap = cv2.VideoCapture(0)

#     while True:
#         # Read a frame from the camera
#         ret, frame = cap.read()

#         # If frame read is unsuccessful, break the loop
#         if not ret:
#             break

#         # Apply Selective Image Extraction
#         processed_frame = selective_image_extraction(frame)

#         # Display the original and processed frames
#         cv2.imshow('Original Frame', frame)
#         cv2.imshow('Selective Image Extraction', processed_frame)

#         # Break the loop when 'q' is pressed
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     # Release the camera and close all windows
#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     capture_and_process_video()
