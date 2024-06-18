import pytest

from hermys.modules.auth.password import is_password_strong


@pytest.mark.anyio
def test_is_password_strong():
    assert is_password_strong('12345Aa@')
    with pytest.raises(ValueError):
        assert is_password_strong('short')
    with pytest.raises(ValueError):
        assert is_password_strong('needonedigit')
    with pytest.raises(ValueError):
        assert is_password_strong('0MUSTHAVELOWER')
    with pytest.raises(ValueError):
        assert is_password_strong('0musthaveupper')
    with pytest.raises(ValueError):
        assert is_password_strong('0MustHaveEspecial')
