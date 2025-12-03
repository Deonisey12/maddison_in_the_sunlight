import sys
sys.path.append("src/bot")

import logging

from telegram import *
from telegram.ext import *

from functools import partial


from commands import BotCommands


class TelegramBot():

    def __init__(self, database, token_path=""):
        with open(token_path, "r") as f:
            self.__token = f.read()
            
        self.__cmd = BotCommands(database)

        logging.basicConfig(
            format="%(asctime)s-%(name)s-%(levelname)s-%(message)s", level=logging.INFO
        )
        logging.getLogger("httpx").setLevel(logging.WARNING)
        self.logger = logging.getLogger(__name__)

        self._app = Application.builder().token(self.__token).build()

    def addCmdHandlers(self):
        self._app.add_handler(CommandHandler("start", self.__cmd.start))
        self._app.add_handler(CommandHandler("test", self.__cmd.echo))
        self._app.add_handler(CommandHandler("create", self.__cmd.create))
        self._app.add_handler(CommandHandler("form", self.__cmd.test_form))

    def addCallbackHandlers(self):
        self._app.add_handler(CallbackQueryHandler(self.__cmd.button_callback))

    def Start(self):
        self.addCmdHandlers()
        self.addCallbackHandlers()
        self._app.run_polling(allowed_updates=Update.ALL_TYPES)