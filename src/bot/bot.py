import sys
sys.path.append("src/bot")

import logging

from telegram import *
from telegram.ext import *

from functools import partial


from cmd_handler import CmdHandler

class Commands():
    START = "start"
    TEST = "test"
    CREATE = "create"
    FORM = "form"
    LIST = "list"

    DESCRIPTIONS = {
        START: "начать работу",
        TEST: "echo",
        CREATE: "создать сущность",
        FORM: "вывод тестовой формы",
        LIST: "список сущностей по типу"
    }

    @staticmethod
    def Commands():
        res = []
        for cmd in Commands.DESCRIPTIONS.keys():
            res.append(BotCommand(cmd, Commands.DESCRIPTIONS[cmd]))

        return res

class TelegramBot():

    def __init__(self, database, token_path=""):
        with open(token_path, "r") as f:
            self.__token = f.read()
        self.__cmd = CmdHandler(database)

        logging.basicConfig(
            format="%(asctime)s-%(name)s-%(levelname)s-%(message)s", level=logging.INFO
        )
        logging.getLogger("httpx").setLevel(logging.WARNING)
        self.logger = logging.getLogger(__name__)

        self._app = Application.builder().token(self.__token).post_init(self.post_init).build()


    def addCmdHandlers(self):
        self._app.add_handler(CommandHandler(Commands.START, self.__cmd.start))
        self._app.add_handler(CommandHandler(Commands.TEST, self.__cmd.echo))
        self._app.add_handler(CommandHandler(Commands.CREATE, self.__cmd.create))
        self._app.add_handler(CommandHandler(Commands.FORM, self.__cmd.test_form))
        self._app.add_handler(CommandHandler(Commands.LIST, self.__cmd.list))

        self._app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.__cmd.message))


    def addCallbackHandlers(self):
        self._app.add_handler(CallbackQueryHandler(self.__cmd.button_callback))


    async def post_init(self, application: Application):
        await application.bot.set_my_commands(Commands.Commands())


    def Start(self):
        self.addCmdHandlers()
        self.addCallbackHandlers()

        self._app.run_polling(allowed_updates=Update.ALL_TYPES)