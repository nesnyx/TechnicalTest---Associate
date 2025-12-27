from fastapi import FastAPI
from app.api.routes import router



app = FastAPI(title="Learning RAG Demo",root_path="/api/v1")
app.include_router(router=router)


@app.get("/healthy")
async def healthy():
    return {"message": "healthy oke"}