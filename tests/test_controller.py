import pytest
from atm.controller import ATMController
from atm.mock.mock_bank import MockBank
from atm.mock.mock_cash_bin import MockCashBin


def make_atm():
    bank = MockBank()
    bank.add_card(
        card_number="1234-5678",
        pin="1234",
        accounts={"checking": 500, "savings": 1000},
    )
    cash_bin = MockCashBin(initial_cash=5000)
    return ATMController(bank=bank, cash_bin=cash_bin)


# 카드 삽입
def test_insert_card():
    atm = make_atm()
    atm.insert_card("1234-5678")    # got number from hardware


# PIN 입력
def test_correct_pin():
    atm = make_atm()
    atm.insert_card("1234-5678")
    result = atm.enter_pin("1234")
    assert result == True


def test_wrong_pin():
    atm = make_atm()
    atm.insert_card("1234-5678")
    result = atm.enter_pin("0000")
    assert result == False


# 계좌 선택
def test_get_accounts():
    atm = make_atm()
    atm.insert_card("1234-5678")
    atm.enter_pin("1234")
    accounts = atm.get_accounts()
    assert "checking" in accounts
    assert "savings" in accounts


def test_select_account():
    atm = make_atm()
    atm.insert_card("1234-5678")
    atm.enter_pin("1234")
    atm.select_account("checking")


# 잔액 조회
def test_see_balance():
    atm = make_atm()
    atm.insert_card("1234-5678")
    atm.enter_pin("1234")
    atm.select_account("checking")
    balance = atm.see_balance()
    assert balance == 500


def test_see_balance_savings():
    atm = make_atm()
    atm.insert_card("1234-5678")
    atm.enter_pin("1234")
    atm.select_account("savings")
    balance = atm.see_balance()
    assert balance == 1000


# 입금
def test_deposit():
    atm = make_atm()
    atm.insert_card("1234-5678")
    atm.enter_pin("1234")
    atm.select_account("checking")
    new_balance = atm.deposit(200)
    assert new_balance == 700


def test_deposit_then_check_balance():
    atm = make_atm()
    atm.insert_card("1234-5678")
    atm.enter_pin("1234")
    atm.select_account("checking")
    atm.deposit(200)
    assert atm.see_balance() == 700


def test_deposit_zero_raises():
    atm = make_atm()
    atm.insert_card("1234-5678")
    atm.enter_pin("1234")
    atm.select_account("checking")
    with pytest.raises(ValueError):
        atm.deposit(0)


def test_deposit_negative_raises():
    atm = make_atm()
    atm.insert_card("1234-5678")
    atm.enter_pin("1234")
    atm.select_account("checking")
    with pytest.raises(ValueError):
        atm.deposit(-100)


# 출금
def test_withdraw():
    atm = make_atm()
    atm.insert_card("1234-5678")
    atm.enter_pin("1234")
    atm.select_account("checking")
    new_balance = atm.withdraw(100)
    assert new_balance == 400


def test_withdraw_then_check_balance():
    atm = make_atm()
    atm.insert_card("1234-5678")
    atm.enter_pin("1234")
    atm.select_account("checking")
    atm.withdraw(100)
    assert atm.see_balance() == 400


def test_withdraw_all_money():
    atm = make_atm()
    atm.insert_card("1234-5678")
    atm.enter_pin("1234")
    atm.select_account("checking")
    new_balance = atm.withdraw(500)
    assert new_balance == 0


def test_withdraw_more_than_balance_raises():
    atm = make_atm()
    atm.insert_card("1234-5678")
    atm.enter_pin("1234")
    atm.select_account("checking")
    with pytest.raises(RuntimeError):
        atm.withdraw(9999)


def test_withdraw_zero_raises():
    atm = make_atm()
    atm.insert_card("1234-5678")
    atm.enter_pin("1234")
    atm.select_account("checking")
    with pytest.raises(ValueError):
        atm.withdraw(0)


def test_withdraw_when_atm_has_no_cash():
    bank = MockBank()
    bank.add_card("1234-5678", "1234", {"checking": 500})
    empty_cash_bin = MockCashBin(initial_cash=0)
    atm = ATMController(bank=bank, cash_bin=empty_cash_bin)
    atm.insert_card("1234-5678")
    atm.enter_pin("1234")
    atm.select_account("checking")
    with pytest.raises(RuntimeError):
        atm.withdraw(100)
    assert atm.see_balance() == 500 


# 카드 반환
def test_eject_card():
    atm = make_atm()
    atm.insert_card("1234-5678")
    atm.enter_pin("1234")
    atm.eject_card()
    with pytest.raises(RuntimeError):
        atm.see_balance()


def test_can_reuse_atm_after_eject():
    atm = make_atm()
    atm.insert_card("1234-5678")
    atm.enter_pin("1234")
    atm.eject_card()

    atm.insert_card("1234-5678")
    result = atm.enter_pin("1234")
    assert result == True
