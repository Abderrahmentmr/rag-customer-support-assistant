from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
from app.main import ask

st.set_page_config(
    page_title="Chatbot Algérie Télécom",
    page_icon="📡",
    layout="wide"
)

# ─────────────────────────────────────────────
# STYLE
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* === PALETTE === */
:root {
    --green:      #00A651;
    --green-dk:   #007d3c;
    --green-bg:   #eaf7f0;
    --navy:       #0d1b2a;
    --page-bg:    #f0f7f3;
    --bot-bubble: #d4ede0;
    --border:     rgba(0,166,81,0.25);
}

/* === FOND PAGE === */
.stApp { background: var(--page-bg) !important; }

/* Masquer chrome Streamlit */
#MainMenu, footer, header { visibility: hidden; }

/* === EN-TÊTE === */
.at-header {
    background: var(--navy);
    border-radius: 0 0 16px 16px;
    padding: 14px 22px 11px;
    display: flex; align-items: center; gap: 14px;
    margin-bottom: 16px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.20);
}
.at-logo {
    background: var(--green); border-radius: 50%;
    width: 42px; height: 42px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem; flex-shrink: 0;
}
.at-header h1 { margin:0; color:#fff; font-size:1.15rem; font-weight:700; line-height:1.2; }
.at-header p  { margin:0; color:#8cb8a0; font-size:0.78rem; }
.at-badge {
    margin-left: auto;
    background: var(--green); color:#fff;
    font-size:0.68rem; font-weight:700;
    padding: 4px 10px; border-radius:20px;
}

/* === BULLE UTILISATEUR (vert foncé) === */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg,#00A651,#007d3c) !important;
    border: none !important;
    border-radius: 18px 18px 4px 18px !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) *,
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) p,
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) span {
    color: #ffffff !important;
}

/* === BULLE ASSISTANT (vert clair, texte NOIR) === */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: var(--bot-bubble) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 18px 18px 18px 4px !important;
    box-shadow: 0 2px 8px rgba(0,166,81,0.10);
}
/* Force le texte du bot en noir – règle la plus haute priorité possible */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) *,
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) p,
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) li,
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) span,
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) strong,
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) em,
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) code {
    color: #0d1b2a !important;
}

/* === BOUTONS CHIPS (vert-blanc) === */
.stButton > button {
    background: #ffffff !important;
    color: #007d3c !important;
    border: 1.5px solid #00A651 !important;
    border-radius: 20px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    transition: all 0.15s ease !important;
    padding: 6px 14px !important;
}
.stButton > button:hover,
.stButton > button:focus {
    background: #00A651 !important;
    color: #ffffff !important;
    border-color: #007d3c !important;
}
.stButton > button:active {
    background: #007d3c !important;
    color: #ffffff !important;
}

/* === BOUTON LANGUE (sidebar) === */
div[data-testid="stSidebar"] .lang-wrap .stButton > button {
    background: rgba(255,255,255,0.07) !important;
    color: #c8e0d0 !important;
    border: 1.5px solid rgba(255,255,255,0.18) !important;
    border-radius: 10px !important;
}
div[data-testid="stSidebar"] .lang-wrap .stButton > button:hover {
    background: #00A651 !important;
    color: #fff !important;
}

/* === BOUTON VIDER (rouge) === */
div[data-testid="stSidebar"] .danger-wrap .stButton > button {
    background: rgba(200,30,30,0.08) !important;
    color: #c0392b !important;
    border: 1.5px solid rgba(200,30,30,0.30) !important;
    border-radius: 10px !important;
}
div[data-testid="stSidebar"] .danger-wrap .stButton > button:hover {
    background: #c0392b !important;
    color: #fff !important;
}

/* === BOUTON EXPORT === */
div[data-testid="stSidebar"] .export-wrap .stDownloadButton > button,
div[data-testid="stSidebar"] .export-wrap .stButton > button {
    background: rgba(0,166,81,0.10) !important;
    color: #007d3c !important;
    border: 1.5px solid #00A651 !important;
    border-radius: 10px !important;
}

/* === SIDEBAR FOND === */
section[data-testid="stSidebar"] {
    background: var(--navy) !important;
    border-right: 1px solid rgba(0,166,81,0.12) !important;
}
/* Texte sidebar */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] li,
section[data-testid="stSidebar"] label {
    color: #c8e0d0 !important;
}

/* === BOUTON NATIF SIDEBAR (le < > de Streamlit) rendu visible en vert === */
[data-testid="collapsedControl"] {
    background: var(--green) !important;
    border-radius: 0 10px 10px 0 !important;
    width: 28px !important;
    opacity: 1 !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
}
[data-testid="collapsedControl"]:hover {
    background: var(--green-dk) !important;
}
[data-testid="collapsedControl"] svg {
    fill: #ffffff !important;
    stroke: #ffffff !important;
}

/* === ZONE DE SAISIE === */
[data-testid="stChatInputContainer"] {
    background: #ffffff !important;
    border: 2px solid var(--border) !important;
    border-radius: 16px !important;
}
[data-testid="stChatInputContainer"]:focus-within {
    border-color: var(--green) !important;
    box-shadow: 0 0 0 3px rgba(0,166,81,0.10) !important;
}
/* texte dans la zone de saisie */
[data-testid="stChatInputContainer"] textarea {
    color: #0d1b2a !important;
}

