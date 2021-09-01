import pytest

from samples.unit_testing_pattern.customer import Customer
from samples.unit_testing_pattern.store import Store


@pytest.fixture
def store() -> Store:
    store = Store()
    return store


@pytest.fixture
def customer() -> Customer:
    return Customer()
