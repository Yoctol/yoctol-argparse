import pytest

from ..namespace import NestedNamespace


def test_successfully_setattr():
    args = NestedNamespace()
    setattr(args, 'a.b.c', 1)
    setattr(args, 'a.b.d', 2)
    assert isinstance(args.a, NestedNamespace)
    assert isinstance(args.a.b, NestedNamespace)
    assert args.a.b.c == getattr(args, 'a.b.c') == 1
    assert args.a.b.d == getattr(args, 'a.b.d') == 2

    setattr(args, 'e', 2)
    assert args.e == 2


def test_raise_error():
    args = NestedNamespace()
    with pytest.raises(AttributeError):
        args.f

    with pytest.raises(ValueError):
        setattr(args, 'a.', 1)

    with pytest.raises(ValueError):
        setattr(args, '..a', 1)
