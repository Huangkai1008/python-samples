import logging
from typing import Callable, List, Optional, Type, Union

from samples.architecture_patterns_with_python.allocation.domain.command import (
    Allocate,
    ChangeBatchQuantity,
    Command,
    CreateBatch,
)
from samples.architecture_patterns_with_python.allocation.domain.event import (
    Event,
    OutOfStock,
)
from samples.architecture_patterns_with_python.allocation.services import handlers
from samples.architecture_patterns_with_python.allocation.services.handlers import (
    send_out_of_stock_notification,
)
from samples.architecture_patterns_with_python.allocation.services.unit_of_work import (
    AbstractUnitOfWork,
)

logger = logging.getLogger(__name__)

Message = Union[Command, Event]


def handle(
    message: Message,
    uow: AbstractUnitOfWork,
) -> Optional[List]:
    results = []
    queue = [message]
    while queue:
        message = queue.pop(0)
        if isinstance(message, Event):
            handle_event(message, queue, uow)
        elif isinstance(message, Command):
            cmd_result = handle_command(message, queue, uow)
            results.append(cmd_result)
        else:
            raise Exception(f'{message} was not an Event or Command')
    return results


def handle_event(
    event: Event,
    queue: List[Message],
    uow: AbstractUnitOfWork,
) -> None:
    for handler in EVENT_HANDLERS[type(event)]:
        try:
            logger.debug(f'handling event {event} with handler {handler}')
            handler(event, uow=uow)
            queue.extend(uow.collect_new_events())
        except Exception as e:
            logger.exception(f'Exception handling event {event}: {e}')
            continue


def handle_command(
    command: Command,
    queue: List[Message],
    uow: AbstractUnitOfWork,
):
    logger.debug(f'handling command {command}')
    try:
        handler = COMMAND_HANDLERS[type(command)]
        result = handler(command, uow=uow)
        queue.extend(uow.collect_new_events())
        return result
    except Exception:
        logger.exception(f'Exception handling command {command}')
        raise


EVENT_HANDLERS: dict[Type[Event], List[Callable]] = {
    OutOfStock: [send_out_of_stock_notification],
}

COMMAND_HANDLERS: dict[Type[Command], Callable] = {
    Allocate: handlers.allocate,
    CreateBatch: handlers.add_batch,
    ChangeBatchQuantity: handlers.change_batch_quantity,
}
