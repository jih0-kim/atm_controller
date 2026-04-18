from abc import ABC, abstractmethod


class CashBin(ABC):
    """Interface for the physical cash bin in the ATM machine.
    Real implementation would talk to the actual hardware.
    """

    @abstractmethod
    def dispense(self, amount: int) -> None:
        """Physically dispenses cash from the machine.
        Raises an error if there's not enough cash.
        """
        pass

    @abstractmethod
    def accept(self, amount: int) -> None:
        """Accepts cash that the user inserts into the machine."""
        pass

    @abstractmethod
    def available_cash(self) -> int:
        """Returns how much cash is currently in the machine."""
        pass
