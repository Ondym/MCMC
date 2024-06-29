import cv2

def qr_to_list(image_path):
    qr_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if qr_image is None:
        raise ValueError("Image not found or unable to load.")

    _, binary_image = cv2.threshold(qr_image, 128, 255, cv2.THRESH_BINARY)

    binary_list = (binary_image // 255).tolist()
    
    return binary_list

image_path = 'QR.png'
binary_list = qr_to_list(image_path)

for row in binary_list:
    print(row)
