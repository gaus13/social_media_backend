import pytest
from app.calc import add, sub, mul, BankAcc, NoMoney

@pytest.fixture
def zero_bank_acc():
    return BankAcc()

@pytest.fixture
def bank_account():
    return BankAcc(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (3,2,5), 
    (7,1,8),
    (2,2,4)
])
def test_add(num1, num2, expected):
    print("Testing add function")
    assert add(num1, num2)==  expected

def test_sub():
    assert sub(9,5) == 4 

def test_mul():
    assert mul(2, 3) == 6      

def test_bank_initial_amount(bank_account):
        assert bank_account.balance == 50

def test_bank_def_amount(zero_bank_acc):
    assert zero_bank_acc.balance == 0

def test_withdraw(bank_account):
     bank_account.withdraw(20)
     assert bank_account.balance == 30


@pytest.mark.parametrize("deposite, withdraw, expected", [
    (300,200,100), 
    (50,10,40),
    (1200,200,1000),
    ])
def test_bank_transaction(zero_bank_acc, deposite, withdraw, expected):
     zero_bank_acc.deposite(deposite)
     zero_bank_acc.withdraw(withdraw)
     assert zero_bank_acc.balance == expected    

def test_no_money(bank_account):  
       with pytest.raises(NoMoney): 
          bank_account.withdraw(200)