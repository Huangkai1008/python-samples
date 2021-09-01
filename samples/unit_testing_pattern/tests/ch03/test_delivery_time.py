import datetime as dt

import pytest

from samples.unit_testing_pattern.ch03.delivery import is_delivery_valid


class TestDelivery:
    @pytest.mark.parametrize(
        'delivery,expected',
        [
            pytest.param(
                dt.datetime.now() + dt.timedelta(days=-1),
                False,
                id='past_date',
            ),
            pytest.param(
                dt.datetime.now() + dt.timedelta(days=-1),
                False,
                id='now',
            ),
            pytest.param(
                dt.datetime.now() + dt.timedelta(days=1),
                False,
                id='backward_one_day',
            ),
        ],
    )
    def test_delivery_is_invalid(self, delivery: dt.datetime, expected: bool) -> None:
        assert is_delivery_valid(delivery) == expected

    @pytest.mark.parametrize(
        'delivery,expected',
        [
            pytest.param(
                dt.datetime.now() + dt.timedelta(days=2),
                True,
                id='backward_two_day',
            ),
            pytest.param(
                dt.datetime.now() + dt.timedelta(days=3),
                True,
                id='backward_three_day',
            ),
        ],
    )
    def test_delivery_is_valid(self, delivery: dt.datetime, expected: bool) -> None:
        assert is_delivery_valid(delivery) == expected
