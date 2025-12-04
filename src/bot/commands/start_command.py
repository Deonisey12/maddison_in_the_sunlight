import sys
sys.path.append("src/bot")

import telegram as tg
import telegram.ext as tgx

from .base_command import BaseCommand


class StartCommand(BaseCommand):
    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        await update.message.reply_html(
            rf"Hi {user.name}!"
        )

