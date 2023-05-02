import asyncio
from typing import List
import nbformat
import rocksdb
import uuid
from server.generation.base import Variant

from server.storage.base_file_storage import FileStorage


class RocksDBStorage(FileStorage):
    _instance = None
    _lock = asyncio.Lock()

    @classmethod
    async def get_instance(cls):
        if cls._instance is None:
            async with cls._lock:
                if cls._instance is None:
                    cls._instance = rocksdb.DB(
                        ".lab_man_storage.db",
                        rocksdb.Options(create_if_missing=True),
                    )
        return cls._instance

    async def save_file(self, content):
        file_id = str(uuid.uuid4())
        db = await self.get_instance()
        db.put(file_id.encode(), content)
        return file_id

    async def get_file(self, file_id):
        db = await self.get_instance()
        get_value = db.get(file_id.encode())
        if get_value:
            return get_value
        else:
            raise FileNotFoundError(f"File with ID {file_id} not found")

    async def delete_file(self, file_id):
        db = await self.get_instance()
        get_value = db.get(file_id.encode())
        if get_value:
            db.delete(file_id.encode())
        else:
            raise FileNotFoundError(f"File with ID {file_id} not found")


async def save_variants(variants: List[Variant]):
    db = RocksDBStorage()
    for var in variants:
        content = nbformat.writes(var.notebook).encode("utf-8")
        file_key = await db.save_file(content)
        var.key = file_key
    return variants
