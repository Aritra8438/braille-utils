import base64
from flask import Flask, request, jsonify, render_template, Response
from utils.braille_to_text import braille_to_text
from utils.text_to_braille import text_to_braille
from utils.image_to_braille import image_to_braille
from utils.braille_image_to_text import braille_image_to_text
import json
import logging
import os

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def render_home():
    logging.info("Accessed endpoint: / (render_home)")
    if request.method == "GET":
        return render_template("index.html")
    return jsonify({"error": "Method not allowed"}), 405


@app.route("/braille-to-text-api", methods=["GET"])
def api_braille_to_text():
    logging.info("Accessed endpoint: /braille-to-text-api (api_braille_to_text)")
    if request.method == "GET":
        braille_input = request.args.get("braille_input")
        return (
            jsonify(
                {
                    "text_output": braille_to_text(braille_input),
                }
            ),
            200,
        )
    return jsonify({"error": "Method not allowed"}), 405


@app.route("/braille-to-text", methods=["GET"])
def render_braille_to_text():
    logging.info("Accessed endpoint: /braille-to-text (render_braille_to_text)")
    if request.method == "GET":
        return render_template("braille_to_text.html")
    return jsonify({"error": "Method not allowed"}), 405


@app.route("/text-to-braille-api", methods=["GET"])
def api_text_to_braille():
    logging.info("Accessed endpoint: /text-to-braille-api (api_text_to_braille)")
    if request.method == "GET":
        text_input = request.args.get("text_input")
        return Response(
            json.dumps(
                {"braille_output": text_to_braille(text_input)}, ensure_ascii=False
            ),
            content_type="application/json",
        )
    return jsonify({"error": "Method not allowed"}), 405


@app.route("/text-to-braille", methods=["GET"])
def render_text_to_braille():
    logging.info("Accessed endpoint: /text-to-braille (render_text_to_braille)")
    if request.method == "GET":
        return render_template("text_to_braille.html")
    return jsonify({"error": "Method not allowed"}), 405


@app.route("/about", methods=["GET"])
def render_about():
    logging.info("Accessed endpoint: /about (render_about)")
    if request.method == "GET":
        return render_template("about.html")
    return jsonify({"error": "Method not allowed"}), 405


@app.route("/text-image-to-braille-api", methods=["POST"])
def api_image_to_braille():
    logging.info("Accessed endpoint: /text-image-to-braille-api (api_image_to_braille)")
    if request.method == "POST":
        if "image" not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files["image"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        image_path = f"uploads/{file.filename}"
        file.save(image_path)
        logging.info(f"File {file.filename} successfully saved to {image_path}")

        text_output, braille_output = image_to_braille(image_path)

        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        encoded_image = base64.b64encode(image_data).decode("utf-8")
        os.remove(image_path)
        return (
            jsonify(
                {
                    "braille_output": braille_output,
                    "text_output": text_output,
                    "image": encoded_image,
                }
            ),
            200,
        )
    return jsonify({"error": "Method not allowed"}), 405


@app.route("/text-image-to-braille", methods=["GET"])
def render_image_to_braille():
    logging.info("Accessed endpoint: /text-image-to-braille (render_image_to_braille)")
    if request.method == "GET":
        return render_template("text_image_to_braille.html")
    return jsonify({"error": "Method not allowed"}), 405


@app.route("/braille-image-to-text-api", methods=["POST"])
def api_braille_image_to_text():
    logging.info(
        "Accessed endpoint: /braille-image-to-text-api (api_braille_image_to_text)"
    )
    if request.method == "POST":
        if "image" not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files["image"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        image_path = f"uploads/{file.filename}"
        file.save(image_path)
        logging.info(f"File {file.filename} successfully saved to {image_path}")

        braille_output, text_output = braille_image_to_text(image_path)

        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        encoded_image = base64.b64encode(image_data).decode("utf-8")
        os.remove(image_path)
        return (
            jsonify(
                {
                    "braille_output": braille_output,
                    "text_output": text_output,
                    "image": encoded_image,
                }
            ),
            200,
        )
    return jsonify({"error": "Method not allowed"}), 405


@app.route("/braille-image-to-text", methods=["GET"])
def render_braille_image_to_text():
    logging.info(
        "Accessed endpoint: /braille-image-to-text (render_braille_image_to_text)"
    )
    if request.method == "GET":
        return render_template("braille_image_to_text.html")
    return jsonify({"error": "Method not allowed"}), 405


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
