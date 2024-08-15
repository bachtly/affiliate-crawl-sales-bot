from bson.objectid import ObjectId

from config import config
from models.ProductModel import ProductModel
from services.adapters.AccesstradeAdapter import AccesstradeAdapter
from utils.database.Orm import Orm
from utils.environment.Environment import Environment
from utils.logger.Logger import Logger


class AccesstradeLink:
    def __init__(self, databaseName, productProvider):
        self.databaseName = databaseName
        self.env = Environment(databaseName)
        self.productProvider = productProvider

    def UpdateProductAffiliateUrl(self, productId):
        product = ProductModel.GetProductFromId(self.databaseName, productId)

        with AccesstradeAdapter(self.productProvider) as adapter:
            urlAffiliate = adapter.GetAffiliateUrl(product.url_original)

        with Orm(self.databaseName, config.DB_PRODUCT_TABLE) as orm:
            query = {'_id': ObjectId(productId)}
            data = {'url_affiliate': urlAffiliate}
            count = orm.Update(query=query, data=data)
            if count <= 0:
                e = Exception('Fail update url affiliate')
                Logger().Error(str(e), {'query': query, 'data': data})
                raise e

        Logger().Info("Success update product affiliate url", {'id': productId, 'url_affiliate': urlAffiliate})
