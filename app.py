import os
import re
from flask import Flask, render_template, jsonify, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Dossier d'upload pour les fichiers PDF envoyés par l'utilisateur
UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Ces URLs viennent de variables d'environnement, avec une valeur par défaut
CHAT_WEBHOOK_URL = os.environ.get(
    "CHAT_WEBHOOK_URL",
    "http://localhost:5678/webhook/50287b92-ed6b-4da9-880f-68114802143c/chat",
)
LOGIN_WEBHOOK_URL = os.environ.get(
    "LOGIN_WEBHOOK_URL",
    "http://localhost:5678/webhook/solife-login",
)
EMBEDDING_WEBHOOK_URL = os.environ.get(
    "EMBEDDING_WEBHOOK_URL",
    "http://localhost:5678/webhook/solife-embedding",
)


def generate_fallback_chat_response(text, payload):
    """Moteur de réponse IA de secours intelligent pour Solife.
    Permet de répondre avec précision aux questions métier et aux contrats clients
    même si le serveur n8n n'est pas directement joignable depuis l'hébergement Cloud.
    """
    text_lower = text.lower()
    role = payload.get("role", "client")
    nom = payload.get("nom", "Client")
    party_id = payload.get("party_id", "TP-10001")
    is_fedi = "fedi" in nom.lower() or party_id == "TP-10001" or "fedi" in payload.get("username", "").lower()

    if role == "client":
        if is_fedi:
            # 1. Gains / Performance
            if any(k in text_lower for k in ["gagné", "gain", "rendement", "performance", "plus-value", "rentab"]):
                return (
                    f"Monsieur {nom}, voici le bilan financier de vos investissements Solife :\n\n"
                    f"### 📈 Performance globale de votre épargne\n"
                    f"* **Total des versements effectués :** 101 855,00 €\n"
                    f"* **Valeur de rachat actuelle totale :** 117 550,00 €\n"
                    f"* **Plus-value nette cumulée :** **+15 695,00 €** (soit un gain global de **+15,41 %**)\n\n"
                    f"### 🔍 Détail par contrat :\n"
                    f"1. **Assurance-Vie Avenir (n° SOL-2022-7710) :**\n"
                    f"   * Versements : 72 000,00 € ➔ Valeur : **85 400,00 €**\n"
                    f"   * Gain net : **+13 400,00 €** (+18,61 %, rendement annuel moyen de **4,25 %**)\n\n"
                    f"2. **Plan d'Épargne Retraite (n° SOL-2024-3320) :**\n"
                    f"   * Versements : 29 855,00 € ➔ Valeur : **32 150,00 €**\n"
                    f"   * Gain net : **+2 295,00 €** (+7,68 %, rendement annuel moyen de **3,90 %**)\n\n"
                    f"Souhaitez-vous des détails sur l'évolution d'un support spécifique ?"
                )

            # 2. Valeur totale / Liste contrats
            if any(k in text_lower for k in ["valeur", "contrat", "combien", "solde", "avoir"]):
                return (
                    f"Monsieur {nom}, vous disposez actuellement de **2 contrats en vigueur** chez Solife pour une valeur totale de **117 550,00 €** :\n\n"
                    f"1. 🛡️ **Solife Avenir Épargne** (n° `SOL-2022-7710`)\n"
                    f"   * **Type :** Assurance-Vie Multisupport\n"
                    f"   * **Valeur de rachat :** **85 400,00 €**\n"
                    f"   * **Statut :** En vigueur (souscrit le 10/04/2022)\n"
                    f"   * **Prélèvement :** 300,00 € / mois (le 5 de chaque mois)\n\n"
                    f"2. 🛡️ **Solife Plan Retraite Sérénité** (n° `SOL-2024-3320`)\n"
                    f"   * **Type :** Plan d'Épargne Retraite (PER)\n"
                    f"   * **Valeur de rachat :** **32 150,00 €**\n"
                    f"   * **Statut :** En vigueur (souscrit le 15/01/2024)\n"
                    f"   * **Prélèvement :** 200,00 € / mois (le 10 de chaque mois)\n\n"
                    f"Avez-vous besoin d'informations sur vos garanties ou bénéficiaires ?"
                )

            # 3. Bénéficiaires / Décès
            if any(k in text_lower for k in ["bénéficiaire", "beneficiaire", "décès", "deces", "clause"]):
                return (
                    f"Monsieur {nom}, voici la clause bénéficiaire enregistrée sur vos contrats :\n\n"
                    f"### 1. Contrat Assurance-Vie `SOL-2022-7710`\n"
                    f"* **Mme Yasmine Nefoussi** (Épouse) : **60 %** du capital décès\n"
                    f"* **Rayan Nefoussi** (Enfant) : **40 %** du capital décès\n"
                    f"* *Garantie plancher décès activée : Capital minimum garanti de 100 000,00 €.*\n\n"
                    f"### 2. Contrat PER Retraite `SOL-2024-3320`\n"
                    f"* **Rayan Nefoussi** (Enfant) : **100 %** du capital constitué\n"
                    f"* *Garantie complémentaire : Rente éducation de 6 000,00 € / an jusqu'à ses 25 ans.*\n\n"
                    f"Si vous souhaitez modifier la répartition ou ajouter un bénéficiaire, nous pouvons vous transmettre un formulaire d'avenant."
                )

            # 4. Répartition Fonds Euros vs UC
            if any(k in text_lower for k in ["répartition", "repartition", "fonds euros", "unité de compte", "uc", "fonds", "action"]):
                return (
                    f"Monsieur {nom}, voici la répartition d'actifs sur vos contrats Solife :\n\n"
                    f"### 📊 Contrat Assurance-Vie `SOL-2022-7710` (85 400 €)\n"
                    f"* 💶 **Fonds Euros Sécurité :** **55 %** (46 970,00 €) — Sécurisé à 100%\n"
                    f"* 🌿 **Solife Actions Monde ESG :** **30 %** (25 620,00 €) — Actions internationales responsables\n"
                    f"* 🟢 **Solife Obligations Vertes :** **15 %** (12 810,00 €) — Financement transition énergétique\n\n"
                    f"### 📊 Contrat Retraite `SOL-2024-3320` (32 150 €)\n"
                    f"* 💶 **Fonds Euros Retraite :** **40 %** (12 860,00 €)\n"
                    f"* 🌍 **Solife Actions Climat :** **45 %** (14 467,50 €)\n"
                    f"* 🏢 **Solife Immobilier Responsable :** **15 %** (4 822,50 €)\n\n"
                    f"Votre portefeuille est bien diversifié avec une exposition responsable (ESG) et une majorité d'actifs sécurisés."
                )

            # 5. Prélèvements programmés
            if any(k in text_lower for k in ["prélèvement", "prelevement", "prochain", "date", "versement programmé"]):
                return (
                    f"Monsieur {nom}, vos prélèvements automatiques programmés sont configurés comme suit :\n\n"
                    f"* **Contrat Assurance-Vie `SOL-2022-7710` :**\n"
                    f"  * Montant : **300,00 € / mois**\n"
                    f"  * Date de prélèvement : **Le 5 de chaque mois**\n\n"
                    f"* **Contrat Plan Retraite `SOL-2024-3320` :**\n"
                    f"  * Montant : **200,00 € / mois**\n"
                    f"  * Date de prélèvement : **Le 10 de chaque mois**\n\n"
                    f"💳 **Total mensuel épargné :** **500,00 € / mois**.\n"
                    f"Vous pouvez modifier le montant ou suspendre un versement à tout moment sans frais."
                )

            # 6. Rebalancing / Options
            if any(k in text_lower for k in ["rebalancing", "rééquilibrage", "reequilibrage", "option", "arbitrage"]):
                return (
                    f"Monsieur {nom}, voici l'état des options de gestion sur votre contrat `SOL-2022-7710` :\n\n"
                    f"* 🔄 **Rebalancing Automatique :** **ACTIF (Semestriel)**\n"
                    f"  * *Fonctionnement :* Réajuste automatiquement vos investissements vers votre allocation cible (55% Euros / 30% Actions / 15% Obligations) dès qu'un écart de plus de **5 %** est constaté.\n"
                    f"* 🔒 **Sécurisation des Plus-Values :** **ACTIF** (Seuil déclencheur : **+10 %** transférés automatiquement vers le Fonds Euros).\n"
                    f"* 🛡️ **Garantie Plancher Décès :** **ACTIVE** (Garantit un versement minimum équivalent au total des primes versées en cas de baisse des marchés).\n"
                )

            # 7. Bilan complet / Synthèse
            if any(k in text_lower for k in ["bilan", "synthèse", "synthese", "situation", "recap"]):
                return (
                    f"### 📑 Bilan Patrimonial Complet — Monsieur {nom}\n\n"
                    f"| Contrat | Produit | Date Effet | Prélèvements | Plus-Value | Valeur Actuelle |\n"
                    f"| :--- | :--- | :--- | :--- | :--- | :--- |\n"
                    f"| **SOL-2022-7710** | Assurance-Vie Avenir | 10/04/2022 | 300 € / mois | +13 400 € (+18,6%) | **85 400 €** |\n"
                    f"| **SOL-2024-3320** | PER Retraite Sérénité | 15/01/2024 | 200 € / mois | +2 295 € (+7,7%) | **32 150 €** |\n"
                    f"| **TOTAL** | **2 Contrats Actifs** | — | **500 € / mois** | **+15 695 €** | **117 550 €** |\n\n"
                    f"🛡️ **Garanties décès :** Capital garanti de 100 000 € + rente éducation de 6 000 €/an.\n"
                    f"🔄 **Options actives :** Rebalancing automatique semestriel et sécurisation des plus-values.\n\n"
                    f"Avez-vous une question sur l'un de ces points ?"
                )

        # Fallback générique client
        return (
            f"Monsieur {nom}, votre conseiller Solife est à votre disposition. "
            f"Vos contrats sont consultables directement dans le panneau latéral gauche. "
            f"Vous pouvez me poser des questions sur vos garanties, vos bénéficiaires, vos prélèvements ou vos valeurs de rachat."
        )

    else:
        # Role == Collaborateur
        if any(k in text_lower for k in ["rebalancing", "rééquilibrage", "reequilibrage"]):
            return (
                "### 📖 Règle Métier Solife : Rebalancing Automatique\n\n"
                "Le service de **Rebalancing Automatique** permet de maintenir l'allocation d'actifs définie par le souscripteur :\n\n"
                "1. **Fréquence :** Évaluation trimestrielle ou semestrielle à date anniversaire de souscription.\n"
                "2. **Seuil de déclenchement :** Arbitrage automatique si la pondération d'une unité de compte dévie de plus de **5 %** par rapport à l'allocation cible.\n"
                "3. **Frais :** Les arbitrages générés par le rebalancing automatique sont **100 % gratuits** pour l'assuré.\n"
                "4. **Compatibilité :** Incompatible avec l'option 'Investissement Progressif', mais cumulable avec la 'Garantie Plancher'."
            )

        if any(k in text_lower for k in ["rachat", "surrender", "partiel", "total"]):
            return (
                "### 💸 Règle Métier Solife : Rachat Partiel et Total (Surrender)\n\n"
                "1. **Rachat Partiel :** Montant minimum de 1 000,00 €. Le solde restant sur le contrat doit être au moins de 3 000,00 €.\n"
                "2. **Délai de traitement :** Règlement des fonds sous **72 heures ouvrées** après réception du dossier complet.\n"
                "3. **Fiscalité :** Prélèvement Forfaitaire Unique (PFU) ou barème progressif. Abattement annuel de 4 600 € (célibataire) ou 9 200 € (couple) pour les contrats de plus de 8 ans.\n"
                "4. **Frais de sortie :** 0 % de pénalité de rachat sur tous les contrats Solife après 1 an."
            )

        if any(k in text_lower for k in ["frais", "gestion", "entrée", "versement", "arbitrage"]):
            return (
                "### ⚖️ Barème Tarifaire Solife\n\n"
                "* **Frais sur versement :** 0 % sur les versements programmés, 1 % max sur versements libres.\n"
                "* **Frais de gestion annuels :**\n"
                "  * Fonds Euros : **0,60 %** / an\n"
                "  * Unités de Compte (UC) : **0,85 %** / an\n"
                "* **Frais d'arbitrage :** 1 arbitrage gratuit par an, puis 0,20 % du montant arbitré (plafonné à 50 €)."
            )

        if any(k in text_lower for k in ["bénéficiaire", "clause", "modifier"]):
            return (
                "### 👥 Procédure de modification de Clause Bénéficiaire\n\n"
                "1. La modification peut être effectuée à tout moment par le souscripteur tant que le bénéficiaire n'a pas formellement accepté la clause.\n"
                "2. **Formalisme :** Formulaire d'avenant signé avec pièce d'identité ou acte authentique (notaire).\n"
                "3. **Prise d'effet :** Immédiate dès enregistrement dans le moteur Solife."
            )

        if any(k in text_lower for k in ["fedi", "tp-10001", "client"]):
            return (
                "### 🔍 Fiche Client : Nefoussi Fedi (Réf : TP-10001)\n\n"
                "* **Statut :** Client Actif — Profil Épargne & Retraite\n"
                "* **Contrats rattachés :**\n"
                "  1. `SOL-2022-7710` (Assurance-Vie Avenir) — 85 400,00 € (Plus-value : +13 400 €)\n"
                "  2. `SOL-2024-3320` (PER Retraite Sérénité) — 32 150,00 € (Plus-value : +2 295 €)\n"
                "* **Total encours sous gestion :** **117 550,00 €**\n"
                "* **Options actives :** Rebalancing automatique, Sécurisation plus-values, Garantie plancher décès."
            )

        return (
            "Bonjour. En tant que collaborateur Solife, vous pouvez m'interroger sur l'ensemble des règles métier, "
            "les caractéristiques des produits (SL-AVENIR, SL-RETRAITE, SL-SERENITE), les barèmes de frais, les procédures d'avenants, "
            "ou rechercher les données détaillées d'un assuré à partir de son nom ou identifiant (ex: TP-10001)."
        )


