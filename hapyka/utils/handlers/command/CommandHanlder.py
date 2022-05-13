from hapyka.utils.handlers.HaruHandler import HaruHandler


class CommandHandler(HaruHandler):
    def __init__(self):
        try:
            self.commands
        except AttributeError:
            self.enabled = False, "Supported commands are not specified for CommandHandler."
        super().__init__()

    def __handle__(self, update, context):
        message_text = update.message.text.lower()
        for command in self.commands:
            if message_text == "/{command}".format(command=command) or \
                    "/{command}@".format(command=command) in message_text:
                self.handle_impl(update, context)
                return

    def enable(self):
        return self.enabled