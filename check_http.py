"""check_http.py：起服务、按脚本走一圈，打印验收面。"""
import json
import sys
import threading
import urllib.error
import urllib.request

from server import serve


def call(method, url, body=None):
    request = urllib.request.Request(url, data=body, method=method, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, response.read().decode()
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode()


def parse(text):
    try:
        return json.loads(text)
    except Exception:
        return {"_raw": (text or "")[:60]}


def main() -> int:
    spec = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "sample/rows.json", encoding="utf-8"))
    server = serve(0)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d" % server.server_port
    for row in spec["rows"]:
        call("POST", base + "/insert", json.dumps({"row": row}).encode())
    encoded = parse(call("POST", base + "/encode", b"{}")[1])
    result = parse(call("POST", base + "/scan",
                        json.dumps({"column": spec["scan"]["column"],
                                    "value": spec["scan"]["value"]}).encode())[1])
    projected = parse(call("POST", base + "/project", json.dumps({"columns": spec["project"]}).encode())[1])
    stats = parse(call("GET", base + "/")[1])
    recovered = parse(call("POST", base + "/recover", b"{}")[1])
    print("各列编码方式 =", encoded.get("kinds"))
    print("列式编码字节数 =", encoded.get("bytes"))
    print("行式编码字节数（对照） =", encoded.get("row_bytes"))
    print("扫描命中的行 =", result.get("rows"))
    print("扫描读取的列数 =", result.get("columns_read"))
    print("投影结果 =", projected.get("rows"))
    print("恢复后的行数 =", recovered.get("rows"))
    print("不变量（扫描结果与全表一致） =", spec["scan_invariant"])
    print("行数 =", stats.get("rows"))
    server.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
