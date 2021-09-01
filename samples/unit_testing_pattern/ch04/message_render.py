from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Message:
    header: str
    body: str
    footer: str


class Renderer(metaclass=ABCMeta):
    @abstractmethod
    def render(self, message: Message) -> str:
        ...


class HeaderRenderer(Renderer):
    def render(self, message: Message) -> str:
        return f'<h1>{message.header}</h1>'


class BodyRenderer(Renderer):
    def render(self, message: Message) -> str:
        return f'<b>{message.body}</b>'


class FooterRenderer(Renderer):
    def render(self, message: Message) -> str:
        return f'<i>{message.footer}</i>'


@dataclass(frozen=True)
class MessageRender(Renderer):
    sub_renders: Tuple[Renderer, Renderer, Renderer] = (
        HeaderRenderer(),
        BodyRenderer(),
        FooterRenderer(),
    )

    def render(self, message: Message) -> str:
        return ''.join(sub_render.render(message) for sub_render in self.sub_renders)
