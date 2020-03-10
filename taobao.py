
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import getpass
Chrome_options = Options()
Chrome_options.add_argument('--start-maximized')
Chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe', chrome_options=Chrome_options)


driver.get('https://login.taobao.com/member/login.jhtml')
time.sleep(1)
# driver.find_element_by_link_text('密码登录').click()
# time.sleep(1)
driver.find_element_by_id('TPL_username_1').send_keys('没故事的mr_c')
time.sleep(1)
password = input('密码：')
time.sleep(1)
driver.find_element_by_id('TPL_password_1').click()
time.sleep(1)
driver.find_element_by_id('TPL_password_1').send_keys(password)
time.sleep(1)
driver.find_element_by_id('TPL_password_1').send_keys(Keys.ENTER)
time.sleep(5)
# a = input()
driver.find_element_by_id('TPL_password_1').send_keys(password)
time.sleep(1)
driver.find_element_by_id('TPL_password_1').send_keys(Keys.ENTER)
time.sleep(3)
# search.send_keys('台灯')
# search.send_keys(Keys.ENTER)
# driver.implicitly_wait(3)
# item_list = driver.find_elements_by_xpath("//div[@class='item J_MouserOnverReq  ']")
# print(len(item_list))
# save = pd.DataFrame(columns=['商品名', '价格', '店铺', '销量'])
# dic = {'商品名': '', '价格': '', '店铺': '', '销量': ''}
# spm = []
# jg = []
# dp = []
# xl = []
# for x in item_list:
#     spm.append(x.find_element_by_xpath("div[@class='ctx-box J_MouseEneterLeave J_IconMoreNew']/div/a").text)
#     print(spm[-1])
#     jg.append(x.find_element_by_tag_name('strong').text)
#     dp.append(x.find_element_by_xpath("div/div/div[@class='shop']/a").find_elements_by_tag_name('span')[-1].text)
#     print(dp[-1])
#     # ('shopname J_MouseEneterLeave J_ShopInfo').find_elements_by_tag_name('span')[-1].text
#     xl.append(x.find_element_by_class_name('deal-cnt').text)
# print(spm)
# print(jg)
# print(dp)
# print(xl)
# save['商品名'] = spm
# save['价格'] = jg
# save['店铺'] = dp
# save['销量'] = xl
# save.to_excel('taobao.xls')


def get_data(name):
    driver.get('https://www.taobao.com')
    driver.implicitly_wait(3)
    search = driver.find_element_by_id('q')
    search.send_keys(name)
    search.send_keys(Keys.ENTER)
    driver.implicitly_wait(3)
    item_list = driver.find_elements_by_xpath("//div[@class='item J_MouserOnverReq  ']")
    print(len(item_list))
    save = pd.DataFrame(columns=['商品名', '价格', '店铺', '销量'])
    dic = {'商品名': '', '价格': '', '店铺': '', '销量': ''}
    spm = []
    jg = []
    dp = []
    xl = []
    for x in item_list:
        spm.append(x.find_element_by_xpath("div[@class='ctx-box J_MouseEneterLeave J_IconMoreNew']/div/a").text)
        print(spm[-1])
        jg.append(x.find_element_by_tag_name('strong').text)
        dp.append(x.find_element_by_xpath("div/div/div[@class='shop']/a").find_elements_by_tag_name('span')[-1].text)
        print(dp[-1])
        # ('shopname J_MouseEneterLeave J_ShopInfo').find_elements_by_tag_name('span')[-1].text
        xl.append(x.find_element_by_class_name('deal-cnt').text)
    # print(spm)
    # print(jg)
    # print(dp)
    # print(xl)
    save['商品名'] = spm
    save['价格'] = jg
    save['店铺'] = dp
    save['销量'] = xl
    save.to_excel(name+'.xls')

get_data('台灯')
get_data('吸顶灯')


