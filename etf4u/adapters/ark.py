import csv, urllib.request, logging
from utils import HEADERS

log = logging.getLogger(f"etf4u.{__name__}")

FUNDS = ["arkk", "arkw", "arkq", "arkf", "arkg"]


def get_fund_file(fund):
    funds_filenames = {
        "arkk": "ARK_INNOVATION_ETF_ARKK_HOLDINGS",
        "arkw": "ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS",
        "arkq": "ARK_AUTONOMOUS_TECHNOLOGY_&_ROBOTICS_ETF_ARKQ_HOLDINGS",
        "arkf": "ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS",
        "arkg": "ARK_GENOMIC_REVOLUTION_MULTISECTOR_ETF_ARKG_HOLDINGS",
    }
    return (
        "https://ark-funds.com/wp-content/fundsiteliterature/csv/"
        + funds_filenames[fund]
        + ".csv"
    )


def fetch(fund):
    result = {}
    fund_csv_url = get_fund_file(fund)
    req = urllib.request.Request(fund_csv_url, headers=HEADERS)
    res = urllib.request.urlopen(req)
    data = csv.reader([l.decode("utf-8") for l in res.readlines()])
    next(data)
    for holding in data:
        ticker = holding[3]
        weight = holding[7]
        if not ticker or not weight:
            break
        result[ticker] = result.get(ticker, 0) + float(weight)
    return result