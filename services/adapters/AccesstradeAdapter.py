import re
from time import sleep

from selenium.webdriver.common.keys import Keys

from utils.crawler.Crawler import Crawler
from utils.file.File import File
from utils.logger.Logger import Logger

RENDER_TIME = 15
SHORT_RENDER_TIME = 5
ADS_WAIT_TIME = 60


class AccesstradeAdapter:
    def __init__(self, productProvider):
        self.crawler = Crawler()
        self.productProvider = productProvider

    def __enter__(self):
        self.crawler.__enter__()
        return self

    def __exit__(self, *args):
        self.crawler.__exit__()

    def GetAffiliateUrl(self, urlOriginal):
        self.Login()
        Logger().Info('Accesstrade login success')

        self.RenderMainPage()
        Logger().Info('Accesstrade render main page success')

        self.OpenProductRightPanel()
        Logger().Info('Open product panel success')

        urlAffiliate = self.GenerateAffiliateUrl(urlOriginal)
        Logger().Info('Success generate url affiliate', {'url_affiliate': urlAffiliate})

        return urlAffiliate

    def Login(self):
        self.crawler.Get('https://id.accesstrade.vn/login')
        sleep(RENDER_TIME)
        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'RenderLoginPage.png'))

        self.crawler.FillText('//*[@id="username"]', '')
        self.crawler.FillText('//*[@id="password"]', '')
        self.crawler.Type(Keys.ENTER)

        sleep(RENDER_TIME)
        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'AfterLogin.png'))

    def RenderMainPage(self):
        self.crawler.Get('https://pub2.accesstrade.vn/campaign/result?category=E-COMMERCE')
        sleep(RENDER_TIME)
        self.crawler.Get('https://pub2.accesstrade.vn/campaign/result?category=E-COMMERCE')
        sleep(RENDER_TIME)
        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'RenderMainPage.png'))

        # close dialog (alert panel on top)
        try:
            self.crawler.Click('//*[@id="onesignal-slidedown-cancel-button"]', timeout=ADS_WAIT_TIME)
            sleep(SHORT_RENDER_TIME)
            self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'CloseDialog.png'))
        except:
            ### optional action, do not raise error
            pass

        # close ads
        try:
            self.crawler.GetElementByXpath('//ngb-modal-window', timeout=ADS_WAIT_TIME)
            self.crawler.Click('//header')
        except:
            ### optional action, do not raise error
            pass

        sleep(SHORT_RENDER_TIME)
        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'CloseAdsRenderMainPage.png'))

    def OpenProductRightPanel(self):
        xpath = '//*[@id="list_campaigns"]/div[2]/div[2]/div/div[1]/div[1]/div[2]/h5'
        campaignTitles = self.crawler.GetTexts(xpath)
        Logger().Info('Get all campaign titles', {'campaign_titles': campaignTitles})

        for idx, title in enumerate(campaignTitles):
            Logger().Info('Compare campaign title with product provider',
                          {'title': title, 'provider': self.productProvider})
            if re.search(self.productProvider, title.lower()):
                xpath = f'//*[@id="list_campaigns"]/div[2]/div[2]/div[{idx + 1}]/div[1]/div[1]/div[2]/h5'
                self.crawler.Click(xpath)

        sleep(SHORT_RENDER_TIME)
        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'OpenProductPanel.png'))

        # expand the panel
        # self.crawler.Click('//app-list-campaigns/div[2]/i[1]')
        # sleep(SHORT_RENDER_TIME)
        # self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'ExpandProductPanel.png'))

    def GenerateAffiliateUrl(self, urlOriginal):
        # fill in the original link
        self.crawler.Click('//*[@id="product_link"]', timeout=SHORT_RENDER_TIME)
        sleep(SHORT_RENDER_TIME)
        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'OpenProductTabInProductPanel.png'))

        self.crawler.FillText('//*[@id="original-link"]', urlOriginal)
        # check the option "shorten"
        self.crawler.Click('//*[@id="customCheck1"]')
        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'DataFilledInProductTab.png'))

        # click button to create link and then get the link
        self.crawler.Click('//*[@id="btn_create"]')
        sleep(SHORT_RENDER_TIME)
        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'LinkGenerateButtonClicked.png'))

        urlAffiliate = self.crawler.GetAttribute('//*[@id="created_short_url"]', 'value')

        return urlAffiliate
