from abc import ABC, abstractmethod


class BankAPI(ABC):
    """Interface for talking to a bank system.
    Real implementation would call actual bank endpoints.
    """

    @abstractmethod
    def check_pin(self, card_number: str, pin: str) -> bool:
        """Returns True if PIN is correct, False otherwise.
        The bank never sends the actual PIN to ATM.
        """
        pass

    @abstractmethod
    def get_accounts(self, card_number: str) -> list[str]:
        """Returns list of account IDs linked to this card."""
        pass

    @abstractmethod
    def get_balance(self, account_id: str) -> int:
        """Returns current balance in dollars."""
        pass

    @abstractmethod
    def deposit(self, account_id: str, amount: int) -> int:
        """Deposits amount and returns new balance."""
        pass

    @abstractmethod
    def withdraw(self, account_id: str, amount: int) -> int:
        """Withdraws amount and returns new balance.
        Should raise an error if balance is insufficient.
        """
        pass