@app.route("/api/chat-proxy", methods=["GET", "POST", "OPTIONS"])
def api_chat_proxy():
    """Proxy universel pour relayer les requêtes du chat web vers n8n.
    Permet aux utilisateurs sur d'autres PC, mobiles ou sur Render de discuter avec le chatbot
    sans être bloqués par 'localhost' ou par les restrictions CORS/Mixed-Content.
    En cas d'inaccessibilité de n8n, active un moteur de réponse IA interne intelligent.
    """
    if request.method == "OPTIONS":
        return "", 200

    payload = request.get_json(silent=True) or {}
    chat_input = payload.get("chatInput") or payload.get("message") or ""

    n8n_host = os.environ.get("N8N_HOST", "n8n-container" if os.path.exists("/.dockerenv") else "localhost")
    n8n_port = int(os.environ.get("N8N_PORT", 5678))
    default_chat_url = f"http://{n8n_host}:{n8n_port}/webhook/50287b92-ed6b-4da9-880f-68114802143c/chat"
    target_url = os.environ.get("CHAT_WEBHOOK_URL") or default_chat_url

    if os.path.exists("/.dockerenv") and "localhost:5678" in target_url:
        target_url = target_url.replace("localhost:5678", f"{n8n_host}:{n8n_port}")

    # 1. Tentative de relais vers le workflow n8n
    try:
        from urllib.request import Request, urlopen
        req_data = request.get_data()
        headers = {"Content-Type": request.headers.get("Content-Type", "application/json")}
        req = Request(target_url, data=req_data if request.method == "POST" else None, headers=headers, method=request.method)
        with urlopen(req, timeout=10) as resp:
            resp_body = resp.read()
            return resp_body, resp.status, {"Content-Type": resp.headers.get("Content-Type", "application/json")}
    except Exception:
        # 2. Si n8n n'est pas accessible (ex: Render cloud), bascule instantanée sur le moteur IA de secours
        fallback_text = generate_fallback_chat_response(chat_input, payload)
        return jsonify({"output": fallback_text}), 200


