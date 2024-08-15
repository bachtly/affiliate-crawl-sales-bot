from utils.database.Orm import Orm
from utils.decorator.Singleton import singleton
from utils.logger.Logger import Logger


@singleton
class Environment:
    DB_ENV_TABLE = "env_tab"
    EMAIL_FACEBOOK_KEY = "email_facebook"
    PASSWORD_FACEBOOK_KEY = "password_facebook"
    PAGE_NAME_FACEBOOK_KEY = "page_name_facebook"
    PAGE_ID_FACEBOOK_KEY = "page_id_facebook"
    VIRAL_PAGE_NAMES_KEY = "viral_page_names"
    PUBLISH_SCHEDULE_KEY = "publish_schedule"
    PRODUCT_SCHEDULE_KEY = "product_schedule"
    MARKETING_SCHEDULE_KEY = "marketing_schedule"
    SHOPS_KEY = "shops"

    databaseName = None

    def __init__(self, databaseName):
        self.databaseName = databaseName

    def GetEmailFacebook(self):
        env = self.GetEnvFromDB()

        if self.EMAIL_FACEBOOK_KEY not in env.keys():
            e = Exception(f'{self.EMAIL_FACEBOOK_KEY} does not exist in env')
            Logger().Error(str(e))
            raise e

        return env[self.EMAIL_FACEBOOK_KEY]

    def GetPasswordFacebook(self):
        env = self.GetEnvFromDB()

        if self.PASSWORD_FACEBOOK_KEY not in env.keys():
            e = Exception(f'{self.PASSWORD_FACEBOOK_KEY} does not exist in env')
            Logger().Error(str(e))
            raise e

        return env[self.PASSWORD_FACEBOOK_KEY]

    def GetPageNameFacebook(self):
        env = self.GetEnvFromDB()

        if self.PAGE_NAME_FACEBOOK_KEY not in env.keys():
            e = Exception(f'{self.PAGE_NAME_FACEBOOK_KEY} does not exist in env')
            Logger().Error(str(e))
            raise e

        return env[self.PAGE_NAME_FACEBOOK_KEY]

    def GetPageIdFacebook(self):
        env = self.GetEnvFromDB()

        if self.PAGE_ID_FACEBOOK_KEY not in env.keys():
            e = Exception(f'{self.PAGE_ID_FACEBOOK_KEY} deos not exist in env')
            Logger().Error(str(e))
            raise e

        return env[self.PAGE_ID_FACEBOOK_KEY]

    def GetViralPageNames(self):
        env = self.GetEnvFromDB()

        if self.VIRAL_PAGE_NAMES_KEY not in env.keys():
            e = Exception(f'{self.VIRAL_PAGE_NAMES_KEY} does not exist in env')
            Logger().Error(str(e))
            raise e

        if type(env[self.VIRAL_PAGE_NAMES_KEY]) is not list:
            raise 'Environment ViralPageNames is not of type list'

        return env[self.VIRAL_PAGE_NAMES_KEY]

    def GetPublishSchedule(self):
        env = self.GetEnvFromDB()

        if self.PUBLISH_SCHEDULE_KEY not in env.keys():
            e = Exception(f'{self.PUBLISH_SCHEDULE_KEY} does not exist in env')
            Logger().Error(str(e))
            raise e

        publish_schedule = env[self.PUBLISH_SCHEDULE_KEY]

        if type(publish_schedule) is not list:
            e = Exception('Environment.PublishSchedule type not list')
            Logger().Error(str(e), {"publish_schedule": publish_schedule})
            raise e

        if len([i for i in publish_schedule if type(i) is not list or len(i) != 2]) > 0:
            e = Exception('Environment.PublishSchedule is not in correct format')
            Logger().Error(str(e), {"publish_schedule": publish_schedule})
            raise e

        return publish_schedule

    def GetProductSchedule(self):
        env = self.GetEnvFromDB()

        if self.PRODUCT_SCHEDULE_KEY not in env.keys():
            e = Exception(f'{self.PRODUCT_SCHEDULE_KEY} does not exist in env')
            Logger().Error(str(e))
            raise e

        product_schedule = env[self.PRODUCT_SCHEDULE_KEY]

        if type(product_schedule) is not list:
            e = Exception('Environment.ProductSchedule type not list')
            Logger().Error(str(e), {"product_schedule": product_schedule})
            raise e

        if len([i for i in product_schedule if type(i) is not list or len(i) != 2]) > 0:
            e = Exception('Environment.ProductSchedule is not in correct format')
            Logger().Error(str(e), {"product_schedule": product_schedule})
            raise e

        return product_schedule

    def GetMarketingSchedule(self):
        env = self.GetEnvFromDB()

        if self.MARKETING_SCHEDULE_KEY not in env.keys():
            e = Exception(f'{self.MARKETING_SCHEDULE_KEY} does not exist in env')
            Logger().Error(str(e))
            raise e

        marketing_schedule = env[self.MARKETING_SCHEDULE_KEY]

        if type(marketing_schedule) is not list:
            e = Exception('Environment.MarketingSchedule type not list')
            Logger().Error(str(e), {"marketing_schedule": marketing_schedule})
            raise e

        if len([i for i in marketing_schedule if type(i) is not list or len(i) != 2]) > 0:
            e = Exception('Environment.MarketingSchedule is not in correct format')
            Logger().Error(str(e), {"marketing_schedule": marketing_schedule})
            raise e

        return marketing_schedule

    def GetShops(self):
        env = self.GetEnvFromDB()

        if self.SHOPS_KEY not in env.keys():
            e = Exception(f'{self.SHOPS_KEY} does not exist in env')
            Logger().Error(str(e))
            raise e

        shops = env[self.SHOPS_KEY]

        if type(shops) is not dict:
            e = Exception('Environment.Shops type not dict')
            Logger().Error(str(e), {"shops": shops})
            raise e

        if len([i for i in shops.values() if type(i) is not list]) > 0:
            e = Exception(f'Environment Shops is not in correct format')
            Logger().Error(str(e), {"shops": shops})
            raise e

        return shops

    def GetEnvFromDB(self):
        with Orm(self.databaseName, self.DB_ENV_TABLE) as orm:
            env = orm.Find({}, limit=0)
            if len(env) < 1:
                e = Exception('Environment is empty')
                Logger().Error(str(e), {"env": env})
                raise e

        return env[0]

    def SetDatabaseName(self, databaseName):
        self.databaseName = databaseName
