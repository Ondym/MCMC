from PIL import Image, ImageDraw, ImageFont
import os

# Define the color and font
rectangle_color = '#BCE3FF'
text_color = 'black'
font_path = 'arial.ttf'  # Update with the path to Arial font if necessary

def process_images(folder_path):
    # Get all image files in the specified directory
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg'))]

    for image_file in image_files:
        # Open the image
        img_path = os.path.join(folder_path, image_file)
        img = Image.open(img_path)
        draw = ImageDraw.Draw(img)
        
        # Define the rectangle position and size
        rect_x, rect_y = 0, 0
        rect_width, rect_height = 140, 70
        
        # Draw the rectangle
        draw.rectangle([rect_x, rect_y, rect_x + rect_width, rect_y + rect_height], fill=rectangle_color)
        
        # Get the file name without extension and remove trailing zeros
        base_name = os.path.splitext(image_file)[0].rstrip('0')
        base_name = base_name.rstrip('.')
        text = f"T={base_name}"
        
        # Load the font
        try:
            font = ImageFont.truetype(font_path, 35)
        except IOError:
            font = ImageFont.load_default()
        
        # Calculate text position
        text_x = rect_x + 15
        text_y = rect_y + (rect_height - font.getsize(text)[1]) // 2 - 5
        
        # Draw the text
        draw.text((text_x, text_y), text, fill=text_color, font=font)
        
        # Save the image
        output_path = os.path.join(folder_path, f"processed_{image_file}")
        img.save(output_path)
        print(f"Processed {image_file}")

# Specify the folder path
folder_path = 'GIF'  # Replace with your folder path

# Run the function
process_images(folder_path)
