import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def braille_to_text(braille_string):
    logging.info("Function braille_to_text called with input: %s", braille_string)

    braille_to_english = {
        "⠁": "a",
        "⠃": "b",
        "⠉": "c",
        "⠙": "d",
        "⠑": "e",
        "⠋": "f",
        "⠛": "g",
        "⠓": "h",
        "⠊": "i",
        "⠚": "j",
        "⠅": "k",
        "⠇": "l",
        "⠍": "m",
        "⠝": "n",
        "⠕": "o",
        "⠏": "p",
        "⠟": "q",
        "⠗": "r",
        "⠎": "s",
        "⠞": "t",
        "⠥": "u",
        "⠧": "v",
        "⠺": "w",
        "⠭": "x",
        "⠽": "y",
        "⠵": "z",
        "⠂": ",",
        "⠲": ".",
        "⠖": "!",
        "⠦": "?",
        "⠆": ";",
        "⠄": "'",
        "⠤": "-",
        "⠿": "#",
        "⠮": "th",
        "⠫": "st",
        "⠼": "number",
        "⠠": "capital",
        "⠤": "hyphen",
        "⠐": "accent",
        "⠰": "abbreviation",
        "⠀": " ",
    }

    number_prefix = "⠼"
    capital_prefix = "⠠"

    result = ""
    i = 0

    while i < len(braille_string):
        char = braille_string[i]

        if char == capital_prefix and i + 1 < len(braille_string):
            i += 1
            next_char = braille_string[i]
            if next_char in braille_to_english:
                result += braille_to_english[next_char].upper()
            else:
                result += next_char

        elif char == number_prefix and i + 1 < len(braille_string):
            i += 1
            number_map = {
                "⠁": "1",
                "⠃": "2",
                "⠉": "3",
                "⠙": "4",
                "⠑": "5",
                "⠋": "6",
                "⠛": "7",
                "⠓": "8",
                "⠊": "9",
                "⠚": "0",
            }

            while i < len(braille_string) and braille_string[i] in number_map:
                result += number_map[braille_string[i]]
                i += 1
            i -= 1

        elif char in braille_to_english:
            result += braille_to_english[char]
        else:
            result += char

        i += 1

    return result
