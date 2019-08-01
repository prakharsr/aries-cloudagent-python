"""Pi response"""

from datetime import datetime
from typing import Union

from marshmallow import fields

from ...agent_message import AgentMessage, AgentMessageSchema
from ...util import datetime_now, datetime_to_str

from ..message_types import READ_SENSOR_RESPONSE

HANDLER_CLASS = (
    "aries_cloudagent.messaging.raspberrypi_interactions."
    + "handlers.read_sensor_response_handler.ReadSensorResponseHandler"
)


class ReadSensorResponse(AgentMessage):
    """Class defining the structure of a raspberry pi response message."""

    class Meta:
        """Basic message metadata class."""

        handler_class = HANDLER_CLASS
        message_type = READ_SENSOR_RESPONSE
        schema_class = "ReadSensorResponseSchema"

    def __init__(
        self,
        *,
        sent_time: Union[str, datetime] = None,
        content: str = None,
        temperature: float = None,
        humidity: float = None,
        pressure: float = None,
        **kwargs
    ):
        """
        Initialize basic message object.

        Args:
            sent_time: Time message was sent
            content: message content
        """
        super(ReadSensorResponse, self).__init__(**kwargs)
        if not sent_time:
            sent_time = datetime_now()
        self.sent_time = datetime_to_str(sent_time)
        self.content = content
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity


class ReadSensorResponseSchema(AgentMessageSchema):
    """Basic message schema class."""

    class Meta:
        """Basic message schema metadata."""

        model_class = ReadSensorResponse

    sent_time = fields.Str(required=False)
    content = fields.Str(required=True)

    temperature = fields.Float(required=False)
    humidity = fields.Float(required=False)
    pressure = fields.Float(required=False)
