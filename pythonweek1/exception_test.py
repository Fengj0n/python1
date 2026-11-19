import httpx
import time
def mock_api(request):
    path = request.url.path
    if path == "/network":
        raise httpx.ConnectError(
            "网络连接失败", request=request
        )
    if path == "/400":
        return httpx.Response(400)
    if path == "/500":
        return httpx.Response(500)
    if path == "/json":
        return httpx.Response(200, text="非法JSON")
    return httpx.Response(200, json={"ok": True})
def request_api(client, url):
    for attempt in range(2):
        try:
            response = client.get(url, timeout=3)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError:
            print("网络异常，连接失败")
        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            if 400 <= status < 500:
                print(f"客户端异常：{status}")
                return None
            print(f"服务端异常：{status}")
        except ValueError:
            print("JSON 解析失败")
            return None
        if attempt == 0:
            print("准备重试...")
            time.sleep(1)
    print("重试失败，返回兜底结果")
    return None

with httpx.Client(
    transport=httpx.MockTransport(mock_api)
) as client:

    for path in ["network", "400", "500", "json"]:
        print(f"\n测试：{path}")
        request_api(client, f"https://test.local/{path}")