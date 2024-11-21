import cv2
import glob
import os

# Ask user for the folder path containing the images
folder_path = input("Please enter the path to the folder containing the images: ")

# Verify that the folder path exists
if not os.path.exists(folder_path):
    print("The specified folder does not exist. Please check the path and try again.")
else:
    # Create a new folder to save grayscale images
    output_folder = os.path.join(folder_path, "grayscale_images")
    os.makedirs(output_folder, exist_ok=True)

    # Process each image in the specified folder
    for image_path in glob.glob(os.path.join(folder_path, "*.jpg")):  # Adjust extension if needed
        # Read the image
        image = cv2.imread(image_path)
        
        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Get the image filename and save the grayscale version
        image_name = os.path.basename(image_path)
        gray_image_path = os.path.join(output_folder, f"gray_{image_name}")
        cv2.imwrite(gray_image_path, gray_image)

        print(f"Converted {image_name} to grayscale and saved to {gray_image_path}")

    print("All images have been processed and saved in the 'grayscale_images' folder.")
