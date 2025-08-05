from docx import Document
import pandas as pd

def get_document(path) -> Document:
    document = Document(path)
    return document

#return the informations list of indicated table
def extract_table_info(tables, table_index) -> list:
    table_infos = []
    table = tables[table_index]
    for row in table.rows:
        row_contents = [cell.text for cell in row.cells]
        table_infos.append(row_contents)
    return table_infos

def get_table_dataframe(path, table_index):
    try:
        path = path                #change the "path" according to yours
        document = get_document(path=path)
        print('file located')

    except Exception as e:
        print('cant locate file')

    #extract all tables in the file -> list
    try:
        tables = document.tables                #tables: A list of all tables in the file
        print('read table successful')

    except Exception as e:
        print('cant extract table from file')

    #todo: extract certain table by table_index
    try:
        if table_index < 0 or table_index >= len(tables):
            print('Invalid table_index')
            return None
        else:
            table_infos = extract_table_info(tables=tables, table_index=table_index)
            df = pd.DataFrame(table_infos)
            return df

    except Exception as e:
        print('error extracting single table or converting into DataFrame')