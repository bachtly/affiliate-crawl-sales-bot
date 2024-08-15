import os
import random
import re
import shutil
import urllib.request
from time import sleep

from selenium.webdriver.common.keys import Keys
from utils.logger.logging import ErrorLogger, InfoLogger

from utils.crawler.Crawler import Crawler


class FacebookNewfeedAdapter:
    def __init__(self, email, password, page_name, page_id, viral_page_names):
        self.crawler = Crawler()
        self.render_time = 5
        self.render_post_time = 2
        self.ads_wait_time = 5
        self.url = ''
        self.viral_page_names = viral_page_names
        self.negative_emojis = ['Buồn', 'Phẫn nộ']
        self.positive_emojis = ['Haha']

        self.email = email
        self.password = password
        self.page_name = page_name
        self.page_id = page_id

        self.tmp_photo_dir = 'tmp'

        self.photos = []
        self.url_affiliate = ''

        self.max_scroll = 20

    def init(self):
        return self.crawler.init()

    def close(self):
        return self.crawler.close()

    def write_comment(self, product):
        self.photos = product['photos']
        self.product_id = str(product['_id'])
        self.url_affiliate = product['url_affiliate']

        res = self.login()
        if res:
            ErrorLogger.error('internal.newfeed_adapter.write_comment.fail')
            return res
        sleep(1)
        self.crawler.Screenshot('logger/login.png')

        if self.verify_login():
            ErrorLogger.error('internal.newfeed_adapter.write_comment.verify_login_not_implemented')
            return Exception('Login needs verify')
        sleep(1)
        self.crawler.Screenshot('logger/verify_login.png')

        res = self.render_main_page()
        if res:
            ErrorLogger.error('internal.newfeed_adapter.write_comment.render_main_page_fail')
            return Exception('Login needs verify')
        sleep(1)
        self.crawler.Screenshot('logger/render_main_page.png')

        res = self.comment_on_posts()
        if res:
            ErrorLogger.error('internal.newfeed_adapter.render_posts.fail')
            return res
        sleep(1)
        self.crawler.Screenshot('logger/complete_comment.png')

    def login(self):
        res = self.crawler.Get("https://facebook.com")
        if res:
            ErrorLogger.error("Error internal.newfeed_adapter.login")
            return res
        sleep(self.render_time)

        res = self.crawler.Click('//*[@id="email"]')
        if res:
            ErrorLogger.error("internal.newfeed_adapter.fail_click_email_textbox")
            return res
        res = self.crawler.Type(self.email)
        if res:
            ErrorLogger.error("internal.newfeed_adapter.fail_input_email")
            return res
        self.crawler.Screenshot('logger/type_email.png')

        res = self.crawler.Click('//*[@id="pass"]')
        if res:
            ErrorLogger.error("internal.newfeed_adapter.fail_click_password_textbox")
            return res
        res = self.crawler.Type(self.password)
        if res:
            ErrorLogger.error("internal.newfeed_adapter.fail_input_password")
            return res
        self.crawler.Screenshot('logger/type_pass.png')

        res = self.crawler.Click('//*[@id="content"]//button')
        if res:
            ErrorLogger.error("internal.newfeed_adapter.fail_click_login_button")
            return res

        return None

    def verify_login(self):
        elem, res = self.crawler.GetElementByXpath('//*[@id="checkpointSubmitButton"]')
        if res or not elem: return False

        return True

    def render_main_page(self):
        ### in case screen is diabled due to "Allow notification" of browser or sth like that
        for _ in range(3):
            xpath = '//*[@data-pagelet="TopOfHome"]//*[text)="Tin"]'
            _ = self.crawler.Click(xpath)
            sleep(1)

        xpath = '//*[@aria-label="Cài đặt và kiểm soát tài khoản"]//*[@aria-label="Trang cá nhân của bạn"]'
        res = self.crawler.Click(xpath)
        if res:
            ErrorLogger.error("internal.newfeed_adapter.render_main_page.fail_click_open_account_menu")
            return res
        sleep(1)

        xpath = '//*[@aria-label="Trang cá nhân của bạn"]//span[text()="Xem tất cả trang cá nhân"]'
        res = self.crawler.Click(xpath)
        if res:
            ErrorLogger.error("internal.newfeed_adapter.render_main_page.fail_click_open_account_list")
            return res
        sleep(1)

        xpath = f'//*[@aria-label="Trang cá nhân của bạn"]//span[text()="{self.page_name}"]'
        res = self.crawler.Click(xpath)
        if res:
            ErrorLogger.error("internal.newfeed_adapter.render_main_page.fail_click_account_item")
            return res
        sleep(self.render_time)

        return None

    def comment_on_posts(self):
        try:
            for _ in range(self.max_scroll):
                self.crawler.driver.execute_script(
                    f'window.scrollTo(0, 1*document.body.scrollHeight);')
                sleep(self.render_post_time)

                post_names, res = self.get_post_names()
                if res:
                    ErrorLogger.error(f'internal.newfeed_adapter.comment_on_posts.get_post_names_fail.')
                    continue
                InfoLogger.info(f'internal.newfeed_adapter.comment_on_posts.pages {str({"page_names": post_names})}')

                for i, name in enumerate(post_names):
                    if name == '': continue

                    xpath = f'//h3[text()="Bài viết trên Bảng tin"]/following-sibling::div/div[{i + 1}]'
                    elem, res = self.crawler.GetElementByXpath(xpath)
                    if res:
                        InfoLogger.warn(f'internal.newfeed_adapter.comment_on_posts.fail_get_post_elem.')
                        continue

                    self.crawler.action.move_to_element(elem)
                    self.crawler.action.perform()

                    sleep(1)

                    recrawl_name, res = self.crawler.GetText(f'{xpath}//h4[1]//span[1]/a[1]')
                    if recrawl_name not in self.viral_page_names:
                        continue

                    is_negative = self.is_negative_sentiment(xpath)
                    if is_negative:
                        content = self.crawler.GetText(f'{xpath}//div[@data-ad-preview="message"]//span')
                        InfoLogger.warn(
                            f'internal.newfeed_adapter.comment_on_posts.negative_content. Details: {str({"content": content})}')
                        continue

                    is_viral = self.is_viral_post(xpath)
                    if not is_viral:
                        continue

                    res = self.comment_on_post(i + 1, recrawl_name)
                    if res:
                        ErrorLogger.error(f'internal.newfeed_adapter.comment_on_posts.comment_on_post_fail.')
                        continue

                    # sleep(self.anti_spam_time)
                    return None

        except Exception as e:
            ErrorLogger.error(f'internal.newfeed_adapter.comment_on_posts.fail. Details: {str({"error": e})}')
            return e

        return None

    def is_viral_post(self, xpath):
        xpath = f'{xpath}//span[@aria-label="Xem ai đã bày tỏ cảm xúc về tin này"]/following-sibling::*'
        text, res = self.crawler.GetText(xpath)
        if res:
            ErrorLogger.error(f'internal.newfeed_adapter.is_viral_post.fail_get_text.')
            return False
        InfoLogger.info(
            f'internal.newfeed_adapter.is_viral_post.check. {str({"comments": text, "xpath": xpath})}')

        if 'K' in text:
            return True

        if re.search('\d+', text):
            n_comments = re.search('\d+', text).group()
            if n_comments == '': return False
            if int(n_comments) > 200:
                return True

        return False

    def is_negative_sentiment(self, xpath):
        # If have positive emo then positive
        positive_conditions = [f'contains(@aria-label,"{i}")' for i in self.positive_emojis]
        positive_exp = ' or '.join(positive_conditions)
        emoji_xpath = f'{xpath}//span[@aria-label="Xem ai đã bày tỏ cảm xúc về tin này"]/span/span' + \
                      f'//div[{positive_exp}]'

        elems, res = self.crawler.GetElementsByXpath(emoji_xpath)
        if res:
            return False
        if len(elems) > 0: return False

        # If have negative emo then negative
        negative_conditions = [f'contains(@aria-label,"{i}")' for i in self.negative_emojis]
        negative_exp = ' or '.join(negative_conditions)
        emoji_xpath = f'{xpath}//span[@aria-label="Xem ai đã bày tỏ cảm xúc về tin này"]/span/span' + \
                      f'//div[{negative_exp}]'

        elems, res = self.crawler.GetElementsByXpath(emoji_xpath)
        if res:
            InfoLogger.warn(f'internal.newfeed_adapter.is_negative_sentiment.fail_get_emoji_elems.')
            return False
        if len(elems) > 0: return True

        return False

    def get_post_names(self):
        xpath = '//h3[text()="Bài viết trên Bảng tin"]/following-sibling::div/div//h4[1]//span[1]/a[1]'
        texts, res = self.crawler.GetTexts(xpath)
        if res:
            ErrorLogger.error(f'internal.newfeed_adapter.get_post_names.crawler_fail_get_texts.')
            return None, res

        return texts, None

    def comment_on_post(self, idx, host_name):
        xpath = f'//h3[text()="Bài viết trên Bảng tin"]/following-sibling::div/div[{idx}]'

        res = self.open_comment_panel(xpath)
        if res:
            ErrorLogger.error(f'internal.newfeed_adapter.comment_on_post.open_comment_panel_fail.')
            return None, res
        self.crawler.Screenshot('logger/open_comment_panel.png')

        comment_text, res = self.clone_comment(xpath, host_name)
        if res:
            ErrorLogger.error(f'internal.newfeed_adapter.comment_on_post.open_comment_panel_fail.')
            return None, res
        InfoLogger.info(
            f'internal.newfeed_adapter.comment_on_post.success_clone_comment. {str({"comment_text": comment_text})}')

        refined_comment_text, res = self.refine_comment(comment_text)
        if res:
            ErrorLogger.error(f'internal.newfeed_adapter.comment_on_post.refine_comment_fail.')
            return res
        InfoLogger.info(
            f'internal.newfeed_adapter.comment_on_post.success_refine_comment. {str({"refined_comment": refined_comment_text})}')

        res = self.submit_comment(xpath, refined_comment_text)
        if res:
            ErrorLogger.error(f'internal.newfeed_adapter.comment_on_post.submit_comment_fail.')
            return res

        InfoLogger.info(f'internal.newfeed_adapter.comment_on_post.success.')
        return None

    def change_comment_role(self, root):
        role_btn_xpath = root + '//button[@aria-label="Nút chọn vai trò"]'
        res = self.crawler.Click(role_btn_xpath)
        if res:
            ErrorLogger.error(f'internal.newfeed_adapter.change_comment_role.fail_click_role_btn.')
            return res

        sleep(self.render_time)
        self.crawler.Screenshot('logger/open_role_panel.png')
        open('logger/click_role_btn.html', 'w').write(self.crawler.driver.page_source)

        role_texts_xpath = '//*[@role="menu"]//*[@role="menuitemradio"]//span'
        texts, res = self.crawler.GetTexts(role_texts_xpath)
        if res:
            ErrorLogger.error(f'internal.newfeed_adapter.change_comment_role.fail_get_role_item.')
            return res
        InfoLogger.info(f'internal.newfeed_adapter.change_comment_role.get_role_text. {str({"roles": texts})}')

        try:
            for i, text in enumerate(texts):
                if text == self.page_name:
                    role_xpath = f'//*[@role="menu"]//*[@role="menuitemradio"][{i + 1}]'
                    self.crawler.Click(role_xpath)
                    sleep(self.render_time)

                    self.crawler.Screenshot('logger/click_role_btn.png')

        except Exception as e:
            ErrorLogger.error(
                f'internal.newfeed_adapter.change_comment_role.fail_click_role_item. Details: {str({"error": e})}')
            return e

        return None

    def open_comment_panel(self, root):
        xpath = root + '//div[@aria-label="Viết bình luận"]'
        res = self.crawler.Click(xpath)
        if res:
            ErrorLogger.error(f'internal.newfeed_adapter.open_comment_panel.fail_click_comment_panel.')
            return res
        sleep(self.render_time)

        res = self.crawler.Click(xpath)
        if res:
            ErrorLogger.error(f'internal.newfeed_adapter.open_comment_panel.fail_click_comment_panel.')
            return res
        sleep(self.render_time)

        xpath = root + '//div[@data-visualcompletion="ignore-dynamic"]/div[1]/div[2]/div[last()]//span[1]'
        res = self.crawler.Click(xpath)
        if res:
            InfoLogger.warn(f'internal.newfeed_adapter.open_comment_panel.fail_click_more_comment.')
            pass

        sleep(self.render_time)

        return None

    def clone_comment(self, root, host_name):
        xpath_username = root + '//div[@data-visualcompletion="ignore-dynamic"]/div[1]/div[2]/ul/li//span/a/span'
        usernames, res = self.crawler.GetTexts(xpath_username)
        if res:
            ErrorLogger.error(f'internal.newfeed_adapter.clone_comment.fail_get_usernames.')
            return None, res

        comment_text = ''
        for i, u in enumerate(usernames):
            if u == host_name: continue

            xpath_comment_text = root + f'//div[@data-visualcompletion="ignore-dynamic"]/div[1]/div[2]/ul/li[{i + 1}]//span[@lang="vi-VN"]'
            comment_text, res = self.crawler.GetText(xpath_comment_text)
            if res:
                InfoLogger.warn(f'internal.newfeed_adapter.clone_comment.fail_get_comment_text.')
                continue

            break

        if not comment_text:
            InfoLogger.warn(f'internal.newfeed_adapter.clone_comment.empty_comment_text.')

        return comment_text, None

    def refine_comment(self, comment_text):
        greetings = [
            # 'Không liên quan nhưng page đang giảm giá dến 50% cho đồ nữ, mọi người ghé page em tha hồ lựa nha :* :*',
            # 'Không liên quan nhưng đồ page em hơi đẹp và rẻ ạ :P :P',
            # 'Chúc mọi người 1 ngày tốt lành ạ. Ghé page em xem đồ GIẢM GIÁ nhaaaa <3 <3',
            # 'Btw, muốn mua đồ đẹp mà rẻ ghé page em nha ạ ^_^ ^_^',
            # 'Quẹo vô page em lựa đồ giảm giá nha mọi ng O:-) O:-)',
            # 'Quẹo lựa quẹo lựa, đồ đã đẹp còn rẻ nha mọi ngừi ơiiiii <3 <3',
            'Chúc mọi người 1 ngày tốt lành',
            'Chúc những ai thấy comment này sẽ được hạnh phúc <3',
            'Ai đọc được comment nãy sẽ mãi bình an <3',
        ]

        ### prevent ENTER or TAB when typing
        comment_text = re.sub(r'\n|\t', ' ', comment_text)

        comment_text = self.mitigate_comment(comment_text)

        # 2 comment cases: replicate the auth comment or just simply smile
        if random.randint(1, 10) < 6 and comment_text != '':
            comment_text_ret = comment_text + '... =)))'
        else:
            comment_text_ret = '.. :) :)'

        comment_text_ret += ' '
        comment_text_ret += self.url_affiliate

        return comment_text_ret, None

    def mitigate_comment(self, comment_text):
        ### Mitigate negative effects of bad comments as there are a lot of toxic cmts nowadays

        words = [i for i in comment_text.split(' ')]
        comment_text = ' '.join(words[:10]) + '...'

        return comment_text

    def write_comment_text(self, root, refined_comment_text):
        # xpath = root + '//div[@data-visualcompletion="ignore-dynamic"]//form[@role="presentation"]/div[1]'
        xpath = root + '//div[contains(@aria-label,"Bình luận dưới tên")]//ancestor::ul/li[1]//div[contains(@aria-label,"Bình luận dưới tên")]//ul//div[contains(text(),"Phản hồi")]'
        res = self.crawler.Click(xpath)
        if res:
            ErrorLogger.error(f'internal.newfeed_adapter.write_comment_text.fail_open_reply_box.')
            return res

        sleep(self.render_time)

        xpath = root + '//div[contains(@aria-label,"Bình luận dưới tên")]//ancestor::ul/li[1]//div[contains(@aria-label,"Trả lời")]'
        res = self.crawler.Click(xpath)
        if res:
            ErrorLogger.error(f'internal.newfeed_adapter.write_comment_text.fail_click_reply_box.')
            return res

        sleep(1)

        res = self.crawler.Type(refined_comment_text)
        if res:
            ErrorLogger.error(f'internal.newfeed_adapter.write_comment_text.fail_type_content.')
            return res

    def attach_photo(self, root):
        photo_url = self.photos[0]
        dir = self.create_photo_dir(photo_url)
        dir = os.path.abspath(dir)

        xpath = root + '//div[contains(@aria-label,"Bình luận dưới tên")]//ancestor::ul/li[1]//form[@role="presentation"]//ul//input'
        elem, res = self.crawler.GetElementByXpath(xpath)
        if res:
            ErrorLogger.error("Error internal.newfeed_adapter.attach_photo.fail_get_photo_input_elem")
            return res

        self.crawler.driver.execute_script("arguments[0].class='';", elem)
        sleep(1)

        elem.send_keys(dir)
        sleep(self.render_time)

        self.clear_photo_dir(self.tmp_photo_dir)

        sleep(1)
        return None

    def create_photo_dir(self, url):
        if not os.path.exists(self.tmp_photo_dir): os.makedirs(self.tmp_photo_dir)

        n_files = len(os.listdir(self.tmp_photo_dir))
        photo_dir = f"{self.tmp_photo_dir}/{n_files}.png"
        urllib.request.urlretrieve(url, photo_dir)
        return photo_dir

    def clear_photo_dir(self, dir):
        shutil.rmtree(dir)

    def submit_comment(self, xpath, refined_comment_text):
        res = self.write_comment_text(xpath, refined_comment_text)
        if res:
            ErrorLogger.error(f'internal.newfeed_adapter.comment_on_post.write_comment_text_fail.')
            return res

        sleep(1)
        self.crawler.Screenshot('logger/write_comment_text.png')

        res = self.attach_photo(xpath)
        if res:
            InfoLogger.warn(f'internal.newfeed_adapter.comment_on_post.attach_photo_fail.')

        sleep(self.render_time)

        res = self.crawler.Type(Keys.ENTER)
        if res:
            ErrorLogger.error(f'internal.newfeed_adapter.comment_on_post.cannot_submit_comment.')
            return res

        sleep(self.render_time)

        return None
