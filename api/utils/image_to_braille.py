import easyocr
from utils.text_to_braille import text_to_braille
import cv2
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def image_to_braille(image_path):
    logging.info(f"Starting image_to_braille function for image: {image_path}")

    reader = easyocr.Reader(["en"])
    logging.info("Initialized EasyOCR reader")

    image = cv2.imread(image_path)
    logging.info("Image loaded successfully")

    result = reader.readtext(image_path)
    logging.info(f"Text detection completed. Found {len(result)} text regions")

    for bbox, text, _ in result:
        (top_left, _, bottom_right, _) = bbox
        top_left = tuple(map(int, top_left))
        bottom_right = tuple(map(int, bottom_right))

        cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 1)
        logging.info(f"Drew rectangle for text: {text}")

        cv2.putText(
            image,
            text,
            (top_left[0], top_left[1] - 10),
            cv2.FONT_HERSHEY_COMPLEX,
            0.5,
            (0, 255, 0),
            1,
        )
        logging.info(f"Added text annotation: {text}")

    cv2.imwrite(image_path, image)
    logging.info(f"Annotated image saved to: {image_path}")

    text = " ".join([res[1] for res in result])
    logging.info(f"Extracted text: {text}")

    braille_text = text_to_braille(text)
    logging.info("Converted text to Braille")

    return text, braille_text
