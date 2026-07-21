from pathlib import Path
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from .store import save_index, to_float32

# Racine du projet : .../chatbot_algerie_telecom
BASE_DIR = Path(__file__).resolve().parents[2]
KB_DIR = BASE_DIR / "data" / "kb"

#MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = str(BASE_DIR / "models" / "all-MiniLM-L6-v2")


KB_FILES = {
    "kb_articles.json": "article",
    "kb_faq.json": "faq",
    "kb_services.json": "service",
    "kb_rules.json": "rule",
}

#Convertit nimporte quelle valeur en texte propre, sans crash
def safe_str(value) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def list_to_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        cleaned = [safe_str(v) for v in value if safe_str(v)]
        return " | ".join(cleaned)
    return safe_str(value)


def load_json_file(path: Path):
    """
    Charge un fichier JSON et retourne toujours une liste d'objets.
    """
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {path}")

    data = json.loads(path.read_text(encoding="utf-8"))

    if isinstance(data, dict):
        return [data]

    raise ValueError(f"Format JSON non supporté dans : {path}")

#Transforme un objet JSON en texte lisible qu'on pourra vectoriser
def article_to_text(item: dict) -> str:
    parts = [
        "Type: article de connaissance",
        f"ID: {safe_str(item.get('id'))}",
        f"Titre: {safe_str(item.get('titre'))}",
        f"Service: {safe_str(item.get('service'))}",
        f"Catégorie: {safe_str(item.get('categorie'))}",
        f"Sous-catégorie: {safe_str(item.get('sous_categorie'))}",
        f"Intent possible: {safe_str(item.get('intent_possible'))}",
        f"Description: {safe_str(item.get('description'))}",
        f"Symptômes: {list_to_text(item.get('symptomes'))}",
        f"Causes possibles: {list_to_text(item.get('causes_possibles'))}",
        f"Vérification client: {list_to_text(item.get('verification_client'))}",
        f"Action agent: {safe_str(item.get('action_agent'))}",
        f"Réponse agent: {safe_str(item.get('reponse_agent'))}",
        f"Escalade: {safe_str(item.get('escalade'))}",
        f"Mots-clés: {list_to_text(item.get('mots_cles'))}",
        f"Exemples de requêtes utilisateur: {list_to_text(item.get('examples_user_queries'))}",
        f"Statut: {safe_str(item.get('statut'))}",
    ]
    return "\n".join([p for p in parts if p.split(":", 1)[-1].strip()])
''
#Transforme un objet JSON en texte lisible qu'on pourra vectoriser
def faq_to_text(item: dict) -> str:
    parts = [
        "Type: faq",
        f"ID: {safe_str(item.get('id'))}",
        f"Question: {safe_str(item.get('question'))}",
        f"Réponse: {safe_str(item.get('reponse'))}",
        f"Service: {safe_str(item.get('service'))}",
        f"Catégorie: {safe_str(item.get('categorie'))}",
        f"Sous-catégorie: {safe_str(item.get('sous_categorie'))}",
        f"Intent possible: {safe_str(item.get('intent_possible'))}",
        f"Variantes de question: {list_to_text(item.get('variante_questions'))}",
        f"Mots-clés: {list_to_text(item.get('mots_cles'))}",
        f"Statut: {safe_str(item.get('statut'))}",
    ]
    return "\n".join([p for p in parts if p.split(":", 1)[-1].strip()])

#Transforme un objet JSON en texte lisible qu'on pourra vectoriser
def service_to_text(item: dict) -> str:
    parts = [
        "Type: fiche service",
        f"ID: {safe_str(item.get('id'))}",
        f"Service: {safe_str(item.get('service'))}",
        f"Titre: {safe_str(item.get('titre'))}",
        f"Type de service: {safe_str(item.get('type_service'))}",
        f"Description: {safe_str(item.get('description'))}",
        f"Positionnement: {safe_str(item.get('positionnement'))}",
        f"Prérequis généraux: {list_to_text(item.get('prerequis_generaux'))}",
        f"Documents possibles: {list_to_text(item.get('documents_possibles'))}",
        f"Catégories couvertes: {list_to_text(item.get('categories_couvertes'))}",
        f"Sous-catégories couvertes: {list_to_text(item.get('sous_categories_couvertes'))}",
        f"Intents associés: {list_to_text(item.get('intents_associes'))}",
        f"Actions selfcare: {list_to_text(item.get('actions_selfcare'))}",
        f"FAQ associées: {list_to_text(item.get('faq_associees'))}",
        f"Articles associés: {list_to_text(item.get('articles_associes'))}",
        f"Résumé support: {safe_str(item.get('resume_support'))}",
        f"Mots-clés: {list_to_text(item.get('mots_cles'))}",
        f"Statut: {safe_str(item.get('statut'))}",
    ]
    return "\n".join([p for p in parts if p.split(":", 1)[-1].strip()])

