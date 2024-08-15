# from model.post_model import Post
# from common.logging import ErrorLogger, InfoLogger
#
# import re
# import random
#
#
# EMOJIs = {
#     'smiling-eyes': '^_^',
#     'tounge': ':P',
#     'winking': ';)',
#     'sunglass': '8)',
#     'angel': 'O:-)',
#     'kiss': ':*',
#     'heart': '<3',
#     'winktoungue': ';P',
#     'flushkiss': '-3-'
# }
#
#
# class PostWriter:
#     def __init__(self, product_provider):
#         self.product_provider = product_provider
#         pass
#
#     def write_posts(self, product, n=1):
#         content = ''
#
#         # greeting, res = self.greeting()
#         # if res:
#         #     ErrorLogger.error('post_writer.write_posts.greeting_error');
#         #     return None, res
#         # content += greeting
#         # content += '\n'
#
#         title = product['title'].upper()
#         if product['title'][0]=='[': content += title
#         else: content += f'[{title}]'
#         content += '\n'
#
#         content += '-----\n'
#
#         price_sentence, res = self.price(product['price_original'], product['price_discount'])
#         if res:
#             ErrorLogger.error('post_writer.write_posts.price_sentence_error')
#             return None, res
#         if price_sentence!='':
#             content += price_sentence
#             content += '\n'
#
#         content += f'{EMOJIs["heart"]} {EMOJIs["heart"]} {EMOJIs["heart"]} Xem THÔNG TIN CHI TIẾT qua {self.product_provider.upper()} ở đây: {product["url_affiliate"]}'
#         content += '\n'
#
#         content += '-----\n'
#
#         description, res = self.summarize_description(product['description'])
#         if res:
#             ErrorLogger.error(str(res))
#             return None, res
#         content += description
#         content += '\n'
#
#         if 'hashtag' in product.keys():
#             if product['hashtag'] != '':
#                 content += f'#{product["hashtag"]}'
#                 content += '\n'
#
#         product_id_hashtag = str(product['_id'])[-6:]
#         content += f'#{product_id_hashtag}'
#         content += '\n'
#
#         post = Post()
#         post.set_content(content)
#         post.set_product_id(product['_id'])
#
#         return [post.__dict__], None
#
#     def greeting(self):
#         try:
#             emoji_values = [i for i in EMOJIs.values()]
#             emoji = emoji_values[random.randint(0, len(EMOJIs)-1)]
#             greetings = [
#                 f'Hàng về hàng về',
#                 f'Hàng về hàng về mọi ngừi ơiiii',
#                 f'Khách mua ủng hộ em vớiiii',
#                 f'Hàng nóng hổi vừa thổi vừa xem',
#                 f'Đồ đã cập bến',
#                 f'Quẹo lựa quẹo lựa'
#             ]
#
#             idx = random.randint(0, len(greetings)-1)
#
#             greeting_with_emoji = f'{greetings[idx]} {emoji} {emoji}'
#
#             return greeting_with_emoji, None
#
#         except Exception as e:
#             ErrorLogger.error(f'post_writer.greeting.error. Details: {str(e)}')
#             return None, e
#
#     def price(self, price_original, price_discount):
#         try:
#             price_sentence = ''
#             price = price_original
#
#             if 0 < price_discount and price_discount+1 < price_original:
#                 percentage = int( (price_original-price_discount)/price_original*100 )
#                 if percentage >= 5:
#                     price_sentence += f'GIẢM SỐC TỚI: {percentage}%. '
#                     price = price_discount
#
#             # price_str = self.refine_price(price)
#
#             # price_sentence += f'Giá chỉ: {price_str}'
#             return price_sentence, None
#
#         except Exception as e:
#             ErrorLogger.error(f'post_write.price.error. Details: {str(e)}')
#             return None, e
#
#     def refine_price(self, price):
#         price = str(price)
#         price_str = ''
#         for idx, c in enumerate(price):
#             if idx>0 and (len(price)-idx)%3 == 0:
#                 price_str += '.'
#             price_str += c
#         return price_str
#
#     def summarize_description(self, description):
#         try:
#             lines = description.split('\n')
#             lines = [i for i in lines if i]
#
#             selected_lines = lines[:10]
#             summary = '\n'.join(selected_lines)
#
#             return summary, None
#
#         except Exception as e:
#             ErrorLogger.error(str(e))
#             return None, e
