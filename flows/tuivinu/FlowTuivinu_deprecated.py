# import random
#
# from common.logging import ErrorLogger, InfoLogger
# from module.api.creator import CreatorController
# from module.api.link import LinkController
# from module.api.marketing import MarketingController
# from module.api.product import ProductController
# from module.api.publisher import PublisherController
# from module.scheduler import Scheduler
#
#
# class FlowTuivinu:
#     def __init__(self):
#         self.link_flow = 'accesstrade'
#         self.publish_flow = 'facebookpage'
#         self.marketing_flow = 'newfeed_page_comment'
#
#         self.product_providers = [
#             'shopee',
#             'lazada'
#         ]
#         self.product_provider = self.product_providers[0]
#
#         self.email_facebook = ''
#         self.password_facebook = ''
#         self.page_id_facebook = ''
#         self.page_name_facebook = ''
#         self.database_name = 'tuivinu_db'
#         self.keywords = [
#             'túi xách baguette nữ',
#             'túi xách clutch nữ',
#             'túi xách đeo chéo nữ',
#             'túi tote nữ',
#             'túi xách bucket nữ',
#             'ví nữ kéo khóa',
#             'ví nữ nắp gập',
#             'ví nữ dễ thương'
#         ]
#         self.viral_page_names = [
#             'Insight mất lòng',
#             'Xanh Mượt',
#             'Theanh28 Entertainment',
#             'Cao Thủ',
#             'Tizi Đích Lép',
#         ]
#
#     def process(self):
#         jobs = {
#             'crawl': self.job_crawl,
#             'publishing': self.job_publish,
#             'marketing': self.job_marketing,
#         }
#         hyper_params = {
#             'crawl': {'times': [(4, 0), (6, 0)], 'interval': False},
#             'publishing': {'times': [(21, 0), (23, 0)], 'interval': False},
#             'marketing': {'times': [(1, 30), (3, 30), (8, 30), (12, 30), (16, 30), (21, 30), (23, 30)],
#                           'interval': False},
#         }
#         schedulers = {
#             'crawl': Scheduler(jobs['crawl'], hyper_params['crawl']['times'], hyper_params['crawl']['interval']),
#             'publishing': Scheduler(jobs['publishing'], hyper_params['publishing']['times'],
#                                     hyper_params['publishing']['interval']),
#             'marketing': Scheduler(jobs['marketing'], hyper_params['marketing']['times'],
#                                    hyper_params['marketing']['interval']),
#         }
#
#         res = schedulers['crawl'].Run()
#         if res:
#             ErrorLogger.error('module.flow.flow_tuivinu.fail_scheduling_job_crawl')
#             return res
#         InfoLogger.info(
#             f'module.flow.flow_tuivinu.success_scheduling_job_crawl. Details: {str({"params": hyper_params["crawl"]})}')
#
#         res = schedulers['publishing'].Run()
#         if res:
#             ErrorLogger.error('module.flow.flow_tuivinu.fail_scheduling_job_publish')
#             return res
#         InfoLogger.info(
#             f'module.flow.flow_tuivinu.success_scheduling_job_publish. Details: {str({"params": hyper_params["publishing"]})}')
#
#         res = schedulers['marketing'].Run()
#         if res:
#             ErrorLogger.error('module.flow.flow_tuivinu.fail_scheduling_job_marketing')
#             return res
#         InfoLogger.info(
#             f'module.flow.flow_tuivinu.success_scheduling_job_marketing. Details: {str({"params": hyper_params["marketing"]})}')
#
#         return None
#
#     def job_crawl(self):
#         idx = random.randint(0, len(self.product_providers) - 1)
#         self.product_provider = self.product_providers[idx]
#
#         product_resp, res = ProductController.Get(
#             self.keywords,
#             self.database_name,
#             self.product_provider
#         )
#         InfoLogger.info(f"Response from Product Controller: {product_resp}")
#         if res: return res
#         if not product_resp['status']:
#             err = Exception(f'flow.process_flow.error_from_product_server.')
#             ErrorLogger.error(f'flow.process_flow.error_from_product_server. Details: {str({"resp": product_resp})}')
#             return err
#
#         if product_resp['data']['new_item_id']:
#             link_resp, res = LinkController.Get(
#                 self.link_flow,
#                 product_resp['data']['new_item_id'],
#                 self.database_name,
#                 self.product_provider
#             )
#             InfoLogger.info(f"Response from Link Controller: {link_resp}")
#             if res: return res
#             if not link_resp['status']:
#                 err = Exception(f'flow.process_flow.error_from_link_server.')
#                 ErrorLogger.error(f'flow.process_flow.error_from_link_server. Details: {str({"resp": link_resp})}')
#                 return err
#
#         if product_resp['data']['new_item_id']:
#             post_resp, res = CreatorController.Get(
#                 product_resp['data']['new_item_id'],
#                 self.database_name,
#                 self.product_provider
#             )
#             InfoLogger.info(f"Response from Creator Controller: {post_resp}")
#             if res: return res
#             if not post_resp['status']:
#                 err = Exception(f'flow.process_flow.error_from_post_server.')
#                 ErrorLogger.error(f'flow.process_flow.error_from_post_server. Details: {str({"resp": post_resp})}')
#                 return err
#
#     def job_publish(self):
#         publisher_resp, res = PublisherController.post(
#             self.publish_flow,
#             self.email_facebook,
#             self.password_facebook,
#             self.page_name_facebook,
#             self.page_id_facebook,
#             self.database_name
#         )
#         InfoLogger.info(f"Response from Publisher Controller: {publisher_resp}")
#         if res: return res
#         if not publisher_resp['status']:
#             err = Exception(f'flow.process_flow.error_from_publisher_server.')
#             ErrorLogger.error(
#                 f'flow.process_flow.error_from_publisher_server. Details: {str({"resp": publisher_resp})}')
#             return err
#
#     def job_marketing(self):
#         marketing_resp, res = MarketingController.post(
#             self.marketing_flow,
#             self.email_facebook,
#             self.password_facebook,
#             self.page_name_facebook,
#             self.page_id_facebook,
#             self.database_name,
#             self.viral_page_names,
#         )
#         InfoLogger.info(f"Response from Marketing Controller: {marketing_resp}")
#         if res: return res
#         if not marketing_resp['status']:
#             err = Exception(f'flow.process_flow.error_from_marketing_server.')
#             ErrorLogger.error(
#                 f'flow.process_flow.error_from_marketing_server. Details: {str({"resp": marketing_resp})}')
#             return err
