"""Raspberry Pi admin routes."""

from aiohttp import web
from aiohttp_apispec import docs, request_schema

from marshmallow import fields, Schema

from ...storage.error import StorageNotFoundError

from ..connections.manager import ConnectionManager
from ..connections.models.connection_record import ConnectionRecord

from .messages.read_sensor import ReadSensor


@docs(tags=["read_sensor"], summary="Read temperature locally")
async def read_temperature(request: web.BaseRequest):
    """
    Request handler for retrieving local sensor data.

    Args:
        request: aiohttp request object

    """
    context = request.app["request_context"]
    sense = SenseHat()
    temperature = sense.get_temperature()

    return web.json_response({"temperature", temperature})


@docs(tags=["read_sensor"], summary="Send a read_sensor message to a connection")
# @request_schema(ReadSensorSchema())
async def connections_send_read_sensor_request(request: web.BaseRequest):
    """
    Request handler for sending a raspberry pi read Sensor request to a connection.

    Args:
        request: aiohttp request object

    """
    context = request.app["request_context"]
    connection_id = request.match_info["id"]
    outbound_handler = request.app["outbound_message_router"]
    params = await request.json()

    try:
        connection = await ConnectionRecord.retrieve_by_id(context, connection_id)
    except StorageNotFoundError:
        raise web.HTTPNotFound()

    if connection.is_ready:
        msg = ReadSensor(sensors=params["sensors"])
        await outbound_handler(msg, connection_id=connection_id)

        conn_mgr = ConnectionManager(context)
        await conn_mgr.log_activity(
            connection,
            "read_sensor",
            connection.DIRECTION_SENT,
            {"sensors": params["sensors"]},
        )

    return web.json_response({})

@docs(tags=["display_message"], summary="Send a display_message message to a connection")
# @request_schema(ReadSensorSchema())
async def connections_send_display_message_request(request: web.BaseRequest):
    """
    Request handler for sending a raspberry pi read Sensor requestto a connection.

    Args:
        request: aiohttp request object

    """
    context = request.app["request_context"]
    connection_id = request.match_info["id"]
    outbound_handler = request.app["outbound_message_router"]
    params = await request.json()

    try:
        connection = await ConnectionRecord.retrieve_by_id(context, connection_id)
    except StorageNotFoundError:
        raise web.HTTPNotFound()

    if connection.is_ready:
        msg = DisplayMessage(content=params["content"],
                            scroll_speed=params["scroll_speed"],
                            text_colour=params["text_colour"],
                            back_colour=params["back_colour"])
        await outbound_handler(msg, connection_id=connection_id)

        conn_mgr = ConnectionManager(context)
        await conn_mgr.log_activity(
            connection,
            "display_message",
            connection.DIRECTION_SENT,
            {"content": params["content"]},
        )

    return web.json_response({})

@docs(tags=["display_letter"], summary="Send a display_letter message to a connection")
# @request_schema(ReadSensorSchema())
async def connections_send_display_letter_request(request: web.BaseRequest):
    """
    Request handler for sending a raspberry pi read Sensor requestto a connection.

    Args:
        request: aiohttp request object

    """
    context = request.app["request_context"]
    connection_id = request.match_info["id"]
    outbound_handler = request.app["outbound_message_router"]
    params = await request.json()

    try:
        connection = await ConnectionRecord.retrieve_by_id(context, connection_id)
    except StorageNotFoundError:
        raise web.HTTPNotFound()

    if connection.is_ready:
        msg = DisplayLetter(letter=params["letter"],
                            text_colour=params["text_colour"],
                            back_colour=params["back_colour"])
        await outbound_handler(msg, connection_id=connection_id)

        conn_mgr = ConnectionManager(context)
        await conn_mgr.log_activity(
            connection,
            "display_letter",
            connection.DIRECTION_SENT,
            {"content": params["letter"]},
        )

    return web.json_response({})

@docs(tags=["set_pixels"], summary="Send a set_pixels message to a connection")
async def connections_send_set_pixels_request(request: web.BaseRequest):
    """
    Request handler for sending a raspberry pi read Sensor requestto a connection.

    Args:
        request: aiohttp request object

    """
    context = request.app["request_context"]
    connection_id = request.match_info["id"]
    outbound_handler = request.app["outbound_message_router"]
    params = await request.json()

    try:
        connection = await ConnectionRecord.retrieve_by_id(context, connection_id)
    except StorageNotFoundError:
        raise web.HTTPNotFound()

    if connection.is_ready:
        msg = SetPixels(pixels=params["pixels"])
        await outbound_handler(msg, connection_id=connection_id)

        conn_mgr = ConnectionManager(context)
        await conn_mgr.log_activity(
            connection,
            "set_pixels",
            connection.DIRECTION_SENT,
            {"content": params["letter"]},
        )

    return web.json_response({})

async def register(app: web.Application):
    """Register routes."""

    app.add_routes(
        [
            web.get("/read_temperature", read_temperature),
            web.post("/connections/{id}/read_sensor", connections_send_read_sensor_request),
            web.post("/connections/{id}/display_message", connections_send_display_message_request),
            web.post("/connections/{id}/display_letter", connections_send_display_letter_request),
            web.post("/connections/{id}/set_pixels", connections_send_set_pixels_request),
        ]
    )


