def test_welcome_square(client, fake_download):
    r = client.post(
        "/v1/welcome",
        params={"url": "https://example.com/a.png", "username": "Zenitsu", "style": "square"},
    )
    assert r.status_code == 200


def test_welcome_all_styles(client, fake_download):
    for style in ("square", "round", "hex", "star", "heart"):
        r = client.post(
            "/v1/welcome",
            params={"url": "https://example.com/a.png", "username": "Z", "style": style},
        )
        assert r.status_code == 200, style


def test_welcome_bad_style(client):
    r = client.post(
        "/v1/welcome",
        params={"url": "https://example.com/a.png", "username": "Z", "style": "triangle"},
    )
    assert r.status_code == 422