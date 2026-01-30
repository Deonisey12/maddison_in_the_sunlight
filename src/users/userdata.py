import datetime
import json
import os


class UserData():
    
    Path = 'local/users'
    
    def __init__(self, username: str):
        self.username = username

        self.character = None

        self.inGameData = datetime.datetime(1981, 12, 28)

        self.inventory = {}

        self.skills = []

        self.quests = []
        self.tasks = []
        self.settings = []

        self._scene = -1

        self.actions_max = 0
        self.actions = 0


    def AddItemToInventory(self, id, num = 1):
        if type(id) != str:
            id = str(id)

        if id in self.inventory.keys():
            self.inventory[id] += num
        else:
            self.inventory[id] = num

        self.Save()

    def RmItemFromInventory(self, id, num = 1):
        if type(id) != str:
            id = str(id)

        if id in self.inventory.keys():
            if self.inventory[id] < num:
                return False
            
            self.inventory[id] -= num
            if self.inventory[id] == 0:
                self.inventory.pop(id)

            self.Save()            
            return True
        return False

    def ForceRmItemFromInventory(self, id, num = 1):
        if type(id) != str:
            id = str(id)

        if id in self.inventory.keys():
            self.inventory[id] -= num
            
            if self.inventory[id] <= 0:
                self.inventory.pop(id)

            self.Save() 

    @property
    def Scene(self):
        return self._scene

    @Scene.setter
    def Scene(self, value: int):
        self._scene = value
        self.Save()

    def Save(self):
        os.makedirs(UserData.Path, exist_ok=True)
        with open(os.path.join(UserData.Path, self.username + '.json'), 'w') as f:
            res_dict = {}
            
            res_dict['username'] = self.username
            res_dict['inGameData'] = self.inGameData.isoformat()
            res_dict['character'] = self.character

            res_dict['actions_max'] = self.actions_max
            res_dict['actions'] = self.actions

            res_dict['scene'] = self._scene

            res_dict['inventory'] = []
            for item in self.inventory:
                res_dict['inventory'].append(f"{item}:{self.inventory[item]}")
                
            json.dump(res_dict, f)
    
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
        if 'actions_max' in json_dct and json_dct['actions_max']:
            ud.actions_max = json_dct['actions_max']
        if 'actions' in json_dct and json_dct['actions']:
            ud.actions = json_dct['actions']
        if 'character' in json_dct and json_dct['character']:
            ud.character = json_dct['character']
        if 'scene' in json_dct and json_dct['scene']:
            ud._scene = json_dct['scene']
        for inventory in json_dct.get('inventory', []):
            ud.inventory[inventory.split(':')[0]] = int(inventory.split(':')[1])
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

    @staticmethod
    def LoadByName(username: str):
        with open(f"local/users/{username}.json", "r") as f:
            data = f.read()
            js_data = json.loads(data)
            user_data = UserData.JsonDecoder(js_data)
        return user_data
