"""Pi request"""

from datetime import datetime
from typing import Union

from marshmallow import fields



from ...agent_message import AgentMessage, AgentMessageSchema
from ...util import datetime_now, datetime_to_str

from ..message_types import READ_SENSOR

HANDLER_CLASS = (
    "aries_cloudagent.messaging.raspberrypi_interactions."
    + "handlers.read_sensor_handler.ReadSensorHandler"
)


class ReadSensor(AgentMessage):
    """Class defining the structure of a raspberry pi request message."""

    class Meta:
        """Basic message metadata class."""

        handler_class = HANDLER_CLASS
        message_type = READ_SENSOR
        schema_class = "ReadSensorSchema"

    def __init__(
        self,
        *,
        sent_time: Union[str, datetime] = None,
        read_temperature: bool = True,
        read_pressure: bool = True,
        read_humidity: bool = True,
        content: str = None,
        **kwargs
    ):
        """
        Initialize basic message object.

        Args:
            sent_time: Time message was sent
            content: message content
        """
        super(ReadSensor, self).__init__(**kwargs)
        if not sent_time:
            sent_time = datetime_now()
        self.sent_time = datetime_to_str(sent_time)
        self.read_temperature = read_temperature
        self.read_pressure = read_pressure
        self.read_humidity = read_humidity


class ReadSensorSchema(AgentMessageSchema):
    """Basic message schema class."""

    class Meta:
        """Basic message schema metadata."""

        model_class = ReadSensor

    sent_time = fields.Str(required=False)
    content = fields.Str(required=True)

    read_temperature = fields.Bool(default=True, required=False)
    read_pressure = fields.Bool(default=True, required=False)
    read_humidity = fields.Bool(default=True, required=False)