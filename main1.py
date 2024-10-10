import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def add_texture_to_outline(image_path, texture_path):
    # Load the image and texture
    img = cv2.imread(image_path)
    texture = cv2.imread(texture_path)

    # Check if the images were loaded successfully
    if img is None or texture is None:
        print("Error: Could not load image or texture.")
        return

    # Resize the image and texture for consistent processing
    img = cv2.resize(img, (600, 600))
    texture = cv2.resize(texture, (600, 600))

    # Convert to grayscale and create outline
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_img, threshold1=50, threshold2=150)

    # Create a blank image to draw contours
    outline_img = np.zeros_like(gray_img)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(outline_img, contours, -1, (255), thickness=1)

    # Convert outline image to color for blending
    outline_color = cv2.cvtColor(outline_img, cv2.COLOR_GRAY2BGR)

    # Blend the texture with the outline image
    blended = cv2.addWeighted(outline_color, 0.5, texture, 0.5, 0)

    # Display the original image, outline, and blended image
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.title("Original Image")
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.title("Outline Drawing")
    plt.imshow(outline_img, cmap='gray')
    plt.axis("off")
    
    plt.subplot(1, 3, 3)
    plt.title("Outline with Texture")
    plt.imshow(cv2.cvtColor(blended, cv2.COLOR_BGR2RGB))
    plt.axis("off")

    plt.tight_layout()
    plt.show()

def select_file(title):
    """Open a file dialog to select an image."""
    Tk().withdraw()  # Hide the root window
    filename = askopenfilename(title=title, filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
    return filename

# Select images using file dialogs
image_path = select_file("Select the main image")
texture_path = select_file("Select the texture image")

# Call the function with the selected paths
if image_path and texture_path:  # Ensure paths are valid
    add_texture_to_outline(image_path, texture_path)
else:
    print("No image or texture selected.")
