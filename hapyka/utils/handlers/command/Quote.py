import datetime

import telegram

from hapyka.database.models.QuoteModel import QuoteModel
from hapyka.dictionaries.generic import WHERE_IS_THE_MESSAGE, QUOTED
from hapyka.database.db import get_transaction
from hapyka.utils.handlers.command.CommandHanlder import CommandHandler
from hapyka.utils.tg_utils import reply_text, get_sender_by_message

enabled = True


class Quote(CommandHandler):
    def __init__(self):
        self.enabled = enabled
        self.commands = ["quote"]
        super().__init__()

    def handle_impl(self, update: telegram.Update, context):
        session, session_transaction = get_transaction()
        msg_to_quote = update.message.reply_to_message
        msg_to_quote_text = msg_to_quote.text
        if not msg_to_quote_text or msg_to_quote_text is None:
            msg_to_quote_text = msg_to_quote.caption
            if not msg_to_quote_text or msg_to_quote_text is None:
                reply_text(update, context, WHERE_IS_THE_MESSAGE)
        quoted_by = update.message.from_user.id
        written_by = msg_to_quote.from_user.id
        when_quoted = datetime.datetime.utcnow()
        when_written = msg_to_quote.date
        quote = msg_to_quote_text
        with session_transaction:
            quote_obj = QuoteModel(quoted_by_id=quoted_by, written_by=written_by,
                                   when_written=when_written, when_quoted=when_quoted,
                                   quote=quote, quoted_by_text=get_sender_by_message(update.message)
                                   )
            session.add(quote_obj)
        reply_text(update, context, QUOTED)

    def enable(self):
        return self.enabled
