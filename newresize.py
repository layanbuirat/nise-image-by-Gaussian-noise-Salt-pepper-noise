import os
import cv2
import glob
from multiprocessing import Pool, cpu_count

# Function to resize a single image
def resize_image(args):
    image_path, target_size, output_folder = args
    try:
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Warning: Could not open image file '{image_path}'. Skipping.")
            return

        # Resize the image
        resized_image = cv2.resize(image, target_size)

        # Save the resized image in the output folder
        image_name = os.path.basename(image_path)
        resized_image_path = os.path.join(output_folder, image_name)
        cv2.imwrite(resized_image_path, resized_image)
        print(f"Resized and saved '{image_name}' to '{resized_image_path}'")
    except Exception as e:
        print(f"Error processing image '{image_path}': {e}")

# Function to collect all image paths from a folder and its subfolders
def collect_image_paths(folder_path):
    image_paths = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp")):
                image_paths.append(os.path.join(root, file))
    return image_paths

# Main processing function
def process_images_in_folder(main_folder_path, target_size):
    # Collect all image paths
    image_paths = collect_image_paths(main_folder_path)
    print(f"Found {len(image_paths)} images in '{main_folder_path}'")

    # Create output folders dynamically
    args_list = []
    for image_path in image_paths:
        output_folder = os.path.join(os.path.dirname(image_path), "resized_images")
        os.makedirs(output_folder, exist_ok=True)
        args_list.append((image_path, target_size, output_folder))

    # Use multiprocessing for faster processing
    with Pool(processes=cpu_count()) as pool:
        pool.map(resize_image, args_list)

# Get input from the user
if __name__ == "__main__":
    main_folder_path = input("Enter the path for the main folder: ")
    if not os.path.exists(main_folder_path):
        print(f"Error: The folder '{main_folder_path}' does not exist.")
        exit()

    target_width = int(input("Enter the target width for resizing (e.g., 256): "))
    target_height = int(input("Enter the target height for resizing (e.g., 256): "))
    target_size = (target_width, target_height)

    process_images_in_folder(main_folder_path, target_size)
    print("All images have been resized successfully.")
