import os
from ultralytics import YOLO

# Load the YOLOv8m model
model = YOLO("yolov8m.pt")

# Verify the model is loaded
print("Model loaded successfully!")

# Paths for source and destination folders
source_folder = "./source"
destination_folder = "./destination2"

# Create the destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

# Iterate over all files in the source folder
for file_name in os.listdir(source_folder):
    file_path = os.path.join(source_folder, file_name)

    # Ensure only image files are processed
    if not file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        print(f"Skipping non-image file: {file_name}")
        continue

    print(f"Processing image: {file_name}")
    # Perform inference
    results = model(file_path, conf=0.5)

    # Save results
    for result in results:
        save_path = os.path.join(destination_folder, file_name)  # Save with the same name in the destination folder
        annotated_image = result.plot()  # Get the annotated image as a numpy array
        import cv2  # Ensure OpenCV is available
        cv2.imwrite(save_path, annotated_image)  # Save the annotated image
        print(f"Saved: {save_path}")
