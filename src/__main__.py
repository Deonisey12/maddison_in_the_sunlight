import os

from bot.bot import *
from entities.database import Database

if __name__ == "__main__":

    database = Database()
    database.Load()

    # database.CreateEntity("Scene", 0, "Test main", "Test main. Test mainmain!")

    # print(database.GetEntityById('Scene', 5))

    vtm_bot = TelegramBot(os.path.join(os.getcwd(),".token"))
    vtm_bot.Start()



