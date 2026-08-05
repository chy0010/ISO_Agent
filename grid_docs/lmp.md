# Locational Marginal Price (LMP)

Locational Marginal Price (LMP) is the price of electricity at a specific
location on the grid at a specific time. It represents the marginal cost of
serving the next increment of demand (one more MWh) at that location, given
the current supply offers, demand, and physical limits of the transmission
system. MISO, SPP, PJM, ERCOT, NYISO, ISO-NE, and CAISO all price wholesale
energy using LMP.

## The three components of LMP

An LMP at any location decomposes into three parts:

1. **Energy component** (system marginal energy cost): the base cost of energy,
   the same across the whole system. It reflects the offer price of the
   marginal generator that would supply the next MWh if the grid had no
   physical limits.

2. **Congestion component**: the extra cost (or credit) caused by transmission
   constraints. When a transmission line hits its limit, cheaper generation
   "upstream" of the constraint cannot reach demand "downstream" of it, so more
   expensive local generation must run instead. Congestion is what makes prices
   differ from one location to another. A positive congestion component means
   that location is constrained and prices are higher there; a negative
   component means the opposite.

3. **Loss component**: the cost of electrical losses — energy dissipated as heat
   as power flows across the network — relative to a reference point. Delivering
   power to a distant location incurs more losses, raising its price.

LMP = Energy + Congestion + Loss.

## Why LMPs differ across locations

If the transmission grid had unlimited capacity and no losses, every location
would have the same price (just the energy component). In reality, lines have
limits and power flow has losses, so prices separate by location. When you see
a high LMP in one zone and a low LMP in a neighboring zone, the difference is
almost always congestion: a transmission constraint is preventing cheaper power
from reaching the higher-priced location.
