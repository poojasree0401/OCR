import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import pytesseract
import cv2
import numpy as np

# Function to preprocess the image before OCR
def preprocess_image(image_path):
    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to convert the image to black and white
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Resize the image to fit within the GUI while maintaining aspect ratio
    max_height = 400
    scale_factor = max_height / image.shape[0]
    resized = cv2.resize(threshold, None, fx=scale_factor, fy=scale_factor)

    return resized

# Function to perform OCR on the preprocessed image
def perform_ocr():
    # Get the path of the selected image
    image_path = image_path_var.get()
    if image_path:
        try:
            # Preprocess the image
            preprocessed_image = preprocess_image(image_path)

            # Perform OCR using pytesseract
            text = pytesseract.image_to_string(preprocessed_image)
            output_text.delete(1.0, tk.END)  # Clear previous text
            output_text.insert(tk.END, text)  # Insert new text
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {e}")
    else:
        messagebox.showwarning("Warning", "Please select an image first.")

# Function to handle image selection
def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        # Display selected image in the GUI
        image_path_var.set(file_path)
        img = Image.open(file_path)
        img.thumbnail((400, 400))  # Resize image to fit in GUI
        img = ImageTk.PhotoImage(img)
        image_label.config(image=img)
        image_label.image = img
    else:
        messagebox.showwarning("Warning", "No image selected.")

# Create the main GUI window
root = tk.Tk()
root.title("OCR GUI")

# Set the minimum size of the GUI window
root.minsize(800, 600)  # Width x Height

# Variables
image_path_var = tk.StringVar()

# GUI Layout
image_select_button = tk.Button(root, text="Select Image", command=select_image)
image_select_button.pack(pady=10)

image_frame = tk.Frame(root)
image_frame.pack()

image_label = tk.Label(image_frame)
image_label.pack()

ocr_button = tk.Button(root, text="Perform OCR", command=perform_ocr)
ocr_button.pack(pady=10)

output_label = tk.Label(root, text="Output Text:")
output_label.pack()

# Text widget to display output text with scrolling
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=10)  # Moderate initial height
output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Fill both x and y directions with padding

# Run the GUI application loop
root.mainloop()

