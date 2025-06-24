"""
CAPMBot: Adaptive CAPM-Based Trading Agent for Trading Simulation.

Description: This bot participates in a simulated marketplace using the Capital Asset Pricing Model (CAPM).
It evaluates the expected payoff and risk (variance) of each security and optimises trades using a 
mean-variance utility function. Includes features for risk aversion tuning, dynamic order handing,
and intelligen portfolio management.

This bot simulates a CAPM-based strategy in a trading evironment.
It dynamically assess whether to accept orders based on expected payoff penalised by variance.
It supports both proactive and reactive trading modes.

Author: Noah Putna.
"""

# -- Import Statements -- 

from typing import Dict, List
from fmclient import Agent, Session, Order, OrderSide, OrderType, Holding
import numpy as np 

# -- CAPMBot Class Definition

class CAPMBot(Agent):
    """A trading agent that implements a CAPM-based utility function to decide trades."""

    def __init__(self, account, email, password, marketplace_id, risk_aversion = 0.5):
        """Initialise the CAPMBot with account credentials and trading settings."""

        # Initialise bot and commence trading.
        super().__init__(account, email, password, marketplace_id, name="CAPM Bot")

        # Risk aversion parameter used in utility equation.
        self.risk_aversion = risk_aversion

        # Stores expected payoff distributions and market references.
        self._payoffs: Dict[str, List[int]] = {}
        self._market_ids: Dict[str, object] = {}

        # Current holdings (cash and assets).
        self.holdings: Holding = None

        # Parameters for liquidity management.
        self.cash_threshold = 10
        self.note_discount = 2
    
    def initialised(self):
        """Called when the bot is connected and initialised. Assigns market referenes and descriptions."""

        try:
            # Extract payoff distributions and associate market ID's with asset names.
            for market_id, market in self.markets.items():
                item = market.item
                self._payoffs[item] = [int(x) for x in market.description.split(",")]

                # Store a reference to the market object keyed by asset name.
                self._market_ids[item] = market
            
            # Log confirmation of successful initialisation.
            self.inform("Bot initialised.")

        except Exception as e:
            #Catch and log unexpected initialisation errors.
            self.error(f"Error during initialisation: {e}")
    
    def received_holdings(self, holdings: Holding):
        """Store and log current cash and asset holdings."""

        # Store the latest holdings and information from the server.
        self.holdings = holdings

        # Log the available cash to console.
        self.inform(f"Cash available: {holdings.cash_available}")
    
    def received_session_info(self, session: Session):
        """Respond to session status updates (open or closed)."""

        # Check if the trading session has started or ended, and log accordingly.
        if session.is_open:
            self.inform("Session opened.")
        else:
            self.inform("Session closed.")

    def order_accepted(self, order: Order):
        """Handle successful order submission and log it."""

        # Log the details of the order that was successfully accepted by the market.
        self.inform(f"Order accepted: {order.order_side} {order.units} @ {order.price}")

    def order_rejected(self, info, order: Order):
        """Handle rejected orders with recovery strategy."""

        # Log the rejection reason for debugging purposes.
        self.error(f"Order rejected: {info}")

        # Attempt to raise cash by selling notes - if order was rejected due to lack of cash.
        if 'ORDER_INSUFFICIENT_ASSETS' in str(info):
            self.inform("Attempting to raise cash.")
            self.raise_cash_via_notes()
    
    def received_orders(self, orders: List[Order]):
        """ Core logic of trading bot. Based on current market activity and asset holdings,
        calculate optimal portfolio and place optimal trades. """

        # Wait until holdings are available before making decisions.
        if not self.holdings:
            return
        
        # Use CAPM logic to select the best asset to trade.
        optimal = self.select_best_asset()

        if optimal:
            asset, side, price = optimal

            # If cash amount is available, place the order. Otherwise, attempt to raise the cash by liquidating notes.
            if self.can_afford(side, price):
                self.place_order(asset, side, price)
            else:
                self.inform("Cannot afford optimal asset. Attempting to raise cash.")
                self.raise_cash_via_notes()

    def calculate_expectation_and_variance(self, asset: str):
        """ Calculate the expected payoff and variance for an asset. """

        # Equal probabilities for all payoff outcomes (uniform distribution).
        payoffs = np.array(self._payoffs[asset])
        probabilities = np.ones_like(payoffs) / len(payoffs)

        # Compute expected value (mean).
        expectation = np.dot(payoffs, probabilities)

        # Compute variance: E[(X - E[X])^2].
        variance = np.dot(probabilities, (payoffs - expectation) ** 2)

        return expectation, variance
    
    def select_best_asset(self):
        """ Evalulate all assets and return the best candidate for trading based on the
        CAPM utility score: expected payoff - λ * variance. """

        best_score = float("-inf")
        best_decision = None

        for asset, market in self._market_ids.items():
            # Skip assets with no active public orders.
            if not market.public_orders:
                continue
            
            # Compute CAPM metrics.
            expectation, variance = self.calculate_expectation_and_variance(asset)
            utility = expectation - self.risk_aversion * variance

            current_price = market.price

            # Only consider assets where utility exceeds current market price.
            if utility > current_price:
                score = utility - current_price
                if score > best_score:
                    best_score = score
                    best_decision = (asset, OrderSide.BUY, int(current_price))

        return best_decision
    
    def can_afford(self, side: OrderSide, price: int):
        """ Check whether the bot can afford the order based on available cash."""

        if side == OrderSide.BUY:
            return self.holdings.cash_available >= price
        return True
    
    def place_order(self, asset: str, side: OrderSide, price: int):
        """ Submit a limit order to the market. """

        try:
            # Create a new order object for relevant market.
            order = Order.create_new(self._market_ids[asset])

            # Set order parameters to define it as a limit order with 1 unit.
            order.order_type = OrderType.LIMIT
            order.order_side = side
            order.price = price
            order.units = 1
            order.ref = "main_order"

            # Send the order to the market.
            self.send_order(order)

        except Exception as e:
            # Log any errors during order submission.
            self.error(f"Failed to place order: {e}")

    def raise_cash_via_notes(self):
        """ Attempt to sell notes at a discount to raise cash if below threshold.
        This acts as a liquidity safeguard."""

        # Check if notes exist and are available for sale.
        if "Note" not in self._market_ids or self.holdings.get("Note", 0) <= 0:
            self.inform("No notes available to sell.")
            return

        try:
            # Access the market object for notes.
            market = self._market_ids["Note"]

            # Determine a discounted price to increase chance of sale.
            price = max(1, market.price - self.note_discount)

            # Prepare a new sell order for one unit of notes.
            order = Order.create_new(market)
            order.order_type = OrderType.LIMIT
            order.order_side = OrderSide.SELL
            order.price = price
            order.units = 1
            order.ref = "note_liquidation"

            # Send the order to the market to raise cash.
            self.send_order(order)

        except Exception as e:
            # Log any failure in the liquidation process.
            self.error(f"Error raising cash: {e}")

# Launch the bot using personalised trading account.
if __name__ == "__main__":
    """ Main entry point of the program.
    Instantiates and runs the trading bot with user-defined credentials and settings.

    SECURITY INFORMATION:
    Avoid harcoding credentials - replace FM_EMAIL and FM_PASSWORD with environment variables. """

    FM_ACCOUNT = "regular-idol"
    FM_EMAIL = "FM_EMAIL"       # Replace with environment variable in real use.
    FM_PASSWORD = "FM_PASSWORD" # Replace with environment variable in real use.
    MARKETPLACE_ID = 1181

    bot = CAPMBot(FM_ACCOUNT, FM_EMAIL, FM_PASSWORD, MARKETPLACE_ID)
    bot.run()