#Transforme un objet JSON en texte lisible qu'on pourra vectoriser
def rule_to_text(item: dict) -> str:
    parts = [
        "Type: règle métier",
        f"ID: {safe_str(item.get('id'))}",
        f"Thème: {safe_str(item.get('theme'))}",
        f"Type de règle: {safe_str(item.get('rule_type'))}",
        f"Périmètre service: {list_to_text(item.get('service_scope'))}",
        f"Périmètre catégorie: {list_to_text(item.get('categorie_scope'))}",
        f"Condition: {safe_str(item.get('condition'))}",
        f"Action: {safe_str(item.get('action'))}",
        f"Justification: {safe_str(item.get('justification'))}",
        f"Pré-vérifications: {list_to_text(item.get('pre_checks'))}",
        f"Escalade: {safe_str(item.get('escalade'))}",
        f"Articles liés: {list_to_text(item.get('related_article_ids'))}",
        f"FAQ liées: {list_to_text(item.get('related_faq_ids'))}",
        f"Mots-clés: {list_to_text(item.get('mots_cles'))}",
        f"Statut: {safe_str(item.get('statut'))}",
    ]
    return "\n".join([p for p in parts if p.split(":", 1)[-1].strip()])

#Transforme un objet JSON en texte lisible qu'on pourra vectoriser
def record_to_text(doc_type: str, item: dict) -> str:
    if doc_type == "article":
        return article_to_text(item)
    if doc_type == "faq":
        return faq_to_text(item)
    if doc_type == "service":
        return service_to_text(item)
    if doc_type == "rule":
        return rule_to_text(item)

    return json.dumps(item, ensure_ascii=False, indent=2)


def get_record_title(doc_type: str, item: dict) -> str:
    if doc_type == "article":
        return safe_str(item.get("titre"))
    if doc_type == "faq":
        return safe_str(item.get("question"))
    if doc_type == "service":
        return safe_str(item.get("service") or item.get("titre"))
    if doc_type == "rule":
        return safe_str(item.get("theme"))
    return safe_str(item.get("id"))


def read_all_kb():
    """
    Lit tous les fichiers JSON de la base de connaissance.
    Retourne une liste de dicts :
    {
        "source": nom_fichier,
        "doc_type": type_document,
        "record_id": id,
        "title": titre,
        "text": contenu_texte
    }
    """
    if not KB_DIR.exists():
        raise FileNotFoundError(f"Dossier KB introuvable : {KB_DIR}")

    docs = []

    for file_name, doc_type in KB_FILES.items():
        path = KB_DIR / file_name
        items = load_json_file(path)

        for item in items:
            text = record_to_text(doc_type, item).strip()
            if not text:
                continue

            docs.append({
                "source": file_name,
                "doc_type": doc_type,
                "record_id": safe_str(item.get("id")),
                "title": get_record_title(doc_type, item),
                "text": text
            })

    return docs


def chunk_text(text: str, max_chars: int = 800, overlap: int = 120):
    """
    Découpe un texte en morceaux avec chevauchement.
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + max_chars, text_length)
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == text_length:
            break

        start = end - overlap

    return chunks


def build_index():
    """
    Construit l'index FAISS à partir des fichiers JSON de data/kb/.
    """
    docs = read_all_kb()

    if not docs:
        raise RuntimeError("Aucun document KB trouvé dans data/kb/")

    print(f"{len(docs)} enregistrement(s) KB trouvé(s).")

    chunk_records = []

    for doc in docs:
        chunks = chunk_text(doc["text"])

        for i, chunk in enumerate(chunks):
            chunk_records.append({
                "id": len(chunk_records),
                "source": doc["source"],
                "doc_type": doc["doc_type"],
                "record_id": doc["record_id"],
                "title": doc["title"],
                "chunk_index": i,
                "text": chunk
            })

    if not chunk_records:
        raise RuntimeError("Aucun chunk généré à partir de la KB.")

    print(f"{len(chunk_records)} chunk(s) généré(s).")

    model = SentenceTransformer(MODEL_PATH)
    texts = [record["text"] for record in chunk_records]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    vectors = to_float32(np.vstack(embeddings))
    dim = vectors.shape[1]

    # Cosine similarity = vecteurs normalisés + Inner Product
    index = faiss.IndexFlatIP(dim) #crée un objet FAISS et le stocke dans la variable index
    index.add(vectors)

    save_index(index, chunk_records)

    print(f"{len(chunk_records)} chunk(s) indexé(s).")
    return len(chunk_records)


if __name__ == "__main__":
    total = build_index()
    print(f"Index créé avec succès : {total} chunks.")