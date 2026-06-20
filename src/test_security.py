
from typing import Any

from _dev.managers.security import DefaultSecurityManager, SecurityContext, SecurityUser


db:dict[int, dict[str, Any]] = {
    1: {
        "accid": 1,
        "name": "Aung Aung",
        "amount": 10000
    },
    2: {
        "accid": 2,
        "name": "Thidar",
        "amount": 10000
    },
    3: {
        "accid": 3,
        "name": "Su Su",
        "amount": 10000
    },
}

def login(accid:int):
    acc = db.get(accid)
    if acc:SecurityContext.setuser(SecurityUser(
        userid=str(acc), username=acc.get("name"), roles=["member"]
    ))

sec = DefaultSecurityManager()

login(1)

@sec.hasroles(["member"])
def profile(accid:int):
    return db.get(accid)

p = profile(1)

print(p)