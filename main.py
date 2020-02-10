from selenium import webdriver

driver = webdriver.Chrome("chromedriver.exe")


def nexus_login(browser: webdriver.Chrome):
    browser.get("https://users.nexusmods.com/auth/sign_in")
    assert "Users" in browser.title, "Unexpected webpage!"

    username = browser.find_element_by_id("user_login")
    username.send_keys("sean.treefrog@gmail.com")
    password = browser.find_element_by_id("user_password")
    password.send_keys(".2s4_4qXgWfK#?E")
    browser.find_element_by_name("commit").click()


def nexus_download(browser: webdriver.Chrome, url: str):
    browser.get(url)
    try:
        button = browser.find_element_by_id("//a[@class='btn inline-flex' and ./span/text()='Manual download']")
    except:
        raise
    button.get_attribute("href")


if __name__ == "__main__":
    assert "None"
    nexus_login(driver)