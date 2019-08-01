"""Basic message handler."""

from ...base_handler import BaseHandler, BaseResponder, RequestContext
from ...connections.manager import ConnectionManager

from ..messages.read_sensor import ReadSensor
from ..messages.read_sensor_response import ReadSensorResponse


class ReadSensorResponseHandler(BaseHandler):
    """Message handler class for basic messages."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Message handler logic for basic messages.

        Args:
            context: request context
            responder: responder callback
        """
        self._logger.debug(f"ReadSensorResponseHandler called with context {context}")
        assert isinstance(context.message, ReadSensorResponse)

        self._logger.info("Received read sensor response: %s", context.message.content)


        body = context.message.content
        temperature = context.message.temperature
        pressure = context.message.pressure
        humidity = context.message.humidity
        meta = {"content": body, 
                "read_temperature" : temperature,
                "read_pressure" : pressure, 
                "read_humidity" : humidity}

        conn_mgr = ConnectionManager(context)
        await conn_mgr.log_activity(
            context.connection_record,
            "read_sensor_reply",
            context.connection_record.DIRECTION_RECEIVED,
            meta,
        )

        