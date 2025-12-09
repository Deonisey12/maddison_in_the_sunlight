import sys
sys.path.append("src/bot")

import logging

import telegram as tg
import telegram.ext as tgx

from cmd_handler import CmdHandler
from cmd_dictionary import Commands
from message_handler import LocalMessageHandler

class TelegramBot():

    def __init__(self, database, token_path=""):
        with open(token_path, "r") as f:
            self.__token = f.read()

        logging.basicConfig(
            format="%(asctime)s-%(name)s-%(levelname)s-%(message)s", level=logging.INFO
        )
        logging.getLogger("httpx").setLevel(logging.WARNING)
        self.logger = logging.getLogger(__name__)

        self._reply_markup = tg.ReplyKeyboardMarkup(
            [[tg.KeyboardButton(c)] for c in Commands.DESCRIPTIONS.values()]
        )
        self.__cmd = CmdHandler(database, self._reply_markup)
        self.__msg = LocalMessageHandler(database, self.__cmd)

        self._app = tgx.Application.builder().token(self.__token).post_init(self.post_init).build()
        


    def addCmdHandlers(self):
        self._app.add_handler(tgx.CommandHandler(Commands.START, self.__cmd.start))
        self._app.add_handler(tgx.CommandHandler(Commands.TEST, self.__cmd.echo))
        self._app.add_handler(tgx.CommandHandler(Commands.CREATE, self.__cmd.create))
        self._app.add_handler(tgx.CommandHandler(Commands.FORM, self.__cmd.test_form))
        self._app.add_handler(tgx.CommandHandler(Commands.LIST, self.__cmd.list))

        self._app.add_handler(tgx.MessageHandler(tgx.filters.TEXT & ~tgx.filters.COMMAND, self.__msg.execute))
        

    def addCallbackHandlers(self):
        self._app.add_handler(tgx.CallbackQueryHandler(self.__cmd.button_callback))


    async def post_init(self, application: tgx.Application):
        try:
            scope = tg.BotCommandScopeDefault()
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