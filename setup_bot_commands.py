import requests
import os
import sys
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(SCRIPT_DIR, ".token")
BOT_FILE = os.path.join(SCRIPT_DIR, "src", "bot", "bot.py")

with open(TOKEN_PATH, "r") as f:
    TOKEN = f.read().strip()

with open(BOT_FILE, "r", encoding="utf-8") as f:
    source = f.read()

command_pattern = r'CommandHandler\("([^"]+)"'
matches = re.findall(command_pattern, source)

descriptions = {
    "start": "начать работу",
    "test": "echo",
    "create": "создать сущность",
    "form": "вывод тестовой формы",
    "list": "список сущностей по типу"
}

commands = [{"command": cmd, "description": descriptions.get(cmd, "команда бота")} for cmd in matches]

url = f"https://api.telegram.org/bot{TOKEN}/setMyCommands"
response = requests.post(url, json={"commands": commands})

result = response.json()
if result.get("ok"):
    print(f"Команды бота успешно установлены! ({len(commands)} команд)")
else:
    print(f"Ошибка: {result.get('description', 'Неизвестная ошибка')}")
    sys.exit(1)

