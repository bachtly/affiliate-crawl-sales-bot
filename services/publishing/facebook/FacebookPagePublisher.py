from config import config
from services.adapters.FacebookPageAdapter import FacebookPageAdapter
from utils.database.Orm import Orm
from utils.environment.Environment import Environment
from utils.logger.Logger import Logger


class FacebookPagePublisher:
    PUBLISHER_NAME = 'FacebookPagePublisher'

    def __init__(self, databaseName):
        self.databaseName = databaseName
        self.env = Environment(databaseName)

    def PublishFacebookPage(self):
        # get all published product ids
        with Orm(self.databaseName, config.DB_PUBLISH_TABLE) as orm:
            publishings = orm.Find({config.PUBLISH_PUBLISHER_KEY: FacebookPagePublisher.PUBLISHER_NAME})
            publishedProductIds = [i[config.PUBLISH_PRODUCT_ID_KEY] for i in publishings]

        # get a product not yet published
        with Orm(self.databaseName, config.DB_PRODUCT_TABLE) as orm:
            products = orm.Find({'_id': {'$nin': publishedProductIds}}, limit=1, sortBy=('updated_at', -1))
            if len(products) <= 0:
                Logger().Warn("All product should have been already published", {
                    "published_product_ids": publishedProductIds,
                    'publisher': FacebookPagePublisher.PUBLISHER_NAME
                })
                return

        product = products[0]
        Logger().Info('Success get not-published product', product)

        with FacebookPageAdapter() as adapter:
            adapter.Login(self.env.GetEmailFacebook(), self.env.GetPasswordFacebook())
            adapter.VerifyLogin()
            adapter.RenderMainPage(self.env.GetPageIdFacebook(), self.env.GetPageNameFacebook())
            adapter.OpenTextArea(self.env.GetPageNameFacebook())
            adapter.Write(product[config.PRODUCT_POST_KEY], product[config.PRODUCT_PHOTOS_KEY])
            adapter.Publish()

        with Orm(self.databaseName, config.DB_PUBLISH_TABLE) as orm:
            publishing = {
                config.PUBLISH_PRODUCT_ID_KEY: product['_id'],
                config.PUBLISH_PUBLISHER_KEY: FacebookPagePublisher.PUBLISHER_NAME,
            }
            insertedIds = orm.Insert(publishing)

        Logger().Info('Success publish product', {
            'publisher': FacebookPagePublisher.PUBLISHER_NAME,
            'productId': product['_id'],
            'publishing_id': insertedIds
        })
