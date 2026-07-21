import requests
import unicodedata
from app.rag.retriever import retrieve, build_context

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "phi3"


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text


import random

def get_smalltalk_response(question: str):
    q = normalize_text(question)

    
    greetings = {
        "bonjour", "salut", "bonsoir", "hello", "salam", "cc", "coucou",
        "hey", "hi", "bjr", "bsr", "slt", "salam alikom", "wa alikom salam",
        "ahlan", "marhba", "good morning", "good evening", "yo", "wesh",
        "bonjour bonjour", "salut salut", "coucou coucou", "allo", "allô"
    }

    thanks = {
        "merci", "merci beaucoup", "thanks", "non merci", "merci bien",
        "je vous remercie", "je te remercie", "thank you", "thx", "mrc",
        "merci infiniment", "merci pour votre aide", "merci pour l aide",
        "c est tres utile", "tres utile", "utile", "ca m a aide",
        "vous m avez aide", "parfait merci", "super merci", "ok merci",
        "d accord merci", "nickel merci", "impeccable merci"
    }

    goodbye = {
        "au revoir", "bye", "a bientot", "bonne nuit", "non au revoir",
        "bonne journee", "bonne soiree", "bonne fin de journee",
        "a plus", "a plus tard", "a tout a l heure", "a toute",
        "ciao", "tchao", "bye bye", "goodbye", "on se revoit",
        "je vous dis au revoir", "je pars", "je dois y aller",
        "merci au revoir", "ok au revoir", "c est bon au revoir"
    }

    how_are_you = {
        "ca va", "comment ca va", "comment vous allez", "comment tu vas",
        "ca va ?", "cv", "tu vas bien", "vous allez bien",
        "comment allez vous", "quoi de neuf", "la forme", "t es en forme",
        "ca roule", "comment vas tu", "tout va bien"
    }

    who_are_you = {
        "qui es tu", "qui etes vous", "tu es qui", "vous etes qui",
        "c est quoi ce chatbot", "c est quoi ce bot", "tu es un robot",
        "tu es une ia", "vous etes une ia", "t es un humain",
        "tu es humain", "tu es une machine", "presentez vous",
        "presente toi", "dis moi qui tu es", "c est quoi ce service",
        "comment tu t appelles", "comment vous appelez vous",
        "quel est ton nom", "ton nom"
    }

    what_can_you_do = {
        "que peux tu faire", "tu peux faire quoi", "vous pouvez faire quoi",
        "aide moi", "aide", "help", "comment tu peux m aider",
        "comment vous pouvez m aider", "c est quoi tes fonctionnalites",
        "a quoi tu sers", "a quoi vous servez", "tu sers a quoi",
        "tu peux m aider", "vous pouvez m aider", "je ne sais pas quoi demander",
        "par ou commencer", "que faire", "explique toi", "explique vous"
    }

    yes = {
        "oui", "oui merci", "yes", "ouais", "yep", "bien sur",
        "exactement", "tout a fait", "effectivement", "affirmatif",
        "ok", "d accord", "c est ca", "voila", "correct", "juste"
    }

    no = {
        "non", "no", "nope", "pas vraiment", "pas du tout",
        "absolument pas", "nenni", "nan"
    }

    insults = {
        "idiot", "nul", "inutile", "stupide", "bete", "mauvais",
        "horrible", "catastrophique", "deplorable", "zero", "naze"
    }

    compliments = {
        "bravo", "excellent", "super", "genial", "top", "bien",
        "parfait", "impressionnant", "incroyable", "magnifique",
        "bien joue", "chapeau", "tres bien"
    }

  
    greetings_responses = [
        "Bonjour 👋 Je suis l'assistant Algérie Télécom. Comment puis-je vous aider ?",
        "Salut 😊 Bienvenue chez Algérie Télécom ! Quelle est votre question ?",
        "Bonjour ! Ravi de vous retrouver 👋 En quoi puis-je vous être utile ?",
        "Bonsoir 🌙 Je suis là pour vous aider. Que puis-je faire pour vous ?",
        "Bonjour ! Comment puis-je vous assister aujourd'hui ? 😊",
    ]

    thanks_responses = [
        "Avec plaisir 😊 Avez-vous une autre question ?",
        "Je suis là pour ça ! N'hésitez pas si vous avez d'autres questions 👍",
        "Ravi d'avoir pu vous aider 😊 Y a-t-il autre chose ?",
        "C'est avec plaisir ! N'hésitez pas à revenir si besoin 🙏",
        "Merci à vous ! Une autre question peut-être ? 😊",
    ]

    goodbye_responses = [
        "Au revoir 👋 N'hésitez pas à revenir si vous avez besoin d'aide.",
        "Bonne journée ! À bientôt 😊",
        "Au revoir ! Je reste disponible quand vous avez besoin 👋",
        "Bonne continuation ! Revenez quand vous voulez 😊",
        "À bientôt 👋 Algérie Télécom reste à votre service !",
    ]

    how_are_you_responses = [
        "Je suis un assistant, donc toujours en pleine forme ! 😄 Et vous ? En quoi puis-je vous aider ?",
        "Très bien merci ! Prêt à vous aider 💪 Quelle est votre question ?",
        "Opérationnel à 100% ! 😄 Comment puis-je vous aider ?",
        "Toujours disponible pour vous aider ! Quelle est votre demande ? 😊",
    ]

    who_are_you_responses = [
        "Je suis l'assistant virtuel d'Algérie Télécom 🤖 Je suis là pour répondre à vos questions sur les pannes, la fibre, le paiement, et plus encore !",
        "Je suis un chatbot intelligent au service d'Algérie Télécom 💬 Posez-moi vos questions sur internet, le modem, les factures ou les services.",
        "Je suis votre assistant Algérie Télécom 🤖 Je peux vous aider sur les problèmes techniques, les factures, la résiliation, et bien d'autres sujets !",
    ]

    what_can_you_do_responses = [
        "Je peux vous aider sur :\n• 🔧 Pannes internet ou modem\n• 💡 Fibre optique et ADSL\n• 💳 Paiement de factures\n• 📋 Résiliation de contrat\n• 📞 Contacter le support\n\nQue souhaitez-vous savoir ?",
        "Voici ce que je sais faire :\n• Diagnostiquer une panne internet\n• Expliquer comment payer une facture\n• Informer sur les offres et services\n• Guider pour contacter le support\n\nQuelle est votre question ? 😊",
        "Je suis spécialisé dans les services Algérie Télécom ! Posez-moi vos questions sur les pannes, la fibre, le modem, les factures ou la résiliation 💬",
    ]

    yes_responses = [
        "Parfait ! Que puis-je faire pour vous ? 😊",
        "Super ! Posez votre question, je suis là 👍",
        "Très bien ! Comment puis-je vous aider ? 😊",
    ]

    no_responses = [
        "D'accord ! N'hésitez pas à revenir si vous avez besoin 😊",
        "Pas de problème ! Je reste disponible si vous avez une question 👍",
        "Très bien ! À votre disposition si besoin 😊",
    ]

    insults_responses = [
        "Je comprends votre frustration 😔 Je fais de mon mieux pour vous aider. Quelle est votre question ?",
        "Désolé si je n'ai pas pu répondre à vos attentes 🙏 Essayons de nouveau, quelle est votre demande ?",
        "Je suis là pour vous aider du mieux possible 😊 Reformulez votre question et je ferai de mon mieux !",
    ]

    compliments_responses = [
        "Merci beaucoup ! 😊 C'est très gentil. Y a-t-il autre chose que je peux faire pour vous ?",
        "Oh merci ! 🙏 Ravi d'avoir pu vous aider. Une autre question ?",
        "Merci pour ce retour positif 😊 Je reste disponible pour vous !",
    ]

    # ─────────────────────────────────────────
    # LOGIQUE DE CORRESPONDANCE
    # ─────────────────────────────────────────

    if q in greetings:
        return random.choice(greetings_responses)

    if q in thanks:
        return random.choice(thanks_responses)

    if q in goodbye:
        return random.choice(goodbye_responses)

    if q in how_are_you:
        return random.choice(how_are_you_responses)

    if q in who_are_you:
        return random.choice(who_are_you_responses)

    if q in what_can_you_do:
        return random.choice(what_can_you_do_responses)

    if q in yes:
        return random.choice(yes_responses)

    if q in no:
        return random.choice(no_responses)

    if q in insults:
        return random.choice(insults_responses)

    if q in compliments:
        return random.choice(compliments_responses)

    return None


