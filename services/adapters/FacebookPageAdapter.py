import os
import shutil
import urllib.request
from time import sleep

from utils.crawler.Crawler import Crawler
from utils.file.File import File
from utils.logger.Logger import Logger

RENDER_TIME = 10
SHORT_RENDER_TIME = 5
ADS_WAIT_TIME = 5
TEMP_PHOTO_DIR = 'tmp'


class FacebookPageAdapter:
    def __init__(self):
        self.crawler = Crawler()

    def __enter__(self):
        self.crawler.__enter__()
        return self

    def __exit__(self, *args):
        self.crawler.__exit__()

    def Login(self, email, password):
        self.crawler.Get("https://facebook.com")
        sleep(RENDER_TIME)
        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'RenderLoginPage.png'))

        self.crawler.Click('//*[@id="email"]')
        self.crawler.Type(email)
        self.crawler.Click('//*[@id="pass"]')
        self.crawler.Type(password)

        self.crawler.Click('//*[@id="content"]//button')
        sleep(RENDER_TIME)

        Logger().Info('Success login')
        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'AfterClickLoginButton.png'))

    def VerifyLogin(self):
        try:
            elem = self.crawler.GetElementByXpath('//*[@id="checkpointSubmitButton"]')
            if not elem: return
        except:
            # Optional action
            return

        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'NeedVerifyLogin.png'))
        e = Exception('Need to verify login, have not implemented yet')
        Logger().Error(str(e))
        raise e

    def RenderMainPage(self, pageId, pageName):
        self.crawler.Get(f"https://facebook.com/{pageId}")
        sleep(RENDER_TIME)

        xpath = '//*[@aria-label="Cài đặt và kiểm soát tài khoản"]//*[@aria-label="Trang cá nhân của bạn"]'
        self.crawler.Click(xpath)
        sleep(SHORT_RENDER_TIME)

        xpath = '//*[@aria-label="Trang cá nhân của bạn"]//span[text()="Xem tất cả trang cá nhân"]'
        self.crawler.Click(xpath)
        sleep(SHORT_RENDER_TIME)
        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'ViewAllAccountPages.png'))

        xpath = f'//*[@aria-label="Trang cá nhân của bạn"]//span[text()="{pageName}"]'
        self.crawler.Click(xpath)
        sleep(RENDER_TIME)

        Logger().Info('Success render main facebook page')
        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'RenderMainPage.png'))

    def OpenTextArea(self, pageName):
        try:
            xpath = f'//*[text()="Đã chuyển sang {pageName}"]'
            elem = self.crawler.GetElementByXpath(xpath)
            if elem:
                # self.crawler.Click('//*[@data-pagelet="ProfileComposer"]//span[text()="Bạn đang nghĩ gì?"]')
                sleep(RENDER_TIME)
        except:
            # optional action
            pass

        ### re-click in case the panel "CONFIRM SWITCH TO NEW PAGE" appears
        ### if facebook changes this behavior in the future, we also need to change
        self.crawler.Click('//span[text()="Bạn đang nghĩ gì?"]')
        sleep(SHORT_RENDER_TIME)
        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'ClickOnProfileComposer.png'))

        # re-click in case the browser request for "notification"
        try:
            xpath = '//*[text()="Đối tượng mặc định"]'
            elem = self.crawler.GetElementByXpath(xpath)
            if not elem: self.crawler.Click('//span[text()="Bạn đang nghĩ gì?"]')
        except:
            self.crawler.Click('//span[text()="Bạn đang nghĩ gì?"]')
            sleep(SHORT_RENDER_TIME)
            self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'ClickOnProfileComposer.png'))

        try:
            xpath = '//*[text()="Đối tượng mặc định"]'
            elem = self.crawler.GetElementByXpath(xpath)
            if elem:
                xpath = '//div[@aria-label="Xong"]'
                self.crawler.Click(xpath)
            sleep(SHORT_RENDER_TIME)
        except:
            # optional
            pass

        Logger().Info("Success open text area")
        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'SuccessOpenTextArea.png'))

    def Write(self, post, photoUrls):
        # click text field before typing
        self.crawler.Click(f'//*[@aria-label="Bạn đang nghĩ gì?"]')

        self.crawler.Type(post)

        ### attach photos
        for photoUrl in photoUrls:
            self.AttachPhoto(photoUrl, TEMP_PHOTO_DIR)
            sleep(SHORT_RENDER_TIME)
        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'AttachAllPhotos.png'))

        ### insert links to descriptions of each photo, help customer buy product directly
        self.WritePhotosDescription(post)
        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'InsertAllPhotosDescriptions.png'))

        ### remove tmp photo dir
        self.ClearPhotoDir(TEMP_PHOTO_DIR)

    def AttachPhoto(self, url, dir):
        dir = self.CreatePhotoDir(url, dir)
        dir = os.path.abspath(dir)

        self.crawler.Click('//*[@aria-label="Ảnh/video"]')
        sleep(SHORT_RENDER_TIME)

        elem = self.crawler.GetElementByXpath('//div[@role="dialog"]/form[@method="POST"]//input')
        self.crawler.driver.execute_script("arguments[0].class='';", elem)
        sleep(SHORT_RENDER_TIME)

        elem.send_keys(dir)

    def WritePhotosDescription(self, post):
        xpath = '//form//*[@aria-label="File phương tiện đính kèm"]//*[contains(@aria-label, "Chỉnh sửa")]'
        self.crawler.Click(xpath)
        sleep(SHORT_RENDER_TIME)
        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'OpenPhotoDescriptionPanel.png'))

        # a workaround with bug when typing 2 letters -> out-focus
        xpath = '//*[@aria-label="Quay lại"]'
        self.crawler.Click(xpath)
        sleep(SHORT_RENDER_TIME)

        xpath = '//form//*[@aria-label="File phương tiện đính kèm"]//*[contains(@aria-label, "Chỉnh sửa")]'
        self.crawler.Click(xpath)
        sleep(SHORT_RENDER_TIME)
        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'OpenPhotoDescriptionPanel.png'))

        xpath = '//*[@aria-label="Chú thích"]'
        elems = self.crawler.GetElementsByXpath(xpath)
        for i, elem in enumerate(elems):
            self.crawler.action.move_to_element(elem)
            self.crawler.action.click()
            self.crawler.action.perform()
            sleep(SHORT_RENDER_TIME)

            self.crawler.Type(post)
            sleep(SHORT_RENDER_TIME)
        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'WriteAllPhotoDescriptions.png'))

        xpath = '//*[@aria-label="Xong"]'
        self.crawler.Click(xpath)
        sleep(RENDER_TIME)
        Logger().Info('Success write all photo descriptions')

    def CreatePhotoDir(self, url, dir):
        if not os.path.exists(dir): os.makedirs(dir)
        n_files = len(os.listdir(dir))
        photo_dir = f"{dir}/{n_files}.png"
        urllib.request.urlretrieve(url, photo_dir)
        return photo_dir

    def ClearPhotoDir(self, dir):
        shutil.rmtree(dir)

    def Publish(self):
        self.crawler.Click('//*[@aria-label="Đăng"]')
        sleep(RENDER_TIME)
        self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'ClickPublishButton.png'))

        self.ClosePublishPopup()

        Logger().Info('Success publish')

    def ClosePublishPopup(self):
        try:
            xpath = '//*[@aria-label="Chat trực tiếp với khách hàng"]//*[@aria-label="Đóng"]'
            self.crawler.Click(xpath, timeout=RENDER_TIME)
            sleep(SHORT_RENDER_TIME)
            self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'ClosePopupChatWithCustomer.png'))
        except:
            # Optional action
            pass

        try:
            xpath = '//*[@aria-label="Đăng ưu đãi, mã giảm giá hay khuyến mãi?"]//*[@aria-label="Đóng"]'
            self.crawler.Click(xpath, timeout=RENDER_TIME)
            sleep(SHORT_RENDER_TIME)
            self.crawler.Screenshot(File.GetLogPhotoFileDir(self, 'ClosePopupPromotions.png'))
        except:
            # Optional action
            pass
