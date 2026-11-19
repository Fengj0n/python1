import asyncio
import time

async def fake_api():
    await asyncio.sleep(5)
    return "API 正常返回结果"
async def main():
    start = time.time()
    try:
        result = await asyncio.wait_for(
            fake_api(),
            timeout=2
        )
    #     调用超限时间和对应的函数部分
    except asyncio.TimeoutError:
        result = "API 超时，使用默认结果"

    print(result)
    print(f"耗时：{time.perf_counter() - start:.2f}s")

    print("程序继续执行，没有崩溃")


asyncio.run(main())