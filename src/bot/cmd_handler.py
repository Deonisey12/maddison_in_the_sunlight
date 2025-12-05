import sys
sys.path.append("src/bot")

import telegram as tg
import telegram.ext as tgx

from entities.database import Database
from callback import CallbackHandler
from decorators import delete_command_message
from commands import (
    StartCommand,
    HelpCommand,
    EchoCommand,
    CreateCommand,
    TestFormCommand,
    ListCommand,
    MessageCommand,
)


class CmdHandler:
    
    def __init__(self, database: Database):
        self._start_command = StartCommand()
        self._help_command = HelpCommand()
        self._echo_command = EchoCommand()
        self._create_command = CreateCommand(database)
        self._test_form_command = TestFormCommand(database)
        self._callback_handler = CallbackHandler(database)
        self._list_command = ListCommand(database)
        self._message_command = MessageCommand(database)

    @delete_command_message
    async def start(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        await self._start_command.execute(update, context)

    @delete_command_message
    async def help_command(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        await self._help_command.execute(update, context)

    @delete_command_message
    async def echo(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        await self._echo_command.execute(update, context)

    @delete_command_message
    async def create(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        await self._create_command.execute(update, context)

    @delete_command_message
    async def test_form(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        await self._test_form_command.execute(update, context)

    @delete_command_message
    async def list(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        await self._list_command.execute(update, context)

    async def message(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        await self._message_command.execute(update, context)

    async def button_callback(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        await self._callback_handler.execute(update, context)
