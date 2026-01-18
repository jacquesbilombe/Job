from fastapi import FastAPI
from routers.poost import router as post_router

app = FastAPI()
app.include_router(post_router)
