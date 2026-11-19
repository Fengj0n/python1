# pythonweek1 · W1 练习集

AI Agent 开发学习计划第 1 周的五个练手脚本：**异步并发、超时降级、JSON 校验、异常分层、流式输出**。

每个脚本都是独立可运行的最小实验，用来验证一个具体的工程能力点。

## 环境要求

- Python 3.12（`uv` 会按 `.python-version` 自动准备）
- [uv](https://docs.astral.sh/uv/) 包管理器

## 快速开始

```bash
git clone https://github.com/Fengj0n/python1.git
cd python1/pythonweek1
cp .env.example .env          # 然后填入自己的 API Key
uv run python async_test.py
```

三步即可运行任意脚本，**不需要手动激活虚拟环境**。

## 环境变量

| 变量 | 说明 | 示例 |
| --- | --- | --- |
| `OPENAI_API_KEY` | 大模型 API Key | `sk-xxxxxxxx` |
| `OPENAI_BASE_URL` | 接口地址 | `https://api.deepseek.com` |
| `LLM_MODEL` | 模型名称 | `deepseek-flash` |

真实值只写在 `.env` 里；`.env` 已被 `.gitignore` 忽略，仓库里只保留 `.env.example` 模板。

## 五个脚本

| 文件 | 演示什么 | 期望结果 |
| --- | --- | --- |
| `async_test.py` | `asyncio.gather` 并发调用 | 两个请求（2s / 1s）总耗时 ≈ **2.00s**，而不是 3s |
| `timeout_test.py` | `asyncio.wait_for` 超时降级 | 2s 超时后打印兜底结果，进程不崩，耗时 ≈ **2.00s** |
| `json_test.py` | Pydantic 严格校验 | 4 组输入分别为：通过 / 缺字段 / 类型错误 / 非法 JSON |
| `exception_test.py` | httpx 错误分层与重试 | 网络错、400、500、解析错 四条分支各自处理 |
| `stream_test.py` | 流式输出与首字延迟 | 逐字打印，首字延迟 2–3s |

## 踩过的坑

1. **串行 await**：连续写三次 `results.append(await f())`，会把 3 个 1 秒的调用串成 3 秒。并发要用 `asyncio.gather(...)`。
2. **两种时钟不能混用**：`time.time()` 返回 Unix 时间戳（约 1.79e9），`time.perf_counter()` 返回开机以来的秒数（约 3.7e4）。测耗时只能用后者，混用会算出 -1.79e9 这样的负数。
3. **TLS 与代理**：本机 Python 3.8 直连 HTTPS 会 `EOF occurred in violation of protocol`，需要 `HTTPS_PROXY=http://127.0.0.1:7890`；Python 3.12 直连正常。
4. **`.env` 不能进仓库**：API Key 一旦提交并推送，公开仓库几分钟内就会被爬虫扫走，必须吊销重签。

## 目录结构

```
pythonweek1/
├── .env.example          # 环境变量模板（可提交）
├── .gitignore            # 已忽略 .env / .venv
├── .python-version       # 3.12
├── pyproject.toml        # 依赖声明
├── uv.lock               # 锁定版本，保证可复现
├── async_test.py
├── exception_test.py
├── json_test.py
├── stream_test.py
├── timeout_test.py
└── src/pythonweek1/      # uv 生成的包骨架，本周未使用
```
