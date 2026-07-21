from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
from app.main import ask

st.set_page_config(
    page_title="Chatbot Algérie Télécome",
    page_icon="💬",
    layout="wide"
)

# ---------- STYLE ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #071427 0%, #0b1f3a 100%);
        color: white;
    }

    .main-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.2rem;
    }

    .sub-title {
        text-align: center;
        color: #c9d7ee;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    .hero-box {
        background: linear-gradient(135deg, #0f2b52 0%, #12396a 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.25);
    }

    .brand-accent {
        color: #f7b500;
        font-weight: 700;
    }

    .stChatMessage {
        border-radius: 18px;
        padding: 8px;
    }

    div[data-testid="stChatMessageContent"] {
        border-radius: 16px;
        padding: 0.9rem 1rem;
    }

    section[data-testid="stSidebar"] {
        background: #081a30;
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    .sidebar-title {
        color: white;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .source-box {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 12px 14px;
        margin-top: 8px;
    }

    .source-item {
        color: #e8eefc;
        margin-bottom: 8px;
        font-size: 0.96rem;
    }

    .footer-note {
        text-align: center;
        color: #9fb3d9;
        font-size: 0.85rem;
        margin-top: 20px;
    }

    .stButton>button {
        background: linear-gradient(135deg, #f7b500 0%, #ff9800 100%);
        color: #0b1f3a;
        border: none;
        border-radius: 12px;
        font-weight: 700;
        padding: 0.6rem 1rem;
    }

    .stButton>button:hover {
        color: #0b1f3a;
        border: none;
        opacity: 0.95;
    }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="main-title">💬 Chatbot Algérie Télécom</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Assistant intelligent <span class="brand-accent">RAG</span> connecté à votre base de connaissance</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="hero-box">
    <span class="brand-accent">Bienvenue</span><br>
    Posez votre question sur les pannes internet, le modem, la fibre, le paiement, la résiliation ou les services.
</div>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙️ Options</div>', unsafe_allow_html=True)

    if st.button("🗑️ Vider l'historique"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("**Exemples des questions les plus posées :**")
    st.markdown("- J'ai une panne d'internet")
    st.markdown("- Mon internet est lent")
    st.markdown("- Comment payer ma facture ?")
    st.markdown("- Comment résilier ?")
    st.markdown("- Mon modem ne fonctionne pas")
    st.markdown("- Pas de tonalité")
    st.markdown("- Pas d’appels Emis/reçus")
    st.markdown("- Fritures sur ligne")
    st.markdown("- Chute de débit internet")
    st.markdown("- Pas d’internet")
    st.markdown("- Liaison spécialisée")
    st.markdown("- IDOOM Internet PRO")
    st.markdown("- Intranet/VPN")
    st.markdown("- Problèmes signaux non rétablis")
    st.markdown("- Ping élevé")
    st.markdown("- Upload faible")
    st.markdown("- Coupures répétitives")
    st.markdown("- Problème de couverture réseau (4G LTE)")
    st.markdown("- Pas de tonalité / pas d'internet")

# ---------- HISTORIQUE ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- AFFICHAGE MESSAGES ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        # Afficher seulement les sources utilisées
        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander("Sources utilisées"):
                st.markdown('<div class="source-box">', unsafe_allow_html=True)

                displayed_titles = set()
                for src in msg["sources"]:
                    title = (src.get("title") or "Source sans titre").strip()
                    if title not in displayed_titles:
                        displayed_titles.add(title)
                        st.markdown(f'<div class="source-item">• {title}</div>', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

# ---------- INPUT ----------
question = st.chat_input("Pose ta question ici...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Recherche et génération de la réponse..."):
            try:
                answer, results, context = ask(question)
                st.markdown(answer)

                # Afficher seulement les sources utilisées
                if results:
                    with st.expander("Sources utilisées"):
                        st.markdown('<div class="source-box">', unsafe_allow_html=True)

                        displayed_titles = set()
                        for src in results:
                            title = (src.get("title") or "Source sans titre").strip()
                            if title not in displayed_titles:
                                displayed_titles.add(title)
                                st.markdown(f'<div class="source-item">• {title}</div>', unsafe_allow_html=True)

                        st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                answer = f"Une erreur est survenue : {e}"
                results = []
                context = ""
                st.error(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": results,
        "context": context
    })

st.markdown('<div class="footer-note">Algérie Télécom Assistant • Interface Streamlit</div>', unsafe_allow_html=True)