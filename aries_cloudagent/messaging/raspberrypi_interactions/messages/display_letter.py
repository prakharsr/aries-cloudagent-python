"""Pi request"""

from datetime import datetime
from typing import Union

from marshmallow import fields

from ...agent_message import AgentMessage, AgentMessageSchema
from ...util import datetime_now, datetime_to_str

from ..message_types import DISPLAY_LETTER

HANDLER_CLASS = (
    "aries_cloudagent.messaging.raspberrypi_interactions."
    + "handlers.display_letter_handler.DisplayLetterHandler"
)


class DisplayLetter(AgentMessage):
    """Class defining the structure of a raspberry pi request message."""

    class Meta:
        """Basic message metadata class."""

        handler_class = HANDLER_CLASS
        message_type = DISPLAY_LETTER
        schema_class = "DisplayLetterSchema"

    def __init__(
        self,
        *,
        sent_time: Union[str, datetime] = None,
        text_colour: list = None,
        back_colour: list = None,
        letter: str = None,
        **kwargs
    ):
        """
        Initialize basic message object.

        Args:
            sent_time: Time message was sent
            letter: letter to display
        """
        super(DisplayLetter, self).__init__(**kwargs)
        if not sent_time:
            sent_time = datetime_now()
        self.sent_time = datetime_to_str(sent_time)
        self.letter = letter
        if not text_colour:
            text_colour = [255, 255, 255]
        self.text_colour = text_colour
        if not back_colour:
            back_colour = [0, 0, 0]
        self.back_colour = back_colour
        


class DisplayLetterSchema(AgentMessageSchema):
    """Basic message schema class."""

    class Meta:
        """Basic message schema metadata."""

        model_class = DisplayLetter

    sent_time = fields.Str(required=False)
    letter = fields.Str(required=True)

    text_colour = fields.List(fields.Integer(), default=[255,255,255], required=False)
    back_colour = fields.List(fields.Integer(), default=[0,0,0], required=False)
