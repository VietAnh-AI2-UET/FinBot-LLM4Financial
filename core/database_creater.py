from docx_table_reader import get_table_dataframe
from docx_table_reader import get_document
import os
import re

#checking text validation
def gibbrish_detector(text):
    #contain special character or number --> remove
    if re.fullmatch(r"[^\w\sÀ-Ỵà-ỵ]{3,}", text):
        return True
    if len(re.findall(r"[A-Z]{2,}", text)) > 5:
        return True
    if re.search(r"[\^_~@#\$%]", text):
        return True
    return False

def is_valid_text(text):
    if not text.strip():
        return False
    if len(text.strip()) < 5:
        return False
    if gibbrish_detector(text):
        return False
    if re.search(r"[a-zA-ZÀ-Ỵà-ỵ]", text):  # có ký tự chữ
        return True
    return False

#find the header of table
def get_table_header(document, table_index, max_lookback=10):
    paras = document.paragraphs
    table = document.tables[table_index]
    table_element = table._element

    #find table XML position
    body_elements = list(document.element.body.iterchildren())
    table_position = None
    for i, el in enumerate(body_elements):
        if el == table_element:
            table_position = i
            break

    if table_position is not None:
        #tray back to find table header
        count = 0
        for i in range(table_position - 1, -1, -1):
            if count > max_lookback:
                break
            para_candidate = paras[i].text.strip()
            if is_valid_text(para_candidate):
                return para_candidate
            count += 1

    return f"Table {table_index}"
    

#todo: create vector embedding for input file


#read input path
try:
    base_dir = os.path.dirname(__file__)
    path = os.path.abspath(os.path.join(base_dir, '..', '000000014601738_VI_BaoCaoTaiChinh_KiemToan_2024_HopNhat_14032025110908.docx'))
    print('file located')

except Exception as e:
    print('cant locate file')

#read document
try:
    document = get_document(path=path)
    print('document reading successful')

except Exception as e:
    print('cant read document')

#find table header
try:
    table_header = get_table_header(document=document, table_index=3, max_lookback=5)
    print(table_header)

except Exception as e:
    print('cant find table header')