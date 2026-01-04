import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from items_views import router as items_router
from users.views import router as users_router
from core.models import Base, db_helper
from api_v1 import router as router_v1
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_prefix)
app.include_router(items_router)
app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", reload=True)
