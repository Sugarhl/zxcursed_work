# import asyncio
import unittest
from fastapi import HTTPException
import nbformat
from nbformat.v4 import new_notebook
from server.storage.rocks_db_storage import RocksDBStorage


class RocksDBStorageTestCase(unittest.IsolatedAsyncioTestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        self.db = RocksDBStorage()
        super().__init__(methodName)

    async def test_save_and_get_file(self):
        content = b"test content"
        file_id = await self.db.save_file(content)
        self.assertIsInstance(file_id, str)
        self.assertEqual(await self.db.get_file(file_id), content)

    async def test_update_file(self):
        content1 = b"test content 1"
        content2 = b"test content 2"
        file_id = await self.db.save_file(content1)
        updated = await self.db.update_file(file_id, content2)
        self.assertTrue(updated)
        self.assertEqual(await self.db.get_file(file_id), content2)

    async def test_get_file_checked(self):
        content = b'{"cells": []}'
        file_id = await self.db.save_file(content)
        self.assertEqual(await self.db.get_file_checked(file_id), content)
        with self.assertRaises(HTTPException):
            await self.db.get_file_checked("invalid_file_id")

    async def test_delete_file(self):
        content = b"test content"
        file_id = await self.db.save_file(content)
        await self.db.delete_file(file_id)
        self.assertIsNone(await self.db.get_file(file_id))
        with self.assertRaises(FileNotFoundError):
            await self.db.delete_file("invalid_file_id")

    async def test_save_notebook(self):
        nb = new_notebook()
        content = nbformat.writes(nb).encode("utf-8")
        file_id = await self.db.save_file(content)
        self.assertIsInstance(file_id, str)
        self.assertEqual(await self.db.get_file(file_id), content)
        with self.assertRaises(HTTPException):
            await self.db.get_file_checked("invalid_file_id")

    async def test_update_notebook(self):
        nb1 = new_notebook()
        nb2 = new_notebook()
        content1 = nbformat.writes(nb1).encode("utf-8")
        content2 = nbformat.writes(nb2).encode("utf-8")
        file_id = await self.db.save_file(content1)
        updated = await self.db.update_file(file_id, content2)
        self.assertTrue(updated)
        self.assertEqual(await self.db.get_file(file_id), content2)
        self.assertFalse(await self.db.update_file("invalid_file_id", content2))

    async def test_delete_notebook(self):
        nb = new_notebook()
        content = nbformat.writes(nb).encode("utf-8")
        file_id = await self.db.save_file(content)
        await self.db.delete_file(file_id)
        self.assertIsNone(await self.db.get_file(file_id))
        with self.assertRaises(FileNotFoundError):
            await self.db.delete_file("invalid_file_id")
