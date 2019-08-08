"""Basic message handler."""

from ...base_handler import BaseHandler, BaseResponder, RequestContext
from ...connections.manager import ConnectionManager

from ..messages.read_sensor import ReadSensor
from ..messages.sensor_value import SensorValue

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
            {"message_id": context.message._id, "sensors": sensors, "state": "received"},
        )

        sense = SenseHat()
        sense.clear()
        temperature = None
        humidity = None
        pressure = None
        orientation = None
        accelerometer = None
        compass = None
        gyroscope = None
        stick_events = []

        if "temperature" in sensors:
            temperature = sense.get_temperature()
        if "humidity" in sensors:
            humidity = sense.get_humidity()
        if "pressure" in sensors:
            pressure = sense.get_pressure()
        if "orientation" in sensors:
            orientation = sense.get_orientation_degrees()
        if "accelerometer" in sensors:
            accelerometer = sense.get_accelerometer_raw()
        if "compass" in sensors:
            compass = sense.get_compass_raw()
        if "gyroscope" in sensors:
            gyroscope = sense.get_gyroscope_raw()
        if "stick_event" in sensors:
            stick_event_objects = sense.stick.get_events()
            for event in stick_event_objects:
                event_dict = {}
                event_dict['timestamp'] = event.timestamp
                event_dict['direction'] = event.direction
                event_dict['action'] = event.action
                stick_event.append(event_dict)

        reply_msg = SensorValue(temperature=temperature, 
                                humidity=humidity, 
                                pressure=pressure,
                                orientation=orientation,
                                accelerometer=accelerometer,
                                compass=compass,
                                gyroscope=gyroscope,
                                stick_events=stick_events)
            
        await responder.send_reply(reply_msg)
        await conn_mgr.log_activity(
            context.connection_record,
            "sensor_value",
            context.connection_record.DIRECTION_SENT,
            {"content": "reply"},
        )
