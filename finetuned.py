import os
import cv2
from ultralytics import YOLO

# Load the models
car_model = YOLO("best.pt")        # Model for detecting cars
general_model = YOLO("yolov8m.pt") # Model for detecting all other objects

# Verify models are loaded
print("Models loaded successfully!")

# Paths for source and destination folders
source_folder = "./source"
destination_folder = "./results"

# Create the destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

# Helper function to get the class ID for a given class name
def get_class_id(model, class_name):
    return next((cls_id for cls_id, name in model.names.items() if name == class_name), None)

# Get the class ID for "car"
car_class_id = get_class_id(car_model, "car")
if car_class_id is None:
    raise ValueError("The 'c ar' class was not found in the car_model's names dictionary.")

# Iterate over all files in the source folder
for file_name in os.listdir(source_folder):
    file_path = os.path.join(source_folder, file_name)

    # Ensure only image files are processed
    if not file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        print(f"Skipping non-image file: {file_name}")
        continue

    print(f"Processing image: {file_name}")
    
    # Run inference on both models
    car_results = car_model(file_path, conf=0.5)
    general_results = general_model(file_path, conf=0.5)

    # Merge results
    final_boxes = []
    for result in car_results:
        for box in result.boxes:
            # Check if the class is "car"
            if int(box.cls.item()) == car_class_id:  # Match class ID for "car"
                final_boxes.append(box)  # Add car detections

    for result in general_results:
        for box in result.boxes:
            # Add all detections except for cars
            if int(box.cls.item()) != car_class_id:  # Exclude "car" class
                final_boxes.append(box)

    # Annotate the image with the final boxes
    image = cv2.imread(file_path)
    for box in final_boxes:
        # Extract box data
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        class_id = int(box.cls.item())
        confidence = box.conf.item()
        class_name = general_model.names[class_id]  # Use names from the general model
        
        # Draw the box on the image
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, f"{class_name} {confidence:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Save the annotated image
    save_path = os.path.join(destination_folder, file_name)
    cv2.imwrite(save_path, image)
    print(f"Saved: {save_path}")
