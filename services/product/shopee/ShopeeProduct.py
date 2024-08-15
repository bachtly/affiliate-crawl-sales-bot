from random import randint

from services.adapters.ShopeeAdapter import ShopeeAdapter
from utils.environment.Environment import Environment
from utils.logger.Logger import Logger


class ShopeeProduct:
    def __init__(self, databaseName):
        self.PROVIDER_NAME = "shopee"
        self.databaseName = databaseName
        self.env = Environment(databaseName)

    def GetNewProduct(self):
        shopItems = self.env.GetShops().items()
        shopItem = list(shopItems)[randint(0, len(shopItems) - 1)]

        shop = shopItem[0]
        keywords = shopItem[1]
        keyword = keywords[randint(0, len(keywords) - 1)]

        with ShopeeAdapter(self.databaseName, shop, keyword) as adapter:
            newItemId = adapter.GetNewProduct()

        Logger().Info('Shopee get new product success', {"id": newItemId})
        return newItemId

    def GetProduceProviderName(self):
        return self.PROVIDER_NAME