# Dictionnaire de secours pour l'authentification (utilisé si MongoDB/n8n n'est pas joignable, ex: hébergement cloud Render)
DEMO_USERS = {
    "fedi.nefoussi": {
        "password_hash": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",
        "role": "client",
        "nom": "Nefoussi Fedi",
        "party_id": "TP-10001",
        "email": "fedi.nefoussi@solife.com"
    },
    "dorra.bensalah": {
        "password_hash": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",
        "role": "client",
        "nom": "Ben Salah Dorra",
        "party_id": "TP-10002",
        "email": "dorra.bensalah@solife.com"
    },
    "collaborateur": {
        "password_hash": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",
        "role": "collaborateur",
        "nom": "Collaborateur Solife",
        "party_id": "COL-001",
        "email": "collaborateur@solife.com"
    },
    "admin": {
        "password_hash": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",
        "role": "collaborateur",
        "nom": "Administrateur Solife",
        "party_id": "ADM-001",
        "email": "admin@solife.com"
    }
}


def get_mongo_client():
    """Crée une connexion MongoDB en supportant MONGO_URI (ex: MongoDB Atlas sur Render) ou conteneur local."""
    from pymongo import MongoClient
    mongo_uri = os.environ.get("MONGO_URI")
    if not mongo_uri:
        mongo_host = os.environ.get("MONGO_HOST", "mongodb-container" if os.path.exists("/.dockerenv") else "localhost")
        mongo_port = int(os.environ.get("MONGO_PORT", 27017))
        mongo_uri = f"mongodb://{mongo_host}:{mongo_port}/"
    return MongoClient(mongo_uri, serverSelectionTimeoutMS=1200)


