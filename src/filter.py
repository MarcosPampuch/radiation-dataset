import pandas as pd

project_path = '<SET PROJECT PATH>'
hour_intervals = list(range(10, 22))  # WHICH HOUR INTERVAL SHOULD BE RETAINED
initial_df = pd.read_csv(f'{project_path}data/raw/data.csv', sep=';')


## TRANSFORMING FIELD HORA
initial_df['HORA'] = initial_df['HORA'].apply(lambda x: x[0:2]).astype(int)

## FILTERING HOURS
df = initial_df[initial_df['HORA'].isin(hour_intervals)]

## DROPPING DAYS WITH HUGE IRRADICAO_GLOBAL MISSSING/UNREALISTIC DATA

grouped_date_df = df[(df['IRRADICAO_GLOBAL'] == '-9999') | (df['IRRADICAO_GLOBAL'] == '-9999,0') | df['IRRADICAO_GLOBAL'].isna()].groupby(['DATA']).count()
grouped_date_list = grouped_date_df[grouped_date_df['HORA'] > 1].index ## COLUMN HOUR BECAME A COUNTER HERE
df = df[df['DATA'].isin(grouped_date_list) == False]

## DROPPING COLUMNS TEMPERATURA_ORVALHO AND UMIDADE_AR
df = df.drop(columns=['TEMPERATURA_ORVALHO', 'UMIDADE_AR'])


## REPLACE MISSING/UNREALISTIC VALUES
def value_replacer(row):
    if (row.isnull().values.any()) or (row.astype('string') == '-9999.0').any():
        c_list = list(df.columns)
        del c_list[4]
        for column in c_list:
            if str(row[column]) == '-9999.0' or str(row[column]) == 'nan' or str(row[column]) == '-9999,0':
                bad_row_index = df[(df['DATA'] == row['DATA']) & (df['HORA'] == row['HORA'])].index[0]
                date_df = df[df['DATA'] == row['DATA']][column].dropna()
                df.loc[[bad_row_index], column] = round(date_df[date_df >= -100].mean())
    if (row['IRRADICAO_GLOBAL'] == '-9999') or (str(row['IRRADICAO_GLOBAL']) == 'nan'):
        bad_row_index = df[(df['DATA'] == row['DATA']) & (df['HORA'] == row['HORA'])].index[0]
        df.loc[[bad_row_index], 'IRRADICAO_GLOBAL'] = (df.loc[bad_row_index - 1] if df.loc[bad_row_index]['HORA'] > 10 else df.loc[bad_row_index + 1])['IRRADICAO_GLOBAL']
        df.loc[[bad_row_index], 'HORA'] = row['HORA']


## FORMAT DATA COLUMN
df['DATA'] = pd.to_datetime(df['DATA'].apply(lambda x: x.replace('/', '-')))



## FORMAT PRECIPITACAO_TOTAL COLUMN
df['PRECIPITACAO_TOTAL'] = df['PRECIPITACAO_TOTAL'].apply(lambda x: '0'+str(x).replace(',','.') if str(x)[0] == ',' else str(x).replace(',','.'))
df['PRECIPITACAO_TOTAL'] = df['PRECIPITACAO_TOTAL'].astype('float64')

## FORMAT PRESSAO_ATMOSFERICA_NA_ESTACAO COLUMN
df['PRESSAO_ATMOSFERICA_NA_ESTACAO'] = df['PRESSAO_ATMOSFERICA_NA_ESTACAO'].apply(lambda x: str(x).replace(',','.')).astype('float64')

## FORMAT TEMPERATURA_AR COLUMN
df['TEMPERATURA_AR'] = df['TEMPERATURA_AR'].apply(lambda x: str(x).replace(',','.')).astype('float64')

## FORMAT TEMPERATURA_ORVALHO COLUMN
# df['TEMPERATURA_ORVALHO'] = df['TEMPERATURA_ORVALHO'].apply(lambda x: str(x).replace(',','.')).astype('float64')

## FORMAT TEMPERATURA_MAX COLUMN
df['TEMPERATURA_MAX'] = df['TEMPERATURA_MAX'].apply(lambda x: str(x).replace(',','.')).astype('float64')

## FORMAT TEMPERATURA_MIN COLUMN
df['TEMPERATURA_MIN'] = df['TEMPERATURA_MIN'].apply(lambda x: str(x).replace(',','.')).astype('float64')

## FORMAT DIRECAO_VENTO COLUMN
# df['DIRECAO_VENTO'] = df['DIRECAO_VENTO'].astype('int')

## FORMAT RAJADA_MAX_VENTO COLUMN
df['RAJADA_MAX_VENTO'] = df['RAJADA_MAX_VENTO'].apply(lambda x: str(x).replace(',','.')).astype('float64')

## FORMAT VELOCIDADE_VENTO COLUMN
df['VELOCIDADE_VENTO'] = df['VELOCIDADE_VENTO'].apply(lambda x: float('0'+str(x).replace(',','.')) if str(x)[0] == ',' else str(x).replace(',','.'))
df['VELOCIDADE_VENTO'] = df['VELOCIDADE_VENTO'].astype('float64')


df.apply(value_replacer, axis=1)

## FORMAT DIRECAO_VENTO COLUMN
df['DIRECAO_VENTO'] = df['DIRECAO_VENTO'].astype('int')

## FORMAT IRRADICAO_GLOBAL COLUMN
df['IRRADICAO_GLOBAL'] = df['IRRADICAO_GLOBAL'].apply(lambda x: str(x).replace(',','.')).astype('float64')


## SEND TO CASTED
df.to_csv(f'{project_path}data/casted/data.csv', index=False, sep=';')
