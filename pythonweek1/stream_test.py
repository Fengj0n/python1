from openai import OpenAI
from dotenv import load_dotenv
import os
import time
load_dotenv()
client = OpenAI()
start = time.perf_counter()
first = True
stream = client.chat.completions.create(
    model=os.getenv("LLM_MODEL"),
    messages=[{"role": "user", "content": "介绍一下AI Agent"}],
    stream=True
)
for chunk in stream:
    if chunk.choices:
        # 这个是为了放置列表中是空的
        content = chunk.choices[0].delta.content
        if content:
            if first:
                print(f"首字延迟：{time.perf_counter() - start:.2f}s")
                first = False
            print(content, end="", flush=True)
#             表示立即打印文本内容
print(f"\n总耗时：{time.perf_counter() - start:.2f}s")