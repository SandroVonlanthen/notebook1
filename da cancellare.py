import codecs
import os

import time
from venv import create
from selenium import webdriver

from selenium.webdriver.common.by import By


driver = webdriver.Chrome()


driver.get("https://www.chess.com/login_and_go?returnUrl=https://www.chess.com/")
element = driver.find_element(by=By.ID, value="username")
element.send_keys("Notebook3")
element = driver.find_element(by=By.ID, value="password")
element.send_keys("Notebook3SocialComputing")
element = driver.find_element(by=By.ID, value="login")
element .click()
element = driver.find_element(by=By.ID, value="quick-link-lessons").click()
element = driver.find_element(by=By.CLASS_NAME, value="ui_outside-close-component").click()
element= driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
driver.get_screenshot_as_file("webpage.png")
driver.save_screenshot("test.png")

S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment                                                                                                                
driver.find_element_by_tag_name('body').screenshot('web_screenshot.png')

#Notebook3
#Notebook3SocialComputing