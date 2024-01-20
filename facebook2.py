import os
import tkinter as tk
from time import sleep
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def configure_driver():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    # chrome_options.add_argument('--headless') #invisible window
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

def post_to_group(driver, group_url, post_text, files_path=[]):
    for i in group_url:
        driver.get(i)
        fb_create_post = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Write something...']"))
        )
        fb_create_post.click()
        sleep(3)
        active_post_area = driver.switch_to.active_element
        active_post_area.send_keys(post_text)
        
        # Image element finder and clicker
        image_logo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Photo/video"]'))
        )
        image_logo.click()
        
        for file_path in files_path:
            file_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file'][multiple]"))
            )
            file_input.send_keys(file_path)
            sleep(2)

        # Further actions to click on 'Post' button if needed
        post_span = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Post']"))
        )
        post_span.click()
        fb_waiting_post = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Write something...']"))
        )
        # Wait for the post to appear in the feed
        WebDriverWait(driver, 30).until(
            lambda driver: post_text in driver.page_source
        )


def close_browser(driver, root):
    driver.quit()
    if root:
        root.destroy()
    
    
def show_confirmation_box(driver):
    # Create the main window
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    # Make the Tkinter window modal and bring it to the front
    root.attributes("-topmost", True)
    root.grab_set()
    try:
        # Wait for the element containing the text
        login_notification = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Check your notifications on another device')]"))
        )
        if login_notification:
            result = messagebox.askyesno("Confirmation: Press 'YES' after confirming your login and 'NO' to close.")
            if result:
                pass # Perform actions if the user clicks 'Yes'
            else:
                close_browser(driver, root) # Perform actions if the user clicks 'No'
                
    except Exception as e:
        print(f"Error occurred while posting: {e}")
    finally:
        # Release the modal state after the messagebox is closed
        root.attributes("-topmost", False)
        root.grab_release()
        # Close the Tkinter window
        root.destroy()


def post_fb(fb_email, fb_password, fb_group, fb_post_text, fb_files_path):
    driver = configure_driver()
    root = None  # Initialize root to None
    try:
        login_facebook(driver, fb_email, fb_password)
        show_confirmation_box(driver)
        post_to_group(driver, fb_group, fb_post_text, fb_files_path)
    finally:
        close_browser(driver, root)
