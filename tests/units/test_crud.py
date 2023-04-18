# import unittest
# import pytest
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker, declarative_base

# import server.crud as crud
# from server.schemas import UserIn, LabSolutionCommentCreate

# # Set up the in-memory SQLite database for testing
# DATABASE_URL = "sqlite+aiosqlite:///./test.db"
# engine = create_async_engine(DATABASE_URL, echo=True)
# Base = declarative_base()
# Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# @pytest.mark.asyncio
# class TestCrud(unittest.IsolatedAsyncioTestCase):
#     async def asyncSetUp(self) -> None:
#         self.db = Session()

#     async def asyncTearDown(self) -> None:
#         await self.db.close()

#     async def test_generate_salt(self):
#         salt = crud.generate_salt()
#         self.assertIsInstance(salt, str)

#     async def test_add_to_db(self):
#         # Add a test model and test its add_to_db functionality
#         # Replace <YourTestModel> with a model from your application
#         # test_model = <YourTestModel>(...)

#         # model_id = await crud.add_to_db(test_model, self.db)
#         # self.assertIsInstance(model_id, int)

#         # result = await self.db.get(<YourTestModel>, model_id)
#         # self.assertIsNotNone(result)
#         pass

#     # Add other test functions for create_user, create_student, create_tutor, etc.


# if __name__ == "__main__":
#     unittest.main()
