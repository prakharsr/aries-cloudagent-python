"""Sensor Value from raspberry pi"""

from datetime import datetime
from typing import Union

from marshmallow import fields

from ...agent_message import AgentMessage, AgentMessageSchema
from ...util import datetime_now, datetime_to_str

from ..message_types import SENSOR_VALUE

HANDLER_CLASS = (
    "aries_cloudagent.messaging.raspberrypi_interactions."
    + "handlers.sensor_value_handler.SensorValueHandler"
)


class SensorValue(AgentMessage):
    """Class defining the structure of a raspberry pi sensor value."""

    class Meta:
        """Basic message metadata class."""

        handler_class = HANDLER_CLASS
        message_type = SENSOR_VALUE
        schema_class = "SensorValueSchema"

    def __init__(
        self,
        *,
        sent_time: Union[str, datetime] = None,
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
        super(SensorValue, self).__init__(**kwargs)
        if not sent_time:
            sent_time = datetime_now()
        self.sent_time = datetime_to_str(sent_time)

        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity


class SensorValueSchema(AgentMessageSchema):
    """Basic message schema class."""

    class Meta:
        """Basic message schema metadata."""

        model_class = SensorValue

    sent_time = fields.Str(required=False)

    temperature = fields.Float(required=False)
    humidity = fields.Float(required=False)
    pressure = fields.Float(required=False)
