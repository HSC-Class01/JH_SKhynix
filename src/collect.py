import json, time
from pathlib import Path
import pandas as pd
from dart_client import financial_statement, REPORT_CODES, CORP_CODE

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
RAW.mkdir(parents=True, exist_ok=True)
PROC.mkdir(parents=True, exist_ok=True)

START_YEAR = 2010
END_YEAR = 2026


def collect():
    rows = []
    status = []
    # OpenDART financial APIs provide structured financial statement data from 2015 onward.
    for year in range(max(2015, START_YEAR), END_YEAR + 1):
        for period, code in REPORT_CODES.items():
            payload = financial_statement(year, code, "CFS")
            path = RAW / f"{year}_{period}_CFS.json"
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            if payload.get("status") == "000":
                for x in payload.get("list", []):
                    x["bsns_year"] = year
                    x["period"] = period
                    x["fs_div"] = "CFS"
                    rows.append(x)
                status.append({"year":year,"period":period,"status":"ok","count":len(payload.get("list",[]))})
            else:
                status.append({"year":year,"period":period,"status":payload.get("status"),"message":payload.get("message")})
            time.sleep(0.15)
    df = pd.DataFrame(rows)
    if not df.empty:
        df.to_csv(PROC / "financial_statements.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(status).to_csv(PROC / "collection_status.csv", index=False, encoding="utf-8-sig")
    manifest = {
        "corp_code": CORP_CODE,
        "start_year_requested": START_YEAR,
        "structured_financial_data_start_year": 2015,
        "end_year": END_YEAR,
        "note": "2010-2014 are outside the OpenDART structured financial-statement API coverage; no fabricated values are inserted.",
    }
    (PROC / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__":
    collect()
