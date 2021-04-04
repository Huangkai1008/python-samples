from sqlalchemy import text
from sqlalchemy.orm import Session

from samples.architecture_patterns_with_python.allocation.domain.model import OrderLine


def test_order_line_mapper_can_load_lines(session: Session) -> None:
    session.execute(
        text(
            "INSERT INTO order_line (order_id, sku, qty) VALUES "
            '("order1", "RED-CHAIR", 12),'
            '("order1", "RED-TABLE", 13),'
            '("order2", "BLUE-LIPSTICK", 14)'
        )
    )
    expected = [
        OrderLine('order1', 'RED-CHAIR', 12),
        OrderLine('order1', 'RED-TABLE', 13),
        OrderLine('order2', 'BLUE-LIPSTICK', 14),
    ]
    assert session.query(OrderLine).all() == expected