def build_prompt(context: str, question: str) -> str:
    return f"""
Tu es un assistant pour Algérie Télécom.

Règles importantes :
- Utilise uniquement les informations pertinentes du contexte
- Ignore les parties du contexte qui ne correspondent pas à la question
- Si aucune information pertinente n’est trouvée, dis seulement : Je ne sais pas
- Ne jamais inventer
- Réponds en français simple et clair

Contexte :
{context}

Question :
{question}
"""


def call_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 200
        }
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=300)
    response.raise_for_status()

  #On reçoit la réponse du modèle, on la transforme en dictionnaire{cle, valeur}, puis on extrait juste le texte.
    data = response.json()
    return data.get("response", "").strip()


def ask(question: str):
    
    question = question.strip() #strip enleve les espace au debut de "" et  la fin 

    if not question:
        return "Veuillez poser une question.", [], ""

    smalltalk_answer = get_smalltalk_response(question)
    if smalltalk_answer:
        return smalltalk_answer, [], ""

    print("[DEBUG] début ask()")

    results = retrieve(question, top_k=4)
    print("[DEBUG] retrieve OK")

    
    results = [r for r in results if r["score"] > 0.3] #on garde uniquement ceux dont le score depasse 0.3.

    if not results:
        print("[DEBUG] aucun résultat pertinent")
        return "Je n’ai pas trouvé d’information précise pour cette demande. Pouvez-vous reformuler votre question ou ajouter plus de détails ?", [], ""

    context = build_context(results)
    prompt = build_prompt(context, question)

    print("[DEBUG] appel API Ollama...")
    answer = call_ollama(prompt)
    print("[DEBUG] réponse Ollama OK")

    return answer, results, context


if __name__ == "__main__":
    question = input("Pose ta question : ")
    answer, _, _ = ask(question)
    print("\n===== RÉPONSE =====\n")
    print(answer)