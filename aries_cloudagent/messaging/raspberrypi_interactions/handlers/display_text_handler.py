"""Basic message handler."""

from ...base_handler import BaseHandler, BaseResponder, RequestContext
from ...connections.manager import ConnectionManager

from ..messages.display_text import DisplayText
from ...basicmessage.messages.basicmessage import BasicMessage

from sense_hat import SenseHat


class DisplayTextHandler(BaseHandler):
    """Message handler class for basic messages."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Message handler logic for basic messages.

        Args:
            context: request context
            responder: responder callback
        """
        self._logger.debug(f"DisplayTextHandler called with context {context}")
        assert isinstance(context.message, DisplayText)

        self._logger.info("Received text: %s", context.message.content)

        body = context.message.content
        read_temperature = context.message.scroll_speed
        back_colour = context.message.back_colour
        text_colour = context.message.text_colour
        meta = {"content": body, 
                "scroll_speed" : scroll_speed,
                "text_colour" : text_colour, 
                "back_colour" : back_colour}

        # For Workshop: mark invitations as copyable
        if context.message.content and context.message.content.startswith("http"):
            meta["copy_invite"] = True

        conn_mgr = ConnectionManager(context)
        await conn_mgr.log_activity(
            context.connection_record,
            "display_text",
            context.connection_record.DIRECTION_RECEIVED,
            meta,
        )

        await responder.send_webhook(
            "display_text",
            {"message_id": context.message._id, "content": body, "state": "received"},
        )

        sense = SenseHat()
        sense.clear()
        sense.show_message(content, text_colour=text_colour, back_colour=back_colour, scroll_speed=scroll_speed)

        reply_msg = BasicMessage(content="Display Text Message received")
            
        await responder.send_reply(reply_msg)
        await conn_mgr.log_activity(
            context.connection_record,
            "message",
            context.connection_record.DIRECTION_SENT,
            {"content": "reply"},
        )
