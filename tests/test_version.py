import tickflow


def test_version_is_string():
    assert isinstance(tickflow.__version__, str)
    assert tickflow.__version__.count(".") == 2
