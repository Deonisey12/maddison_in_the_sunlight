import os

from bot.bot import *
from entities.database import Database

if __name__ == "__main__":

    database = Database()
    database.Load()

    # database.CreateEntity("Scene", 0, "Test main", "Test main. Test mainmain!")
    # print(database.GetEntityById('Scene', 5))

    # database.CreateEntity("Scene", 0, "Test Form", "Test form description")
    # database.CreateEntity("Scene", 1, "Button 1", "Test Button 1. Test Button 1!")
    # database.CreateEntity("Scene", 2, "Button 2", "Test Button 2. Test Button 2!")

    vtm_bot = TelegramBot(database, os.path.join(os.getcwd(),".token"))
    vtm_bot.Start()
