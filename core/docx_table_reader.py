from docx import Document
import pandas as pd

def read_docx_file(path) -> Document:
    document = Document(path)
    return document

#return the informations list of indicated table
def extract_table_info(tables, index) -> list:
    table_infos = []
    table = tables[index]
    for row in table.rows:
        row_contents = [cell.text for cell in row.cells]
        table_infos.append(row_contents)
    return table_infos

def get_table_dataframe(path, index):
    try:
        path = path                #change the "path" according to yours
        document = read_docx_file(path=path)
        print('file located')

    except Exception as e:
        print('cant locate file')

    #extract all tables in the file -> list
    try:
        tables = document.tables                #tables: A list of all tables in the file
        print('read table successful')

    except Exception as e:
        print('cant extract table from file')

    #todo: extract certain table by index
    try:
        if index < 0 or index >= len(tables):
            print('Invalid index')
        else:
            table_infos = extract_table_info(tables=tables, index=index)
            df = pd.DataFrame(table_infos)
            return df

    except Exception as e:
        print('error extracting single table or converting into DataFrame')