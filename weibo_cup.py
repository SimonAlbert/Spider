from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

driver.get('https://weibo.com/')
time.sleep(5)
driver.find_element_by_id('loginname').send_keys('17853260016')
driver.find_element_by_name('password').send_keys('lomx2731269***')
time.sleep(3)
driver.find_element_by_name('password').send_keys(Keys.ENTER)
# vcode = input('验证码：')

# driver.find_element_by_name('verifycode').send_keys(vcode)
# driver.find_element_by_name('password').send_keys(Keys.ENTER)
time.sleep(3)
driver.get('https://weibo.com/')
time.sleep(3)

elements = driver.find_elements_by_class_name('W_face_radius')
print(len(elements))
elements[0].click()

