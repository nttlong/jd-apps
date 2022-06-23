from rcmpct import async_wrap
from asgiref.sync import async_to_sync, sync_to_async

import datetime
import time
@async_wrap
def test():
    time.sleep(1)
    return 1


@async_wrap
def test2():
    time.sleep(2)
    return 2

async def total():
    return await test()+ await test2()



n=datetime.datetime.now()
# fx=async_to_sync(test)()+async_to_sync(test2)()
fx= async_to_sync(total)()
m=(datetime.datetime.now()-n).seconds
print(m)
print(fx)

