from unittest import mock
from unittest.mock import Mock

from samples.unit_testing_pattern.customer import Customer
from samples.unit_testing_pattern.product import Product


@mock.patch('samples.unit_testing_pattern.store.Store')
class TestCustomerWithLondonStyle:
    def test_purchase_succeeds_when_enough_inventory(self, mock_store: Mock) -> None:
        mock_store.has_enough_inventory.return_value = True
        customer = Customer()

        # Act
        success = customer.purchase(mock_store, Product.Shampoo, 5)

        # Assert
        assert success is True
        mock_store.remove_inventory.assert_called_once_with(Product.Shampoo, 5)

    def test_purchase_fails_when_not_enough_inventory(self, mock_store: Mock) -> None:
        # Arrange
        mock_store.has_enough_inventory.return_value = False
        customer = Customer()

        # Act
        success = customer.purchase(mock_store, Product.Shampoo, 15)

        # Assert
        assert success is False
        mock_store.remove_inventory.assert_not_called()
