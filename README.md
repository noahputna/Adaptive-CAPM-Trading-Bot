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

---

## Setup

Update the folliwng fields in `__main__` before running:

```python
FM_EMAIL = "FM_EMAIL"      
FM_PASSWORD = "FM_PASSWORD"
```
Do **not** hardcode credentials. Use environment variables in production:

```bash
export FM_EMAIL="your-email"
export FM_PASSWORD="your-password"
```
Use ```os.getenv()``` in your Python code to fetch credentials securely:
```python
import os

email = os.getenv("FM_EMAIL")
password = os.getenv("FM_PASSWORD")
```

## Run the Bot
```bash
python CAPM_bot.py
```

---

## Parameters
| Parameter        | Default    | Description                                   |
|------------------|------------|-----------------------------------------------|
| `risk_aversion`  | `0.5` | Higher value = more risk-averse decision making.   |
| `note_discount`  | `2`   | Discount applied when selling notes to raise cash. |
| `cash_threshold` | `10`  | Minimum desired cash buffer.                       |

## Example Strategy
If the expected payoff of **Stock A** is **90** with variance **16**, and the market price is **85**:<br>
Utility = 90 - 0.5 * 16 = 82<br>

Since utility < market price, the bot **will not buy**.
If the price drops below **82**, the bot will place a buy order for 1 unit.
