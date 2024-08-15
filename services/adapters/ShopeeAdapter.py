import re
from time import sleep

from unidecode import unidecode

from config.config import *
from models.ProductModel import ProductModel
from utils.crawler.Crawler import Crawler
from utils.database.Orm import Orm
from utils.file.File import File
from utils.logger.Logger import Logger

MAX_PAGE = 3
RENDER_TIME = 10
RENDER_ITEM_TIME = 5
ADS_WAIT_TIME = 10


class ShopeeAdapter:
    def __init__(self, database_name, shop, keyword):
        self.crawler = Crawler()
        self.database_name = database_name
        self.shop = shop
        self.keyword = keyword

        self.orm = Orm(self.database_name, DB_PRODUCT_TABLE)

    def __enter__(self):
        self.crawler.__enter__()
        self.orm.__enter__()
        return self

    def __exit__(self, *arg):
        self.crawler.__exit__()
        self.orm.__exit__()

    def GetNewProduct(self):
        newItemId = None

        for pageNum in range(MAX_PAGE):
            self.RenderSearchPage(self.shop, self.keyword, pageNum)
            newItemId = self.SelectItem()
            if newItemId is not None: break

        return newItemId

    def RenderSearchPage(self, shop, keyword, pageNum):
        url = f'https://shopee.vn/search?keyword={keyword}&page={pageNum}&shop={shop}'

        self.crawler.Get(url)
        sleep(RENDER_TIME)
        Logger().Info(f'Shopee adapter render main page', {"url": url})
        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'RenderSearchPage.png'))

        # it is optional to close ads, so if it is error, simply ignore
        self.CloseAds()
        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'CloseAds.png'))

        self.RenderSearchPageItems()
        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'RenderSearchPageItems.png'))

        return None

    def CloseAds(self):
        try:
            self.crawler.Click('//*[@class="home-popup__content"]', (-10, -10), ADS_WAIT_TIME)
        except Exception as e:
            Logger().Warn("Shopee Adapter close ads fail")

    def RenderSearchPageItems(self):
        try:
            total_scrolls = 20
            for i in range(total_scrolls):
                self.crawler.ScrollTo(round((i + 1) / total_scrolls, 2))
                sleep(RENDER_ITEM_TIME)
        except Exception as e:
            Logger().Warn("Shopee Adapter RenderSearchPageItems fail")

    def SelectItem(self):
        titles = self.GetAllTitles()
        for i, title in enumerate(titles):
            prods = self.orm.Find({'title': title})
            if len(prods): continue

            xpath = f'//*[@class="row shopee-search-item-result__items"]/div[{i + 1}]/a'
            itemUrl = self.crawler.GetAttribute(xpath, 'href')
            self.crawler.Click(xpath)
            sleep(RENDER_TIME)
            self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'ClickItemDetails.png'))

            product_details = self.ExtractProductDetails(itemUrl)
            product_dict = product_details.__dict__

            inserted_ids = self.orm.Insert([product_dict])
            if not inserted_ids:
                e = Exception('Insert fail, no item inserted')
                Logger().Error(str(e))
                raise e

            return str(inserted_ids[0])

        return None

    def GetAllTitles(self):
        xpath = '//*[@class="row shopee-search-item-result__items"]/div/a/div/div/' \
                + 'div[2]/div[1]/div[1]/div'
        title_elements = self.crawler.GetElementsByXpath(xpath)

        titles = []
        for idx, e in enumerate(title_elements):
            xpath = f'//*[@class="row shopee-search-item-result__items"]/div[{idx + 1}]/a/div/div/' \
                    + 'div[2]/div[1]/div[1]/div'
            titles += [self.crawler.GetText(xpath)]

        return titles

    def ExtractProductDetails(self, itemUrl):
        # info
        xpath = '//*[contains(@class,"product-briefing")]/div[last()]/div[1]/div[1]/span[1]'
        title = self.crawler.GetText(xpath)

        xpath = '//*[@class="product-detail page-product__detail"]/div[last()]/div[last()]/div[1]/p[1]'
        description = self.crawler.GetText(xpath)

        price_original_str = self.crawler.GetText('//*[contains(@class,"product-briefing")]/div[last()]/div[1]/'
                                                  + 'div[3]/div[last()]/div[1]/div[1]/div[1]/div[1]')
        price_original = self.PreprocessPrice(price_original_str)

        price_discount_str = self.crawler.GetText('//*[contains(@class,"product-briefing")]/div[last()]/div[1]/'
                                                  + 'div[3]/div[last()]/div[1]/div[1]/div[1]/div[last()]/div[1]')
        price_discount = self.PreprocessPrice(price_discount_str)

        # media - SHOULD BE THE LAST DETAIL TO CRAWL BECAUSE IT NEEDS RENDERING NEW THINGS
        urls = self.GetPhotos()

        # wrap
        product = ProductModel()

        product.SetTitle(title)
        product.SetUrlOriginal(itemUrl)
        product.SetDescription(description)
        product.SetPriceOriginal(price_original)
        product.SetPriceDiscount(price_discount)
        product.SetPhotos(urls)
        product.SetKeyword(self.keyword)
        product.SetHashtag(re.sub(r'\s', '_', unidecode(self.keyword)))

        return product

    def PreprocessPrice(self, price_str):
        try:
            price_str = price_str.split('-')[-1]
            price_str = re.sub(r'[^0-9]', '', price_str)

        except Exception as e:
            Logger().Error(str(e), {"price_str": price_str})
            raise e

        return int(price_str)

    def GetPhotos(self):
        xpath = '//*[contains(@class,"product-briefing")]//*[contains(@style, "background-image")]'
        self.crawler.Click(xpath)
        sleep(RENDER_TIME)

        xpath = '//*[contains(@style, "background-image")]'
        styles = self.crawler.GetAttributes(xpath, 'style')

        urls = [re.sub(r'.*\("', '', re.sub(r'"\).*', '', i)) for i in styles]  # get url text between '(' and ')'
        urls = [re.sub('_tn$', '', url) for url in urls]  # remove _tn to get high resolution photos
        urls = list(set(urls))  # remove duplicate photos
        urls = urls[1:]

        return urls
