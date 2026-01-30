from src.users import UserData


class Function:
    def execute(self, user_data: UserData, *_vaarg) -> bool:
        raise NotImplementedError("Method 'execute' must be implemented in subclass")