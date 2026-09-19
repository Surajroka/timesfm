# Assets monitored by the Adaptive Trading Agent.
# Keep this small while developing on the Twelve Data free plan.

STOCKS = [
    "AAPL",
    "NVDA",
    
]

ETFS = [
    "SPY",
 
]

METALS = []


def get_all_symbols():
    """Return every symbol monitored by the system."""
    return STOCKS + ETFS + METALS