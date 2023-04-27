import logging
from fastapi import FastAPI
from server.database import async_database, create_tables
from server.api.login import router as login_router
from server.api.registration import router as registration_router
from server.api.solutions import router as solutions_router
from server.api.lab import router as lab_router
from server.api.lab_variants import router as variants_router
from server.api.group import router as group_router
from server.api.template import router as template_router

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
app.include_router(lab_router, prefix="/lab", tags=["Lab"])
app.include_router(variants_router, prefix="/variatns", tags=["Variants"])
app.include_router(group_router, prefix="/group", tags=["Group"])
app.include_router(template_router, prefix="/temp", tags=["Template"])


@app.get("/")
async def root():
    return {"message": "Welcome!"}
