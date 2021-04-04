import uuid
from typing import Callable, Optional

import pytest
import requests

from samples.architecture_patterns_with_python import config


def random_suffix() -> str:
    return uuid.uuid4().hex[:6]


def random_sku(name: Optional[str] = '') -> str:
    return f'sku-{name}-{random_suffix()}'


def random_batch_ref(name: Optional[str] = '') -> str:
    return f'batch-{name}-{random_suffix()}'


def random_order_id(name: Optional[str] = '') -> str:
    return f'order-{name}-{random_suffix()}'


@pytest.mark.usefixtures('restart_api')
def test_happy_path_returns_201_and_allocated_batch(add_stock: Callable) -> None:
    sku, other_sku = random_sku(), random_sku('other')
    early_batch = random_batch_ref('1')
    later_batch = random_batch_ref('2')
    other_batch = random_batch_ref('3')
    add_stock(
        [
            (later_batch, sku, 100, '2011-01-02'),
            (early_batch, sku, 100, '2011-01-01'),
            (other_batch, other_sku, 100, None),
        ]
    )
    data = {'order_id': random_order_id(), 'sku': sku, 'qty': 3}
    url = config.get_api_url()

    r = requests.post(f'{url}/allocate', json=data)

    assert r.status_code == 201
    assert r.json()['batch_ref'] == early_batch


@pytest.mark.usefixtures('restart_api')
def test_unhappy_path_returns_400_and_error_message() -> None:
    unknown_sku, orderid = random_sku(), random_order_id()
    data = {'order_id': orderid, 'sku': unknown_sku, 'qty': 20}
    url = config.get_api_url()

    r = requests.post(f'{url}/allocate', json=data)

    assert r.status_code == 400
    assert r.json()['message'] == f'Invalid sku {unknown_sku}'
