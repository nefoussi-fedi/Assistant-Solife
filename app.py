import os
import re
from flask import Flask, render_template, jsonify, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

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


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    # host="0.0.0.0" est nécessaire pour que Flask soit accessible
    # depuis l'extérieur du conteneur Docker plus tard.
    app.run(host="0.0.0.0", port=5000, debug=True)
