# import io
# import json
# from fastapi import UploadFile
# import pytest

# from server.schemas import SolutionUpload, LabSolutionCommentCreate
# from server.utils import UserType


# @pytest.mark.asyncio
# async def test_upload_solution(test_app, authorized_student_token):
#     headers = {"Authorization": f"Bearer {await authorized_student_token}"}
#     solution_data = SolutionUpload(
#         lab_variant_id=1, solution_text="Test solution", solution_file=UploadFile("test.txt"))

#     # Creating a file-like buffer to hold the content of the file
#     test_file = io.BytesIO(b"Test file content")

#     # Creating a multipart request with the file and JSON data
#     response = test_app.post("/solutions/upload_solution",
#                              headers=headers,
#                              data={"solution": json.dumps(
#                                  solution_data.dict(exclude={"solution_file"}))},
#                              files={"solution_file": ("test.txt", test_file, "text/plain")})

#     if user_type == "Student":
#         assert response.status_code == 201, response.text
#         assert "solution_id" in response.json()
#     else:
#         assert response.status_code == 403, response.text
#         assert "Only students are allowed to upload solutions" in response.json()[
#             "detail"]


# @pytest.mark.asyncio
# async def test_create_lab_solution_comment(test_app, authorized_student_token):
#     headers = {
#         "Authorization": f"Bearer {await authorized_student_token}"}
#     comment_data = LabSolutionCommentCreate(solution_id=1, text="Test comment")
#     response = test_app.post("/solutions/create_lab_solution_comment",
#                              json=json.loads(comment_data.json()), headers=headers)

#     assert response.status_code == 201, response.text
#     assert "comment_id" in response.json()
