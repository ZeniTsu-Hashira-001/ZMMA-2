def test_brat_ok(client):
    r = client.post("/v1/brat", params={"text": "hello world"})
    assert r.status_code == 200
    assert r.headers["content-type"] == "image/png"


def test_brat_empty_text(client):
    r = client.post("/v1/brat", params={"text": ""})
    assert r.status_code == 422  # validation Pydantic


def test_brat_invalid_color(client):
    r = client.post("/v1/brat", params={"text": "hi", "fg": "notacolor"})
    assert r.status_code == 400


def test_brat_size_bounds(client):
    assert client.post("/v1/brat", params={"text": "hi", "size": 50}).status_code == 422
    assert client.post("/v1/brat", params={"text": "hi", "size": 5000}).status_code == 422