import sys
import types
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
        CREATE: "создать сущность",
        LIST: "список сущностей по типу",
        TEST: "echo",
    }

    @staticmethod
    def get_bot_commands():
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

        menu = [[InlineKeyboardButton("Создать сущность", callback_data="create_entity")],
                     [InlineKeyboardButton("Список сущностей", callback_data="list_entities")]]
        reply_markup = InlineKeyboardMarkup(menu)
        self._app.bot.set_chat_menu_button(reply_markup)


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
        try:
            scope = BotCommandScopeDefault()
            commands = Commands.get_bot_commands()
                
            await application.bot.delete_my_commands(scope=scope)
            await application.bot.set_my_commands(commands, scope=scope)
            await application.bot.set_chat_menu_button()
            
        except Exception as e:
            self.logger.error(f"Ошибка при установке команд бота: {e}", exc_info=True)


    def Start(self):
        self.addCmdHandlers()
        self.addCallbackHandlers()

        self._app.run_polling(allowed_updates=Update.ALL_TYPES)