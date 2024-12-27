import requests
import datetime
import json

START_DATE = datetime.date(2020, 1, 1)
END_DATE = datetime.date(2024, 12, 1)

NEW_DELHI = {"longitude": "28.7", "latitude": "77.1"}

NASA_POWER_API_PARAMS = {
    "solar_fluxes_related": [
        "ALLSKY_SFC_SW_DNI",
        "ALLSKY_SFC_SW_DIFF",
        "TOA_SW_DWN",
        "ALLSKY_SRF_ALB",
        "ALLSKY_SFC_PAR_TOT",
        "CLRSKY_SFC_PAR_TOT",
        "ALLSKY_SFC_UVA",
        "ALLSKY_SFC_UVB",
        "ALLSKY_SFC_UV_INDEX"
    ],
    "temp_thermal_ir_flux": [
        "T2M",
        "T2MDEW",
        "T2MWET",
        "TS",
        "T2M_RANGE",
        "T2M_MAX",
        "T2M_MIN",
        "ALLSKY_SFC_LW_DWN"
    ],
    "climate_humidity_precipitation": [
        "CDD0",
        "CDD10",
        "CDD18_3",
        "HDD0",
        "HDD10",
        "HDD18_3",
        "QV2M",
        "RH2M",
        "PRECTOTCORR"
    ],
    "wind_pressure": [
        "PS",
        "WS10M",
        "WS10M_MAX",
        "WS10M_MIN",
        "WS10M_RANGE",
        "WS50M",
        "WD10M",
        "WS50M_MAX",
        "WS50M_MIN",
        "WS50M_RANGE",
        "WD50M"
    ]
}

def main():
    
    base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "community": "AG",
        "longitude": NEW_DELHI['longitude'],
        "latitude": NEW_DELHI['latitude'],
        "start": START_DATE.strftime("%Y%m%d"),
        "end": END_DATE.strftime("%Y%m%d"),
        "format": "JSON",
    } 

    for nasa_power_api_param_name in NASA_POWER_API_PARAMS:
        nasa_power_api_params = ",".join(NASA_POWER_API_PARAMS[nasa_power_api_param_name])

        url = base_url + f"?parameters={nasa_power_api_params}"
        response = requests.get(url, params)
        if response.status_code != 200:
            raise Exception(f"Status code: {response.status_code}")
        
        with open(f"data/raw/{nasa_power_api_param_name}.json", "w") as outfile:
            json.dump(response.json(), outfile, indent=4)

if __name__ == "__main__":
    main()