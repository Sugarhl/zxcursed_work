import asyncio
from math import e
import os
from typing import List
import nbformat
import rocksdb
import uuid
from server.generation.generators.base import Variant

from server.storage.base_file_storage import FileStorage
from server.validation.checks import file_check


HOME = os.path.expanduser("~")
ROOT = os.path.join(HOME, ".app_storage")
STORAGE = os.path.join(ROOT, ".lab_man_storage.db")


class RocksDBStorage(FileStorage):
    _instance = None
    _lock = asyncio.Lock()

    @classmethod
    async def get_instance(cls):
        if cls._instance is None:
            async with cls._lock:
                if cls._instance is None:
                    if not os.path.exists(ROOT):
                        os.makedirs(ROOT)
                    cls._instance = rocksdb.DB(
                        STORAGE,
                        rocksdb.Options(create_if_missing=True),
                    )
        return cls._instance

    async def save_file(self, content):
        file_id = str(uuid.uuid4())
        db = await self.get_instance()
        db.put(file_id.encode(), content)
        return file_id

    async def update_file(self, file_key, content):
        db = await self.get_instance()
        get_value = await self.get_file(file_key)
        if get_value:
            db.delete(file_key.encode())
            db.put(file_key.encode(), content)
            return True
        return False

    async def get_file(self, file_id):
        db = await self.get_instance()
        get_value = db.get(file_id.encode())
        if get_value:
            return get_value
        else:
            return None

    async def get_file_checked(self, file_id):
        file = await self.get_file(file_id=file_id)
        file_check(file)
        return file

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
