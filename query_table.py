from selenium import webdriver
import time

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

total_result = ''
for province_name in province_list:
    if province_name == '全部':
        continue
    print(province_name)    # 打印-- 省份 --名字
    province_item = driver.find_element_by_link_text(province_name)    # 该省份名字对应的选项
    province_item.click()   # 点击该省份名字
    time.sleep(wait_time)

    button_search.click()   # 点击查询按钮
    time.sleep(wait_time)

    table = driver.find_element_by_class_name('por_table_content')  # 找到表格
    lines = table.find_elements_by_tag_name('tr')   # 表格的每一行
    result_out = ''
    for line in lines:
        line_data = line.find_elements_by_tag_name('td')    # 表格每一行的所有元素，第一行为标题行，如有需要可以去掉
        line_out = ''
        for data in line_data:
            data_title = data.get_property('title')
            if data_title != '':
                line_out = line_out + data_title + ','
            else:
                line_out = line_out + data.text + ','
        print(line_out)
        # result_out = result_out + line_out + '\n'
    # print(result_out)
    # total_result = total_result + result_out + '\n'
    print()

    # boxes[1].click()    # 点击城市下拉框
    # time.sleep(wait_time)
    # city_element = driver.find_element_by_id('cityList')   # 找到城市下拉框里的所有元素
    # city_list = str(city_element.text).split('\n')    # 城市下拉框里的所有文字列表，内容为string类型
    # for city_name in city_list:
    #     if city_name == '全部':
    #         continue
    #     print('- %s' % city_name)   # 打印-- 城市 --名字
    boxes[0].click()
    time.sleep(wait_time)
