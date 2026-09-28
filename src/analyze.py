from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
IN = ROOT / "data" / "processed" / "financial_statements.csv"
OUT = ROOT / "data" / "processed" / "financial_metrics.csv"

ALIASES = {
    "revenue": ["매출액", "수익(매출액)", "영업수익"],
    "gross_profit": ["매출총이익"],
    "operating_income": ["영업이익", "영업이익(손실)"],
    "pretax_income": ["법인세비용차감전순이익", "세전이익"],
    "net_income": ["당기순이익", "당기순이익(손실)"],
    "controlling_net_income": ["지배기업의 소유주에게 귀속되는 당기순이익", "지배주주순이익"],
    "assets": ["자산총계"],
    "current_assets": ["유동자산"],
    "cash": ["현금및현금성자산"],
    "receivables": ["매출채권"],
    "inventory": ["재고자산"],
    "ppe": ["유형자산"],
    "liabilities": ["부채총계"],
    "current_liabilities": ["유동부채"],
    "borrowings": ["단기차입금", "장기차입금", "유동성장기차입금"],
    "equity": ["자본총계"],
    "cfo": ["영업활동으로 인한 현금흐름", "영업활동현금흐름"],
    "cfi": ["투자활동으로 인한 현금흐름", "투자활동현금흐름"],
    "cff": ["재무활동으로 인한 현금흐름", "재무활동현금흐름"],
    "capex": ["유형자산의 취득", "유형자산 취득", "유형자산의 취득액"],
    "interest_expense": ["이자비용"],
    "depreciation": ["감가상각비"],
}


def num(s):
    if pd.isna(s): return np.nan
    s = str(s).replace(",", "").strip()
    if s in {"", "-", "nan", "None"}: return np.nan
    try: return float(s)
    except ValueError: return np.nan


def pick(g, aliases):
    for name in aliases:
        x = g[g["account_nm"].astype(str).str.strip() == name]
        if not x.empty:
            return x.iloc[0]["thstrm_amount_num"]
    return np.nan


def build():
    df = pd.read_csv(IN, dtype=str)
    df["thstrm_amount_num"] = df.get("thstrm_amount", pd.Series(index=df.index)).map(num)
    out=[]
    for (year, period), g in df.groupby(["bsns_year","period"], dropna=False):
        row={"year":int(year),"period":period}
        for metric, aliases in ALIASES.items():
            if metric == "borrowings":
                vals=[pick(g,[a]) for a in aliases]
                row[metric]=np.nansum(vals) if any(pd.notna(v) for v in vals) else np.nan
            else:
                row[metric]=pick(g, aliases)
        row["gross_margin"] = row["gross_profit"]/row["revenue"] if row["revenue"] else np.nan
        row["operating_margin"] = row["operating_income"]/row["revenue"] if row["revenue"] else np.nan
        row["net_margin"] = row["net_income"]/row["revenue"] if row["revenue"] else np.nan
        row["current_ratio"] = row["current_assets"]/row["current_liabilities"] if row["current_liabilities"] else np.nan
        row["debt_ratio"] = row["liabilities"]/row["equity"] if row["equity"] else np.nan
        row["equity_ratio"] = row["equity"]/row["assets"] if row["assets"] else np.nan
        row["net_debt"] = row["borrowings"]-row["cash"] if pd.notna(row["borrowings"]) and pd.notna(row["cash"]) else np.nan
        row["fcf"] = row["cfo"]-abs(row["capex"]) if pd.notna(row["cfo"]) and pd.notna(row["capex"]) else np.nan
        row["interest_coverage"] = row["operating_income"]/abs(row["interest_expense"]) if pd.notna(row["operating_income"]) and pd.notna(row["interest_expense"]) and row["interest_expense"] != 0 else np.nan
        out.append(row)
    result=pd.DataFrame(out).sort_values(["year","period"])
    result.to_csv(OUT,index=False,encoding="utf-8-sig")

if __name__ == "__main__":
    build()
