import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

character_map = {
    "a": "⠁",
    "b": "⠃",
    "k": "⠅",
    "l": "⠇",
    "c": "⠉",
    "i": "⠊",
    "f": "⠋",
    "m": "⠍",
    "s": "⠎",
    "p": "⠏",
    "e": "⠑",
    "h": "⠓",
    "o": "⠕",
    "r": "⠗",
    "d": "⠙",
    "j": "⠚",
    "g": "⠛",
    "n": "⠝",
    "t": "⠞",
    "q": "⠟",
    "u": "⠥",
    "v": "⠧",
    "x": "⠭",
    "z": "⠵",
    "w": "⠺",
    "y": "⠽",
    "num": "⠼",
    "caps": "⠠",
    ".": "⠲",
    "'": "⠄",
    ",": "⠂",
    "-": "⠤",
    "/": "⠌",
    "!": "⠖",
    "?": "⠦",
    "$": "⠲",
    ":": "⠒",
    ";": "⠰",
    "(": "⠶",
    ")": "⠶",
    " ": " ",
    "1": "⠁",
    "2": "⠃",
    "3": "⠉",
    "4": "⠙",
    "5": "⠑",
    "6": "⠋",
    "7": "⠛",
    "8": "⠓",
    "9": "⠊",
    "0": "⠚",
}

number_punctuations = [".", ",", "-", "/", "$"]
escape_characters = ["\n", "\r", "\t"]


def text_to_braille(text_to_convert):
    """Convert text to braille."""
    logging.info("Starting text to braille conversion.")
    if type(text_to_convert) is not str:
        logging.error("Input is not a string.")
        raise TypeError("Only strings can be converted")
    result = map_characters(text_to_convert)
    logging.info("Text to braille conversion completed.")
    return result


def map_characters(text_to_convert):
    """Map characters to braille symbols."""
    logging.info("Mapping characters to braille symbols.")
    isNumber = False
    convertedText = ""
    for character in text_to_convert:
        if character in escape_characters:
            convertedText += character
            continue
        if character.isupper():
            logging.info(f"Detected uppercase character: {character}")
            convertedText += character_map.get("caps")
            character = character.lower()
        if character.isdigit():
            if not isNumber:
                isNumber = True
                logging.info(f"Detected number: {character}")
                convertedText += character_map.get("num")
        else:
            if isNumber and character not in number_punctuations:
                isNumber = False
        try:
            convertedText += character_map.get(character)
        except:
            logging.warning(f"Character not found in map: {character}")
    logging.info("Character mapping completed.")
    return convertedText
