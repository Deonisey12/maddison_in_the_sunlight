import sys
sys.path.append("src/bot")

import logging

from telegram import *
from telegram.ext import *

from functools import partial


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

        self._app = Application.builder().token(self.__token).build()

    def addCmdHandlers(self):
        self._app.add_handler(CommandHandler("start", partial(self.__cmd.start, self.__cmd)))
        self._app.add_handler(CommandHandler("test", partial(self.__cmd.echo, self.__cmd)))
        self._app.add_handler(CommandHandler("create", partial(self.__cmd.create, self.__cmd)))
        self._app.add_handler(CommandHandler("form", partial(self.__cmd.test_form, self.__cmd)))

    def addCallbackHandlers(self):
        self._app.add_handler(CallbackQueryHandler(partial(self.__cmd.button_callback, self.__cmd)))

    def Start(self):
        self.addCmdHandlers()
        self.addCallbackHandlers()
        self._app.run_polling(allowed_updates=Update.ALL_TYPES)