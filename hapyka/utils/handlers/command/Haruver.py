from hapyka.dictionaries.generic import HARUKA_VER_TEMPLATE
from hapyka.utils.handlers.command.CommandHanlder import CommandHandler
from hapyka.utils.tg_utils import reply_text
from __main__ import version, release
enabled = True


class Haruver(CommandHandler):
    def __init__(self):
        self.enabled = enabled
        self.commands = ["ver", "version", "nkvdver", "haruver"]
        super().__init__()

    def handle_impl(self, update, context):
        reply_text(update, context, HARUKA_VER_TEMPLATE.format(version, release))

    def enable(self):
        return self.enabled
