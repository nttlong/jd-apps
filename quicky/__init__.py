import asyncio
def deasync(*args,**kwargs):

    def wrapper(*x,**y):
        handler = x[0]
        def run(*a,**b):
            # import time
            # time.sleep(0.001)
            # async_response = []
            #
            # async def run_and_capture_result(*b,**d):
            #     r = await handler(*b,**d)
            #     async_response.append(r)
            # loop=None
            # try:
            #     # loop = asyncio.get_running_loop()
            # except Exception as e:
            #     cc=e
            # coroutine = asyncio.coroutine(handler(*a,**b))
            # loop =asyncio.get_running_loop()
            # ret =loop.run_until_complete(coroutine)
            return handler(*a,**b)

        return run

    return wrapper