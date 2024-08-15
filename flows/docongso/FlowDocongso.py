import threading

from services.link.accesstrade.AccesstradeLink import AccesstradeLink
from services.post.facebook.FacebookPostWriter import FacebookPostWriter
from services.product.shopee.ShopeeProduct import ShopeeProduct
from services.publishing.facebook.FacebookPagePublisher import FacebookPagePublisher
from utils.environment.Environment import Environment
from utils.logger.Logger import Logger
from utils.scheduler.Scheduler import Scheduler


class FlowDocongso:
    DATABASE_NAME = "docongso_dbv2"

    def __init__(self):
        self.env = Environment(FlowDocongso.DATABASE_NAME)
        self.logger = Logger(self.__class__.__name__)

    def Run(self):
        Logger().Info(f'Application {self.__class__.__name__} is running')

        productFlowScheduler = Scheduler(
            self.ExecuteProductFlow,
            self.env.GetProductSchedule,
            FlowDocongso.DATABASE_NAME + "_product_flow"
        )
        productFlowScheduler.Run()

        publishFlowScheduler = Scheduler(
            self.ExecutePublishFlow,
            self.env.GetPublishSchedule,
            FlowDocongso.DATABASE_NAME + "_publish_flow"
        )
        publishFlowScheduler.Run()

    def ExecuteProductFlow(self):
        try:
            productService = ShopeeProduct(FlowDocongso.DATABASE_NAME)
            productId = productService.GetNewProduct()

            linkService = AccesstradeLink(FlowDocongso.DATABASE_NAME, productService.GetProduceProviderName())
            linkService.UpdateProductAffiliateUrl(productId)

            postService = FacebookPostWriter(FlowDocongso.DATABASE_NAME)
            postService.UpdateProductPostContent(productId)
        except Exception as e:
            Logger().Error("Unknown error", {"error": e})
            raise e

    def ExecutePublishFlow(self):
        try:
            publishService = FacebookPagePublisher(FlowDocongso.DATABASE_NAME)
            publishService.PublishFacebookPage()
        except Exception as e:
            Logger().Error("Unknown error", {"error": e})
            raise e

    def ExecuteMarketingFlow(self):
        localVars = threading.local()
        localVars.flow = FlowDocongso.DATABASE_NAME

        # product = random.random() < 0.3 ? LazadaProduct(): ShoppeProduct()
        # product = ShopeeProduct(FlowDocongso.DATABASE_NAME)
        #
        # product.GetNewProduct()
        pass
