import sys
sys.path.append("src/bot")

import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from commands import BotCommands


class TelegramBot():

    def __init__(self, token_path=""):
        with open(token_path, "r") as f:
            self.__token = f.read()
            self.__cmd = BotCommands

        logging.basicConfig(
            format="%(asctime)s-%(name)s-%(levelname)s-%(message)s", level=logging.INFO
        )
        logging.getLogger("httpx").setLevel(logging.WARNING)
        self.logger = logging.getLogger(__name__)

    def Start(self):
        application = Application.builder().token(self.__token).build()

        application.add_handler(CommandHandler("start", self.__cmd.start))
        application.add_handler(CommandHandler("help", self.__cmd.help_command))

        application.add_handler(CommandHandler("create", self.__cmd.create))

        application.run_polling(allowed_updates=Update.ALL_TYPES)