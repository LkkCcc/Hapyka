#!/usr/bin/env python
import datetime

from hapyka.utils.Config import Config

start_time = datetime.datetime.now()
config_container = Config()
version = "1.0.2 (release 3a)"
release = '''
Quotes!
Press F to pay respects to NKVD-bot (R.I.P 2017-2022)
'''

import logging
import sys

from hapyka.utils.logger import get_logger
logger = get_logger()

from hapyka.database.db import initialize
initialize()

from hapyka.classes.Haruka import Haruka

handler = logging.StreamHandler(sys.stdout)

bot_token = config_container.get("bot_tg_token")
bot = Haruka(bot_token)

finished_loading_time = datetime.datetime.now()
load_time = "{:.2f}".format(finished_loading_time.timestamp() - start_time.timestamp())

logger.info("Haruka v{} started successfully in {}s. Release: {}".format(version, load_time, release))
