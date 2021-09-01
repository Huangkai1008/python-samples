from samples.unit_testing_pattern.ch06.listing1.price_engine import calculate_discount
from samples.unit_testing_pattern.ch06.listing1.product import Product


class TestPriceEngine:
    # Output-based testing
    def test_discount_of_two_products(self) -> None:
        product1: Product = Product('Hand wash')
        product2: Product = Product('Shampoo')

        discount: float = calculate_discount(product1, product2)

        assert discount == 0.02
