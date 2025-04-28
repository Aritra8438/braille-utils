import logging
from ultralytics import YOLO
import cv2
from utils.text_to_braille import text_to_braille

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Loading YOLO model...")
model = YOLO("./api/static/last.pt")


def process_overlapping_boxes(combined_results, iou_threshold=0.3):
    logging.info(
        "Called process_overlapping_boxes with IOU threshold: %s", iou_threshold
    )

    def calculate_iou(box1, box2):
        x1 = max(box1[0], box2[0])
        y1 = max(box1[1], box2[1])
        x2 = min(box1[2], box2[2])
        y2 = min(box1[3], box2[3])

        intersection = max(0, x2 - x1) * max(0, y2 - y1)
        area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
        area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
        union = area1 + area2 - intersection

        return intersection / union if union > 0 else 0

    combined_results.sort(key=lambda x: x[1], reverse=True)
    filtered_results = []

    for box, confidence, cls in combined_results:
        if all(
            calculate_iou(box, other_box[0]) < iou_threshold
            for other_box in filtered_results
        ):
            filtered_results.append((box, confidence, cls))

    logging.info(
        "Filtered overlapping boxes. Total boxes after filtering: %d",
        len(filtered_results),
    )
    return filtered_results


def detect_line_breaks_and_spaces(combined_result):
    logging.info("Called detect_line_breaks_and_spaces")
    if not combined_result:
        logging.info("No combined results provided. Returning empty string.")
        return ""

    remaining_boxes = combined_result.copy()
    lines = []

    while remaining_boxes:
        min_box_idx = min(
            range(len(remaining_boxes)),
            key=lambda i: remaining_boxes[i][0][0] + remaining_boxes[i][0][1],
        )

        min_box = remaining_boxes[min_box_idx][0]
        min_box_height = min_box[3] - min_box[1]
        min_box_width = min_box[2] - min_box[0]
        min_box_class = remaining_boxes[min_box_idx][2]

        current_line = [min_box_class]

        used_indices = [min_box_idx]

        potential_same_line = []
        for i, (box, _, cls) in enumerate(remaining_boxes):
            if i != min_box_idx:
                y_diff = abs(box[1] - min_box[1])
                if y_diff <= min_box_height * 0.5:
                    potential_same_line.append((i, box, cls))

        potential_same_line.sort(key=lambda x: x[1][0])

        prev_box = min_box
        for i, box, cls in potential_same_line:
            # Calculate horizontal distance between boxes
            distance = box[0] - prev_box[0]

            # Add space if distance is greater than 1.6 times min_box_width
            if distance > 1.6 * min_box_width:
                current_line.append(" ")

            current_line.append(cls)
            used_indices.append(i)
            prev_box = box

        for idx in sorted(used_indices, reverse=True):
            remaining_boxes.pop(idx)

        lines.append("".join(current_line))

    logging.info("Detected lines: %d", len(lines))
    return "\n".join(lines)


def braille_image_to_text(image_path, test=False):
    logging.info("Called braille_image_to_text with image path: %s", image_path)

    logging.info("Running YOLO model on the image...")
    results = model(image_path)

    logging.info("Processing YOLO results...")
    class_mapping = results[0].names
    boxes = [
        [int(element) for element in row] for row in results[0].boxes.xyxy.tolist()
    ]
    confidences = results[0].boxes.conf.tolist()
    classes = [class_mapping[int(cls)] for cls in results[0].boxes.cls.tolist()]
    combined_results = list(zip(boxes, confidences, classes))
    combined_result = process_overlapping_boxes(combined_results)

    logging.info("Annotating image with detected boxes...")
    image = cv2.imread(image_path)

    for box, _, cls in combined_result:
        x1, y1, x2, y2 = box
        label = cls
        thickness = 1

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), thickness)

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = (y2 - y1) / 100
        text_thickness = 1 if font_scale < 0.5 else 2
        text_size = cv2.getTextSize(label, font, font_scale, text_thickness)[0]
        text_x = x1
        text_y = y1 - 10 if y1 - 10 > 10 else y1 + 10
        cv2.rectangle(
            image,
            (text_x, text_y - text_size[1] - 10),
            (text_x + text_size[0] + 10, text_y),
            (0, 255, 0),
            -1,
        )
        cv2.putText(
            image,
            label,
            (text_x + 5, text_y - 5),
            font,
            font_scale,
            (0, 0, 0),
            text_thickness,
        )

    if test is False:
        cv2.imwrite(image_path, image)
    logging.info("Annotated image saved to: %s", image_path)

    logging.info("Detecting line breaks and spaces...")
    paragraphs = detect_line_breaks_and_spaces(combined_result)

    logging.info("Converting detected text to Braille...")
    braille_text = text_to_braille(paragraphs)

    logging.info("Braille conversion completed.")
    return braille_text, paragraphs
