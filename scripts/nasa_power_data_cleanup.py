import json
import pandas as pd
import os
from glob import glob


def main():
    output_dir = "data/processed/"
    os.makedirs(output_dir, exist_ok=True)

    nasa_power_data_files = glob("data/raw/nasa_power_data/*.json")
    main_df = pd.DataFrame()
    for raw_file in nasa_power_data_files:
        with open(raw_file, "r") as infile:
            data = json.load(infile)

        current_df = pd.DataFrame(data["properties"]["parameter"])

        if main_df.empty:
            main_df = current_df
        else:
            main_df = main_df.merge(
                current_df, how="outer", left_index=True, right_index=True
            )

    main_df["date"] = main_df.index
    main_df["date"] = main_df["date"].apply(pd.to_datetime)

    output_filepath = os.path.join(output_dir, "delhi_nasa_power_climate_data.csv")
    main_df.to_csv(output_filepath)


if __name__ == "__main__":
    main()