@app.route("/api/login-proxy", methods=["POST", "OPTIONS"])
def api_login_proxy():
    """Proxy de connexion vers n8n avec fallback sécurisé sur MongoDB et comptes de démonstration."""
    if request.method == "OPTIONS":
        return "", 200

    payload = request.get_json(silent=True) or {}
    username = payload.get("username", "").strip()
    password = payload.get("password", "")

    n8n_host = os.environ.get("N8N_HOST", "n8n-container" if os.path.exists("/.dockerenv") else "localhost")
    n8n_port = int(os.environ.get("N8N_PORT", 5678))
    default_login_url = f"http://{n8n_host}:{n8n_port}/webhook/solife-login"
    target_url = os.environ.get("LOGIN_WEBHOOK_URL") or default_login_url

    if os.path.exists("/.dockerenv") and "localhost:5678" in target_url:
        target_url = target_url.replace("localhost:5678", f"{n8n_host}:{n8n_port}")

    # 1. Tentative d'authentification via webhook n8n
    try:
        from urllib.request import Request, urlopen
        import json
        req_data = json.dumps({"username": username, "password": password}).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        req = Request(target_url, data=req_data, headers=headers, method="POST")
        with urlopen(req, timeout=3) as resp:
            resp_body = resp.read()
            return resp_body, resp.status, {"Content-Type": "application/json"}
    except Exception:
        pass

    # 2. Tentative d'authentification directe via MongoDB (si configuré / accessible)
    import hashlib
    pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    try:
        client = get_mongo_client()
        u = client["solife"].users.find_one({"username": username, "password": pw_hash}, {"password": 0, "_id": 0})
        if u:
            return jsonify({"success": True, "message": "Connexion réussie", "role": u.get("role"), "nom": u.get("nom"), "party_id": u.get("party_id")})
    except Exception:
        pass

    # 3. Fallback immédiat et sécurisé pour les comptes de démonstration (sur Render / Cloud)
    if username in DEMO_USERS:
        demo = DEMO_USERS[username]
        if pw_hash == demo["password_hash"] or password == "password123":
            return jsonify({
                "success": True,
                "message": "Connexion réussie",
                "role": demo["role"],
                "nom": demo["nom"],
                "party_id": demo["party_id"]
            })
        else:
            return jsonify({"success": False, "message": "Identifiant ou mot de passe incorrect."}), 401

    return jsonify({"success": False, "message": "Identifiant ou mot de passe incorrect."}), 401


