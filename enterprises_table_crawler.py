from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://finance.vietstock.vn/doanh-nghiep-a-z?page=1')

def fill_text_box(id, content):
    text_box = driver.find_element(By.ID, id)
    text_box.clear()
    text_box.send_keys(content)

def login(driver):
    #find login link
    login_link = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Đăng nhập"))
    )
    login_link.click()

    email_box_id = 'txtEmailLogin'
    password_box_id = 'passwordLogin'

    #wait until email and password box appear
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, email_box_id))
    )
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, password_box_id))
    )

    #enter the email and password
    fill_text_box(email_box_id, 'dfghfgh7777@gmail.com')
    fill_text_box(password_box_id, '15102004')

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'btnLoginAccount'))
    )
    login_button.click()
    time.sleep(10)

def find_table(driver, table_by_css):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, table_by_css))
    )
    table = driver.find_element(By.CSS_SELECTOR, table_by_css)
    return table

def find_table_header(table):
    header_contents = []
    headers = table.find_elements(By.TAG_NAME, 'th')
    header_texts = [header.text for header in headers]
    header_contents = header_texts
    print('header collected')
    return header_contents

def find_table_content(table):
    row_contents = []
    table_body = table.find_element(By.TAG_NAME, 'tbody')
    table_rows = table_body.find_elements(By.TAG_NAME, 'tr')
    #loop in table_rows
    for table_row in table_rows:            #voi moi hang trong bang
        table_row_contents = table_row.find_elements(By.TAG_NAME, 'td')             #tim tat ca noi dung cua hang (trong the td)
        table_row_content_texts = [table_row_content_text.text for table_row_content_text in table_row_contents]                #trich xuat noi dung (text cua the td) va luu vao 1 list
        row_contents.append(table_row_content_texts)                #them list chua noi dung vao row_contents
    print('table data collected')
    return row_contents

def move_page():
    next_button = 'btn-next1'
    WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, next_button))
            )               #cho nut chuyen trang co the click
    next_button = driver.find_element(By.NAME, next_button)
    next_button.click()
    time.sleep(5)
    print('went to the next page')

try:
    login(driver)
    table = find_table(driver, table_by_css='#az-container > div.table-responsive.clear-fix.no-m-b > table')
    header_contents = find_table_header(table)
    row_contents = []
    #loop to collect table content
    for page in range(1, 4):
        table = find_table(driver, table_by_css='#az-container > div.table-responsive.clear-fix.no-m-b > table')
        page_row_content = find_table_content(table)
        for row in page_row_content:
            row_contents.append(row)
        #move to the next page
        move_page()

except Exception as e:
    print("error somewhere", e)

print(row_contents)
time.sleep(5)
driver.quit()
