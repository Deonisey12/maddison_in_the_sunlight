import json, os

from generators.generator import Generator
from generators.item import Item

from bot.bot import *

if __name__ == "__main__":
    # generator = Generator()

    # item = generator.Create("Item", "test_item", disc="test_item_disc")

    # item.SaveToJson()
    # print(item)

    # pth = os.path.join(os.getcwd(), "local/items")
    # files = os.listdir(pth)
    # files = [os.path.join(pth, item) for item in files]

    # for f in files:
    #     with open(f, "r") as d:
    #         data = d.read()
    #         s = json.loads(data, object_hook=Item.JsonDecoder)
    #     print(s)
    #     os.remove(f)

    vtm_bot = TelegramBot(os.path.join(os.getcwd(),".token"))
    vtm_bot.Start()



