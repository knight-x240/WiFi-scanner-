import cv2
import pygame
from pyzbar.pyzbar import decode
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 640, 480
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("QR Code Scanner")

def decode_qr_code_from_image(image):
    decoded_objects = decode(image)
    for obj in decoded_objects:
        print("Type:", obj.type)
        print("Data:", obj.data.decode("utf-8"))

def decode_qr_code_from_camera():
    # Capture video from the default camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame.")
            break

        # Decode the QR code from the frame
        decode_qr_code_from_image(frame)

        # Convert the frame to a format suitable for Pygame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame)
        frame = pygame.transform.rotate(frame, -90)
        frame = pygame.transform.flip(frame, True, False)

        # Display the frame in the Pygame window
        window.blit(frame, (0, 0))
        pygame.display.update()

        # Exit on pressing 'q'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    cap.release()
                    pygame.quit()
                    return

def decode_qr_code_from_import():
    # Open a file dialog to select an image file
    Tk().withdraw()  # We don't want a full GUI, so keep the root window from appearing
    image_path = askopenfilename()

    if image_path:
        image = cv2.imread(image_path)
        if image is not None:
            decode_qr_code_from_image(image)
        else:
            print("Error: Could not open image.")
    else:
        print("No file selected.")

if __name__ == "__main__":
    choice = input("Enter '1' to scan from image, '2' to scan from camera, or '3' to import image: ")

    if choice == '1':
        image_path = input("Enter the path to the QR code image: ")
        image = cv2.imread(image_path)
        if image is not None:
            decode_qr_code_from_image(image)
        else:
            print("Error: Could not open image.")
    elif choice == '2':
        decode_qr_code_from_camera()
    elif choice == '3':
        decode_qr_code_from_import()
    else:
        print("Invalid choice. Please enter '1', '2', or '3'.")