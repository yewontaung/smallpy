from dataclasses import dataclass

from _dev.managers.readonly import readonly


@dataclass
@readonly("accid", "amount")
class BankAcc:
    accid:int
    name:str
    amount:int

acc = BankAcc(accid=1, name="Aung Aung", amount=10000)
acc.amount=9000 #Error : Cannot update amount
print(acc)