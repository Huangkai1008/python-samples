from datetime import datetime
from typing import Any

from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from samples.architecture_patterns_with_python import config
from samples.architecture_patterns_with_python.allocation.adapter import orm
from samples.architecture_patterns_with_python.allocation.domain.command import (
    Allocate,
    CreateBatch,
)
from samples.architecture_patterns_with_python.allocation.services import message_bus
from samples.architecture_patterns_with_python.allocation.services.handlers import (
    InvalidSKU,
)
from samples.architecture_patterns_with_python.allocation.services.unit_of_work import (
    SQLAlchemyUnitOfWork,
)

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_database_uri()))
app = Flask(__name__)


@app.route('/batches', methods=['POST'])
def add_batch():
    eta = request.json['eta']
    if eta is not None:
        eta = datetime.fromisoformat(eta).date()

    cmd = CreateBatch(
        request.json['ref'],
        request.json['sku'],
        request.json['qty'],
        eta,
    )
    message_bus.handle(cmd, SQLAlchemyUnitOfWork())
    return 'OK', 201


@app.route('/allocations', methods=['POST'])
def allocate_endpoint() -> Any:
    try:
        cmd = Allocate(
            request.json['order_id'],
            request.json['sku'],
            request.json['qty'],
        )
        uow = SQLAlchemyUnitOfWork()
        results = message_bus.handle(cmd, uow)
        batch_ref = results.pop(0)
    except InvalidSKU as e:
        return {'message': str(e)}, 400

    return {'batch_ref': batch_ref}, 201
