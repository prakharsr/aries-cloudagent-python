"""Basic message handler."""

from ...base_handler import BaseHandler, BaseResponder, RequestContext
from ...connections.manager import ConnectionManager

from ..messages.set_pixels import SetPixels
from ...basicmessage.messages.basicmessage import BasicMessage

from sense_hat import SenseHat


class SetPixelsHandler(BaseHandler):
    """Message handler class for basic messages."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Message handler logic for basic messages.

        Args:
            context: request context
            responder: responder callback
        """
        self._logger.debug(f"SetPixelsHandler called with context {context}")
        assert isinstance(context.message, SetPixels)

        self._logger.info("Received pixels: %s", context.message.pixels)

        pixels = context.message.pixels
        meta = {"pixels": pixels}

        conn_mgr = ConnectionManager(context)
        await conn_mgr.log_activity(
            context.connection_record,
            "set_pixels",
            context.connection_record.DIRECTION_RECEIVED,
            meta,
        )

        await responder.send_webhook(
            "pixels",
            {"message_id": context.message._id, "pixels": pixels, "state": "received"},
        )

        sense = SenseHat()
        sense.clear()
        sense.set_pixels(pixels)

        reply_msg = BasicMessage(content="SetPixels message received")
            
        await responder.send_reply(reply_msg)
        await conn_mgr.log_activity(
            context.connection_record,
            "message",
            context.connection_record.DIRECTION_SENT,
            {"content": "reply"},
        )
