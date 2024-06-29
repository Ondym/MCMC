import os
import shutil
import tkinter as tk
from PIL import Image, ImageTk

def display_images(subdir, images, filenames):
    """
    Display images in a maximized tkinter window with wrapping and labels.
    """
    result = {"choice": None}  # Dictionary to hold the result

    def delete():
        result["choice"] = "delete"
        root.quit()

    def keep():
        result["choice"] = "keep"
        root.quit()

    root = tk.Tk()
    root.title("Image Viewer")
    root.state('zoomed')  # Maximize the window

    # Create a frame for the images
    frame = tk.Frame(root)
    frame.pack(expand=True, fill=tk.BOTH)
    
    # Display subdirectory name at the top center
    subdir_label = tk.Label(frame, text=subdir, font=("Arial", 24))
    subdir_label.pack()

    # Create a canvas to allow scrolling
    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a scrollbar
    scrollbar = tk.Scrollbar(frame, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create another frame inside the canvas
    image_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=image_frame, anchor='nw')

    # Load and display each image
    photos = []
    max_width = 150
    max_height = 150

    row, col = 0, 0
    for img, filename in zip(images, filenames):
        img.thumbnail((max_width, max_height))
        photo = ImageTk.PhotoImage(img)
        photos.append(photo)

        # Create frame for each image and its label
        img_container = tk.Frame(image_frame)
        img_container.grid(row=row, column=col, padx=5, pady=5)

        # Display image
        img_label = tk.Label(img_container, image=photo, borderwidth=0, highlightthickness=0)
        img_label.pack()

        # Display filename under the image
        file_label = tk.Label(img_container, text=os.path.splitext(filename)[0], font=("Arial", 12))
        file_label.pack()

        col += 1
        if col > (canvas.winfo_width() // max_width) - 1:
            col = 0
            row += 1

    # Add buttons for delete and keep
    btn_frame = tk.Frame(root)
    btn_frame.pack()
    button_font = ("Arial", 16)
    delete_btn = tk.Button(btn_frame, text="Delete", command=delete, width=10, height=2, font=button_font)
    keep_btn = tk.Button(btn_frame, text="Keep", command=keep, width=10, height=2, font=button_font)
    delete_btn.pack(side="left", padx=20)
    keep_btn.pack(side="right", padx=20)

    # Update the scrollregion of the canvas
    image_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

    root.mainloop()
    root.destroy()

    return result["choice"]

def process_subdirectories(directory):
    """
    Process each subdirectory in the given directory.
    """
    subdirectories = [os.path.join(directory, d) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

    for subdir in subdirectories:
        # Get all image files in the subdirectory and sort them alphabetically
        image_files = sorted([f for f in os.listdir(subdir) if f.lower().endswith(('png', 'jpg', 'jpeg'))])
        
        # Load all images
        images = [Image.open(os.path.join(subdir, img)) for img in image_files]

        # Display images and get user choice
        choice = display_images(os.path.basename(subdir), images, image_files)
        
        # Handle user choice
        if choice == "delete":
            # Delete the subdirectory and its contents
            shutil.rmtree(subdir)
            print(f"Deleted {subdir}")
        else:
            print(f"Kept {subdir}")

# Example usage
directory_path = 'images-day2'  # Replace with your directory path
process_subdirectories(directory_path)
