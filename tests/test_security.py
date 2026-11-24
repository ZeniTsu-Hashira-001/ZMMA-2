from security import is_safe_url


def test_safe_url_public():
    assert is_safe_url("https://example.com/img.png")


def test_private_blocked():
    assert not is_safe_url("http://127.0.0.1/x")
    assert not is_safe_url("http://10.0.0.1/x")
    assert not is_safe_url("http://192.168.1.1/x")


def test_bad_scheme_blocked():
    assert not is_safe_url("ftp://example.com/x")
    assert not is_safe_url("file:///etc/passwd")