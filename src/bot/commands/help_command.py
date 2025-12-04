import telegram as tg
import telegram.ext as tgx


class HelpCommand:
    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Help!")

