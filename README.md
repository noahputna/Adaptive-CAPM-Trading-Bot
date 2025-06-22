# Adaptive-CAPM-Trading-Bot
This project simulates a **CAPM-based trading bot** that adapts to market conditions using modern portfolio theory. It evaluates potential trades in real-time using **expected payoff penalised by variance**, mimicking the principles of risk-adjusted return optimisation.

Designed within an agent-based market simulation (Flexemarkets), the bot **engages in reactive market-making**, accepting or rejecting trades based on dynamically simulated portfolio performance.

## Features
- **CAPM-Inspired Evaluation:** Executes trades only if they improve expected returns after adjusting for variance.
- **Dynamic Portfolio Simulation:** Simulates post-trade portfolio payoffs to assess optimality.
- **Reactive Market Maker:** Monitors the order book and selectively responds to opportunities.
- **Risk-Aware Logic:** Penalises volatility to prevent overly aggressive posisitions.
