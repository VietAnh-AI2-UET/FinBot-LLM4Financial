from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import time

#kiem tra cai dat chromeDriver va tao driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

#ham cuon trang
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Đợi nội dung tải
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:  # Nếu không có nội dung mới, thoát
            break
        last_height = new_height

try:
    driver.get('https://finance.vietstock.vn/doanh-nghiep-a-z?page=1')              #truy cap web
    scroll_to_bottom(driver)                #cuon den cuoi trang cho xuat hien het html
    table_by_css = '#az-container > div.table-responsive.clear-fix.no-m-b > table'             #table chua thong tin
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, table_by_css))
    )               #cho den khi table_by_css xuat hien
    table = driver.find_element(By.CSS_SELECTOR, table_by_css)              #tim table_by_css
    print('element found')              #neu tim thay bang thi thong bao
    table_header_contents = table.find_elements(By.TAG_NAME, 'th')                #tim tieu de cua bang
    table_header_content_texts = [table_header_content_text.text for table_header_content_text in table_header_contents]                #trich xuat noi dung tieu de cua bang
    print(table_header_content_texts)

    table_body = table.find_element(By.TAG_NAME, 'tbody')
    table_rows = table_body.find_elements(By.TAG_NAME, 'tr')
    #loop in table_rows
    row_contents = []               #list chua noi dung cua cac hang (Type: List[List])
    for table_row in table_rows:            #voi moi hang trong bang
        table_row_contents = table_row.find_elements(By.TAG_NAME, 'td')             #tim tat ca noi dung cua hang (trong the td)
        table_row_content_texts = [table_row_content_text.text for table_row_content_text in table_row_contents]                #trich xuat noi dung (text cua the td) va luu vao 1 list
        row_contents.append(table_row_content_texts)                #them list chua noi dung vao row_contents
    print(row_contents[3])

except:
    print('Something is bitching')
    
finally:
    driver.quit()               #thoat trinh duyet