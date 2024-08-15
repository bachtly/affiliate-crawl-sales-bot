from bson import ObjectId

from config import config
from config.config import *
from models.ProductModel import ProductModel
from utils.database.Orm import Orm
from utils.environment.Environment import Environment
from utils.logger.Logger import Logger


class FacebookPostWriter:
    def __init__(self, databaseName):
        self.databaseName = databaseName
        self.env = Environment(databaseName)

    def UpdateProductPostContent(self, productId):
        productObj = ProductModel.GetRawProductFromId(self.databaseName, productId)

        post = FacebookPostWriter.write(productObj)

        with Orm(self.databaseName, config.DB_PRODUCT_TABLE) as orm:
            query = {'_id': ObjectId(productId)}
            data = {'post': post}
            count = orm.Update(query=query, data=data)
            if count <= 0:
                e = Exception('Fail update post')
                Logger().Error(str(e), {'query': query, 'data': data})
                raise e

        Logger().Info("Success update product post", {'id': productId, 'post': post})

    @staticmethod
    def write(product):
        content = ''

        content += f'[{product[PRODUCT_TITLE_KEY].upper()}]'
        content += '\n'

        content += '---'
        content += '\n'

        content += f'MUA NGAY TẠI: {product[PRODUCT_URL_AFFILIATE_KEY]}'
        content += '\n'

        content += '---'
        content += '\n'

        content += f'{product[PRODUCT_DESCRIPTION_KEY]}'
        content += '\n'

        content += f'#{product[PRODUCT_HASHTAG_KEY]}'
        content += '\n'

        return content
