from contextvars import ContextVar
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable, Protocol, cast


@dataclass(frozen=True)
class SecurityUser:
    userid:str
    username:str
    roles:list[str] = field(default_factory=list)
    disable:bool = field(default=False)

class SecurityException(Exception):
    def __init__(self, message:str, *args):
        super().__init__(*args)
        self.message = message

class SecurityContext:

    @classmethod
    def setuser(cls, user:SecurityUser):
        cls.__user__ = ContextVar("security_user", default=None)
        cls.__user__.set(user)
    
    @classmethod
    def getuser(cls) -> SecurityUser:
        if not getattr(cls, "__user__", None): return None
        user = cls.__user__.get()
        return cast(SecurityUser, user)
    
class SecurityManager(Protocol):

    def hasroles(roles:list[str]):...

    def authenticated(func:Callable[..., Any]):...

class DefaultSecurityManager(SecurityManager):

    def hasroles(self, roles:list[str]):
        roles = roles or []
        def decorate(func:Callable[..., Any]):
            @wraps(func)
            def wrapper(*args, **kwargs):
                user = SecurityContext.getuser()
                if not user:raise

                if not set(roles).intersection(user.roles):raise SecurityContext("Role is not Authorized.")

                return func(*args, **kwargs)


            return wrapper        
        return decorate
    
    def authenticated(self, func:Callable[..., Any]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = SecurityContext.getuser()

            if not user:raise SecurityException("Not Authenticated.")

            return func(*args, **kwargs)
        return wrapper
