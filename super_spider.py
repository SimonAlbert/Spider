import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import jieba
import pandas as pd
import numpy as np
import os
from urllib.request import urlretrieve

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径



# storeurl = "F:\desktop\spider\\tianmao_guochao\wassup"
# storeurl = "F:\desktop\spider\\tianmao_guochao\China_panda"
storeurl = "F:\desktop\spider\\tianmao_guochao\SUPERTOFU"

# storewebpath = 'https://wassup.taobao.com/search.htm?spm=a1z10.1-c-s.w5001-21543236065.2.2bab6ca8FYFV3Q&search=y&scene=taobao_shop'
# storewebpath = 'https://nengmaoshangdian.taobao.com/search.htm?spm=a1z10.1-c-s.w5001-22078129865.8.f99a5793SZ9Y2X&search=y&scene=taobao_shop'
storewebpath = 'https://supertofu.taobao.com/category.htm?spm=a1z10.3-c-s.w4010-18503399518.2.35d664a4hTtort&search=y'

# typelist = ['T恤', '短裤']
# typelist = ['短裤', '长裤']
typelist = ['TEES／T恤', 'ALOHA／夏威夷衬衫', 'PANTS／裤装', 'SHIRTS／衬衫']

class Wassup:
    def __init__(self, url):
        mkdir(storeurl)
        for type in typelist:
            mkdir(storeurl +'\\'+ type)
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = \
            webdriver.Chrome('D:\ChromeGreen\\70.0.3538.102\\chromedriver.exe',options=options)
        self.driver.get('https://login.taobao.com/member/login.jhtml?spm=a1z10.3-c-s.754894437.1.5b1668b6OWdBO3&f=top&redirectURL=https%3A%2F%2Fchris-lv.taobao.com%2Fcategory.htm%3Fspm%3Da1z10.3-c-s.w4010-21996178487.2.44c668b6dd7SWq%26search%3Dy')
        time.sleep(1)

        try:
            self.driver.find_element_by_class_name('weibo-login').click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", self.driver.find_element_by_class_name('weibo-login'))
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="pl_login_logged"]/div/div[2]/div/input').send_keys('17853260016')
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="pl_login_logged"]/div/div[3]/div/input').send_keys('lomx2731269***')
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="pl_login_logged"]/div/div[3]/div/input').send_keys(Keys.ENTER)
        time.sleep(3)

        self.driver.get(url)
        print("登陆完成")
        time.sleep(3)

        self.mainWindow = self.driver.current_window_handle  # 保存主页面句柄

    def get_goods(self, typelist):
        hand = ['商品名', '价格', '销量']
        for type in typelist:
            data = pd.DataFrame(columns=hand)
            time.sleep(6)
            # 点击商品类型
            try:
                self.driver.find_elements_by_link_text(type)[-1].click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", self.driver.find_elements_by_link_text(type)[-1])
            # 翻页
            flag = True
            while flag:

                time.sleep(5)
                href_list = []
                shangpinliebiao = self.driver.find_elements_by_xpath('//dd[@class="detail"]')

                print(shangpinliebiao)
                for item in shangpinliebiao:
                    name = item.find_element_by_xpath('.//a[@class="item-name J_TGoldData"]').text
                    price = item.find_element_by_xpath('.//span[@class="c-price"]').text
                    sale_num = item.find_element_by_xpath('.//span[@class="sale-num"]').text
                    print(name, price, sale_num)
                    data = data.append([{'商品名': name, '价格': price, '销量': sale_num}], ignore_index=True)
                print(data)
                # 保存当前种类商品列表
                time.sleep(5)
                links = self.driver.find_elements_by_xpath('//a[@class="item-name J_TGoldData"]')
                # 依次打开商品页
                for link in links:
                    href_list.append(link.get_attribute('href'))
                    # 进入详情页
                    try:
                        link.click()
                    except Exception:
                        self.driver.execute_script("arguments[0].click();", link)
                    time.sleep(3)
                    handles = self.driver.window_handles
                    self.driver.switch_to.window(handles[1])
                    # 读取评论
                    self.get_comment(type)
                    # 关闭此页
                    self.driver.close()
                    self.driver.switch_to.window(self.mainWindow)
                try:
                    self.driver.find_element_by_xpath('//a[@class="J_SearchAsync next"]').click()
                    flag = True
                except:
                    flag = False

            time.sleep(5)
            data.to_excel(storeurl + "\\" + type + '\\汇总.xls')


    def get_comment(self, type):
        head = self.driver.find_element_by_xpath('//h3[@class="tb-main-title"]').text
        time.sleep(2)

        # 打开评论
        try:
            self.driver.find_element_by_xpath('//*[@id="J_TabBar"]/li[2]/a').click()
        except Exception:
            self.driver.execute_script("arguments[0].click();",
                                       self.driver.find_element_by_xpath('//*[@id="J_TabBar"]/li[2]/a'))
        time.sleep(3)

        try:
            self.driver.find_element_by_xpath('//*[@id="J_TabBar"]/li[2]/a').click()
        except Exception:
            self.driver.execute_script("arguments[0].click();",
                                       self.driver.find_element_by_xpath('//*[@id="J_TabBar"]/li[2]/a'))
        temp = storeurl + "\\" + type + "\\" + head + "\\"
        mkdir(temp[:-1])
        # 保存图片
        images = self.driver.find_elements_by_xpath('//div[@class="tb-pic tb-s50"]/a/img')

        for image in images:
            url = image.get_attribute('src')
            url = url[:-15]+"400x400.jpg"
            try:
                response = requests.get(url)
                with open(temp+url[-32:-24]+'.jpg', 'wb') as fp:
                    fp.write(response.content)
            except:
                print("一张图片错误")
                print(url)
            # 写入图片


        # -3好评，-2中评，-1差评
        pj = ['好评', '中评', '差评']
        # 评论等级选择按钮
        radios = self.driver.find_elements_by_xpath('//input[@name="J_KgRate_ReviewType"]')[-3:]

        for i in range(3):
            # 选择某类评论
            try:
                radios[i].click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", radios[i])
            time.sleep(5)
            self.save_comment(temp + pj[i] + ".xls")

    # 保存一类评论
    def save_comment(self, filename):
            # 滑动屏幕
            js = "var q=document.documentElement.scrollTop=10000"  # documentElement表示获取根节点元素
            self.driver.execute_script(js)
            # 评论文本
            items = []
            # 评论日期
            dates = []
            # 颜色分类
            colours = []
            # flag表示是否存在下一页/是否可以继续翻页
            flag = True
            while flag:
                try:
                    details = self.driver.find_elements_by_xpath('//div[@class="review-details"]')
                    for detail in details:
                        # 找评论文本
                        aa = detail.find_elements_by_xpath('.//div[@class="J_KgRate_ReviewContent tb-tbcr-content "]')
                        aaa = []
                        for a in aa:
                            aaa.append(a.text)
                        items.append("".join(aaa))
                        # 日期
                        bb = detail.find_element_by_xpath('.//span[@class="tb-r-date"]')
                        dates.append(bb.text)
                        cc = detail.find_element_by_xpath('.//div[@class="tb-r-info"]')
                        colours.append(cc.text[17:])
                    try:

                        try:
                            self.driver.find_element_by_xpath('//li[@class="pg-next"]').click()
                        except Exception:
                            self.driver.execute_script("arguments[0].click();",
                                                       self.driver.find_element_by_xpath('//li[@class="pg-next"]'))
                        time.sleep(3)
                        flag = True
                    except Exception:
                        print("已经是最后一页了")
                        flag = False
                        # 没有更多评论

                except Exception:
                    print('此页无评论')
            comment = {
                "评论内容": items,
                "评论时间": dates,
                "颜色分类": colours
            }
            # cols = ['评论内容', '评论时间', '颜色分类']
            df = pd.DataFrame(comment)
            df.to_excel(filename)


if __name__ == '__main__':
    w = Wassup(storewebpath)
    w.get_goods(typelist)



