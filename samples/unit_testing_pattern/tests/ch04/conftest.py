import pytest

from samples.unit_testing_pattern.ch04.message_render import MessageRender


@pytest.fixture
def message_render() -> MessageRender:
    return MessageRender()
