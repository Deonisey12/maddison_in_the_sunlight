import sys
sys.path.append("src/bot")

from entities.database import Database
import telegram as tg
import telegram.ext as tgx

from commands import (
    StartCommand,
    HelpCommand,
    EchoCommand,
    CreateCommand,
    TestFormCommand,
    ButtonCallbackCommand,
    ListCommand,
    MessageCommand,
)


class BotCommands:

    def __init__(self, database: Database):
        self._database = database
        
        self._start_command = StartCommand()
        self._help_command = HelpCommand()
        self._echo_command = EchoCommand()
        self._create_command = CreateCommand(database)
        self._test_form_command = TestFormCommand(database)
        self._button_callback_command = ButtonCallbackCommand(database)
        self._list_command = ListCommand()
        self._message_command = MessageCommand(database)

    async def start(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        await self._start_command.execute(update, context)

    async def help_command(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        await self._help_command.execute(update, context)

    async def echo(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        await self._echo_command.execute(update, context)

    async def create(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        await self._create_command.execute(update, context)

    async def test_form(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        await self._test_form_command.execute(update, context)

    async def button_callback(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        await self._button_callback_command.execute(update, context)

    async def list(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        await self._list_command.execute(update, context)

    async def message(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        await self._message_command.execute(update, context)
