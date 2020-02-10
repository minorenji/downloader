from selenium import webdriver
from selenium.common import exceptions


class Driver:
    def __init__(self):
        self.driver = webdriver.Chrome("chromedriver.exe")

    def downloads_window(self):
        if len(self.driver.window_handles) == 1:
            self.driver.switch_to.new_window('window')

    def nexus_login(self, url: str):
        self.driver.get(url)
        assert "Users" in self.driver.title, "Unexpected webpage!"
        username = self.driver.find_element_by_id("user_login")
        username.send_keys("sean.treefrog@gmail.com")
        password = self.driver.find_element_by_id("user_password")
        password.send_keys(".2s4_4qXgWfK#?E")
        self.driver.find_element_by_name("commit").click()

    def nexus_download(self, url: str):
        self.driver.get(url)
        try:
            self.driver.find_element_by_id('slowDownloadButton').click()
        except exceptions.NoSuchElementException:
            login_link = self.driver.find_element_by_class_name("replaced-login-link").get_attribute("href")
            self.nexus_login(login_link)
            self.nexus_download(url)


if __name__ == "__main__":
    new_driver = Driver()
    new_driver.nexus_download("https://www.nexusmods.com/skyrimspecialedition/mods/266?tab=files&file_id=121306")