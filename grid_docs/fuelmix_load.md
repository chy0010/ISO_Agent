# Fuel Mix and Load

## Load (demand)

Load is the total amount of electricity being consumed across a grid operator's
footprint at a given moment, measured in megawatts (MW). It rises and falls
predictably: higher on hot summer afternoons (air conditioning) and cold winter
mornings (heating), lower overnight. Operators publish a load forecast alongside
actual load; the gap between them indicates how well demand was predicted.

## Fuel mix (generation by source)

Fuel mix is the breakdown of how much power each type of generation source is
producing right now — natural gas, coal, nuclear, wind, solar, hydro, and
others — in MW and as a share of total generation. It changes constantly with
weather, demand, and prices.

## How fuel mix is dispatched

Generators are dispatched roughly in order of marginal cost (economic dispatch).
Low-marginal-cost resources run first: nuclear and renewables (wind, solar)
have near-zero fuel cost, so they run whenever available. Coal and natural gas
fill the remaining demand, with the most expensive units running only during
peak demand. This is why fuel mix shifts across the day: overnight, low demand
is met mostly by baseload nuclear and cheap generation; during peak afternoon
demand, more expensive gas peaking units come online.

## Why grids differ

Different regions have very different fuel mixes because of their resources and
history. SPP (the central plains) is heavily wind-driven and wind is often its
largest single source. MISO (the midcontinent) relies more on natural gas and
coal, with significant nuclear. PJM (mid-Atlantic) has a large nuclear share.
These structural differences mean the same question — "what's powering the
grid?" — has very different answers by region.

## Solar and time of day

Solar generation is zero at night and peaks at midday. Any nighttime snapshot
of fuel mix will show essentially no solar, which is expected, not an error.
Interpreting a fuel mix always requires knowing the time of day.

## Negative values: battery storage

Battery storage can appear as a negative value in a fuel mix. When batteries
are charging, they consume power from the grid rather than generating it, so
their net contribution is negative. When discharging, it is positive. A small
negative storage figure means batteries are charging at that moment.
