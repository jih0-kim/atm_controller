from atm.bank_api import BankAPI
from atm.cash_bin import CashBin


class ATMController:
    """
    Controls the ATM flow.
    Expected flow:
    insert_card -> enter_pin -> select_account -> see_balance / deposit / withdraw -> eject_card
    """

    def __init__(self, bank: BankAPI, cash_bin: CashBin):
        self.bank = bank
        self.cash_bin = cash_bin
        self._reset()

    def _reset(self):
        self._card_number = None
        self._authenticated = False
        self._selected_account = None

    # Card
    def insert_card(self, card_number: str) -> None:
        """Call this when a card is inserted."""
        self._card_number = card_number

    # PIN
    def enter_pin(self, pin: str) -> bool:
        """Returns True if PIN is correct, False otherwise."""
        self._require_card()
        is_correct = self.bank.check_pin(self._card_number, pin)
        if is_correct:
            self._authenticated = True
        return is_correct

    # Account selection
    def get_accounts(self) -> list[str]:
        """Returns accounts linked to the inserted card."""
        self._require_auth()
        return self.bank.get_accounts(self._card_number)

    def select_account(self, account_id: str) -> None:
        """Select which account to work with."""
        self._require_auth()
        accounts = self.bank.get_accounts(self._card_number)
        if account_id not in accounts:
            raise ValueError(f"Account '{account_id}' not found for this card.")
        self._selected_account = account_id

    # Transactions
    def see_balance(self) -> int:
        """Returns current balance in dollars."""
        self._require_account()
        return self.bank.get_balance(self._selected_account)

    def deposit(self, amount: int) -> int:
        """Accepts cash and deposits it. Returns new balance."""
        self._require_account()
        self._check_positive_amount(amount)
        self.cash_bin.accept(amount)
        new_balance = self.bank.deposit(self._selected_account, amount)
        return new_balance

    def withdraw(self, amount: int) -> int:
        """Withdraws cash and dispenses it. Returns new balance."""
        self._require_account()
        self._check_positive_amount(amount)

        new_balance = self.bank.withdraw(self._selected_account, amount)
        self.cash_bin.dispense(amount)
        return new_balance

    # End session
    def eject_card(self) -> None:
        """Ends the session and resets the controller."""
        self._reset()

    # Helpers
    def _require_card(self):
        if self._card_number is None:
            raise RuntimeError("Please insert a card first.")

    def _require_auth(self):
        self._require_card()
        if not self._authenticated:
            raise RuntimeError("Please verify your PIN first.")

    def _require_account(self):
        self._require_auth()
        if self._selected_account is None:
            raise RuntimeError("Please select an account first.")

    def _check_positive_amount(self, amount: int):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
