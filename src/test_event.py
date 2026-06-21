import asyncio
from contextlib import contextmanager
from dataclasses import dataclass

from _dev.managers.asyncs.event import AsyncEventDispatcher, DefaultAsyncEventManager, DefaultAsyncEventQueue


queue = DefaultAsyncEventQueue()
em = DefaultAsyncEventManager(queue)

@dataclass(frozen=True)
class PasswordUpdateEvent:
    userid:int;username:str

@em.listen(PasswordUpdateEvent)
def handle(event:PasswordUpdateEvent):
    print(f"Password Updating Event Happened!\nUserId: {event.userid}\nUserName: {event.username}")

def update_password(userid:int, username:str, newpassword:str):
    print(f"{userid} - {username} is updating password to {newpassword}")
    print("Password Updating Finished...")
    em.publish(PasswordUpdateEvent(userid, username))


def run():

    async def runner():
        dispatcher = AsyncEventDispatcher(em, queue)
        task = asyncio.create_task(dispatcher.run())
        try:
            while True:
                userid = input("User Id : ")
                if userid == "0": break
                username = input("User Name : ")
                newpassword = input("New Password : ")
                update_password(userid, username, newpassword)
                # update_password(1, "Aung Aung", "newpassword")
                await asyncio.sleep(0)
        finally:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    asyncio.run(runner())

if __name__ == "__main__":
    run()
