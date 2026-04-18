# atm_controller

## Project Structure

```
atm/
├── bank_api.py             # Abstract interface for bank system
├── cash_bin.py             # Abstract interface for ATM cash hardware
├── controller.py           # ATM controller
└── mock/
    ├── mock_bank.py        # Fake bank for testing
    └── mock_cash_bin.py    # Fake cash bin for testing
tests/
└── test.py
```

## ATM Flow

```text
insert_card → enter_pin → select_account → see_balance / deposit / withdraw → eject card 
```

## Features

| 기능 | 설명 | 위치 | 역할 |
|------|------|------|------|
| 카드 삽입 | 카드를 ATM에 넣는 시작 단계. | `controller.py` | Controller |
| PIN 입력 | 은행에 PIN이 맞는지 확인 요청. True/False 반환. 실제 PIN은 ATM이 모름 | `controller.py` | Controller |
| 계좌 목록 조회 | 카드에 연결된 계좌 목록을 은행에서 가져옴 | `controller.py` | Controller |
| 계좌 선택 | 목록 중 하나를 선택. | `controller.py` | Controller |
| 잔액 조회 | 현재 계좌 잔액을 정수로 반환 | `controller.py` | Controller |
| 입금 | ATM이 돈을 받고 은행에 입금 요청. 잔액 업데이트하여 반환 | `controller.py` | Controller |
| 출금 | ATM에 있는 현금 확인 → 은행에 출금 요청 → 현금 반환. 잔액 업데이트하여 반환 | `controller.py` | Controller |
| 카드 반환 | 세션 초기화. 이후 모든 동작은 카드 재삽입 필요 | `controller.py` | Controller |
| BankAPI | check_pin / get_accounts / get_balance / deposit / withdraw | `bank_api.py` | Interface |
| CashBin | dispense / accept / available_cash | `cash_bin.py` | Interface |
| MockBank | 메모리에 계좌/PIN/잔액 저장. 테스트용 가짜 은행 | `mock/mock_bank.py` | Mock |
| MockCashBin | 메모리에서 현금 증감 관리. 테스트용 가짜 현금통 | `mock/mock_cash_bin.py` | Mock |


## Setup & Run Tests

```bash
# Clone the repo
git clone https://github.com/jih0-kim/atm_controller.git
cd atm_controller

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .

# Run tests
pytest tests/ -v
```