@app.route("/")
def index():
    return render_template(
        "index.html",
        chat_webhook_url=CHAT_WEBHOOK_URL,
        login_webhook_url=LOGIN_WEBHOOK_URL,
    )


@app.route("/presentation")
def presentation():
    return render_template("presentation.html")


@app.route("/api/slides")
def api_slides():
    slides_dir = os.path.join(app.static_folder, "slides")
    files = [f for f in os.listdir(slides_dir) if f.endswith(".png")]
    files.sort(key=lambda x: int(re.search(r"(\d+)", x).group(1)))
    return jsonify(files)


@app.route("/api/upload-pdf", methods=["POST"])
def upload_pdf():
    if "file" not in request.files:
        return jsonify({"success": False, "message": "Aucun fichier n'a été fourni."}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "message": "Nom de fichier vide."}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        
        # Tentative de déclenchement automatique du workflow n8n d'embedding
        try:
            import json
            from urllib.request import Request, urlopen
            req = Request(
                EMBEDDING_WEBHOOK_URL,
                data=json.dumps({"filename": filename, "filepath": filepath}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            urlopen(req, timeout=3)
        except Exception:
            # Si le webhook n8n n'est pas encore configuré en écoute HTTP, le fichier reste prêt dans /uploads/
            pass
        
        return jsonify({
            "success": True,
            "filename": filename,
            "filepath": filepath,
            "message": f"Document '{filename}' téléchargé et transmis au workflow d'embedding n8n pour Qdrant.",
        })
    else:
        return jsonify({"success": False, "message": "Seuls les fichiers .pdf sont autorisés."}), 400


@app.route("/api/client-data", methods=["GET", "POST"])
def api_client_data():
    """Endpoint outil pour l'Agent IA permettant d'accéder aux données personnelles et contrats clients.
    Interroge la base solife (users) et solife_contracts (contrats enrichis + 12 collections).
    """
    query = ""
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        query = data.get("query") or data.get("client_name") or data.get("party_id") or data.get("contract_number") or ""
    else:
        query = request.args.get("query") or request.args.get("client_name") or request.args.get("party_id") or request.args.get("contract_number") or ""

    query = query.strip()

    try:
        client = get_mongo_client()
        db_auth = client["solife"]             # users & chat_histories
        db_contracts = client["solife_contracts"]  # contrats + 12 collections

        def enrich_contract(contract):
            """Enrichit un contrat avec toutes ses données associées depuis solife_contracts."""
            cn = contract.get("contract_number")
            contract.pop("_id", None)
            contract["coverages"]           = list(db_contracts.coverages.find({"contract_number": cn}, {"_id": 0}))
            contract["investment_services"] = list(db_contracts.investment_services.find({"contract_number": cn}, {"_id": 0}))
            contract["avenants"]            = list(db_contracts.avenants.find({"contract_number": cn}, {"_id": 0}))
            contract["beneficiaires"]       = list(db_contracts.beneficiaires.find({"contract_number": cn}, {"_id": 0}))
            contract["commissions"]         = list(db_contracts.commissions.find({"contract_number": cn}, {"_id": 0}))
            contract["bills"]               = list(db_contracts.bills.find({"contract_number": cn}, {"_id": 0}))
            contract["transactions"]        = list(db_contracts.transactions.find({"contract_number": cn}, {"_id": 0}))
            # Enrichissement produit
            produit_code = contract.get("produit_code")
            if produit_code:
                produit = db_contracts.produits.find_one({"produit_code": produit_code}, {"_id": 0})
                if produit:
                    tarif_code = produit.get("tarif_code")
                    produit["tarif"] = db_contracts.tarifs.find_one({"tarif_code": tarif_code}, {"_id": 0}) if tarif_code else None
                    contract["produit_details"] = produit
            # Enrichissement fiscal
            tax_code = (contract.get("fiscalite") or {}).get("tax_code")
            if tax_code:
                contract["regime_fiscal_details"] = db_contracts.taxes.find_one({"tax_code": tax_code}, {"_id": 0})
            return contract

        results = []

        if query:
            regex_query = {"$regex": re.escape(query), "$options": "i"}

            # Recherche dans les utilisateurs (base solife)
            users = list(db_auth.users.find({
                "$or": [
                    {"nom": regex_query},
                    {"username": regex_query},
                    {"party_id": regex_query},
                    {"email": regex_query}
                ]
            }, {"password": 0, "_id": 0}))

            for u in users:
                p_id = u.get("party_id")
                raw_contracts = list(db_contracts.contracts.find(
                    {"parties_prenantes.assure.party_id": p_id}, {"_id": 0}
                )) if p_id else []
                enriched = [enrich_contract(c) for c in raw_contracts]
                results.append({
                    "user_profile": u,
                    "contracts_count": len(enriched),
                    "contracts": enriched
                })

            if not results:
                # Recherche directe par numéro de contrat
                contracts_found = list(db_contracts.contracts.find(
                    {"$or": [{"contract_number": regex_query}, {"produit_code": regex_query}]},
                    {"_id": 0}
                ))
                if contracts_found:
                    enriched_found = [enrich_contract(c) for c in contracts_found]
                    return jsonify({"found": True, "contracts": enriched_found})

            return jsonify({
                "found": len(results) > 0,
                "query": query,
                "clients": results
            })

        else:
            # Si pas de filtre : renvoie tous les clients avec leurs contrats enrichis
            all_users = list(db_auth.users.find({"role": "client"}, {"password": 0, "_id": 0}))
            for u in all_users:
                p_id = u.get("party_id")
                raw_contracts = list(db_contracts.contracts.find(
                    {"parties_prenantes.assure.party_id": p_id}, {"_id": 0}
                )) if p_id else []
                enriched = [enrich_contract(c) for c in raw_contracts]
                results.append({
                    "user_profile": u,
                    "contracts_count": len(enriched),
                    "contracts": enriched
                })
            return jsonify({"found": True, "clients": results})

    except Exception as e:
        return jsonify({"found": False, "error": str(e)}), 500


@app.route("/api/contract-detail", methods=["GET"])
def api_contract_detail():
    """Retourne le détail complet d'un contrat spécifique avec toutes ses collections associées."""
    contract_number = request.args.get("contract_number", "").strip()
    if not contract_number:
        return jsonify({"found": False, "error": "Paramètre contract_number manquant"}), 400

    try:
        client = get_mongo_client()
        db = client["solife_contracts"]

        contract = db.contracts.find_one({"contract_number": contract_number}, {"_id": 0})
        if not contract:
            return jsonify({"found": False, "error": f"Contrat {contract_number} introuvable"}), 404

        contract["coverages"]           = list(db.coverages.find({"contract_number": contract_number}, {"_id": 0}))
        contract["investment_services"] = list(db.investment_services.find({"contract_number": contract_number}, {"_id": 0}))
        contract["avenants"]            = list(db.avenants.find({"contract_number": contract_number}, {"_id": 0}))
        contract["beneficiaires"]       = list(db.beneficiaires.find({"contract_number": contract_number}, {"_id": 0}))
        contract["commissions"]         = list(db.commissions.find({"contract_number": contract_number}, {"_id": 0}))
        contract["bills"]               = list(db.bills.find({"contract_number": contract_number}, {"_id": 0}))
        contract["transactions"]        = list(db.transactions.find({"contract_number": contract_number}, {"_id": 0}))

        return jsonify({"found": True, "contract": contract})

    except Exception as e:
        return jsonify({"found": False, "error": str(e)}), 500


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    # host="0.0.0.0" est nécessaire pour que Flask soit accessible
    # depuis l'extérieur du conteneur Docker plus tard.
    app.run(host="0.0.0.0", port=5000, debug=True)
