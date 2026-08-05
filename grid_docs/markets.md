# Day-Ahead and Real-Time Markets

US grid operators run a two-settlement market: a day-ahead market and a
real-time market. Both produce Locational Marginal Prices (LMPs), but they
answer different questions.

## Day-ahead market

The day-ahead market clears the day before the operating day. Market
participants submit offers to sell and bids to buy energy for each hour of the
next day. The operator runs a security-constrained optimization that commits
generation and sets an hourly LMP for every location, based on expected demand
and the physical limits of the grid. Day-ahead prices are financially binding:
they let generators and buyers lock in prices in advance and hedge risk. Most
energy is scheduled in the day-ahead market.

## Real-time market

The real-time market operates during the actual operating day, typically
clearing every 5 minutes. It balances the small differences between what was
scheduled day-ahead and what is actually happening — unexpected demand,
generator outages, weather-driven swings in wind and solar. Real-time LMPs can
be more volatile than day-ahead prices because they respond to live conditions.

## Why the two differ

Day-ahead prices reflect expectations; real-time prices reflect reality. If
actual demand is higher than forecast, or a generator trips offline, real-time
prices can spike above the day-ahead price for that hour. Persistent gaps
between day-ahead and real-time prices are a signal that forecasts were off or
that grid conditions changed.
