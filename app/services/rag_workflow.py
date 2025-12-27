from pydantic import BaseModel
from typing import List
from app.services.embeddings import EmbeddingService
from app.storage.qdrant_store import DocumentStore
from langgraph.graph import StateGraph, END

class GraphState(BaseModel):
    question : str
    context : List[str]
    answer : str

class RagWorkflow:
    def __init__(self,embbeder : EmbeddingService, store : DocumentStore):
        self.embedder = embbeder
        self.store = store
        self.chain = self._build_graph()

    def retrieve_node(self, state: dict):
        query = state["question"]
        emb = self.embedder.embed(query)
        state["context"] = self.store.search(query, emb)
        return state

    def answer_node(self, state: dict):
        ctx = state.get("context", [])
        state["answer"] = f"I found this: '{ctx[0][:100]}...'" if ctx else "Sorry, I don't know."
        return state

    def _build_graph(self):
        workflow = StateGraph(dict)
        workflow.add_node("retrieve", self.retrieve_node)
        workflow.add_node("answer", self.answer_node)
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "answer")
        workflow.add_edge("answer", END)
        return workflow.compile()