# from utils.logger.logging import InfoLogger, ErrorLogger
# from utils.database.orm import ORM
# from FacebookPostWriter_deprecated import PostWriter
#
# from bson.objectid import ObjectId
#
#
# def create_post(req):
#     new_item_id = req['new_item_id']
#     database_name = req['database_name']
#     product_provider = req['product_provider']
#
#     product, res = get_product_from_id(database_name, new_item_id)
#     if res: ErrorLogger.error(''); return res
#
#     posts, res = PostWriter(product_provider).write_posts(product, 1)
#     if res: ErrorLogger.error(''); return res
#
#     res = add_posts_to_database(database_name, posts)
#     if res: ErrorLogger.error(''); return res
#
#     return None
#
#
# def get_product_from_id(database_name, new_item_id):
#     orm = ORM()
#     orm.connect(
#         uri='mongodb://root:root@localhost:27017',
#         db_name=database_name,
#         table_name='product_tab'
#     )
#
#     products, res = orm.find({'_id': ObjectId(new_item_id)})
#     if res: ErrorLogger.error(''); return None, res
#     if not products:
#         e = Exception('create_post.get_product_from_id.database_product_not_found.')
#         ErrorLogger.error(str(e) + f' Details: {str({"product_id": new_item_id})}')
#         return None, e
#
#     product = products[0]
#     InfoLogger.info(f"Got product: {product}")
#
#     return product, None
#
# def add_posts_to_database(database_name, posts):
#     orm = ORM()
#     orm.connect(
#         uri='mongodb://root:root@localhost:27017',
#         db_name=database_name,
#         table_name='post_tab'
#     )
#
#     inserted_ids, res = orm.insert(posts)
#     if res: ErrorLogger.error(''); return res
#     InfoLogger.info(f"Inserted posts to db, ids: {inserted_ids}")
#
#     return None
