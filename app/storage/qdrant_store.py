from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance


class DocumentStore:
    def __init__(self,qdrant_url: str,collection_name : str):
        self.qdrant_url = qdrant_url
        self.collection_name = collection_name
        self.docs_memory = []
        try:
            self.client = QdrantClient(self.qdrant_url)
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=128, distance=Distance.COSINE)
            )
            self.using_qdrant = True
        except Exception:
            self.using_qdrant = False 

    def add(self, vector: list[float], text: str):
        doc_id = len(self.docs_memory)
        if self.using_qdrant:
            payload = {"text": text}
            self.client.upsert(
                collection_name=self.collection_name,
                points=[PointStruct(id=doc_id, vector=vector, payload=payload)]
            )
        else:
            self.docs_memory.append(text)

    def search(self, query: str, vector: list):
        results = []
        if self.using_qdrant:
            hits = self.client.search(collection_name=self.collection_name, query_vector=vector, limit=2)
            results = [hit.payload["text"] for hit in hits]
        else:
            results = [doc for doc in self.docs_memory if query.lower() in doc.lower()]
            if not results and self.docs_memory:
                results = [self.docs_memory[0]]
        return results

    