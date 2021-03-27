from selenium import webdriver
import time
import pandas
from tqdm import tqdm

url = 'https://system.eduyun.cn/bmp-web/'   # 网址链接
wait_time = 0.35     # 每一次下拉框点击后的等待时间，单位毫秒，主要是等待数据库返回网页刷新数据，测试取值0.3（即300毫秒）以上没有问题

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.add_argument('--headless')  # 是否打开浏览器界面，加上该参数后，无需打开
driver = webdriver.Chrome(chrome_options=options)

driver.get(url)

boxes = driver.find_elements_by_class_name('qjf_seleautocur')   # 对应该网页的三个下拉框（省、市、区）
boxes[0].click()    # 点击省份下拉框
time.sleep(wait_time)

button_search = driver.find_element_by_class_name('lightBtn')   # 查询按钮

province_element = driver.find_element_by_id('provinceList')   # 找到省份下拉框里的所有元素
province_list = str(province_element.text).split('\n')    # 省份下拉框里的所有文字列表，内容为string类型

total_table_pd = pandas.DataFrame()
for province_name in tqdm(province_list):
    if province_name == '全部':
        continue
    # print(province_name)    # 打印-- 省份 --名字
    province_item = driver.find_element_by_link_text(province_name)    # 该省份名字对应的选项
    province_item.click()   # 点击该省份名字
    time.sleep(wait_time)

    button_search.click()   # 点击查询按钮
    time.sleep(wait_time)

    table = driver.find_element_by_class_name('por_table_content')  # 找到表格
    lines = table.find_elements_by_tag_name('tr')   # 表格的每一行
    province_table_list = []
    line_title_list = []
    for i in range(len(lines)):
        line_data = lines[i].find_elements_by_tag_name('td')  # 表格每一行的所有元素，第一行为标题行，根据需要保留/去除
        line_data_list = [province_name]
        for data in line_data:
            data_title = data.get_property('title')     # 网页中的text为"XXX..."的内容，对应的title的值是完整的
            if data_title != '':
                line_data_list.append(data_title)
            else:
                line_data_list.append(data.text)
        if i == 0:  # 标题行
            line_title_list = line_data_list
            line_title_list[0] = '省份'
            continue
        province_table_list.append(line_data_list)
    province_table_pd = pandas.DataFrame(province_table_list, columns=line_title_list)
    # province_table_pd.to_csv('./result_' + province_name + '.csv', index=False, encoding='utf_8_sig')   # 此处可对每个省份的数据进行单个的存储
    total_table_pd = total_table_pd.append(province_table_pd)

    boxes[0].click()        # 点击省份下拉框
    time.sleep(wait_time)

total_table_pd.to_csv('./result.csv', index=False, encoding='utf_8_sig')    # 保存为csv，该encoding解决本次中文乱码问题
