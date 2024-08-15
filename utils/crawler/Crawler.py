from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from utils.logger.Logger import Logger


class Crawler:
    def __init__(self):
        self.driver = None
        self.action = None

    def __enter__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        try:
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            self.action = ActionChains(self.driver)
            self.driver.set_window_size(1920, 1080)
        except Exception as e:
            Logger().Error(str(e))
            raise e

        return self

    def __exit__(self, *args):
        try:
            self.driver.close()
        except Exception as e:
            Logger().Error(str(e))
            raise e

    def Get(self, url):
        try:
            self.driver.get(url)
        except Exception as e:
            Logger().Error(str(e))
            raise e

    def GetElementByXpath(self, xpath, timeout=None):
        if timeout:
            try:
                _ = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            except TimeoutException as e:
                Logger().Error(str(e), {"xpath": xpath, "timeout": timeout})
                raise e
            except Exception as e:
                Logger().Error(str(e), {"xpath": xpath, "timeout": timeout})
                raise e

        try:
            elem = self.driver.find_element(By.XPATH, xpath)
        except Exception as e:
            Logger().Error(str(e), {"xpath": xpath, "timeout": timeout})
            raise e

        return elem

    def GetElementsByXpath(self, xpath, timeout=None):
        if timeout:
            try:
                _ = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            except TimeoutException as e:
                Logger().Error(str(e), {"xpath": xpath, "timeout": timeout})
                raise e
            except Exception as e:
                Logger().Error(str(e), {"xpath": xpath, "timeout": timeout})
                raise e

        try:
            elem = self.driver.find_elements(By.XPATH, xpath)
        except Exception as e:
            Logger().Error(str(e), {"xpath": xpath, "timeout": timeout})
            raise e

        return elem

    def Click(self, xpath, offset=None, timeout=None):
        try:
            element = self.GetElementByXpath(xpath, timeout)

            self.action.move_to_element(element)
            if offset: self.action.move_by_offset(offset[0], offset[1])
            self.action.click()
            self.action.perform()
        except Exception as e:
            Logger().Error(str(e), {"xpath": xpath, "offset": offset, "timeout": timeout})
            raise e

    def GetText(self, xpath, timeout=None):
        try:
            element = self.GetElementByXpath(xpath, timeout)

        except Exception as e:
            Logger().Error(str(e), {"xpath": xpath, "timeout": timeout})
            raise e

        return element.text

    def GetTexts(self, xpath, timeout=None):
        try:
            elements = self.GetElementsByXpath(xpath, timeout)
            elem_texts = [e.text for e in elements]

        except Exception as e:
            Logger().Error(str(e), {"xpath": xpath, "timeout": timeout})
            raise e

        return elem_texts

    def FillText(self, xpath, keys, timeout=None):
        try:
            elem = self.GetElementByXpath(xpath, timeout)
            elem.send_keys(keys)

        except Exception as e:
            Logger().Error(str(e), {"xpath": xpath, "keys": keys, "timeout": timeout})
            raise e

    def Submit(self, xpath, timeout=None):
        try:
            elem = self.GetElementByXpath(xpath, timeout)
            elem.submit()

        except Exception as e:
            Logger().Error(str(e), {"xpath": xpath, "timeout": timeout})
            raise e

    def GetAttribute(self, xpath, attr):
        try:
            elem = self.GetElementByXpath(xpath)
            attr_value = elem.get_attribute(attr)

        except Exception as e:
            Logger().Error(str(e), {"xpath": xpath, "attribute": attr})
            raise e

        return attr_value

    def GetAttributes(self, xpath, attr):
        try:
            elems = self.GetElementsByXpath(xpath)
            attr_values = [elem.get_attribute(attr) for elem in elems]

        except Exception as e:
            Logger().Error(str(e), {"xpath": xpath, "attribute": attr})
            raise e

        return attr_values

    def Screenshot(self, filename):
        try:
            self.driver.save_screenshot(filename)

        except Exception as e:
            Logger().Error(str(e), {"filename": filename})
            raise e

    def Type(self, keys):
        try:
            self.action.send_keys(keys).perform()

        except Exception as e:
            Logger().Error(str(e), {"keys": keys})
            raise e

    def ScrollTo(self, bodyPercentage):
        try:
            self.driver.execute_script(
                f'window.scrollTo(0, {bodyPercentage}*document.body.scrollHeight);')

        except Exception as e:
            Logger().Error(str(e), {"bodyPercentage": bodyPercentage})
            raise e
