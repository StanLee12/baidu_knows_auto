#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException    
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json

def add_cookis():
  cookies_file = open('cookies2.json')
  cookies = json.loads(cookies_file.read())
  cookies_file.close()

  for cookie in cookies:
    if 'sameSite' in cookie:
      cookie['sameSite'] = 'Strict'
    driver.add_cookie(cookie)

def to_questions_page():
  questions_li = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/ul/li[2]')
  questions_li.click()

def is_element_exist(xpath):
  try:
    driver.find_element(By.XPATH, xpath)
  except NoSuchElementException:
    return False
  return True

def answer():
  order_titles = driver.find_elements(By.CLASS_NAME, 'order-item')
  for title in order_titles:
    item_id = title.get_property('id')
    button_selector = '#' + item_id + ' > div.order-container > div.container-right > button'
    print('Selector', button_selector)
    order_button = driver.find_element(By.CSS_SELECTOR, button_selector)
    print(order_button.get_property('className'))

def is_element_exist(xpath):
  try:
    driver.find_element(By.XPATH, xpath)
  except:
    return False
  return True

def back_to_questions_page():
  questions_tab = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/ul/li[2]')
  questions_tab.click()
  time.sleep(3)
  click_refresh()

def handle_after_enter_contact():
  try:
    print('进入订单会话界面, 等待加载...')
    print('等待聊天框加载...')
    time.sleep(10)
    answer_input = WebDriverWait(driver, 10, 1).until(
      EC.presence_of_element_located((By.XPATH, '//*[@id="textarea"]'))
    )
    print(driver.current_url)
    time.sleep(2)
    answer_input.click()
    time.sleep(1)
    answer_input.send_keys('请稍候...即将为您答题!')
    time.sleep(1)
    answer_btn = driver.find_element(By.XPATH, '//*[@id="rc-tabs-0-panel-order"]/div/div/div[2]/div/div[2]/div[2]/div[2]')
    print('是否可以发送', answer_btn.get_property('className'))
    time.sleep(3)
  except:
    print('获取输入框失败, 返回抢单界面...')
    back_to_questions_page()
  finally:
    print('完成一条消息!')
    

# def do_action(choose):
#   if choose == 'y':
#     to_answer = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div/div[3]/button[2]')
#     to_answer.click()
#     handle_after_enter_contact()
#   else:
#     to_cancel = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div/div[3]/button[1]')
#     to_cancel.click()
#     print('cancele answer!')
#     click_refresh()

# 处理当错误弹窗存在的情况, 暂时让用户输入y/n决定后续操作
def handle_ant_modal_shown():
  message_title = driver.find_element(By.XPATH, '//html/body/div[3]/div/div[2]/div/div[2]/div/div[2]')
  print(message_title.text)
  to_answer = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div/div[3]/button[2]')
  to_answer.click()
  handle_after_enter_contact()

# 检查错误弹窗判断是否已有订单却还没处理
def check_ant_modal():
  modal_xpath = '/html/body/div[3]/div/div[2]'
  if is_element_exist(modal_xpath):
    error_modal = driver.find_element(By.XPATH, modal_xpath)
    error_modal_status = error_modal.get_property('style')
    is_show = error_modal_status != 'display: none;'
    if is_show:
      handle_ant_modal_shown()
    else:
      print('订单已被其他人抢走啦, 等待刷新...')
      click_refresh()
  else:
    print('获取订单异常, 没有找到Modal弹窗, 等待刷新... ')
    click_refresh()

# 通过检查 咨询消息 Tab是否被选中判断是否进入订单对话界面
def check_tab_3_is_selected():
  contact_tab = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/ul/li[3]')
  is_selected = contact_tab.get_property('tabindex') == '1'
  if is_selected:
    handle_after_enter_contact()
  else:
    time.sleep(2)
    check_ant_modal()

def answer_first():
  order_items = driver.find_elements(By.CLASS_NAME, 'order-item')
  first_item_id = order_items[0].get_property('id')
  button_selector = '#' + first_item_id + ' > div.order-container > div.container-right > button'
  order_button = driver.find_element(By.CSS_SELECTOR, button_selector)
  print('点击抢单按钮...')
  order_button.click()
  time.sleep(5)
  check_tab_3_is_selected()

def click_refresh():
  refresh_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[3]/div/div[2]/div/span')
  refresh_btn.click()
  run()

# 根据问题界面的空数据提示文本判断数据是否为空
def run():
  print('启动, 获取订单...')
  try:
    null_text_xpath = '//*[@id="root"]/div/div/div[3]/div/div[4]/div/div[2]'
    null_text = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.XPATH, null_text_xpath))
    )
    if null_text.text:
      print(null_text.text)
      time.sleep(1)
      click_refresh()
    else:
      print('发现问题, 开始抢单～')
      time.sleep(2)
      answer_first()
  except:
    driver.refresh()
    time.sleep(3)
    run()

chrome_options = Options() 
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--start-maximized')
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(10)
driver.get('https://zhidao.baidu.com/pages/consult/index/grabbing-orders?role=consultor')
time.sleep(5)
driver.delete_all_cookies()
time.sleep(1)
add_cookis()
time.sleep(1)
driver.refresh()
time.sleep(5)
to_questions_page()
time.sleep(5)

run()





