# debugging on line 38
# modified on 2/13/2019
# debugging on line 35 and insert a line of comment on line 36
# modified on 2/20/2019
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from API_Test import Return_Valid_Num

ID = input("输入学号:")
PASSWORD = input("输入密码:")

r_url = "http://172.16.213.7/gymbook/gymBookAction.do?ms=viewGymBook&gymnasium_id=2&item_id=5326&userType="
driver = webdriver.Firefox(executable_path="geckodriver.exe")
driver.get(r_url)
driver.find_element_by_xpath('//*[@id="un"]').send_keys(ID)
driver.find_element_by_xpath('//*[@id="pd"]').send_keys(PASSWORD)
driver.find_element_by_xpath('//*[@id="index_login_btn"]').click()

# Data input
root_id = [50419, 50469, 50519, 50569]  # 第一行对应的四个id后面是d=-2的等差
require_list = []
length = eval(input("需要预约几块场地？(一个小时算一块)"))
for i in range(length):
    require_list.append([eval(input("预约几号场馆:1-4"))-1])
    require_list[i].append(eval(input("第几行？:1-14"))-1)


# start fighting when there is 5s left
while True:
    ntime = time.localtime(time.time())
    if ntime.tm_hour == 7 and ntime.tm_min == 29 and ntime.tm_sec > 55:  # gracefully using 'time'
        break
js = "document.getElementsByClassName('modal-footer')[1].children[0].click()"  # 在预约时间外是这句话弹出框点确定由于结构不同，按钮的位置不一样
#  js = "document.getElementsByClassName('modal-footer')[3].children[0].click()"
driver.execute_script(js)
time.sleep(0.5)  # experience value
while True:  # bug here
    try:
        driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[1]/div/div/div[3]/ul/li[3]").click()
        break
    except NoSuchElementException:
        driver.refresh()
        time.sleep(0.5)
time_start = time.time()
last_day = WebDriverWait(driver, 4).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div/div/div[5]/a[4]")))
last_day.click()  # 由于需求是只选最后一天的，这一步点击统统加上
driver.switch_to.frame('overlayView')

# Wait until time is up:
for j in range(length):
    current_id = root_id[require_list[j][0]]-2*require_list[j][1]
    select_element = driver.find_element_by_xpath('//*[@id="resourceTd_' + str(current_id) + '"]')
    if select_element.get_attribute('lock') != "true":
        select_element.click()
    else:
        print("第"+str(j+1)+"个请求"+"已满")

driver.switch_to.default_content()
# 点击预约按钮
driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div/div/div[6]/span/a/span/span').click()
Kaptcha = WebDriverWait(driver, 2).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="kaptchaImage"]')))
Kaptcha.screenshot('Kaptcha.png')

# 调用API识别验证码

result = str(Return_Valid_Num())

js2 = "document.getElementById('checkcodeuser').value='"+result+"'"  # 弹出框输入验证码
js3 = "document.getElementsByClassName('btn')[3].click()"  # 弹出框的确认按钮
driver.execute_script(js2)
driver.execute_script(js3)
js4 = "document.getElementsByClassName('btn')[6].click()"  # 稍后网上支付
driver.execute_script(js4)
time_end = time.time()
print('time cost:', time_end-time_start)


