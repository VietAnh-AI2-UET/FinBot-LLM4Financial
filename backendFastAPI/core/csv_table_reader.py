import pandas as pd
import os

def get_input_path() -> str:
    base_dir = os.getcwd()
    input_path = os.path.abspath(os.path.join(base_dir, '..', '..', 'VietstockFinance_Bao-cao-tai-chinh_20250731-201232.xlsx'))
    return input_path

def get_dataframe(input_path=None) -> pd.DataFrame:
    if input_path == None:
        input_path = get_input_path()
    df = pd.read_excel(input_path, skiprows=13, usecols="A:C")
    df.columns = ['Hạng mục', 'Mã số', 'Giá trị']
    df = df.dropna(subset=['Hạng mục', 'Giá trị'], how='all')
    df = df[~df['Hạng mục'].astype(str).str.contains("TRUNG TÂM|Email|Hotline", na=False)]
    return df


