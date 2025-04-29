import io
from thefuzz import fuzz
import pytest
import os

def test_render_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_api_braille_to_text(client):
    response = client.get("/braille-to-text-api?braille_input=⠁")
    assert response.status_code == 200
    assert response.json["text_output"] == "a"


def test_render_braille_to_text(client):
    response = client.get("/braille-to-text")
    assert response.status_code == 200


def test_api_text_to_braille(client):
    response = client.get("/text-to-braille-api?text_input=a")
    assert response.status_code == 200
    assert response.json["braille_output"] == "⠁"


def test_render_text_to_braille(client):
    response = client.get("/text-to-braille")
    assert response.status_code == 200


def test_render_about(client):
    response = client.get("/about")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "image_path, expected_text, braille_text",
    [
        ("api/static/images/text-1.png", "Translation Hello! How are you doing?", "⠠⠞⠗⠁⠝⠎⠇⠁⠞⠊⠕⠝ ⠠⠓⠑⠇⠇⠕⠖ ⠠⠓⠕⠺ ⠁⠗⠑ ⠽⠕⠥ ⠙⠕⠊⠝⠛⠦⠇"),
    ],
)
def test_text_image_to_braille_api(client, image_path, expected_text, braille_text):
    with open(image_path, "rb") as img_file:
        img_bytes = img_file.read()
        data = {
            "image": (io.BytesIO(img_bytes), os.path.basename(image_path))
        }
        response = client.post("/text-image-to-braille-api", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    assert fuzz.ratio(response.json["text_output"].lower(), expected_text.lower()) > 80
    assert fuzz.ratio(response.json["braille_output"], braille_text) > 80


@pytest.mark.parametrize(
    "image_path, expected_text",
    [
        ("api/static/images/braille-1.jpg", "ABCDEFGHIJ\nKLMNOPQRST\nUVWXYZ"),
        ("api/static/images/braille-2.png", "ABCDEFGHI\nJKLMNOPQR\nSTUVXYZ W"),
        ("api/static/images/braille-3.jpg", "ABCDEFGH\nIJKLMNOP\nQRSTUVWX\nYZ"),
    ],
)
def test_braille_image_to_text_api(client, image_path, expected_text):
    with open(image_path, "rb") as img_file:
        img_bytes = img_file.read()
        data = {
            "image": (io.BytesIO(img_bytes), os.path.basename(image_path))
        }
        response = client.post("/braille-image-to-text-api", data=data, content_type="multipart/form-data")
    ratio = fuzz.ratio(response.json["text_output"], expected_text)
    assert ratio > 80

def test_render_braille_image_to_text(client):
    response = client.get("braille-image-to-text")
    assert response.status_code == 200
    assert b"Braille Image Processing" in response.data

def test_render_text_image_to_braille(client):
    response = client.get("text-image-to-braille")
    assert response.status_code == 200
    assert b"Image Processing" in response.data