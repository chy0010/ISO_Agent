# Why Electricity Prices Rise and Fall

This explains the actual, physical reasons a locational marginal price (LMP) is
high or low at a given time — the cause-and-effect, not the settlement process.

## The core idea: price follows the most expensive plant running

At any moment, the grid meets demand by running generators from cheapest to most
expensive (economic dispatch). The price is set by the **last, most expensive
generator needed** to meet demand — the "marginal" unit. So the question "why is
the price high?" almost always comes down to: **what is the most expensive plant
currently required to run, and why?**

## Reason 1: High demand

When demand is high — a hot summer afternoon, a cold winter morning — the grid
has to run more generators, including expensive "peaker" plants (usually natural
gas) that only switch on when everything cheaper is already maxed out. The more
demand, the more expensive the marginal plant, the higher the price. This is the
single most common reason prices spike. Prices are usually highest in late
afternoon on hot days and lowest overnight.

## Reason 2: Congestion (transmission limits)

When a transmission line hits its limit, cheap power on one side physically
cannot reach demand on the other side. The constrained side must run more
expensive local generation instead, so its price rises — sometimes sharply —
while the other side may stay cheap or even go negative. A high congestion
component in the LMP is a direct signal that a transmission constraint is binding
near that location. This is why two locations on the same grid can have very
different prices at the same moment.

## Reason 3: Low renewable output

Wind and solar have near-zero fuel cost, so when they produce a lot, they push
expensive plants out of the mix and prices fall. When the wind dies down or the
sun sets, that cheap supply disappears and more expensive gas or coal has to make
up the difference — pushing prices up. This is why prices in wind-heavy grids
(like SPP) can swing a lot with the weather: a calm evening can be far more
expensive than a windy afternoon.

## Reason 4: Fuel prices

The marginal plant is often natural gas, so the price of natural gas feeds
directly into electricity prices. When gas is expensive, the gas plants that set
the price cost more to run, and electricity prices rise across the board — even
if demand and congestion are normal.

## Reason 5: Generator or transmission outages

If a large power plant or a key transmission line is offline (planned maintenance
or unexpected failure), the grid loses cheap capacity or a cheap delivery path.
It must lean on more expensive alternatives, raising prices — sometimes only in
the local area affected by the outage.

## Putting it together: how to read a high price

When one location's price is high, work through the LMP components and these
drivers:

- **High congestion component** → a transmission constraint is binding nearby
  (Reason 2). The price is local; other areas may be cheap.
- **High energy component (high everywhere)** → system-wide pressure: high demand
  (Reason 1), low renewables (Reason 3), or expensive fuel (Reason 4).
- **A sudden spike** → often a generator/transmission outage (Reason 5) or a fast
  drop in wind/solar.

So "why is MISO's price higher than SPP's right now?" usually resolves to one of:
SPP has more cheap wind running, MISO has more congestion, MISO has higher demand
relative to its cheap supply, or an outage is affecting one of them. The LMP's
congestion component tells you immediately whether the cause is local
(transmission) or system-wide (supply and demand).
