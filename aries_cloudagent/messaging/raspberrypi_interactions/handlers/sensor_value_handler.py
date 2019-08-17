"""Basic message handler."""

from ...base_handler import BaseHandler, BaseResponder, RequestContext
from ...connections.manager import ConnectionManager

from ..messages.read_sensor import ReadSensor
from ..messages.sensor_value import SensorValue


class SensorValueHandler(BaseHandler):
    """Message handler class for basic messages."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Message handler logic for basic messages.

        Args:
            context: request context
            responder: responder callback
        """
        self._logger.debug(f"SensorValueHandler called with context {context}")
        assert isinstance(context.message, SensorValueHandler)


        temperature = context.message.temperature
        pressure = context.message.pressure
        humidity = context.message.humidity
        orientation = context.message.orientation
        accelerometer = context.message.accelerometer
        compass = context.message.stick_events
        gyroscope = context.message.gyroscope
        stick_events = context.message.stick_events
        pixels = context.message.pixels

        meta = {"temperature" : temperature,
                "pressure" : pressure, 
                "humidity" : humidity,
                "orientation" : orientation,
                "accelerometer" : accelerometer,
                "compass" : compass,
                "gyroscope" : gyroscope,
                "stick_events" : stick_events,
                "pixels" : pixels}

        conn_mgr = ConnectionManager(context)
        await conn_mgr.log_activity(
            context.connection_record,
            "sensor_value",
            context.connection_record.DIRECTION_RECEIVED,
            meta,
        )

        