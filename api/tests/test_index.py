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
