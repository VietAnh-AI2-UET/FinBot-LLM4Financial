from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

#setup for chromeDriver
def set_up_chromeDriver():
    options = Options()

    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-features=WebRtcHideLocalIpsWithMdns")
    #options.add_argument("--headless")
    options.add_experimental_option("prefs", {
        "safebrowsing.enabled": True,
        "profile.default_content_settings.popups": 0,
        "plugins.always_open_pdf_externally": True
    })
    return options

def fill_text_box(id, content):
    text_box = driver.find_element(By.ID, id)
    text_box.clear()
    text_box.send_keys(content)
    time.sleep(1)

def login(driver):
    #find login link
    login_link = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Đăng nhập"))
    )
    login_link.click()
    time.sleep(1)

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
    fill_text_box(id=email_box_id, content='dfghfgh7777@gmail.com')
    fill_text_box(id=password_box_id, content='15102004')

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'btnLoginAccount'))
    )
    login_button.click()
    time.sleep(5)

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
            )               #wait until next page button is ready to be click
    next_button = driver.find_element(By.NAME, next_button)
    next_button.click()
    time.sleep(5)
    print('went to the next page')


try:
    options = set_up_chromeDriver()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://finance.vietstock.vn/doanh-nghiep-a-z?page=1')

except Exception as e:
    print('cant access website')

try:
    login(driver)
    table = find_table(driver, table_by_css='#az-container > div.table-responsive.clear-fix.no-m-b > table')
    header_contents = find_table_header(table)
    row_contents = []
    #loop to collect table content (change the number of page)
    for page in range(1, 196):
        table = find_table(driver, table_by_css='#az-container > div.table-responsive.clear-fix.no-m-b > table')
        page_row_content = find_table_content(table)
        for row in page_row_content:
            row_contents.append(row)
        #move to the next page
        move_page()

except Exception as e:
    print("error somewhere while trying to collecting data", e)

time.sleep(5)
driver.quit()

#todo: extract result into csv
with open('vietstock_enterprises.csv', mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    # Ghi nội dung bảng
    for row in row_contents:
        writer.writerow(row)

print("data stored at vietstock_enterprises.csv")
