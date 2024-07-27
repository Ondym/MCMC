import os
import cv2
import numpy as np
from PIL import Image

def create_heatmap_mp4_from_pngs(folder_path, output_mp4_path, frame_rate=30, history_length=20):
    # Get all PNG files in the folder
    png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
    
    # Sort the files by name
    png_files.sort()
    png_files.reverse()

    if not png_files:
        print("No PNG files found in the specified folder.")
        return

    # Load images to get the size
    first_image = Image.open(os.path.join(folder_path, png_files[0]))
    frame_size = first_image.size
    first_image.close()
    
    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for mp4
    video_writer = cv2.VideoWriter(output_mp4_path, fourcc, frame_rate, frame_size)

    # Initialize a list to keep track of the last 20 frames
    history = []
    change_counts = np.zeros(frame_size, dtype=np.int32)
    
    for i, file in enumerate(png_files):
        img_path = os.path.join(folder_path, file)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        
        if img is None:
            continue

        # Convert the image to binary (0, 255)
        _, binary_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        
        if len(history) >= history_length:
            old_img = history.pop(0)
            change_counts -= (old_img != history[0]).astype(np.int32)
        
        if history:
            change_counts += (binary_img != history[-1]).astype(np.int32)
        
        history.append(binary_img)
        
        # Normalize change counts to a scale of 0 to 255
        normalized_changes = cv2.normalize(change_counts, None, 0, 255, cv2.NORM_MINMAX)
        
        # Convert normalized changes to a color image
        heatmap_color = cv2.applyColorMap(normalized_changes.astype(np.uint8), cv2.COLORMAP_JET)
        
        # Write the frame to the video
        video_writer.write(heatmap_color)
    
    video_writer.release()

timestamp = input("Time of folder creation: ")
folder_path = 'images/anim_' + timestamp  # replace with the path to your folder
output_mp4_path = 'presentation-prep/anim_HI.mp4'     # replace with the desired output GIF path
create_heatmap_mp4_from_pngs(folder_path, output_mp4_path)


# Example usage
