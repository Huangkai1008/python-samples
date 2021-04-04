from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table
from sqlalchemy.orm import registry, relationship

from samples.architecture_patterns_with_python.allocation.domain.model import (
    Batch,
    OrderLine,
    Product,
)

mapper_registry = registry()

product = Table(
    'product',
    mapper_registry.metadata,
    Column('sku', String(255), primary_key=True),
    Column('version_number', Integer, nullable=False, server_default='0'),
)

order_line = Table(
    'order_line',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('sku', String(255)),
    Column('qty', Integer, nullable=False),
    Column('order_id', String(255)),
)

batch = Table(
    'batch',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('reference', String(255)),
    Column('sku', ForeignKey('product.sku')),
    Column('_purchased_qty', Integer, nullable=False),
    Column('eta', Date, nullable=True),
)

allocation = Table(
    'allocation',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('order_line_id', ForeignKey('order_line.id')),
    Column('batch_id', ForeignKey('batch.id')),
)


def start_mappers() -> None:
    lines_mapper = mapper_registry.map_imperatively(OrderLine, order_line)
    batches_mapper = mapper_registry.map_imperatively(
        Batch,
        batch,
        properties={
            '_allocations': relationship(
                lines_mapper,
                secondary=allocation,
                collection_class=set,
            )
        },
    )
    mapper_registry.map_imperatively(
        Product, product, properties={'batches': relationship(batches_mapper)}
    )
