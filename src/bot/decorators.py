import sys
sys.path.append("src/bot")

import logging
import telegram as tg
import telegram.ext as tgx
from functools import wraps


logger = logging.getLogger(__name__)


def delete_command_message(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        update = kwargs.get('update')
        if not update:
            if len(args) > 1:
                update = args[1]
            elif len(args) > 0:
                update = args[0]
        
        try:
            await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Ошибка при выполнении команды: {e}", exc_info=True)
            raise
        
        if update and update.message:
            try:
                await update.message.delete()
            except tg.error.BadRequest as e:
                if "message to delete not found" in str(e).lower():
                    logger.debug("Сообщение уже было удалено")
                elif "not enough rights" in str(e).lower():
                    logger.warning("Недостаточно прав для удаления сообщения")
                else:
                    logger.warning(f"Не удалось удалить сообщение: {e}")
            except Exception as e:
                logger.warning(f"Неожиданная ошибка при удалении сообщения: {e}")
    
    return wrapper
