import datetime
import json
import os

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)

class UserData():
    
    Path = 'local/users'
    
    def __init__(self, username: str):
        self.username = username

        self.character = None

        self.inGameData = datetime.datetime(1981, 12, 28)

        self.inventory = []
        self.skills = []

        self.quests = []
        self.tasks = []
        self.settings = []

    def Save(self):
        os.makedirs(UserData.Path, exist_ok=True)
        with open(os.path.join(UserData.Path, self.username + '.json'), 'w') as f:
            json.dump(self.__dict__, f, cls=DateTimeEncoder)
    
    @staticmethod
    def Load(username: str) -> 'UserData':
        try:
            with open(os.path.join(UserData.Path, username + '.json'), 'r') as f:
                jsf = json.load(f)
            return UserData.JsonDecoder(jsf)
        except Exception as ex:
            return None

    @staticmethod
    def JsonDecoder(json_dct):
        ud = UserData(json_dct['username'])
        if 'inGameData' in json_dct and json_dct['inGameData']:
            if isinstance(json_dct['inGameData'], str):
                ud.inGameData = datetime.datetime.fromisoformat(json_dct['inGameData'])
            else:
                ud.inGameData = datetime.datetime(1981, 12, 28)
        if 'character' in json_dct and json_dct['character']:
            ud.character = json_dct['character']
        for inventory in json_dct.get('inventory', []):
            ud.inventory.append(inventory)
        for skill in json_dct.get('skills', []):
            ud.skills.append(skill)
        for quest in json_dct.get('quests', []):
            ud.quests.append(quest)
        for task in json_dct.get('tasks', []):
            ud.tasks.append(task)
        for setting in json_dct.get('settings', []):
            ud.settings.append(setting)
        return ud

    @staticmethod
    def Delete(username: str):
        file_path = os.path.join(UserData.Path, username + '.json')
        if os.path.exists(file_path):
            os.remove(file_path)

