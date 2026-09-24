"""colsstore.py：列式存储（基线：行式字典）。"""
from __future__ import annotations


class Table:
    def __init__(self):
        self.rows = []
        self.columns = {}
        self.scanned = 0

    def insert(self, row: dict) -> dict:
        """基线：整行存一份。"""
        self.rows.append(dict(row))
        return {"rows": len(self.rows)}

    def scan(self, column: str, value) -> dict:
        """基线：逐行取该列比较（其实读了整行）。"""
        self.scanned = len(self.rows)
        hits = [index for index, row in enumerate(self.rows) if row.get(column) == value]
        return {"rows": hits, "scanned": self.scanned}

    def encode(self) -> dict:
        raise NotImplementedError("列式编码还没实现")

    def encoded_size(self) -> int:
        raise NotImplementedError("编码大小还没实现")

    def project(self, columns) -> dict:
        raise NotImplementedError("按列投影还没实现")

    def persist(self) -> bytes:
        raise NotImplementedError("快照还没实现")

    def restore(self, blob: bytes = None) -> dict:
        raise NotImplementedError("重启恢复还没实现")

    def stats(self) -> dict:
        return {"rows": len(self.rows), "columns": len(self.columns), "scanned": self.scanned}
