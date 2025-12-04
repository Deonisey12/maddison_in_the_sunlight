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
    TEST_FORM = "test_form"
    LIST = "list"

class UserData():
    FORM_ACTIONS = "form_actions"
    CREATE_STATE = "create_state"
    LIST_STATE = "list_state"