/* === EXPANDER SOURCES === */
.streamlit-expanderHeader {
    background: var(--green-bg) !important;
    border-radius: 10px !important;
    color: var(--green-dk) !important;
    font-size: 0.83rem !important;
    font-weight: 600 !important;
    border: 1px solid var(--border) !important;
}
.source-chip {
    display: inline-block;
    background: #fff;
    border: 1px solid var(--border);
    color: var(--green-dk);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.80rem;
    margin: 3px 3px 3px 0;
    font-weight: 500;
}

/* === BANNIÈRE BIENVENUE === */
.info-banner {
    background: var(--green-bg);
    border-left: 4px solid var(--green);
    border-radius: 0 12px 12px 0;
    padding: 10px 14px;
    font-size: 0.86rem;
    color: var(--green-dk);
    margin-bottom: 14px;
}

/* === COMPOSANTS SIDEBAR === */
.sb-logo { text-align:center; padding:6px 0 12px; border-bottom:1px solid rgba(255,255,255,0.07); margin-bottom:10px; }
.sb-logo .ico { font-size:1.7rem; }
.sb-logo h2  { margin:4px 0 0; font-size:.95rem; font-weight:700; color:#fff !important; }
.sb-logo p   { font-size:.73rem; color:#8cb8a0 !important; margin:0; }
.sb-title    { font-size:.67rem; letter-spacing:1.3px; text-transform:uppercase; color:#00A651 !important; font-weight:700; margin:13px 0 6px; }
.stat-row    { display:flex; gap:8px; margin:8px 0; }
.stat-card   { background:rgba(0,166,81,0.12); border:1px solid rgba(0,166,81,0.22); border-radius:10px; padding:8px; flex:1; text-align:center; }
.stat-card .v { font-size:1.15rem; font-weight:700; color:#00A651 !important; }
.stat-card .l { font-size:.66rem; color:#8cb8a0 !important; }
.at-hr       { border:none; border-top:1px solid rgba(255,255,255,0.07); margin:11px 0; }

/* === FOOTER === */
.at-footer { text-align:center; color:#5a7a6a; font-size:.76rem; padding:12px 0 5px; border-top:1px solid var(--border); margin-top:12px; }
.at-footer span { color:var(--green); font-weight:600; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "messages"   not in st.session_state: st.session_state.messages   = []
if "lang"       not in st.session_state: st.session_state.lang       = "fr"
if "show_chips" not in st.session_state: st.session_state.show_chips = True
if "pending_q"  not in st.session_state: st.session_state.pending_q  = None

# ─────────────────────────────────────────────
# LOCALISATION
# ─────────────────────────────────────────────
LABELS = {
    "fr": {
        "subtitle":    "Assistant intelligent RAG • Algérie Télécom",
        "badge":       "EN LIGNE",
        "welcome":     "Bonjour ! Posez votre question sur les pannes, la fibre, le paiement ou tout autre service Algérie Télécom.",
        "placeholder": "Posez votre question ici…",
        "chips_title": "💡 Questions fréquentes — cliquez pour envoyer",
        "sources_lbl": "📎 Sources utilisées",
        "clear_btn":   "🗑️ Vider la conversation",
        "export_btn":  "⬇️ Exporter le chat",
        "lang_btn":    "🌐 عربية",
        "spinner":     "Recherche en cours…",
        "error":       "Erreur : ",
        "msg_lbl":     "messages",
        "chips": [
            "Panne internet",
            "Internet lent",
            "Payer ma facture",
            "Problème fibre",
            "Pas de tonalité",
            "Coupures répétitives",
            "Couverture 4G LTE",
            "Intranet / VPN",
            "Upload faible",
            "Ping élevé",
        ],
    },
    "ar": {
        "subtitle":    "مساعد ذكي RAG • اتصالات الجزائر",
        "badge":       "متصل",
        "welcome":     "مرحباً! اطرح سؤالك حول الأعطال أو الألياف البصرية أو الدفع أو أي خدمة.",
        "placeholder": "اكتب سؤالك هنا…",
        "chips_title": "💡 الأسئلة الشائعة — انقر للإرسال",
        "sources_lbl": "📎 المصادر المستخدمة",
        "clear_btn":   "🗑️ مسح المحادثة",
        "export_btn":  "⬇️ تصدير المحادثة",
        "lang_btn":    "🌐 Français",
        "spinner":     "جارٍ البحث…",
        "error":       "خطأ: ",
        "msg_lbl":     "رسائل",
        "chips": [
            "انقطاع الإنترنت",
            "إنترنت بطيء",
            "دفع الفاتورة",
            "مشكلة الألياف",
            "لا صوت على الخط",
            "انقطاعات متكررة",
            "تغطية 4G LTE",
            "الإنترانت / VPN",
            "رفع بطيء",
            "تأخر عالٍ (Ping)",
        ],
    },
}

L = LABELS[st.session_state.lang]

# ─────────────────────────────────────────────
# EN-TÊTE
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="at-header">
    <div class="at-logo">📡</div>
    <div>
        <h1>Chatbot Algérie Télécom</h1>
        <p>{L['subtitle']}</p>
    </div>
    <div class="at-badge">● {L['badge']}</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
        <div class="ico">📡</div>
        <h2>Algérie Télécom</h2>
        <p>Assistant RAG intelligent</p>
    </div>
    """, unsafe_allow_html=True)

    n_msgs = len(st.session_state.messages)
    n_user = sum(1 for m in st.session_state.messages if m["role"] == "user")
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card"><div class="v">{n_msgs}</div><div class="l">{L['msg_lbl']}</div></div>
        <div class="stat-card"><div class="v">{n_user}</div><div class="l">questions</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="at-hr">', unsafe_allow_html=True)
    st.markdown('<div class="sb-title">🌐 Langue / اللغة</div>', unsafe_allow_html=True)

    st.markdown('<div class="lang-wrap">', unsafe_allow_html=True)
    if st.button(L["lang_btn"], use_container_width=True, key="btn_lang"):
        st.session_state.lang = "ar" if st.session_state.lang == "fr" else "fr"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-title">📋 Actions</div>', unsafe_allow_html=True)

    st.markdown('<div class="export-wrap">', unsafe_allow_html=True)
    if st.session_state.messages:
        chat_text = "\n\n".join(
            f"[{m['role'].upper()}]\n{m['content']}"
            for m in st.session_state.messages
        )
        st.download_button(
            label=L["export_btn"],
            data=chat_text.encode("utf-8"),
            file_name="at_chat_export.txt",
            mime="text/plain",
            use_container_width=True,
            key="btn_export",
        )
    else:
        st.button(L["export_btn"], disabled=True, use_container_width=True, key="btn_export_dis")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="danger-wrap">', unsafe_allow_html=True)
    if st.button(L["clear_btn"], use_container_width=True, key="btn_clear"):
        st.session_state.messages   = []
        st.session_state.pending_q  = None
        st.session_state.show_chips = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="at-hr">', unsafe_allow_html=True)
    st.markdown('<div class="sb-title">💡 Questions fréquentes</div>', unsafe_allow_html=True)
    for chip in L["chips"]:
        st.markdown(f"• {chip}")
    st.markdown('<hr class="at-hr">', unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:.7rem;text-align:center;color:#5a8a6a !important;">Powered by RAG · Algérie Télécom © 2025</p>',
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
# BANNIÈRE BIENVENUE
# ─────────────────────────────────────────────
if not st.session_state.messages and not st.session_state.pending_q:
    st.markdown(f'<div class="info-banner">💬 {L["welcome"]}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CHIPS CLIQUABLES
# Chaque bouton stocke le texte dans pending_q, puis on rerun.
# La question est traitée APRÈS, en bas du script.
# ─────────────────────────────────────────────
if st.session_state.show_chips and not st.session_state.pending_q:
    st.markdown(f"**{L['chips_title']}**")
    cols = st.columns(5)
    for idx, chip in enumerate(L["chips"]):
        with cols[idx % 5]:
            if st.button(chip, key=f"chip_{idx}", use_container_width=True):
                st.session_state.pending_q  = chip
                st.session_state.show_chips = False
                st.rerun()
    st.markdown("---")

# ─────────────────────────────────────────────
# HISTORIQUE
# ─────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander(L["sources_lbl"]):
                seen, html = set(), ""
                for src in msg["sources"]:
                    t = (src.get("title") or "Source sans titre").strip()
                    if t not in seen:
                        seen.add(t)
                        html += f'<span class="source-chip">📄 {t}</span>'
                st.markdown(html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SAISIE MANUELLE
# ─────────────────────────────────────────────
typed = st.chat_input(L["placeholder"])

# Priorité : chip cliqué > texte tapé
question = st.session_state.pending_q or typed
if st.session_state.pending_q:
    st.session_state.pending_q = None   # consommé

# ─────────────────────────────────────────────
# TRAITEMENT DE LA QUESTION
# ─────────────────────────────────────────────
if question:
    st.session_state.show_chips = False

    # Afficher la question de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Appel au backend + affichage de la réponse
    with st.chat_message("assistant"):
        with st.spinner(L["spinner"]):
            try:
                answer, results, context = ask(question)
            except Exception as e:
                answer  = f"{L['error']}{e}"
                results = []
                context = ""

        st.markdown(answer)

        if results:
            with st.expander(L["sources_lbl"]):
                seen, html = set(), ""
                for src in results:
                    t = (src.get("title") or "Source sans titre").strip()
                    if t not in seen:
                        seen.add(t)
                        html += f'<span class="source-chip">📄 {t}</span>'
                st.markdown(html, unsafe_allow_html=True)

    st.session_state.messages.append({
        "role":    "assistant",
        "content": answer,
        "sources": results,
        "context": context,
    })

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown(
    '<div class="at-footer"><span>Algérie Télécom</span> Assistant Intelligent · Tous droits réservés 2025</div>',
    unsafe_allow_html=True,
)