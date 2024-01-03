from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def configure_driver():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def login_facebook(driver, email, password):
    driver.get('https://www.facebook.com')
    user_bar = driver.find_element(By.ID, 'email')
    user_bar.send_keys(email)
    password_bar = driver.find_element(By.ID, 'pass')
    password_bar.send_keys(password)
    password_bar.send_keys(Keys.ENTER)
    sleep(3)

def post_to_group(driver, group_url, post_text):
    driver.get(group_url)
    fb_create_post = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Write something...']"))
    )
    fb_create_post.click()
    sleep(3)
    active_post_area = driver.switch_to.active_element
    active_post_area.send_keys(post_text)
    sleep(1)
    # Further actions to click on 'Post' button if needed
    # post_span = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "//span[text()='Post']"))
    # )
    # post_span.click()

def close_browser(driver):
    driver.quit()

def post_fb(fb_email, fb_password, fb_group, fb_post_text):
    driver = configure_driver()
    try:
        login_facebook(driver, fb_email, fb_password)
        post_to_group(driver, fb_group, fb_post_text)
    finally:
        sleep(5000)
        close_browser(driver)
