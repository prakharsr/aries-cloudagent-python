"""Pi request"""

from datetime import datetime
from typing import Union

from marshmallow import fields

from ...agent_message import AgentMessage, AgentMessageSchema
from ...util import datetime_now, datetime_to_str

from ..message_types import SET_PIXELS

HANDLER_CLASS = (
    "aries_cloudagent.messaging.raspberrypi_interactions."
    + "handlers.set_pixels_handler.SetPixelsHandler"
)


class SetPixels(AgentMessage):
    """Class defining the structure of a raspberry pi request message."""

    class Meta:
        """Basic message metadata class."""

        handler_class = HANDLER_CLASS
        message_type = SET_PIXELS
        schema_class = "SetPixelsSchema"

    def __init__(
        self,
        *,
        sent_time: Union[str, datetime] = None,
        pixels : list = None,
        **kwargs
    ):
        """
        Initialize basic message object.

        Args:
            sent_time: Time message was sent
            letter: letter to display
        """
        super(SetPixels, self).__init__(**kwargs)
        if not sent_time:
            sent_time = datetime_now()
        self.sent_time = datetime_to_str(sent_time)
        self.pixels = pixels


class SetPixelsSchema(AgentMessageSchema):
    """Basic message schema class."""

    class Meta:
        """Basic message schema metadata."""

        model_class = SetPixels

    sent_time = fields.Str(required=False)
    pixels = fields.List(fields.Integer(), required=True)