from __main__ import config_container
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

import hapyka.utils.logger
from hapyka.dictionaries.generic import REPOSTER_CAPTION_TEMPLATE, REPOSTER_INLINE_MARKER, \
    REPOSTER_DISCARD_CALLBACK_DATA_MARKED
from hapyka.dictionaries.internal import HANDLERS_REPOSTER_DISCARD
from hapyka.utils.handlers.HaruHandler import HaruHandler
from hapyka.utils.tg_utils import get_sender_by_update, get_chat_by_update

enabled = True
logger = hapyka.utils.logger.get_logger()
reposter_from_label = "reposter/from"
reposter_to_label = "reposter/to"


class Reposter(HaruHandler):
    def __init__(self):
        self.reposter_from = None
        self.reposter_to = None
        self.reposter_control = None
        self.reposter_anon = None
        super().__init__()

    def enable(self):
        if not enabled:
            return False, "Disabled manually"
        self.reposter_anon = config_container.get("reposter/anon")
        if not self.reposter_anon or self.reposter_anon is None or not isinstance(self.reposter_anon, list):
            return False, "Misconfigured reposter/anon"
        self.reposter_from = config_container.get("reposter/from")
        if not self.reposter_from or self.reposter_from is None or not isinstance(self.reposter_from, list):
            return False, "Misconfigured reposter/from"
        self.reposter_to = config_container.get("reposter/to")
        if not self.reposter_to or self.reposter_to is None or not isinstance(self.reposter_to, list):
            return False, "Misconfigured reposter/to"
        self.reposter_control = config_container.get("reposter/control")
        if not self.reposter_control or self.reposter_control is None or not isinstance(self.reposter_control, list):
            return False, "Misconfigured reposter/control"
        return True

    def generate_markup(self):
        keyboard = [[]]
        for achat in self.reposter_to:
            keyboard[0].append(InlineKeyboardButton(text=achat[1], callback_data="{}{}".format(REPOSTER_INLINE_MARKER,
                                                                                               achat[0])))
        keyboard[0].append(
            InlineKeyboardButton(text=HANDLERS_REPOSTER_DISCARD, callback_data=REPOSTER_DISCARD_CALLBACK_DATA_MARKED))
        markup = InlineKeyboardMarkup(inline_keyboard=keyboard, one_time_keyboard=True, resize_keyboard=True)
        return markup

    def handle_impl(self, update, context):
        chat_id = update.effective_chat.id
        if chat_id in self.reposter_from:
            if update.message is not None:
                image_id = update.message.photo[-1].file_id
                caption = REPOSTER_CAPTION_TEMPLATE.format(get_sender_by_update(update, with_id=False,
                                                                                with_username=False),
                                                           get_chat_by_update(update, with_id=False))
                for achat in self.reposter_control:
                    context.bot.send_photo(achat, photo=image_id, caption=caption, reply_markup=self.generate_markup())
