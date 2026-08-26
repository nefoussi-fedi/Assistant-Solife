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


@app.route("/api/chat-proxy", methods=["GET", "POST", "OPTIONS"])
def api_chat_proxy():
    """Proxy universel pour relayer les requêtes du chat web vers n8n.
    Permet aux utilisateurs sur d'autres PC, mobiles ou sur Render de discuter avec le chatbot
    sans être bloqués par 'localhost' ou par les restrictions CORS/Mixed-Content.
    """
    if request.method == "OPTIONS":
        return "", 200

    n8n_host = os.environ.get("N8N_HOST", "n8n-container" if os.path.exists("/.dockerenv") else "localhost")
    n8n_port = int(os.environ.get("N8N_PORT", 5678))
    default_chat_url = f"http://{n8n_host}:{n8n_port}/webhook/50287b92-ed6b-4da9-880f-68114802143c/chat"
    target_url = os.environ.get("CHAT_WEBHOOK_URL") or default_chat_url

    # Si on tourne dans Docker et que l'URL cible pointe vers localhost, remplacer par le nom de conteneur
    if os.path.exists("/.dockerenv") and "localhost:5678" in target_url:
        target_url = target_url.replace("localhost:5678", f"{n8n_host}:{n8n_port}")

    try:
        from urllib.request import Request, urlopen
        from urllib.error import HTTPError
        req_data = request.get_data()
        headers = {"Content-Type": request.headers.get("Content-Type", "application/json")}
        req = Request(target_url, data=req_data if request.method == "POST" else None, headers=headers, method=request.method)
        with urlopen(req, timeout=45) as resp:
            resp_body = resp.read()
            return resp_body, resp.status, {"Content-Type": resp.headers.get("Content-Type", "application/json")}
    except Exception as e:
        return jsonify({"output": f"Désolé, je rencontre une difficulté de connexion avec le serveur d'intelligence artificielle : {e}"}), 200


@app.route("/api/login-proxy", methods=["POST", "OPTIONS"])
def api_login_proxy():
    """Proxy de connexion vers n8n avec fallback sécurisé sur MongoDB."""
    if request.method == "OPTIONS":
        return "", 200

    n8n_host = os.environ.get("N8N_HOST", "n8n-container" if os.path.exists("/.dockerenv") else "localhost")
    n8n_port = int(os.environ.get("N8N_PORT", 5678))
    default_login_url = f"http://{n8n_host}:{n8n_port}/webhook/solife-login"
    target_url = os.environ.get("LOGIN_WEBHOOK_URL") or default_login_url

    if os.path.exists("/.dockerenv") and "localhost:5678" in target_url:
        target_url = target_url.replace("localhost:5678", f"{n8n_host}:{n8n_port}")

    try:
        from urllib.request import Request, urlopen
        req_data = request.get_data()
        headers = {"Content-Type": "application/json"}
        req = Request(target_url, data=req_data, headers=headers, method="POST")
        with urlopen(req, timeout=5) as resp:
            resp_body = resp.read()
            return resp_body, resp.status, {"Content-Type": "application/json"}
    except Exception:
        # Fallback direct si n8n n'est pas joignable
        try:
            import hashlib
            from pymongo import MongoClient
            payload = request.get_json(silent=True) or {}
            username = payload.get("username", "").strip()
            password = payload.get("password", "")
            pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
            mongo_host = os.environ.get("MONGO_HOST", "mongodb-container" if os.path.exists("/.dockerenv") else "localhost")
            client = MongoClient(f"mongodb://{mongo_host}:27017/", serverSelectionTimeoutMS=1500)
            u = client["solife"].users.find_one({"username": username, "password": pw_hash}, {"password": 0, "_id": 0})
            if u:
                return jsonify({"success": True, "message": "Connexion réussie", "role": u.get("role"), "nom": u.get("nom"), "party_id": u.get("party_id")})
            return jsonify({"success": False, "message": "Identifiant ou mot de passe incorrect."}), 401
        except Exception as err:
            return jsonify({"success": False, "message": f"Erreur de connexion : {err}"}), 500


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
        from pymongo import MongoClient
        mongo_host = os.environ.get("MONGO_HOST", "mongodb-container" if os.path.exists("/.dockerenv") else "localhost")
        mongo_port = int(os.environ.get("MONGO_PORT", 27017))
        client = MongoClient(f"mongodb://{mongo_host}:{mongo_port}/", serverSelectionTimeoutMS=2000)
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
        from pymongo import MongoClient
        mongo_host = os.environ.get("MONGO_HOST", "mongodb-container" if os.path.exists("/.dockerenv") else "localhost")
        mongo_port = int(os.environ.get("MONGO_PORT", 27017))
        client = MongoClient(f"mongodb://{mongo_host}:{mongo_port}/", serverSelectionTimeoutMS=2000)
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
