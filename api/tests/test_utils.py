from utils.braille_to_text import braille_to_text
from utils.text_to_braille import text_to_braille
from utils.image_to_braille import image_to_braille
from utils.braille_image_to_text import braille_image_to_text
import pytest
from thefuzz import fuzz


@pytest.mark.parametrize(
    "braille_input, expected_text",
    [
        ("⠁", "a"),
        ("⠃", "b"),
        ("⠉", "c"),
        ("⠙", "d"),
        ("⠑", "e"),
        ("⠋", "f"),
        ("⠛", "g"),
        ("⠓", "h"),
        ("⠊", "i"),
        ("⠚", "j"),
        ("⠅", "k"),
        ("⠇", "l"),
        ("⠍", "m"),
        ("⠝", "n"),
        ("⠕", "o"),
        ("⠏", "p"),
        ("⠟", "q"),
        ("⠗", "r"),
        ("⠎", "s"),
        ("⠞", "t"),
        ("⠥", "u"),
        ("⠧", "v"),
        ("⠺", "w"),
        ("⠭", "x"),
        ("⠽", "y"),
        ("⠵", "z"),
    ],
)
def test_braille_character_to_text(braille_input, expected_text):
    assert braille_to_text(braille_input) == expected_text


@pytest.mark.parametrize(
    "text_input, expected_braille",
    [
        ("a", "⠁"),
        ("b", "⠃"),
        ("c", "⠉"),
        ("d", "⠙"),
        ("e", "⠑"),
        ("f", "⠋"),
        ("g", "⠛"),
        ("h", "⠓"),
        ("i", "⠊"),
        ("j", "⠚"),
        ("k", "⠅"),
        ("l", "⠇"),
        ("m", "⠍"),
        ("n", "⠝"),
        ("o", "⠕"),
        ("p", "⠏"),
        ("q", "⠟"),
        ("r", "⠗"),
        ("s", "⠎"),
        ("t", "⠞"),
        ("u", "⠥"),
        ("v", "⠧"),
        ("w", "⠺"),
        ("x", "⠭"),
        ("y", "⠽"),
        ("z", "⠵"),
    ],
)
def test_text_character_to_braille(text_input, expected_braille):
    assert text_to_braille(text_input) == expected_braille


@pytest.mark.parametrize(
    "braille_input, expected_text",
    [
        ("⠓⠑⠇⠇⠕⠀⠃⠗⠁⠊⠇⠇⠑", "hello braille"),
        ("⠏⠽⠞⠓⠕⠝⠀⠊⠎⠀⠋⠥⠝", "python is fun"),
        ("⠞⠑⠎⠞⠀⠉⠕⠙⠑⠀⠊⠝⠀⠃⠗⠁⠊⠇⠇⠑", "test code in braille"),
        ("⠉⠕⠙⠑⠀⠺⠊⠞⠓⠀⠝⠥⠍⠃⠑⠗⠎⠀⠁⠝⠙⠀⠉⠁⠏⠊⠞⠁⠇⠎", "code with numbers and capitals"),
        (
            "⠼⠁⠲ ⠠⠏⠽⠞⠓⠕⠝ ⠊⠎ ⠠⠋⠥⠝ ⠺⠊⠞⠓ ⠠⠙⠊⠛⠊⠞⠎ ⠁⠝⠙ ⠠⠎⠏⠁⠉⠑⠎",
            "1. Python is Fun with Digits and Spaces",
        ),
    ],
)
def test_braille_strings_to_text(braille_input, expected_text):
    assert braille_to_text(braille_input) == expected_text


@pytest.mark.parametrize(
    "text_input, expected_braille",
    [
        ("Hello Braille", "⠠⠓⠑⠇⠇⠕ ⠠⠃⠗⠁⠊⠇⠇⠑"),
        ("Python is Fun", "⠠⠏⠽⠞⠓⠕⠝ ⠊⠎ ⠠⠋⠥⠝"),
        ("Test Code in Braille", "⠠⠞⠑⠎⠞ ⠠⠉⠕⠙⠑ ⠊⠝ ⠠⠃⠗⠁⠊⠇⠇⠑"),
        ("Code with Numbers and Capitals", "⠠⠉⠕⠙⠑ ⠺⠊⠞⠓ ⠠⠝⠥⠍⠃⠑⠗⠎ ⠁⠝⠙ ⠠⠉⠁⠏⠊⠞⠁⠇⠎"),
        (
            "1. Python is Fun with Digits and Spaces",
            "⠼⠁⠲ ⠠⠏⠽⠞⠓⠕⠝ ⠊⠎ ⠠⠋⠥⠝ ⠺⠊⠞⠓ ⠠⠙⠊⠛⠊⠞⠎ ⠁⠝⠙ ⠠⠎⠏⠁⠉⠑⠎",
        ),
    ],
)
def test_text_strings_to_braille(text_input, expected_braille):
    assert text_to_braille(text_input) == expected_braille


@pytest.mark.parametrize(
    "text_input",
    [
        "hello",
        "python",
        "braille",
        "code",
        "test",
        "numbers 123",
        "CAPITALS",
        "Mixed Case 123",
    ],
)
def test_text_to_braille_to_text(text_input):
    braille_output = text_to_braille(text_input)
    text_output = braille_to_text(braille_output)
    assert text_output == text_input


@pytest.mark.parametrize(
    "braille_input",
    [
        "⠓⠑⠇⠇⠕",
        "⠏⠽⠞⠓⠕⠝",
        "⠃⠗⠁⠊⠇⠇⠑",
        "⠉⠕⠙⠑",
        "⠞⠑⠎⠞",
    ],
)
def test_braille_to_text_to_braille(braille_input):
    text_output = braille_to_text(braille_input)
    braille_output = text_to_braille(text_output)
    assert braille_output == braille_input


@pytest.mark.parametrize(
    "image_path, expected_text",
    [
        ("api/static/images/braille-1.jpg", "ABCDEFGHIJ\nKLMNOPQRST\nUVWXYZ"),
        ("api/static/images/braille-2.png", "ABCDEFGHI\nJKLMNOPQR\nSTUVXYZ W"),
        ("api/static/images/braille-3.jpg", "ABCDEFGH\nIJKLMNOP\nQRSTUVWX\nYZ"),
    ],
)
def test_braille_image_to_text(image_path, expected_text):
    _, predicted_text = braille_image_to_text(image_path, test=True)
    ratio = fuzz.ratio(predicted_text.lower(), expected_text.lower())
    assert ratio > 80

@pytest.mark.parametrize(
    "image_path, expected_text, braille_text",
    [
        ("api/static/images/text-1.png", "Translation Hello! How are you doing?", "⠠⠞⠗⠁⠝⠎⠇⠁⠞⠊⠕⠝ ⠠⠓⠑⠇⠇⠕⠖ ⠠⠓⠕⠺ ⠁⠗⠑ ⠽⠕⠥ ⠙⠕⠊⠝⠛⠦⠇"),
    ],
)
def test_text_image_to_braille(image_path, expected_text, braille_text):
    predicted_text, braille_text_output = image_to_braille(image_path, test=True)
    ratio = fuzz.ratio(predicted_text.lower(), expected_text.lower())
    assert ratio > 80
    ratio_braille = fuzz.ratio(braille_text_output, braille_text)
    assert ratio_braille > 80
