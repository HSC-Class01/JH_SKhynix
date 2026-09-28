import io, os, zipfile
from pathlib import Path
import requests
import xml.etree.ElementTree as ET

BASE_URL = "https://opendart.fss.or.kr/api"
CORP_CODE = "00164779"  # SK hynix
REPORT_CODES = {"annual":"11011", "half-year":"11012", "q1":"11013", "q3":"11014"}


def api_get(path, params, timeout=60):
    key = os.environ.get("OPENDART_API_KEY")
    if not key:
        raise RuntimeError("OPENDART_API_KEY environment variable is missing")
    p = dict(params)
    p["crtfc_key"] = key
    r = requests.get(f"{BASE_URL}/{path}", params=p, timeout=timeout)
    r.raise_for_status()
    return r


def get_corp_code():
    r = api_get("corpCode.xml", {})
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        xml_name = next(n for n in z.namelist() if n.lower().endswith(".xml"))
        root = ET.fromstring(z.read(xml_name))
    for item in root.findall("list"):
        name = item.findtext("corp_name", "")
        stock = item.findtext("stock_code", "")
        if name in {"SK하이닉스", "에스케이하이닉스(주)"} or stock == "000660":
            return item.findtext("corp_code")
    raise RuntimeError("SK hynix corp_code not found in corpCode.xml")


def financial_statement(year, report_code, fs_div="CFS"):
    r = api_get("fnlttSinglAcntAll.json", {
        "corp_code": CORP_CODE,
        "bsns_year": str(year),
        "reprt_code": report_code,
        "fs_div": fs_div,
    })
    data = r.json()
    if data.get("status") != "000":
        return data
    return data
