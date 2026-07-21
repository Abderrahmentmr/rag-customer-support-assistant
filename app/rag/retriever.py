from functools import lru_cache #pour mémoriser le result d'une fonction en memoire RAM,pour ne pas la recalculer a chaque fois
import numpy as np
from sentence_transformers import SentenceTransformer

from app.rag.store import load_index, to_float32
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = str(BASE_DIR / "models" / "all-MiniLM-L6-v2")
#MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1) #Python charge le modele une seule fois, le garde en RAM, et le reutilise directement pour toutes les questions suivantes.
def get_model():
    return SentenceTransformer(MODEL_PATH)


@lru_cache(maxsize=1)
# charge ces 2 fichiers en memoire RAM index.faiss et chunks.json
def get_index_and_chunks():
    index, chunks = load_index()
    if index is None or not chunks:
        raise RuntimeError("Index FAISS introuvable. Lance d'abord l'ingestion.")
    return index, chunks


def retrieve(query: str, top_k: int = 6):
    """
    Recherche les chunks les plus pertinents pour une question.
    """
    query = query.strip()
    if not query:
        return []

    index, chunks = get_index_and_chunks()
    model = get_model()

    top_k = min(top_k, len(chunks))

    query_embedding = model.encode(query, normalize_embeddings=True ) #On transforme la question en liste de nombres/#N_E en met tous les nombres entre -1 et 1,pou bien compare
    query_vector = to_float32(np.array([query_embedding])) #tableau numpy en float32, format que FAISS comprend

    scores, ids = index.search(query_vector, top_k)#compare le vecteur de la question avec tous les vecteurs index(mes docuemnts) et retourne les plus proches

    results = []
    for score, idx in zip(scores[0], ids[0]):
        if idx == -1:
            continue

        item = chunks[idx]
        results.append({
            "score": float(score),
            "source": item.get("source"),
            "doc_type": item.get("doc_type"),
            "record_id": item.get("record_id"),
            "title": item.get("title"),
            "chunk_index": item.get("chunk_index"),
            "text": item.get("text"),
        })

    return results


def build_context(results: list[dict]) -> str:
    """
    Transforme les resultats retrouvees en contexte texte pour le prompt LLM.
    """
    if not results:
        return ""

    blocks = []

    for i, item in enumerate(results, start=1):
        block = (
            f"[Document {i}]\n"
            f"Type: {item.get('doc_type', '')}\n"
            f"Titre: {item.get('title', '')}\n"
            f"Source: {item.get('source', '')}\n"
            f"Contenu:\n{item.get('text', '')}"
        )
        blocks.append(block)

    return "\n\n".join(blocks) #Colle tous les blocs ensemble avec une ligne vide entre chaque