from selenium import webdriver
from selenium.common import exceptions
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time


class Driver:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome("chromedriver.exe", options=chrome_options)
        self.driver.implicitly_wait(2)
        self.disable_auto_downloads()
        self.main_window = self.driver.current_window_handle
        self.downloads_window()

    def downloads_window(self):
        self.driver.execute_script('''window.open("chrome://downloads/","_blank");''')
        # self.driver.get("chrome://downloads/")
        download_window = self.driver.current_window_handle
        self.driver.switch_to.window(self.main_window)

    def cancel_download(self):
        time.sleep(5)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        root1 = self.driver.find_element_by_tag_name('downloads-manager')
        shadow_root1 = self.expand_shadow_root(root1)
        root2 = shadow_root1.find_element_by_css_selector('downloads-item')
        shadow_root2 = self.expand_shadow_root(root2)
        shadow_root2.find_element_by_css_selector("cr-button[focus-type='cancel']").click()
        self.driver.switch_to.window(self.main_window)

    def nexus_login(self, url: str):
        self.driver.get(url)
        assert "Users" in self.driver.title, "Unexpected webpage!"
        username = self.driver.find_element_by_id("user_login")
        username.send_keys("sean.treefrog@gmail.com")
        password = self.driver.find_element_by_id("user_password")
        password.send_keys(".2s4_4qXgWfK#?E")
        self.driver.find_element_by_name("commit").click()
        self.driver.switch_to.window(self.main_window)
        time.sleep(5)

    def disable_auto_downloads(self):
        self.driver.get("chrome://settings/content/automaticDownloads")
        root1 = self.driver.find_element_by_tag_name("settings-ui")
        shadow_root1 = self.expand_shadow_root(root1)
        root2 = shadow_root1.find_element_by_css_selector('settings-main')
        shadow_root2 = self.expand_shadow_root(root2)
        root3 = shadow_root2.find_element_by_css_selector('settings-basic-page')
        shadow_root3 = self.expand_shadow_root(root3)
        root4 = shadow_root3.find_element_by_css_selector('settings-privacy-page')
        shadow_root4 = self.expand_shadow_root(root4)
        root5 = shadow_root4.find_element_by_css_selector('category-setting-exceptions')
        shadow_root5 = self.expand_shadow_root(root5)
        root6 = shadow_root5.find_element_by_tag_name('site-list')
        shadow_root6 = self.expand_shadow_root(root6)
        shadow_root6.find_element_by_id('addSite').click()
        root7 = shadow_root6.find_element_by_tag_name('add-site-dialog')
        shadow_root7 = self.expand_shadow_root(root7)
        root8 = shadow_root7.find_element_by_css_selector('cr-input')
        shadow_root8 = self.expand_shadow_root(root8)

        site_field = shadow_root8.find_element_by_id('input')
        site_field.send_keys("www.nexusmods.com")
        shadow_root7.find_element_by_class_name("action-button").click()

        root9 = shadow_root4.find_element_by_css_selector('category-default-setting')
        shadow_root9 = self.expand_shadow_root(root9)
        root10 = shadow_root9.find_element_by_css_selector('settings-toggle-button')
        shadow_root10 = self.expand_shadow_root(root10)
        shadow_root10.find_element_by_css_selector('cr-toggle').click()

    def nexus_download(self, url: str, first=None):
        self.driver.get(url)
        if first:
            login_link = self.driver.find_element_by_class_name("replaced-login-link").get_attribute("href")
            self.nexus_login(login_link)
            self.driver.get(url)
        button = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.ID, "slowDownloadButton")))
        time.sleep(1)
        button.click()
        self.driver.implicitly_wait(10)
        download_link = self.driver.find_element_by_class_name('donation-wrapper').find_element_by_tag_name('a'). \
            get_attribute('href')
        self.driver.implicitly_wait(1)
        print(download_link)

        file_name = download_link.split('/')[-1].split('?')[0].replace('%20', ' ')
        try:
            self.cancel_download()
        except exceptions.NoSuchElementException:
            self.driver.switch_to.window(self.main_window)
            return
        self.download_file(download_link, file_name)

    def download_file(self, url: str, file_name: str):
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            current_bytes = 0
            file_path = "E:/STEP Mods/" + file_name
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        current_bytes += 1024 * 1024
                        print(str(current_bytes))
                        # f.flush()

    def expand_shadow_root(self, element):
        shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
        return shadow_root


def download_list(path, driver: Driver):
    with open(path, 'r') as f:
        links = f.readlines()
    links.reverse()
    first = True
    for link in reversed(links):
        if "nexusmods" in link:
            driver.nexus_download(link, first=first)
            first = False
            links.remove(link)
            with open(path, 'w') as f:
                f.writelines(links)


if __name__ == "__main__":
    new_driver = Driver()
    download_list("download_list.txt", new_driver)
    # new_driver.driver.quit()
