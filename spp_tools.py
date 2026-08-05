import warnings
import gridstatus

from cache_utils import ttl_cache

warnings.filterwarnings("ignore")

_spp = gridstatus.SPP()

_FUELS = ["Coal", "Natural Gas", "Nuclear", "Wind", "Solar",
          "Hydro", "Diesel Fuel Oil", "Waste Heat",
          "Waste Disposal Services", "Other"]


@ttl_cache(seconds=300)
def get_fuel_mix() -> dict:
    """
    SPP current generation fuel mix (5-minute), MW and % by source.
    SPP is wind-heavy, so wind is often the largest source.
    """
    df = _spp.get_fuel_mix("latest")
    latest = df.iloc[-1]

    mix = {f: float(latest[f]) for f in _FUELS
           if f in latest and latest[f] > 0}
    total = sum(mix.values())

    breakdown = sorted(
        ({"fuel": f, "mw": round(mw), "share_pct": round(100 * mw / total, 1)}
         for f, mw in mix.items()),
        key=lambda r: r["mw"], reverse=True,
    )

    return {
        "iso": "SPP",
        "product": "fuel_mix",
        "market": "real_time",
        "timestamp": str(latest["Interval Start"]),
        "total_mw": round(total),
        "breakdown": breakdown,
    }


@ttl_cache(seconds=300)
def get_load() -> dict:
    """SPP current system load (5-minute), in MW."""
    df = _spp.get_load("latest")
    latest = df.iloc[-1]
    return {
        "iso": "SPP",
        "product": "load",
        "market": "real_time",
        "timestamp": str(latest["Interval Start"]),
        "load_mw": round(float(latest["Load"])),
    }


@ttl_cache(seconds=300)
def get_lmp(location: str | None = None, top_n: int = 10) -> dict:
    """
    SPP real-time 5-minute LMP ($/MWh) at hub locations.
    SPP has two main hubs: SPPNORTH_HUB and SPPSOUTH_HUB.

    Args:
        location: optional substring filter (e.g. "NORTH", "SOUTH").
        top_n: max locations to return.
    """
    df = _spp.get_lmp_real_time_5_min_by_location(date="latest", location_type="Hub")

    latest_t = df["Interval Start"].max()
    snap = df[df["Interval Start"] == latest_t]

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
        "iso": "SPP",
        "product": "lmp",
        "market": "real_time_5_min",
        "timestamp": str(latest_t),
        "unit": "$/MWh",
        "filter": location,
        "prices": rows,
    }


if __name__ == "__main__":
    import json
    print("FUEL MIX:")
    print(json.dumps(get_fuel_mix(), indent=2))
    print("\nLOAD:")
    print(json.dumps(get_load(), indent=2))
    print("\nLMP:")
    print(json.dumps(get_lmp(), indent=2))