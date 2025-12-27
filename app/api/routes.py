from fastapi import APIRouter,HTTPException
import time,os
from dotenv import load_dotenv
from app.models.schemas import QuestionRequest, DocumentRequest
from app.services.embeddings import EmbeddingService
from app.storage.qdrant_store import DocumentStore
from app.services.rag_workflow import RagWorkflow

load_dotenv()
QDRANT_URL = os.getenv("QUANDRANT_URL")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")    

router = APIRouter()
store = DocumentStore(qdrant_url=QDRANT_URL, collection_name=COLLECTION_NAME)
embedder = EmbeddingService()
rag_workflow = RagWorkflow(embbeder=embedder, store=store)

@router.post("/ask")
def ask_question(req: QuestionRequest):
    start = time.time()
    try:
        result = rag_workflow.chain.invoke({"question": req.question})
        return {
            "question": req.question,
            "answer": result["answer"],
            "context_used": result.get("context", []),
            "latency_sec": round(time.time() - start, 3)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.post("/add")
def add_document(req: DocumentRequest):
    try:
        emb = embedder.embed(req.text)
        store.add(req.text, emb)
        doc_id = len(store.docs_memory)
        return {"id": doc_id, "status": "added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
def status():
    return {
        "qdrant_ready": store.using_qdrant,
        "in_memory_docs_count": len(store.docs_memory),
        "graph_ready": rag_workflow.chain is not None
    }