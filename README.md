# Solar Radiation Dataset
This is a source repo for storing a radiation dataset used to train neural networks and forecast solar radiation in the city of Curitiba-PR, Brazil.
All metrics came from Curitiba's weather station and were downloaded from the [INMET site](https://portal.inmet.gov.br/dadoshistoricos).
The extract, clean and filter processes were all done automacally using Python with libraries like Pandas and Numpy.

## Dataset Metrics
- DATA [yyyy-mm-dd]
- HORA [UTC]
- PRECIPITACAO_TOTAL [mm]
- PRESSAO_ATMOSFERICA_NA_ESTACAO [hPa]
- IRRADICAO_GLOBAL [kJ/m2]
- TEMPERATURA_AR [°C]
- TEMPERATURA_MAX [°C]
- TEMPERATURA_MIN [°C]
- DIRECAO_VENTO [°]
- VELOCIDADE_VENTO [m/s]

## Dataset Filtering Procedures
- Deleted all data from 22h00 till 9h00 due to the lack of solar irradiation values;
- Deleted days where there were missing/inconsistent data;
- Replaced some missing values of a specific metric for it's daily mean;

## Complements
This project is part of a major project to forecast Curitiba's solar radiation and it was support by UTFPR university.


More information about the project can be found in the Labens website.


