import warnings
from datetime import datetime, timedelta
from dotenv import load_dotenv

import pandas as pd
import gridstatus

from cache_utils import ttl_cache

load_dotenv()
warnings.filterwarnings("ignore")

_eia = gridstatus.EIA()

ISO_CODES = {
    "MISO": "MISO",
    "PJM": "PJM",
    "SPP": "SWPP",
    "CAISO": "CISO",
    "ERCOT": "ERCO",
    "NYISO": "NYIS",
    "ISONE": "ISNE",
}

_FUELS = ["Coal", "Natural Gas", "Nuclear", "Wind", "Solar",
          "Hydro", "Petroleum", "Battery Storage", "Other"]


def _recent_window():
    start = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    end = datetime.now().strftime("%Y-%m-%d")
    return start, end


@ttl_cache(seconds=1000)
def get_fuel_mix(iso: str) -> dict:
    iso = iso.upper()
    if iso not in ISO_CODES:
        return {"error": f"iso must be one of {sorted(ISO_CODES)}"}

    code = ISO_CODES[iso]                      # translate to EIA's code

    start, end = _recent_window()
    df = _eia.get_dataset(
        "electricity/rto/fuel-type-data", start=start, end=end, frequency="hourly"
    )
    df = df[df["Respondent"] == code].sort_values("Interval Start")   # filter by code

    if df.empty:                               # guard against no data
        return {"iso": iso, "product": "fuel_mix", "source": "EIA",
                "error": "no recent data available"}

    latest = df.iloc[-1]

    mix = {f: float(latest[f]) for f in _FUELS
           if f in latest and pd.notna(latest[f]) and latest[f] != 0}
    total = sum(mix.values())

    breakdown = sorted(
        ({"fuel": f, "mw": round(mw), "share_pct": round(100 * mw / total, 1)}
         for f, mw in mix.items()),
        key=lambda r: r["mw"], reverse=True,
    )

    return {
        "iso": iso, "product": "fuel_mix", "source": "EIA",
        "timestamp": str(latest["Interval Start"]),
        "total_mw": round(total), "breakdown": breakdown,
    }



@ttl_cache(seconds=1000)
def get_load(iso: str) -> dict:
    iso = iso.upper()
    if iso not in ISO_CODES:
        return {"error": f"iso must be one of {sorted(ISO_CODES)}"}

    code = ISO_CODES[iso]                       # translate

    start, end = _recent_window()
    df = _eia.get_dataset(
        "electricity/rto/region-data", start=start, end=end, frequency="hourly"
    )
    df = df[df["Respondent"] == code].sort_values("Interval Start")   # filter by code
    df = df[df["Load"].notna()]

    if df.empty:                                # guard
        return {"iso": iso, "product": "load", "source": "EIA",
                "error": "no recent data available"}

    latest = df.iloc[-1]

    return {
        "iso": iso, "product": "load", "source": "EIA",
        "timestamp": str(latest["Interval Start"]),
        "load_mw": round(float(latest["Load"])),
        "load_forecast_mw": (
            round(float(latest["Load Forecast"]))
            if pd.notna(latest["Load Forecast"]) else None
        ),
    }


if __name__ == "__main__":
    import json
    for iso in ["MISO", "PJM"]:
        print(f"\n=== {iso} FUEL MIX ===")
        print(json.dumps(get_fuel_mix(iso), indent=2))
        print(f"\n=== {iso} LOAD ===")
        print(json.dumps(get_load(iso), indent=2))