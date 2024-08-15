# from utils.logger.Logger import Logger
#
# import bson
# from bson.objectid import ObjectId
#
# class PublishingModel:
#     def __init__(self):
#         self.publisher_name = ''
#         self.post_id = ObjectId()
#         self.url = ''
#         self.post_id_ext = ''
#         self.user_id_ext = ''
#
#     def set_publisher_name(self, val):
#         if type(val) is type(self.publisher_name):
#             self.publisher_name = val
#             return None
#
#         e = Exception('PublishingModel.publisher_name incorrect datatype')
#         Logger.Error('Incorrect datatype', {"publisher_name_type": type(self.publisher_name), "value_type": type(val)})
#         raise e
#
#     def set_post_id(self, val):
#         if type(val) is type(self.post_id):
#             self.post_id = val
#             return None
#
#         e = Exception('publishing_model.set_post_id.unsupported_datatype')
#         ErrorLogger.error(f'product_model.set_post_id.unsupported_datatype. Details: {str({"post_id_type": type(self.post_id), "value_type": type(val)})}')
#         return e
#
#     def set_url(self, val):
#         if type(val) is type(self.url):
#             self.url = val
#             return None
#
#         e = Exception('publishing_model.set_url.unsupported_datatype')
#         ErrorLogger.error(f'product_model.set_url.unsupported_datatype. Details: {str({"url_type": type(self.url), "value_type": type(val)})}')
#         return e
