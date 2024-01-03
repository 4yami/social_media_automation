from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def post_fb(fbEmail, fbPassword, fbGroup, fbPostText):
    # Chrome options to disable notifications
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    # Create a webdriver instance
    driver = webdriver.Chrome(service=Service(), options=chrome_options)

    # fb
    driver.get('https://www.facebook.com')
    user_bar = driver.find_element(By.ID, 'email')
    user_bar.send_keys(fbEmail)
    user_bar = driver.find_element(By.ID, 'pass')
    user_bar.send_keys(fbPassword)
    user_bar.send_keys(Keys.ENTER)
    sleep(3)
    driver.get(fbGroup)


    # Wait for the element to be clickable (you might need to adjust the locator and timeout)
    fbCreatePost = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Write something...']"))
    )
    fbCreatePost.click()

    sleep(3)
    activePostArea = driver.switch_to.active_element
    activePostArea.send_keys(fbPostText)
    sleep(1)

    # Find and click the <span> with the text 'Post'
    # post_span = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "//span[text()='Post']"))
    # )
    # post_span.click()

    # Close the browser window
    driver.quit()