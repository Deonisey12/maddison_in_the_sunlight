import sys

sys.path.append("src/bot")
sys.path.append("src/entities")

from entities.database import Database
import telegram as tg
import telegram.ext as tgx

from cmd_handler import CmdHandler
from cmd_dictionary import UserData, CreateState, MARKDOWN_V2, Commands
from commands.base_command import BaseCommand
from messages import CreateHandleMessages

class LocalMessageHandler(BaseCommand):
    def __init__(self, database: Database, cmd: CmdHandler):
        self._database = database
        self._cmd = cmd
        self._create_handle_messages = CreateHandleMessages(database)

    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        message_text = update.message.text

        state = context.user_data.get(UserData.CREATE_STATE)
        if not state or not state.get(CreateState.ACTIVE):
            if message_text == Commands.DESCRIPTIONS[Commands.CREATE]:
                await self._cmd.create(update, context)
                return
            elif message_text == Commands.DESCRIPTIONS[Commands.LIST]:
                await self._cmd.list(update, context)
                return
            elif message_text == Commands.DESCRIPTIONS[Commands.TEST]:
                await self._cmd.echo(update, context)
                return
            elif message_text == Commands.DESCRIPTIONS[Commands.INVENTORY]: 
                return
            return

        if state.get(CreateState.ACTIVE):
            await self._create_handle_messages.execute(update, context)
            return

        

