"""
MISO data tools for the grid agent (API's)
"""

import warnings
import gridstatus

from cache_utils import ttl_cache

warnings.filterwarnings("ignore")

_miso = gridstatus.MISO()


@ttl_cache(seconds=300)
def get_fuel_mix():
    """
    Current MISO generation fuel mix (how much power each source is producing).

    Returns a dict with the latest interval's MW by fuel, plus each fuel's
    share of the total, sorted largest first.
    """
    df = _miso.get_fuel_mix("latest")
    latest = df.iloc[-1]

    fuels = [
        "Coal", "Natural Gas", "Nuclear", "Wind", "Solar",
        "Imports", "Battery Storage", "Other",
    ]
    mix = {f: float(latest[f]) for f in fuels if f in latest and latest[f] != 0}
    total = sum(mix.values())

    breakdown = sorted(
        (
            {"fuel": f, "mw": mw, "share_pct": round(100 * mw / total, 1)}
            for f, mw in mix.items()
        ),
        key=lambda r: r["mw"],
        reverse=True,
    )

    return {
        "iso": "MISO",
        "product": "fuel_mix",
        "market": "real_time",
        "timestamp": str(latest["Interval Start"]),
        "total_mw": round(total),
        "breakdown": breakdown,
    }


@ttl_cache(seconds=300)
def get_load():
    """
    Current MISO system load (total electricity demand across the footprint), in MW.
    """
    df = _miso.get_load("latest")
    latest = df.iloc[-1]
    return {
        "iso": "MISO",
        "product": "load",
        "market": "real_time",
        "timestamp": str(latest["Interval Start"]),
        "load_mw": round(float(latest["Load"])),
    }


@ttl_cache(seconds=300)
def get_lmp(location=None, top_n=10):
    """
    MISO real-time locational marginal prices (LMP, $/MWh) by location.
    location: optional substring filter, e.g. "INDIANA".
    """
    df = _miso.get_lmp("latest", market="REAL_TIME_5_MIN")

    latest = df["Interval Start"].max()
    snap = df[df["Interval Start"] == latest]

    if location:
        snap = snap[snap["Location"].str.contains(location, case=False, na=False)]

    rows = [
        {
            "location": r["Location"],
            "location_type": r["Location Type"],
            "lmp": round(float(r["LMP"]), 2),
            "congestion": round(float(r["Congestion"]), 2),
        }
        for _, r in snap.head(top_n).iterrows()
    ]

    return {
        "iso": "MISO",
        "product": "lmp",
        "market": "real_time",
        "timestamp": str(latest),
        "unit": "$/MWh",
        "filter": location,
        "prices": rows,
    }


TOOLS = [get_fuel_mix, get_load, get_lmp]


if __name__ == "__main__":
    import json

    print("FUEL MIX:")
    print(json.dumps(get_fuel_mix(), indent=2))
    print("\nLOAD:")
    print(json.dumps(get_load(), indent=2))
    print("\nLMP (Indiana):")
    print(json.dumps(get_lmp(location="INDIANA", top_n=5), indent=2))