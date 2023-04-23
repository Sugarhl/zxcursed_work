
import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from server.models.lab_solution_comment import LabSolutionComment

import server.schemas as schemas
from server.models.lab_solution import LabSolution
from server.CRUD.utils import add_to_db
from server.utils import UserType



async def create_comment(db: AsyncSession,
                         comment: schemas.LabSolutionCommentCreate,
                         user_id: int,
                         user_type: UserType) -> int:
    db_comment = LabSolutionComment(
        solution_id=comment.solution_id,
        user_id=user_id,
        user_type=user_type,
        reply_id=comment.reply_id,
        comment_text=comment.text,
        created_date=datetime.datetime.utcnow(),
        updated_date=datetime.datetime.utcnow())
    return await add_to_db(db_comment, db=db)