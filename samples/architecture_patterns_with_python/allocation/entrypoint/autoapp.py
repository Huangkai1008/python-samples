from typing import Any

from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from samples.architecture_patterns_with_python import config
from samples.architecture_patterns_with_python.allocation.services import service
from samples.architecture_patterns_with_python.allocation.adapter import orm, repository
from samples.architecture_patterns_with_python.allocation.domain.model import OrderLine, OutOfStock

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_database_uri()))
app = Flask(__name__)


@app.route('/allocate', methods=['POST'])
def allocate_endpoint() -> Any:
    session = get_session()
    repo = repository.SQLAlchemyRepository(session)
    line = OrderLine(
        request.json['order_id'],
        request.json['sku'],
        request.json['qty'],
    )

    try:
        batch_ref = service.allocate(line, repo, session)
    except (OutOfStock, service.InvalidSKU) as e:
        return {'message': str(e)}, 400

    return {'batch_ref': batch_ref}, 201
