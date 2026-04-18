from atm.cash_bin import CashBin


class MockCashBin(CashBin):
    """Fake cash bin for testing. Tracks cash in memory."""

    def __init__(self, initial_cash: int = 10000):
        self._cash = initial_cash

    def dispense(self, amount: int) -> None:
        if self._cash < amount:
            raise RuntimeError("Cash bin is empty.")
        self._cash -= amount

    def accept(self, amount: int) -> None:
        self._cash += amount

    def available_cash(self) -> int:
        return self._cash
