import json, time
from .netweaver import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

nw = NetWeaver(
    root_url="https://finance.yahoo.com/",
    use_undetected=True,
    binary_location = "./drivers/chrome/123.0.6262.0/chrome-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
    executable_path = "./drivers/chrome/123.0.6262.0/chromedriver-mac-x64"
)
print("abc")
nw.sleep(2)
nw.scroll_to_window_scrollHeight()


input(">")
# nw.scroll_to_element_scrollTop()
