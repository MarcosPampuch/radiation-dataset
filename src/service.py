import pandas as pd
import requests
import zipfile
from io import StringIO, BytesIO

project_path = '<SET PROJECT PATH>'
years = list(range(2006, 2023))  # Range of years to download from INMET website
city = 'Curitiba'
df_year_list = []

retention_columns_map = {
    0: 'DATA',
    1: 'HORA',
    2: 'PRECIPITACAO_TOTAL',
    3: 'PRESSAO_ATMOSFERICA_NA_ESTACAO',
    6: 'IRRADICAO_GLOBAL',
    7: 'TEMPERATURA_AR',
    8: 'TEMPERATURA_ORVALHO',
    9: 'TEMPERATURA_MAX',
    10: 'TEMPERATURA_MIN',
    15: 'UMIDADE_AR',
    16: 'DIRECAO_VENTO',
    17: 'RAJADA_MAX_VENTO',
    18: 'VELOCIDADE_VENTO'
}

column_indexes = list(retention_columns_map.keys())
column_names = list(retention_columns_map.values())


for year in years:
    print(f'year: {year}')
    response = requests.get(f'https://portal.inmet.gov.br/uploads/dadoshistoricos/{year}.zip')

    files = zipfile.ZipFile(BytesIO(response.content))
# READ AND CONCAT ALL YEARS IN ONE FILE
    for file_name in files.infolist():
        if str(file_name).find(f'{city.upper()}_') != -1:
            data_list = files.read(file_name.filename).decode('LATIN-1').splitlines()[8:]
            df = pd.read_csv(StringIO('\n'.join(data_list)), delimiter=';')
            ##### RENAME COLUMNS
            df = df.iloc[:, column_indexes]
            df.columns = column_names
            df_year_list.append(df)

unified_df = pd.concat(df_year_list)
unified_df.to_csv(f'{project_path}data/raw/data.csv', index=False, sep=';')