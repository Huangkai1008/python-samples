from samples.unit_testing_pattern.ch03.caculator import sum_of_two_numbers


class TestCalculator:
    def test_sum_of_two_numbers(self) -> None:
        first = 10
        second = 20

        result = sum_of_two_numbers(first, second)

        assert result == 30
