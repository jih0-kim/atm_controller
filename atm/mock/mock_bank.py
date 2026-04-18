from atm.bank_api import BankAPI


class MockBank(BankAPI):
    """Fake bank for testing. No real network calls."""

    def __init__(self):
        # card_number -> pin
        self._pins = {}
        # card_number -> list of account_ids
        self._card_accounts = {}
        # account_id -> balance
        self._balances = {}

    def add_card(self, card_number: str, pin: str, accounts: dict[str, int]):
        self._pins[card_number] = pin
        self._card_accounts[card_number] = list(accounts.keys())
        self._balances.update(accounts)

    def check_pin(self, card_number: str, pin: str) -> bool:
        return self._pins.get(card_number) == pin

    def get_accounts(self, card_number: str) -> list[str]:
        return self._card_accounts.get(card_number, [])

    def get_balance(self, account_id: str) -> int:
        return self._balances[account_id]

    def deposit(self, account_id: str, amount: int) -> int:
        self._balances[account_id] += amount
        return self._balances[account_id]

    def withdraw(self, account_id: str, amount: int) -> int:
        if self._balances[account_id] < amount:
            raise RuntimeError("Insufficient funds.")
        self._balances[account_id] -= amount
        return self._balances[account_id]
