import asyncio
import logging
from collections import defaultdict
import inspect
from typing import Callable, Protocol, Type, TypeVar


E = TypeVar("E")
R = TypeVar("R")

class AsyncEventQueue(Protocol):
    def add(self, event:E):...
    async def pop(self) -> E:...

class DefaultAsyncEventQueue(AsyncEventQueue):
    def __init__(self):
        self.queue:asyncio.Queue[E] = asyncio.Queue()

    def add(self, event:E):
        self.queue.put_nowait(event)

    async def pop(self) -> E:
        return await self.queue.get()

class AsyncEventManager(Protocol):
    async def publish(self, event:E):...
    def listen(self, event:Type[E]) -> Callable[[Callable[[E], R]], Callable[[E], R]]:...
    def handlers(self, event:Type[E]) -> list[Callable[[E], R]]:...

class DefaultAsyncEventManager(AsyncEventManager):

    def __init__(self, queue:AsyncEventQueue):
        self.queue = queue
        self.registry:dict[Type[E], list[Callable[[E], R]]] = defaultdict(list)

    def listen(self, event:Type[E]) -> Callable[[Callable[[E], R]], Callable[[E], R]]:
        def decorate(func:Callable[[E], R]) -> Callable[[E], R]:
            self.registry[event].append(func)
            return func
        return decorate
    
    def publish(self, event:E):
        self.queue.add(event)
    
    def handlers(self, event:Type[E]) -> list[Callable[[E], R]]:
        return self.registry.get(event, [])

class AsyncEventDispatcher:

    def __init__(self, em:AsyncEventManager, queue:AsyncEventQueue):
        self.em = em
        self.queue = queue
        self.logger = logging.getLogger(__name__)

    async def run(self):
        try:
            while True:
                event = await self.queue.pop() 
                for handler in self.em.handlers(type(event)):
                    try:
                        result = handler(event)
                        if inspect.isawaitable(result): await result
                    except Exception as e:
                        self.logger.error(e)
        except asyncio.CancelledError as e:
            self.logger.error(e)
            raise