"""Basic message handler."""

from ...base_handler import BaseHandler, BaseResponder, RequestContext
from ...connections.manager import ConnectionManager

from ..messages.display_message import DisplayMessage
from ...basicmessage.messages.basicmessage import BasicMessage

from sense_hat import SenseHat


class DisplayMessageHandler(BaseHandler):
    """Message handler class for basic messages."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Message handler logic for basic messages.

        Args:
            context: request context
            responder: responder callback
        """
        self._logger.debug(f"DisplayMessageHandler called with context {context}")
        assert isinstance(context.message, DisplayText)

        self._logger.info("Received message: %s", context.message.content)

        content = context.message.content
        scroll_speed = context.message.scroll_speed
        back_colour = context.message.back_colour
        text_colour = context.message.text_colour
        meta = {"content": content, 
                "scroll_speed" : scroll_speed,
                "text_colour" : text_colour, 
                "back_colour" : back_colour}

        # For Workshop: mark invitations as copyable
        if context.message.content and context.message.content.startswith("http"):
            meta["copy_invite"] = True

        conn_mgr = ConnectionManager(context)
        await conn_mgr.log_activity(
            context.connection_record,
            "display_message",
            context.connection_record.DIRECTION_RECEIVED,
            meta,
        )

        await responder.send_webhook(
            "display_message",
            {"message_id": context.message._id, "content": content, "state": "received"},
        )

        sense = SenseHat()
        sense.clear()
        sense.show_message(content, text_colour=text_colour, back_colour=back_colour, scroll_speed=scroll_speed)

        reply_msg = BasicMessage(content="DisplayMessage message received")
            
        await responder.send_reply(reply_msg)
        await conn_mgr.log_activity(
            context.connection_record,
            "message",
            context.connection_record.DIRECTION_SENT,
            {"content": "reply"},
        )
