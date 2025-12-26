from fastapi import APIRouter
import time
from app.models.schemas import QuestionRequest, DocumentRequest

routes = APIRouter()



@routes.post("/ask")
def ask_question(req: QuestionRequest):
    start = time.time()
    try:
        result = chain.invoke({"question": req.question})
        return {
            "question": req.question,
            "answer": result["answer"],
            "context_used": result.get("context", []),
            "latency_sec": round(time.time() - start, 3)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))