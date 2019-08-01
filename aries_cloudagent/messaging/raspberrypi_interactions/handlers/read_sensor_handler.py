"""Basic message handler."""

from ...base_handler import BaseHandler, BaseResponder, RequestContext
from ...connections.manager import ConnectionManager

from ..messages.read_sensor import ReadSensor
from ..messages.read_sensor_reply import ReadSensorResponse

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

        self._logger.info("Received read sensor: %s", context.message.content)

        body = context.message.content
        read_temperature = context.message.read_temperature
        read_pressure = context.message.read_pressure
        read_humidity = context.message.read_humidity
        meta = {"content": body, 
                "read_temperature" : read_temperature,
                "read_pressure" : read_pressure, 
                "read_humidity" : read_humidity}

        # For Workshop: mark invitations as copyable
        if context.message.content and context.message.content.startswith("http"):
            meta["copy_invite"] = True

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

        reply = None
        temperature = None
        pressure = None
        humidity = None
        sense = SenseHat()
        SenseHat.clear()
        if read_temperature:
            temperature = sense.get_temperature()
        if read_humidity:
            humidity = sense.get_humidity()
        if read_pressure:
            pressure = sense.get_pressure()

        reply_msg = ReadSensorResponse(content="reply", temperature=temperature, humidity=humidity, pressure=pressure)
            
        await responder.send_reply(reply_msg)
        await conn_mgr.log_activity(
            context.connection_record,
            "read_sensor_reply",
            context.connection_record.DIRECTION_SENT,
            {"content": "reply"},
        )
