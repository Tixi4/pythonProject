from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from auth_data import username, password
import time
import random
from selenium.common.exceptions import NoSuchElementException

class InstagramBot():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome('..//chromedriver_win32/chromedriver.exe')

    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def login(self):

        browser = self.browser
        browser.get('https://www.instagram.com')
        time.sleep(random.randrange(3, 5))

        username_input = browser.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(2)

        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)
        time.sleep(5)

    def like_foto_hashtage(self, hashtag):

        browser = self.browser
        browser.get(f'https://www.instagram.com/{hashtag}/')
        time.sleep(5)

        for i in range(1, 5):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3, 5))

        hrefs = browser.find_elements_by_tag_name('a')
        posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

        for url in posts_urls:
            try:
                browser.get(url)
                time.sleep(10)
                like_button = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button')
                like_button.click()
                time.sleep(random.randrange(8, 10))
            except Exception as ex:
                print(ex)
                self.close_browser()

    #  Проверяем по xpath существует ли элемент

    def xpath_axists(self, url):

        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    #Ставим лайк на пост  по прямой ссылке

    def put_exactly_like(self, userpost):

        browser = self.browser
        browser.get(userpost)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/div/h2"
        if self.xpath_axists(wrong_userpage):
            print("Такого поста не существует")
            self.close_browser()
        else:
            print("Пост найден, лайкаем!")
            time.sleep(2)

            like_button = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button')
            like_button.click()
            time.sleep(3)

            print(f"Лайк на пост: {userpost} поставлен")
            self.close_browser()

    # Ставим лайк по ссылке на акк пользователя
    def put_many_likes(self,userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/div/h2"
        if self.xpath_axists(wrong_userpage):
            print("Такого пользователя не существует")
            self.close_browser()
        else:
            print("Пользовтель найден, лайкаем!")
            time.sleep(2)

            posts_count = int(browser.find_element_by_xpath("/html/body/div[1]/section/main/div/ul/li[1]/span/span").text)
            loops_count = int(posts_count / 12)
            print(loops_count)

            posts_urls = []
            for i in range(0, loops_count):
                hrefs = browser.find_elements_by_tag_name('a')
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

                for href in hrefs:
                    posts_urls.append(href)

                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(2,4))
                print(f"Итерация #{i}")

            file_name = userpage.split("/")[-2]

            with open (f'{file_name}.txt', 'a') as file:
                for post_url in posts_urls:
                    file.write(post_url + "\n")

            self.close_browser()

            # like_button = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button')
            # like_button.click()
            # time.sleep(3)
            #
            # print(f"Лайк на пост: {userpost} поставлен")
            # self.close_browser()

my_bot = InstagramBot(username, password)
my_bot.login()
my_bot.put_many_likes('https://www.instagram.com/kostya.verenich/')




