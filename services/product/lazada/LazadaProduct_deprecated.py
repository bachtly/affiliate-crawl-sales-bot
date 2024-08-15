# from lazada_adapter import LazadaAdapter
# from utils.logger.logging import InfoLogger, ErrorLogger, InfoLogger
#
# from random import randint
#
# def get_lazada_product_info(req):
#     keywords = req['keywords']
#     database_name = req['database_name']
#
#     adapter = LazadaAdapter(database_name)
#
#     res = adapter.init()
#     InfoLogger.debug(f"res from adapter init: {res}")
#     if res: return None, res
#
#     keyword = keywords[randint(0, len(keywords) - 1)]
#     new_item_id, res = adapter.get_products(keyword)
#     InfoLogger.debug(f"res from adapter get product: {res}")
#     if res: return None, res
#
#     res = adapter.close()
#     if res: return None, res
#
#     return {"new_item_id": new_item_id}, None
