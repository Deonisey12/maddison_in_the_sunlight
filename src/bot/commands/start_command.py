import sys
sys.path.append("src/bot")
sys.path.append("src/users")

import telegram as tg
import telegram.ext as tgx

from .base_command import BaseCommand
from users.userdata import UserData

class StartCommand(BaseCommand):
    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE, reply_markup: tg.ReplyKeyboardMarkup = None):
        user = update.effective_user
        context.user_data.clear()

        old_user_data = UserData.Load(user.username)
        if old_user_data is not None:
            UserData.Delete(user.username)
        
        user_data = UserData(user.username)
        user_data.Save()

        await update.message.reply_text("Регистрация завершена", reply_markup=reply_markup)
