"""Raspberry Pi admin routes."""

from aiohttp import web
from aiohttp_apispec import docs, request_schema

from marshmallow import fields, Schema

from ...storage.error import StorageNotFoundError

from ..connections.manager import ConnectionManager
from ..connections.models.connection_record import ConnectionRecord

from .messages.read_sensor import ReadSensor


# class ReadSensorSchema(Schema):
#     """Request schema for sending a message."""

#     content = fields.Str()


@docs(tags=["read_sensor"], summary="Send a read_sensor message to a connection")
# @request_schema(ReadSensorSchema())
async def connections_send_read_sensor_request(request: web.BaseRequest):
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
        msg = ReadSensor(content=params["content"])
        await outbound_handler(msg, connection_id=connection_id)

        conn_mgr = ConnectionManager(context)
        await conn_mgr.log_activity(
            connection,
            "read_sensor",
            connection.DIRECTION_SENT,
            {"content": params["content"]},
        )

    return web.json_response({})

@docs(tags=["display_text"], summary="Send a display_text message to a connection")
# @request_schema(ReadSensorSchema())
async def connections_send_display_text_request(request: web.BaseRequest):
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
        msg = DisplayText(content=params["content"])
        await outbound_handler(msg, connection_id=connection_id)

        conn_mgr = ConnectionManager(context)
        await conn_mgr.log_activity(
            connection,
            "display_text",
            connection.DIRECTION_SENT,
            {"content": params["content"]},
        )

    return web.json_response({})


async def register(app: web.Application):
    """Register routes."""

    app.add_routes(
        [web.post("/connections/{id}/read_sensor", connections_send_read_sensor_request)]
    )

    app.add_routes(
        [web.post("/connections/{id}/display_text", connections_send_display_text_request)]
    )


