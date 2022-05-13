import datetime

import telegram

from hapyka.database.models.QuoteModel import QuoteModel
from hapyka.dictionaries.generic import  QUOTES_TMPL, NO_QUOTES, NO_QUOTES_SELF
from hapyka.database.db import get_transaction
from hapyka.utils.handlers.command.CommandHanlder import CommandHandler
from hapyka.utils.tg_utils import reply_text

enabled = True


class Quotes(CommandHandler):
    def __init__(self):
        self.enabled = enabled
        self.commands = ["quotes"]
        super().__init__()

    def handle_impl(self, update: telegram.Update, context):
        session, session_transaction = get_transaction()
        if update.message.reply_to_message is None:
            self_quotes = True
        else:
            self_quotes = False

        with session_transaction:
            quotes = []
            if self_quotes:
                user_quotes = session.query(QuoteModel).filter_by(
                    written_by=update.message.from_user.id).order_by(QuoteModel.when_written.asc()).all()
            else:
                user_quotes = session.query(QuoteModel).filter_by(
                    written_by=update.message.reply_to_message.from_user.id).order_by(QuoteModel.when_written.asc()).all()
            for aquote in user_quotes:
                quotes.append(str(aquote))
            if len(quotes) == 0:
                if self_quotes:
                    reply_text(update, context, NO_QUOTES_SELF)
                else:
                    reply_text(update, context, NO_QUOTES)
            else:
                reply_text(update, context, QUOTES_TMPL.format("\n".join(quotes)))

    def enable(self):
        return self.enabled
