import uuid
from typing import Optional


def random_suffix() -> str:
    return uuid.uuid4().hex[:6]


def random_sku(name: Optional[str] = '') -> str:
    return f'sku-{name}-{random_suffix()}'


def random_batch_ref(name: Optional[str] = '') -> str:
    return f'batch-{name}-{random_suffix()}'


def random_order_id(name: Optional[str] = '') -> str:
    return f'order-{name}-{random_suffix()}'
