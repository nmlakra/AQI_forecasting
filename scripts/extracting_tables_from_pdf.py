import camelot
import pandas as pd
from glob import glob
from os import path, makedirs

pdf_file_dir = path.join("data/raw/CPCP_AQI_PDFs/")
output_file_dir = path.join("data/raw/CPCP_AQI_tables/")

makedirs(output_file_dir, exist_ok=True)

pdf_files = glob(pdf_file_dir + "*.pdf")

for pdf_filepath in pdf_files:
    tables = camelot.read_pdf(pdf_filepath, pages="all")

    data_tables = []
    for index, table in enumerate(tables):
        n_rows, n_cols = table.shape
        if n_cols == 6:
            data_tables.append(table.df[1:])

    cleaned_table = pd.concat(data_tables)
    cleaned_table.columns = [
        "S.No",
        "City",
        "Air Quality",
        "Index Value",
        "Prominent Pollutant",
        "Based on Number of Monitoring Stations",
    ]

    output_filename = path.basename(pdf_filepath).removesuffix(".pdf") + ".csv"
    output_filepath = path.join(output_file_dir, output_filename)

    cleaned_table.to_csv(output_filepath)