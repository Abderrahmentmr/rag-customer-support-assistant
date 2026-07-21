import json
from pathlib import Path
import faiss
import numpy as np

# Racine du projet : .../chatbot_algerie_telecom
BASE_DIR = Path(__file__).resolve().parents[2]

VECTOR_STORE_DIR = BASE_DIR / "data" / "vector_store"
VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

INDEX_PATH = VECTOR_STORE_DIR / "faiss.index"
META_PATH = VECTOR_STORE_DIR / "chunks.json"

#svgarde fichier RAM -> disque dur
def save_index(index: faiss.Index, chunks: list[dict]):
    """
    Sauvegarde l'index FAISS et les métadonnées des chunks.
    """
    faiss.write_index(index, str(INDEX_PATH))
    META_PATH.write_text(
        json.dumps(chunks, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def load_index():
    """
    Charge l'index FAISS et les chunks sauvegardés.
    Retourne (index, chunks) ou (None, []) si rien n'existe.
    """
    if not INDEX_PATH.exists() or not META_PATH.exists():
        return None, []

    index = faiss.read_index(str(INDEX_PATH))
    chunks = json.loads(META_PATH.read_text(encoding="utf-8"))
    return index, chunks


def to_float32(x: np.ndarray) -> np.ndarray:
    """
    Convertit un tableau numpy en float32 pour FAISS.
    """
    return x.astype(np.float32)