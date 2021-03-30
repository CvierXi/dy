from selenium import webdriver
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import math
from tqdm import tqdm

url = 'https://forum-portal.thirdbridge.com/'
wait_time = 1
keyword = '食品'

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
# options.add_argument('--headless')  # 是否打开浏览器界面，加上该参数后，无需打开
prefs = {'profile.default_content_settings.popups': 0, "profile.default_content_setting_values.automatic_downloads": 1}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=options)

driver.get(url)

# 登陆页面
driver.find_element_by_id('userName').send_keys('deyuzhao@haixiafund.net')
driver.find_element_by_id('userPassword').send_keys('FR789abcd$')
driver.find_element_by_tag_name('button').click()

locator = (By.NAME, 'searchBar')
WebDriverWait(driver, 40, 1).until(expected_conditions.presence_of_element_located(locator))
driver.find_element_by_name('searchBar').send_keys(keyword)   # 搜索文本框
driver.find_element_by_name('searchButton').click()     # 搜索按钮
time.sleep(5)
driver.find_element_by_css_selector("[class='cc_btn cc_btn_accept_all']").click()   # 讨厌的弹窗


def process_search_result_rows(search_result_rows):
    for row in search_result_rows:
        title = row.find_element_by_class_name('search-result__title-con')
        print('\t', title.text)
        icon = row.find_element_by_class_name('search-result__icon')
        if icon.get_attribute('tabindex') == '0':
            action = ActionChains(driver)
            icon.click()
            time.sleep(wait_time)
            c = driver.find_element_by_xpath("//*[text()='Chinese']")
            if c == '':
                icon.click()
                c = driver.find_element_by_xpath("//*[text()='Chinese']")
            c.click()
            action.click(icon).perform()  # 讨厌的弹窗


total_num = int(str(driver.find_element_by_class_name('limit-select').text).split(' ')[-1])
cycle_num = math.ceil(total_num / 20)
for i in range(cycle_num):
    limit = driver.find_element_by_class_name('limit-select')
    print(limit.text)
    button_next = driver.find_element_by_class_name('next')
    search_result_rows = driver.find_elements_by_class_name('search-result__row')
    process_search_result_rows(search_result_rows)
    button_next.click()
    locator = (By.CLASS_NAME, 'search-result__table')
    WebDriverWait(driver, 40, 1).until(expected_conditions.presence_of_element_located(locator))

print('done')
