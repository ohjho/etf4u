import csv, urllib.request, logging
from utils import HEADERS

log = logging.getLogger(__name__)

FUNDS = ["pbw", "tan", "pbd", "ptf", "psj", "pth", "psi"]


def fetch(fund):
    result = {}
    fund_csv_url = (
        "https://www.invesco.com/us/financial-products/etfs/holdings/main/holdings/0?audienceType=Investor&action=download&ticker="
        + fund.upper()
    )
    req = urllib.request.Request(fund_csv_url, headers=HEADERS)
    res = urllib.request.urlopen(req)
    data = csv.reader([l.decode("utf-8") for l in res.readlines()])
    next(data)
    for holding in data:
        ticker = holding[2].strip()
        weight = holding[5]
        if ticker.startswith("-") or not ticker or not weight:
            break
        result[ticker] = result.get(ticker, 0) + float(weight)
    return result