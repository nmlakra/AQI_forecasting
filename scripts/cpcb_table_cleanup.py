import pandas as pd
import os
from glob import glob

def prominent_pollutant_cleanup(pollutants):
    cleaned_names = []
    if pollutants == 'CO':
        cleaned_names.append(pollutants) # Only CO
    else:
        names, values = pollutants.replace('\n,', ',').split('\n', maxsplit=1)
        pollutant_names = names.split(', ')
        values = values.split('\n')
        i = 0
        for pollutan_name in pollutant_names:
            if pollutan_name != 'CO':
                cleaned_names.append(pollutan_name + values[i])
                i += 1
            else:
                cleaned_names.append(pollutan_name)
    
    return cleaned_names

def main():
    files = glob('data/raw/CPCP_AQI_tables/*.csv')
    output_filepath = 'data/processed/'
    os.makedirs(output_filepath, exist_ok=True)

    for file in files:
        current_df = pd.read_csv(file, index_col=0)
        current_df.drop('S.No', axis=1, inplace=True)
        filename = os.path.basename(file)
        date = filename.removeprefix("AQI_Bulletin_").removesuffix(".csv")
        current_df['date'] = date
        current_df['date'] = current_df['date'].apply(pd.to_datetime)
        current_df['Prominent Pollutant'] = current_df['Prominent Pollutant'].apply(prominent_pollutant_cleanup)
        
        output_file = os.path.join(output_filepath, 'cpcb_aqi_data.csv')
        
        if os.path.exists(output_file):
            current_df.to_csv(output_file, mode='a', index=False, header=False)
        
        else:
            current_df.to_csv(output_file, index=False)
         
        
if __name__ == '__main__':
    main()