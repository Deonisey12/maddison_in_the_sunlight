import sys
sys.path.append("src/bot")

import telegram as tg
import telegram.ext as tgx


class BaseCallback:
    async def execute(self, update: tg.Update, context: tgx.ContextTypes.DEFAULT_TYPE, data: str):
        raise NotImplementedError("Subclasses must implement execute method")

