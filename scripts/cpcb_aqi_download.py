import requests
import datetime
from pathlib import Path
from time import sleep

BASE_URL = "https://cpcb.nic.in/upload/Downloads/"
BASE_OUTPUT_PATH = Path("data/raw/CPCP_AQI_PDFs")
START_DATE = datetime.date(2021, 1, 1)
END_DATE = datetime.date(2024, 12, 1)


def range_date(start_date, end_date, day_step=1):
    c_date = start_date
    while c_date < end_date:
        yield c_date
        c_date += datetime.timedelta(day_step)


def write_to_pdf(response, pdf_filename, chunk_size=8192):
    outfile_path = BASE_OUTPUT_PATH.joinpath(pdf_filename)
    with open(outfile_path, "wb") as outfile:
        for chunk in response.iter_content(chunk_size):
            if chunk:
                outfile.write(chunk)


## FILE NAME -- AQI_Bulletin_<yyyymmdd>.pdf
def main():

    BASE_OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    for c_date in range_date(START_DATE, END_DATE):
        download_pdf_name = f'AQI_Bulletin_{c_date.strftime("%Y%m%d")}.pdf'
        try:
            url = BASE_URL + download_pdf_name
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an exception for HTTP errors
            write_to_pdf(response, download_pdf_name)

            print(f"PDF downloaded successfully and saved as {download_pdf_name}")
            sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"Failed to download the {download_pdf_name}: {e}")


if __name__ == "__main__":
    main()
