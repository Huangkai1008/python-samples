import pytest

from samples.unit_testing_pattern.ch04.message_render import (
    BodyRenderer,
    FooterRenderer,
    HeaderRenderer,
    Message,
    MessageRender,
)


class TestMessageRender:
    @pytest.mark.skip(
        reason='tests should not couples to the SUT’s implementation details and not '
        'the outcome the SUT produces'
    )
    def test_message_render_use_correct_sub_renders(
        self, message_render: MessageRender
    ) -> None:
        assert len(message_render.sub_renders) == 3
        assert isinstance(message_render.sub_renders[0], HeaderRenderer)
        assert isinstance(message_render.sub_renders[1], BodyRenderer)
        assert isinstance(message_render.sub_renders[2], FooterRenderer)

    def test_rendering_a_message(self, message_render: MessageRender) -> None:
        message = Message('h', 'b', 'f')

        html = message_render.render(message)

        assert html == '<h1>h</h1><b>b</b><i>f</i>'
