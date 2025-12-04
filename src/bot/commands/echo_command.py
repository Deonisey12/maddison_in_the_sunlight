import sys
sys.path.append("src/bot")

import telegram as tg
import telegram.ext as tgx

from .base_command import BaseCommand


class EchoCommand(BaseCommand):
    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(update.message.text)

