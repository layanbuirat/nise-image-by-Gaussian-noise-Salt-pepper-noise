import cv2
import numpy as np
import os

# Ask user for input folder path and specify output folders
input_folder = input("Enter the path to the folder containing clear image: ").strip()
input_folder = input_folder.replace("\\", "/")  # Replace backslashes with forward slashes

output_folder_gaussian = os.path.join(input_folder, "gaussian_noise_images")
output_folder_salt_pepper = os.path.join(input_folder, "salt_and_pepper_noise_images")

# Create output folders if they don't exist
os.makedirs(output_folder_gaussian, exist_ok=True)
os.makedirs(output_folder_salt_pepper, exist_ok=True)

# Function to add noise to images
def add_noise(img, noise_type="gaussian", intensity=0.1):
    noisy_img = img.copy()
    if noise_type == "gaussian":
        mean = 0
        sigma = intensity * 255
        gaussian_noise = np.random.normal(mean, sigma, img.shape)
        noisy_img = np.clip(img + gaussian_noise, 0, 255).astype(np.uint8)
    elif noise_type == "salt_and_pepper":
        prob = intensity
        salt_pepper_noise = np.random.rand(*img.shape)
        noisy_img[salt_pepper_noise < prob / 2] = 0
        noisy_img[salt_pepper_noise > 1 - prob / 2] = 255
    return noisy_img

# Loop through each image in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (256, 256))  # Optional resize for consistency

        # Add Gaussian noise and Salt-and-Pepper noise
        noisy_image_gaussian = add_noise(img, noise_type="gaussian", intensity=0.1)
        noisy_image_salt_pepper = add_noise(img, noise_type="salt_and_pepper", intensity=0.05)
        
        # Save noisy images to respective output folders
        output_path_gaussian = os.path.join(output_folder_gaussian, f"gaussian_{filename}")
        output_path_salt_pepper = os.path.join(output_folder_salt_pepper, f"salt_pepper_{filename}")
        
        cv2.imwrite(output_path_gaussian, noisy_image_gaussian)
        cv2.imwrite(output_path_salt_pepper, noisy_image_salt_pepper)
        
        print(f"Processed and saved {filename} with Gaussian and Salt-and-Pepper noise.")
# All images processed and saved to the respective folders
print("All images processed and saved to the respective folders.")

