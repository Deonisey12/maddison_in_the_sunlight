MARKDOWN_V2 = "MarkdownV2"

class CreateState():
    ACTIVE = "active"
    MESSAGES_TO_DELETE = "messages_to_delete"
    TYPE = "type"
    IDS = "ids"
    TEXTS = "texts"


class ListState():
    ACTIVE = "active"
    TYPE = "type"
    ENTITY = "entity"


class Actions():
    CREATE = "create"
    LIST = "list"
    INVENTORY = "inventory"
    FORM = "form"

class UserState():
    FORM_STATE = "form_state"
    CREATE_STATE = "create_state"
    LIST_STATE = "list_state"
    INVENTORY_STATE = "inventory_state"

class InventoryState():
    ACTIVE = "active"
    USER_NAME = "user_name"
    ITEM_ID = "item_id"

class FormState():
    ACTIVE = "active"
    USER_NAME = "user_name"

class Commands():
    START = "start"
    TEST = "test"
    CREATE = "create"
    FORM = "form"
    LIST = "list"
    INVENTORY = "inventory"

    DESCRIPTIONS = {
        CREATE: "Cоздать сущность",
        LIST: "Cписок сущностей",
        FORM: "Form",
        INVENTORY: "Инвентарь",
    }

    @staticmethod
    def get_bot_commands():
        from telegram import BotCommand
        res = []
        for cmd in Commands.DESCRIPTIONS.keys():
            res.append(BotCommand(cmd, Commands.DESCRIPTIONS[cmd]))
        return res
