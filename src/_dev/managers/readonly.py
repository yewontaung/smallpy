from typing import Any, Callable, Type


def readonly(*fields:str):
    fields = set(fields)
    def decorate[T](cls:Type[T]):
        setter = cls.__setattr__
        def __setattr__(obj:T, name:str, value:Any):
            if name in fields:
                if hasattr(obj, name): raise Exception(f"Cannot update {name}")
            setter(obj, name, value)
        cls.__setattr__ = __setattr__
        return cls

    return decorate