from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os
import time
import pandas as pd

#setup for chromeDriver
def set_up_chromeDriver():
    options = Options()

    #set download path to be the "data" folder
    download_dir = os.path.abspath("data")

    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-features=WebRtcHideLocalIpsWithMdns")
    #options.add_argument("--headless")
    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "profile.default_content_settings.popups": 0,
        "plugins.always_open_pdf_externally": True
    })
    return options

#get company stock code for each member
def get_company_stock_code(member):
    #read the enterprises'information table csv file
    df = pd.read_csv("vietstock_enterprises.csv", header=None)

    #extract the company stock code and add them into a list
    stock_code = df[1].dropna().astype(str).str.strip().unique().tolist()

    split_size = len(stock_code) // 3 # = 1300

    stock_code_bach = stock_code[:split_size]                 
    stock_code_ducanh = stock_code[split_size:2*split_size]     
    stock_code_vietanh= stock_code[2*split_size:]

    member = member.strip().lower()
    if member == 'bach':
        return stock_code_bach
    if member == 'ducanh':
        return stock_code_ducanh
    if member == 'vietanh':
        return stock_code_vietanh

def click_element(css_slector):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css_slector))
    )
    time.sleep(1)  # Đợi ngắn để đảm bảo phần tử hiển thị
    element.click()
    time.sleep(1)

def login(driver):
    #find login link
    login_link = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Đăng nhập"))
    )
    login_link.click()

    #enter the email and password
    fill_in_element(css_selector='#txtEmailLogin', text='dfghfgh7777@gmail.com')
    fill_in_element(css_selector='#passwordLogin', text='15102004')

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'btnLoginAccount'))
    )
    login_button.click()
    time.sleep(10)

#fill text in the box
def fill_in_element(css_selector, text):
    element_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,css_selector))
        # Thay CSS_SELECTOR_CUA_PHAN_TU bằng selector của phần tử bạn muốn đợi
    )
    element_input.clear() 
    element_input.send_keys(text)
    time.sleep(1)

def crawl_report(stock_codes):
    for stock_code in stock_codes:
        fill_in_element(css_selector='#txt-search-code', text=stock_code)
        click_element(css_slector='#finance-statement-left > div.text-right.div-statement-button > button')
        click_element(css_slector='#btn-exportExcel')
        click_element(css_slector='#finance-statement-excel-export > div > div > div > div.modal-footer > button')
        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Không có nội dung để xuất')]"))
            )
            print(f"{stock_code} -> Không có nội dung để xuất, bỏ qua")
            try:
                driver.find_element(By.CSS_SELECTOR, "#x > a").click()
            except:
                pass
            continue
        except TimeoutException:
            print(f"{stock_code} -> Có dữ liệu, tiếp tục tải...")

        time.sleep(2)  # đợi file được tải



#START SECTION
#searching for the website
try:
    options = set_up_chromeDriver()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://finance.vietstock.vn/truy-xuat-du-lieu/bao-cao-tai-chinh.htm')
    time.sleep(3)
    print('website first accession successful')

except:
    print('something wrong while trying to access the website before logging in')

#loging in
try:
    login(driver)
    time.sleep(5)
    print('login successfull')
except:
    print('cant login')

#access the website again (this redirect you to a different website after loged in)
try:
    options = set_up_chromeDriver()
    driver.get('https://finance.vietstock.vn/truy-xuat-du-lieu/bao-cao-tai-chinh.htm')
    time.sleep(3)
    print('website second accession successful')

except:
    print('something wrong while trying to access the website after logged in')

#start collecting enterprises'stocks information
try:
    click_element('#request-upgrade-account-popup > div > div > div > div.modal-body > button')
    click_element('#one-term')

    my_stock_codes = get_company_stock_code(member='vietanh')
    crawl_report(my_stock_codes)
    
except:
    print("Không tìm thấy phần tử hoặc hết thời gian chờ")

# Lấy toàn bộ HTML sau khi nội dung đã tải
html = driver.page_source

time.sleep(25)
driver.quit()

