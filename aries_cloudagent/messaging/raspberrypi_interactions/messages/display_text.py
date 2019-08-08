"""Pi request"""

from datetime import datetime
from typing import Union

from marshmallow import fields

from ...agent_message import AgentMessage, AgentMessageSchema
from ...util import datetime_now, datetime_to_str

from ..message_types import DISPLAY_TEXT

HANDLER_CLASS = (
    "aries_cloudagent.messaging.raspberrypi_interactions."
    + "handlers.display_text_handler.DisplayTextHandler"
)


class DisplayText(AgentMessage):
    """Class defining the structure of a raspberry pi request message."""

    class Meta:
        """Basic message metadata class."""

        handler_class = HANDLER_CLASS
        message_type = DISPLAY_TEXT
        schema_class = "DisplayTextSchema"

    def __init__(
        self,
        *,
        sent_time: Union[str, datetime] = None,
        scroll_speed: float= 0.1,
        text_colour: list = None,
        back_colour: list = None,
        content: str = None,
        **kwargs
    ):
        """
        Initialize basic message object.

        Args:
            sent_time: Time message was sent
            content: message content
        """
        super(DisplayText, self).__init__(**kwargs)
        if not sent_time:
            sent_time = datetime_now()
        self.sent_time = datetime_to_str(sent_time)
        self.content = content
        if not scroll_speed:
            scroll_speed = 0.1
        self.scroll_speed = scroll_speed
        if not text_colour:
            text_colour = [255, 255, 255]
        self.text_colour = text_colour
        if not back_colour:
            back_colour = [0, 0, 0]
        self.back_colour = back_colour
        


class DisplayTextSchema(AgentMessageSchema):
    """Basic message schema class."""

    class Meta:
        """Basic message schema metadata."""

        model_class = DisplayText

    sent_time = fields.Str(required=False)
    content = fields.Str(required=True)

    scroll_speed = fields.Float(default=0.1, required=False)
    text_colour = fields.List(fields.Integer(), default=[255,255,255], required=False)
    back_colour = fields.List(fields.Integer(), default=[0,0,0], required=False)
