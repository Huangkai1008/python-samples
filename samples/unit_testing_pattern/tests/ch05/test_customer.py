from unittest import mock
from unittest.mock import Mock

import pytest

from samples.unit_testing_pattern.ch05.customer.controller import CustomerController
from samples.unit_testing_pattern.ch05.customer.customer import Customer
from samples.unit_testing_pattern.ch05.customer.product import Product


class TestCustomer:
    @pytest.mark.skip(reason='concept illustration only')
    @mock.patch('samples.ch05.customer.email.EmailGateway')
    def test_purchase_succeed_when_enough_inventory(
        self, mock_email_gateway: Mock
    ) -> None:
        customer = CustomerController(mock_email_gateway)

        success = customer.purchase(1, 2, 5)

        assert success is True
        mock_email_gateway.send_receipt.assert_called()

    @pytest.mark.skip(
        reason='using mocks to assert intra-system communications'
        ' leads to fragile tests'
    )
    @mock.patch('samples.ch05.customer.store.IStore')
    def test_purchase_succeed_cause_fragile_tests(self, mock_store: Mock) -> None:
        mock_store.has_enough_inventory.return_value = True
        customer = Customer(1, 'user@email.com')

        success = customer.purchase(mock_store, Product(1, 'product-1'), 5)

        assert success is True
        mock_store.remove_inventory.assert_called_once()
