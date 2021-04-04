from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table
from sqlalchemy.orm import registry, relationship

from samples.architecture_patterns_with_python.allocation.domain.model import Batch, OrderLine

mapper_registry = registry()

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
    Column('sku', String(255)),
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
    mapper_registry.map_imperatively(
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
