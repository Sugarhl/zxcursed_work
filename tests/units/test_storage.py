import asyncio
import pytest
from unittest.mock import patch

from server.storage.rocks_db_storage import RocksDBStorage


class TestRocksDBStorage:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.storage = RocksDBStorage()

    def test_save_and_get_file(self):
        content = b"hello world"
        file_id = asyncio.run(self.storage.save_file(content))
        retrieved_content = asyncio.run(self.storage.get_file(file_id))
        assert content == retrieved_content

    def test_delete_file(self):
        content = b"hello world"
        file_id = asyncio.run(self.storage.save_file(content))
        asyncio.run(self.storage.delete_file(file_id))
        with pytest.raises(FileNotFoundError):
            asyncio.run(self.storage.get_file(file_id))
