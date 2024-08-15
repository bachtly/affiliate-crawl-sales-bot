# from services.crawler.Crawler import Crawler
# from models.Product import Product
# from utils.logger.logging import InfoLogger, ErrorLogger, InfoLogger
# from utils.database.orm import ORM
#
# import re
# import os
# from time import sleep
# from unidecode import unidecode
#
#
# class LazadaAdapter:
#     def __init__(self, database_name='affiliate_db'):
#         self.crawler = Crawler()
#         self.render_time = 5
#         self.render_item_time = 1
#         self.ads_wait_time = 5
#         self.orm = None
#         self.url = ''
#         self.item_url = ''
#         self.max_page = 3
#         self.keyword = ''
#         self.database_name = database_name
#
#     def init(self):
#         self.orm = ORM()
#         self.orm.connect(
#             uri='mongodb://root:root@localhost:27017',
#             db_name=self.database_name,
#             table_name='product_tab'
#         )
#
#         return self.crawler.init()
#
#     def close(self):
#         return self.crawler.close()
#
#     def get_products(self, keyword):
#         self.keyword = keyword
#
#         new_item_id, res = self.select_item()
#         if res:
#             ErrorLogger.error(f'get_lazada_women_clothes_info.get_products.fail_select_item.')
#             return None, res
#         self.crawler.screenshot('logger/lazada_complete_select_item.png')
#
#         InfoLogger.info(f'get_lazada_women_clothes_info.get_products.success {str({"new_itemid": new_item_id})}')
#         return new_item_id, None
#
#     def render_page(self, page_num):
#         self.url = f'https://www.lazada.vn/catalog/?q={self.keyword}&page={page_num}'
#         res = self.crawler.get(self.url)
#         if res:
#             ErrorLogger.error(f'get_lazada_women_clothes_info.render_main_page.fail_get_url.')
#             return res
#         sleep(self.render_time)
#         self.crawler.screenshot('logger/lazada_render_main_page.png')
#         InfoLogger.info(f'get_lazada_women_clothes_info.get_products.render_main_page. {str({"url": self.url})}')
#
#         res = self.render_all_items()
#         if res:
#             InfoLogger.warn("lazada_adapter.render_page.fail")
#             pass
#         self.crawler.screenshot('logger/lazada_render_all_items.png')
#
#         return None
#
#     def render_all_items(self):
#         total_scrolls = 20
#         for i in range(total_scrolls):
#             self.crawler.driver.execute_script(
#                 f'window.scrollTo(0, {round((i + 1) / total_scrolls, 2)}*document.body.scrollHeight);')
#             sleep(self.render_item_time)
#
#         InfoLogger.info("lazada_adapter.render_all_items.success")
#         return None
#
#     def select_item(self):
#         for page_num in range(1, self.max_page+1):
#             res = self.render_page(page_num)
#             if res:
#                 InfoLogger.warn(
#                     f'get_lazada_women_clothes_info.get_products.fail_render_page. {str({"page": page_num})}')
#                 continue
#
#             new_item_id, res = self.select_item_from_page(page_num)
#             if new_item_id is None:
#                 InfoLogger.warn(f'lazada_adapter.select_item.no_item_got_from_page. {str({"page": page_num})}')
#                 continue
#
#             return new_item_id, None
#
#         return None, None
#
#     def select_item_from_page(self, page_num):
#         titles, res = self.get_all_titles()
#         if res: return None, res
#         InfoLogger.info(f"lazada_adapter.select_item.titles_crawled_success. Details: {str({'n_titles': len(titles)})}")
#
#         for i, title in enumerate(titles):
#             prods, res = self.orm.find({'title': title})
#             if res:
#                 ErrorLogger.error(f'get_lazada_women_clothes_info.select_item.fail_orm_find.')
#                 return None, res
#
#             if prods:
#                 continue
#
#             xpath = f'//*[@data-qa-locator="general-products"]//*[@data-qa-locator="product-item"][{i + 1}]//a'
#             self.item_url, res = self.get_item_url(xpath)
#             if res:
#                 ErrorLogger.error(f'get_lazada_women_clothes_info.select_item.fail_get_item_url.')
#                 return None, res
#
#             res = self.render_item_page(xpath)
#             if res:
#                 ErrorLogger.error(f'get_lazada_women_clothes_info.select_item.fail_render_item_page.')
#                 return None, res
#             sleep(self.render_time)
#             self.crawler.screenshot('logger/lazada_itempage.png')
#
#             product_details, res = self.extract_product_details()
#             if res:
#                 ErrorLogger.error(f'get_lazada_women_clothes_info.select_item.fail_extract_product_details.')
#                 return None, res
#
#             product_dict = product_details.__dict__
#             inserted_ids, res = self.orm.insert([product_dict])
#             if res:
#                 ErrorLogger.error(f'get_lazada_women_clothes_info.select_item.fail_orm_insert.')
#                 return None, res
#
#             if not inserted_ids:
#                 e = Exception('lazada_adapter.select_item.no_products_are_inserted_to_db.')
#                 ErrorLogger.error(f'lazada_adapter.select_item.fail_orm_insert. {str({"error": e})}')
#                 return None, e
#
#             InfoLogger.info(f'lazada_adapter.select_item.success. {str({"inserted_ids": inserted_ids})}')
#             return str(inserted_ids[0]), None
#
#         return None, None
#
#     def get_all_titles(self):
#         xpath = '//*[@data-qa-locator="general-products"]//*[@data-qa-locator="product-item"]'
#         titles, res = self.crawler.get_texts(xpath)
#         if res:
#             ErrorLogger.error(f'lazada_adapter.get_all_titles.fail_get_texts_titles.')
#             return None, res
#
#         return titles, None
#
#     def get_item_url(self, xpath):
#         url_item, res = self.crawler.get_attribute(xpath, 'href')
#         if res:
#             ErrorLogger.error(f'lazada_adapter.get_item_url.fail_get_href_attr.')
#             return None, res
#
#         InfoLogger.info(f'lazada_adapter.get_item_url.success. {str({"url_item": url_item})}')
#         return url_item, None
#
#     def render_item_page(self, xpath):
#         res = self.crawler.click(xpath)
#         if res:
#             ErrorLogger.error(f'lazada_adapter.render_item_page.fail_click_item.')
#             return res
#
#         sleep(self.render_time)
#
#         InfoLogger.info(f'lazada_adapter.render_item_page.success.')
#         return None
#
#     def extract_product_details(self):
#         # info
#         title, res = self.get_title()
#         if res: return None, res
#
#         description, res = self.get_description()
#         if res: return None, res
#
#         price_original, res = self.get_price_original()
#         price_discount, res = self.get_price_discount()
#         if not price_original:
#             price_original = price_discount
#
#         # media - SHOULD BE THE LAST DETAIL TO CRAWL BECAUSE IT NEEDS RENDERING NEW THINGS
#         photo_dirs, res = self.get_photos()
#         if res: return None, res
#
#         # wrap
#         product = Product()
#
#         res = product.set_title(title)
#         if res: return None, res
#
#         res = product.set_url_original(self.item_url)
#         if res: return None, res
#
#         res = product.set_description(description)
#         if res: return None, res
#
#         res = product.set_price_original(price_original)
#         if res: return None, res
#
#         res = product.set_price_discount(price_discount)
#         if res: return None, res
#
#         res = product.set_photos(photo_dirs)
#         if res:
#             ErrorLogger.error('lazada_adapter.extract_product_detail.unknown_error')
#             return None, res
#
#         res = product.set_keyword(self.keyword)
#         if res: return None, res
#
#         hashtag = re.sub(r'\s', '_', unidecode(self.keyword))
#         res = product.set_hashtag(hashtag)
#         if res: return None, res
#
#         InfoLogger.info(f'lazada_adapter.extract_product_details.success.')
#         return product, None
#
#     def get_title(self):
#         xpath = '//h1[@class="pdp-mod-product-badge-title"]'
#         title, res = self.crawler.get_text(xpath)
#         if res:
#             ErrorLogger.error(f'lazada_adapter.get_title.fail_get_text.')
#             return None, res
#
#         return title, None
#
#     def get_description(self):
#         xpath = '//div[@id="module_product_detail"]'
#         description, res = self.crawler.get_text(xpath)
#         if res:
#             ErrorLogger.error(f'lazada_adapter.get_description.fail_get_text.')
#             return None, res
#
#         return description, None
#
#     def get_price_original(self):
#         price_original, res = self.crawler.get_text('//*[contains(@class, "deleted") and contains(@class, "pdp-price")]')
#         if res:
#             ErrorLogger.error('lazada_adapter.get_price_original.fail_crawl')
#             return None, res
#
#         try:
#             price_str, res = self.preprocess_price(price_original)
#             if res:
#                 ErrorLogger.error('lazada_adapter.get_price_original.fail_preprocess')
#                 return None, res
#             price_int = int(price_str)
#         except Exception as e:
#             ErrorLogger.error(f'lazada_adapter.get_price_original.fail_integer_convert. {str({"error": e})}')
#             return e
#
#         InfoLogger.info(f'lazada_adapter.get_price_original.success. {str({"price_original": price_int})}')
#         return price_int, None
#
#     def get_price_discount(self):
#         price_discount, res = self.crawler.get_text('//*[contains(@class,"pdp-price_type_normal")]')
#         if res:
#             InfoLogger.info('lazada_adapter.get_price_discount.no_discount')
#             return 0, None
#         if price_discount == '':
#             InfoLogger.info('lazada_adapter.get_price_discount.no_discount')
#             return 0, None
#
#         try:
#             price_str, res = self.preprocess_price(price_discount)
#             if res:
#                 ErrorLogger.error('lazada_adapter.get_price_discount.fail_preprocess')
#                 return None, res
#             price_int = int(price_str)
#         except Exception as e:
#             ErrorLogger.error(f'lazada_adapter.get_price_discount.fail_integer_convert. {str({"error": e})}')
#             return e
#
#         InfoLogger.info(f'lazada_adapter.get_price_discount.success. {str({"price_discount": price_int})}')
#         return price_int, None
#
#     def preprocess_price(self, price_str):
#         try:
#             price_str = price_str.split('-')[-1]
#             price_str = re.sub(r'[^0-9]', '', price_str)
#
#         except Exception as e:
#             ErrorLogger.error(f'lazada_adapter.preprocess_price.fail. {str({"error": e})}')
#             return None, e
#
#         return price_str, None
#
#     def get_photos(self):
#         xpath = '//*[contains(@class, "item-gallery__thumbnail")]//img[contains(@class, "item-gallery__thumbnail-image")]'
#         urls, res = self.crawler.get_attributes(xpath, 'src')
#         if res: return None, res
#
#         try:
#             photo_dirs = self.preprocess_photo_urls(urls)
#             if res:
#                 ErrorLogger.error(f'lazada_adapter.get_photos.fail_save_photos. {str({"urls": urls})}')
#                 return None, res
#
#         except Exception as e:
#             ErrorLogger.error(f'lazada_adapter.get_photos.unknown_error. {str({"error": e})}')
#             return None, e
#
#         InfoLogger.info(f'lazada_adapter.get_photos.success. {str({"urls": urls, "photo_dirs": photo_dirs})}')
#         return photo_dirs, None
#
#     def preprocess_photo_urls(self, urls):
#         urls = [re.sub('120x120q80', '720x720q80', url) for url in urls]  # get high resolution photos
#         urls = list(set(urls))  # remove duplicate photos
#         urls = urls[1:]  # possibly first one is video
#
#         return urls
