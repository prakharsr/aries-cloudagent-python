"""Basic message handler."""

from ...base_handler import BaseHandler, BaseResponder, RequestContext
from ...connections.manager import ConnectionManager

from ..messages.read_sensor import ReadSensor
from ..messages.read_sensor_response import ReadSensorResponse

from sense_hat import SenseHat


class ReadSensorHandler(BaseHandler):
    """Message handler class for basic messages."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Message handler logic for basic messages.

        Args:
            context: request context
            responder: responder callback
        """
        self._logger.debug(f"ReadSensorHandler called with context {context}")
        assert isinstance(context.message, ReadSensor)

        self._logger.info("Received read sensor: %s", context.message.sensors)

        sensors = context.message.sensors

        meta = {"sensors": sensors}

        conn_mgr = ConnectionManager(context)
        await conn_mgr.log_activity(
            context.connection_record,
            "read_sensor",
            context.connection_record.DIRECTION_RECEIVED,
            meta,
        )

        await responder.send_webhook(
            "read_sensor",
            {"message_id": context.message._id, "content": body, "state": "received"},
        )

        sense = SenseHat()
        sense.clear()
        if "temperature" in sensors:
            temperature = sense.get_temperature()
        if "humidity" in sensors:
            humidity = sense.get_humidity()
        if "pressure" in sensors:
            pressure = sense.get_pressure()

        reply_msg = ReadSensorResponse(content="reply", temperature=temperature, humidity=humidity, pressure=pressure)
            
        await responder.send_reply(reply_msg)
        await conn_mgr.log_activity(
            context.connection_record,
            "read_sensor_reply",
            context.connection_record.DIRECTION_SENT,
            {"content": "reply"},
        )
