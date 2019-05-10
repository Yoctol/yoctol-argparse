import pytest

from ..types import int_in_range, float_in_range


@pytest.mark.parametrize('func, x, valid', [
    (int_in_range(0), '2', True),
    (int_in_range(0), '0', True),
    (int_in_range(), 'a', False),
    (int_in_range(), '2.', False),
])
def test_int_in_range(func, x, valid):
    if valid:
        assert func(x) == int(x)
    else:
        with pytest.raises(ValueError):
            func(x)


@pytest.mark.parametrize('func, x, valid', [
    (float_in_range(0), '2', True),
    (float_in_range(0), '0', True),
    (float_in_range(0, inclusive=False), '0', False),
    (float_in_range(), 'a', False),
    (float_in_range(), 'inf', False),
])
def test_float_in_range(func, x, valid):
    if valid:
        assert func(x) == float(x)
    else:
        with pytest.raises(ValueError):
            func(x)
