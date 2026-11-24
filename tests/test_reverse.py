def test_reverse_ok(client, fake_download):
    r = client.post("/v1/reverse", params={"url": "https://example.com/a.png"})
    assert r.status_code == 200
    assert r.headers["content-type"] == "image/png"


def test_bw_ok(client, fake_download):
    r = client.post("/v1/bw", params={"url": "https://example.com/a.png"})
    assert r.status_code == 200


def test_reverse_bad_url(client):
    r = client.post("/v1/reverse", params={"url": "not-a-url"})
    assert r.status_code == 422