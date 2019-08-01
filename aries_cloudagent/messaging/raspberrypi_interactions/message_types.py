"""Message type identifiers for raspberry-pi."""

MESSAGE_FAMILY = "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/raspberrypi-interactions/1.0"

READ_SENSOR = f"{MESSAGE_FAMILY}/read_sensor"
READ_SENSOR_RESPONSE = f"{MESSAGE_FAMILY}/read_sensor_response"
DISPLAY_TEXT = f"{MESSAGE_FAMILY}/display_text"

MESSAGE_TYPES = {
	READ_SENSOR: "aries_cloudagent.messaging.raspberrypi_interactions." + "messages.read_sensor.ReadSensor",
    READ_SENSOR_RESPONSE: "aries_cloudagent.messaging.raspberrypi_interactions." +"messages.read_sensor_response.ReadSensorResponse",
    DISPLAY_TEXT: "aries_cloudagent.messaging.raspberrypi_interactions." + "messages.display_text.DisplayText"
}
