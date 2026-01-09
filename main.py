import uvicorn
from fastapi import FastAPI

from api_v1 import router as router_v1
from core.config import settings
from users.views import router as users_router

app = FastAPI()
app.include_router(router=router_v1, prefix=settings.api_prefix)
app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", reload=True)
