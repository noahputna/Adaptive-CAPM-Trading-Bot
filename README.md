# CAPMBot - Adapative CAPM-Based Trading Agent
CAPMBot is a fully autonomous trading agent built for Flexemarkets (a simulated marketplace). It uses a Capital Asset Pricing Model (CAPM) inspired utility function to assess risk-adjusted asset returns and execute strategic trades.

Designed within an agent-based market simulation (Flexemarkets), CAPMBot manages portfolio risk, liquidity, and asset selection - making it suitable for research, education, and competitive trading scenarios.

---

## Features
- **CAPM Utility Strategy**: Calculates expected returns and risk (variance) to select optimal trades using:<br>
Utility = E[Payoff] - λ × Variance<br>
- **Fully Autonomous**: Handles market orders dynamically based on real-time conditions.
- **Liquidity Management**: Sells "Note" assets at a discount to raise cash when needed.
- **Custom Risk Aversion**: Easily tune risk preference using a `risk_aversion` parameter.
- **Safe Order Handling**: Includes error handling for order rejections and logs all key events.

---

## How It Works
1. **Market Initalisation**
  - Reads payoff distributions and market ID's.
2. **Real-Time Trading**
  - Monitors market orders and selects the most profitable opportunity.
3. **Cash Management**
  - Automatically liquidates notes to prevent being cash-constrained.
4. **Performance Objective**
  - Maximises risk-adjusted returns using a CAPM utility function.

---

## File Overview
|File           | Description                                            |
|---------------|--------------------------------------------------------|
| `CAPM_Bot.py` | Main Trading bot implementing all logic and utilities. |


---

## Getting Started
### Pre-requisities
- `fmclient` (Financial Market Simulator SDK)
- `numpy`

Install dependencies:
```bash
pip install numpy
```
