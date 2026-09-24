import json
import threading
import unittest
import urllib.error
import urllib.request

from colsstore import Table
from server import serve

class TestTable(unittest.TestCase):
    def test_insert_counts(self):
        table = Table()
        self.assertEqual(table.insert({"status": "ok"})["rows"], 1)

    def test_scan_hits(self):
        table = Table()
        table.insert({"status": "ok"})
        self.assertEqual(table.scan("status", "ok")["rows"], [0])

    def test_scan_miss(self):
        table = Table()
        table.insert({"status": "ok"})
        self.assertEqual(table.scan("status", "bad")["rows"], [])

    def test_stats_shape(self):
        self.assertIn("rows", Table().stats())

    def test_http_insert_scan(self):
        server = serve(0)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        base = "http://127.0.0.1:%d" % server.server_port
        urllib.request.urlopen(base + "/insert", data=b'{"row": {"status": "ok"}}', timeout=5).read()
        with urllib.request.urlopen(base + "/scan", data=b'{"column": "status", "value": "ok"}',
                                    timeout=5) as response:
            self.assertEqual(json.loads(response.read())["rows"], [0])
        server.shutdown()
