import asyncio
import time
async def fake_api(name,delay):
    print(f"{name} 开始执行")
    await asyncio.sleep(delay)
    print(f"{name} 执行完毕")
    return name
async def main():
    start = time.time()
    # results = await asyncio.gather(fake_api("api1",2),fake_api("api2",1))

    results = []

    results.append(await fake_api("A", 1))
    results.append(await fake_api("B", 1))
    results.append(await fake_api("C", 1))
    print(results)

    print(f"总耗时{time.time()-start}")
asyncio.run(main())

#
