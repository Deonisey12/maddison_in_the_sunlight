from generators.generator import Generator

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


class BotCommands():

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user
        await update.message.reply_html(
            rf"Hi {user.mention_html()}!",
            # reply_markup=ForceReply(selective=True),
        )

    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Help!")

    async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(update.message.text)

    async def create(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        gen = Generator()
        request = ' '.join(update.message.text.split(' ')[1:])
        request = request.split('#')
        print(request)
        try:
            entity = gen.Create(*request)
            entity.SaveToJson()
            await update.message.reply_text("Создано")
        except Exception as ex:
            await update.message.reply_text(f"не удалось ({ex.__str__})")