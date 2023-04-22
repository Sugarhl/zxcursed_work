from fastapi import FastAPI
from server.database import async_database, create_tables
from server.api.login import router as login_router
from server.api.registration import router as registration_router
from server.api.solutions import router as solutions_router

app = FastAPI()


@app.on_event("startup")
async def startup():
    await create_tables()
    await async_database.connect()


@app.on_event("shutdown")
async def shutdown():
    await async_database.disconnect()

app.include_router(login_router, prefix="/auth", tags=["Authentication"])
app.include_router(registration_router,
                   prefix="/registration", tags=["Registration"])
app.include_router(solutions_router, prefix="/solutions", tags=["Solutions"])


@app.get("/")
async def root():
    return {"message": "Welcome!"}
