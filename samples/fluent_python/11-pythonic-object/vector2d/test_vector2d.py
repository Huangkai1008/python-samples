import pytest

from .vector2d import Vector2d


class TestVector2d:
    def test_vector2d_can_access_attributes_directly(self) -> None:
        v = Vector2d(3, 4)

        assert v.x == 3
        assert v.y == 4

    def test_vector2d_cannot_set_attributes_directly(self) -> None:
        v = Vector2d(3, 4)

        with pytest.raises(AttributeError):
            v.x = 5  # noqa

    def test_vector2d_can_be_unpacked_to_a_tuple(self) -> None:
        v = Vector2d(3, 4)

        x, y = v

        assert x == 3
        assert y == 4

    def test_vector2d_can_rebuild_from_repr(self) -> None:
        v = Vector2d(3, 4)

        v_clone = eval(repr(v))

        assert v == v_clone

    def test_vector2d_prints_as_tuple(self) -> None:
        v = Vector2d(3, 4)

        assert str(v) == '(3, 4)'

    def test_vector_can_rebuild_from_bytes(self) -> None:
        v = Vector2d(3, 4)

        v_clone = Vector2d.from_bytes(bytes(v))

        assert v == v_clone

    def test_vector_abs_returns_magnitude(self) -> None:
        v = Vector2d(3, 4)

        assert abs(v) == 5.0

    @pytest.mark.parametrize(
        'v1,v2,expected',
        [(3, 4, True), (0, 0, False)],
    )
    def test_vector2d_bool_returns_whether_magnitude_is_not_zero(
        self, v1: float, v2: float, expected: bool
    ) -> None:
        v = Vector2d(v1, v2)

        actual = bool(v)

        assert actual == expected

    def test_vector2d_is_hashable(self) -> None:
        v = Vector2d(3, 4)

        actual = hash(v)

        assert isinstance(actual, int)
