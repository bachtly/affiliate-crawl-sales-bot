import bson
from bson.objectid import ObjectId

from config import config
from utils.database.Orm import Orm
from utils.logger.Logger import Logger


class ProductModel:
    def __init__(self):
        self.title = ''
        self.description = ''
        self.price_original = bson.Int64(0)
        self.price_discount = bson.Int64(0)
        self.url_original = ''
        self.url_affiliate = ''
        self.photos = []
        self.videos = []
        self.comments = []
        self.ratings = {
            '1': 0,
            '2': 0,
            '3': 0,
            '4': 0,
            '5': 0}
        self.product_id_ext = ''
        self.shop_id_ext = ''
        self.keyword = ''
        self.hashtag = ''

    def SetTitle(self, val):
        if type(val) is type(self.title):
            self.title = val
            return

        e = Exception('ProductModel.Title incorrect datatype')
        Logger().Error(str(e), {"title_type": type(self.title), "value_type": type(val)})
        raise e

    def SetDescription(self, val):
        if type(val) is type(self.description):
            self.description = val
            return

        e = Exception('ProductModel.Description incorrect datatype')
        Logger().Error(str(e), {"description_type": type(self.description), "value_type": type(val)})
        raise e

    def SetUrlOriginal(self, val):
        if type(val) is type(self.url_original):
            self.url_original = val
            return

        e = Exception('ProductModel.UrlOriginal incorrect datatype')
        Logger().Error(str(e), {"url_original_type": type(self.url_original), "value_type": type(val)})
        raise e

    def SetPhotos(self, val):
        if type(val) is type(self.photos):
            self.photos = val
            return

        e = Exception('ProductModel.Photos incorrect datatype')
        Logger().Error(str(e), {"photos_type": type(self.photos), "value_type": type(val)})
        raise e

    def SetPriceOriginal(self, val):
        if type(val) is type(self.price_original):
            self.price_original = val
            return None

        if type(val) is int:
            self.price_original = bson.Int64(val)
            return

        e = Exception('ProductModel.PriceOriginal incorrect datatype')
        Logger().Error(str(e), {"price_original_type": type(self.price_original), "value_type": type(val)})
        raise e

    def SetPriceDiscount(self, val):
        if type(val) is type(self.price_discount):
            self.price_discount = val
            return

        if type(val) is int:
            self.price_discount = bson.Int64(val)
            return

        e = Exception('ProductModel.PriceDiscount incorrect datatype')
        Logger().Error(str(e), {"price_discount_type": type(self.price_discount), "value_type": type(val)})
        raise e

    def SetKeyword(self, val):
        if type(val) is type(self.keyword):
            self.keyword = val
            return

        e = Exception('ProductModel.Keyword incorrect datatype')
        Logger().Error(str(e), {"keyword_type": type(self.keyword), "value_type": type(val)})
        raise e

    def SetHashtag(self, val):
        if type(val) is type(self.hashtag):
            self.hashtag = val
            return

        e = Exception('ProductModel.Hashtag incorrect datatype')
        Logger().Error({"hashtag_type": type(self.hashtag), "value_type": type(val)})
        raise e

    def Parse(self, productObject):
        self.SetTitle(productObject[config.PRODUCT_TITLE_KEY])
        self.SetDescription(productObject[config.PRODUCT_DESCRIPTION_KEY])
        self.SetUrlOriginal(productObject[config.PRODUCT_URL_ORIGINAL_KEY])
        self.SetPhotos(productObject[config.PRODUCT_PHOTOS_KEY])
        self.SetPriceOriginal(productObject[config.PRODUCT_PRICE_ORIGINAL_KEY])
        self.SetPriceDiscount(productObject[config.PRODUCT_PRICE_DISCOUNT_KEY])
        self.SetKeyword(productObject[config.PRODUCT_KEYWORD_KEY])
        self.SetHashtag(productObject[config.PRODUCT_HASHTAG_KEY])

    @staticmethod
    def GetProductFromId(database, id):
        with Orm(database, config.DB_PRODUCT_TABLE) as orm:
            products = orm.Find({'_id': ObjectId(id)})
            if not products:
                e = Exception('Product not found in database')
                Logger().Error(str(e), {'id': id, 'database': database})
                raise e

            productObject = products[0]
            Logger().Info("Success get product from db", productObject)

            product = ProductModel()
            product.Parse(productObject)

        return product

    ### This is a workaround for old modules, should not be used for incoming feature
    @staticmethod
    def GetRawProductFromId(database, id):
        with Orm(database, config.DB_PRODUCT_TABLE) as orm:
            products = orm.Find({'_id': ObjectId(id)})
            if not products:
                e = Exception('Product not found in database')
                Logger().Error(str(e), {'id': id, 'database': database})
                raise e

            productObject = products[0]
            Logger().Info("Success get product from db", productObject)

        return productObject
