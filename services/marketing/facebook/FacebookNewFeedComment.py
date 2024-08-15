from bson.objectid import ObjectId
from utils.logger.logging import InfoLogger, ErrorLogger

from config.config import *
from services.marketing.facebook.FacebookNewfeedAdapter import FacebookNewfeedAdapter
from utils.database.Orm import Orm
from utils.environment.Environment import Environment


class FacebookNewFeedComment:
    def marketing_newfeed_page_comment(
        self,
        email,
        password,
        page_name,
        page_id,
        database_name,
        viral_page_names,
    ):
        env = Environment(database_name)
        productId, res = env.getRecentPublishing()
        if res:
            ErrorLogger.error('module.marketing_newfeed_page_comment')
            return res

        product, res = self.get_product(productId, database_name)
        if res:
            ErrorLogger.error('marketing_newfeed_page_comment.fail_get_product')
            return res

        adapter = FacebookNewfeedAdapter(email, password, page_name, page_id, viral_page_names)
        res = self.write_newfeed_page_comment(product, adapter)
        if res:
            ErrorLogger.error('marketing_newfeed_page_comment.fail_writing_comments')
            return res

        InfoLogger.info('marketing_newfeed_page_comment.success')

        return None

    def get_product(self, product_id, database_name):
        orm = Orm()
        orm.Connect(
            uri='mongodb://root:root@localhost:27017',
            db_name=database_name,
            table_name=DB_PRODUCT_TABLE
        )

        products, res = orm.Find({'_id': ObjectId(product_id)})
        if res:
            return None, res

        if len(products) == 0:
            err = Exception(f'no product with id {product_id} in db')
            ErrorLogger.error(
                f'marketing_newfeed_page_comment.get_product.fail. Details {str({"error": str(err)})}')
            return None, err

        return products[0], None

    def write_newfeed_page_comment(self, product, adapter):
        res = adapter.init()
        if res:
            ErrorLogger.error('module.marketing_newfeed_page_comment.write_newfeed_page_comment.fail_init_adapter')
            return None, res

        res = adapter.write_comment(product)
        if res:
            ErrorLogger.error('module.marketing_newfeed_page_comment.write_newfeed_page_comment.fail_write_comment')
            return None, res

        res = adapter.close()
        if res:
            ErrorLogger.error('module.marketing_newfeed_page_comment.write_newfeed_page_comment.fail_close')
            return None, res

        return None
