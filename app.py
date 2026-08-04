import os
from flask import Flask, render_template

app = Flask(__name__)

# Ces URLs viennent de variables d'environnement, avec une valeur par défaut
# pratique pour tester en local. On les changera dans docker-compose selon
# l'environnement (local vs conteneurs Docker).
CHAT_WEBHOOK_URL = os.environ.get(
    "CHAT_WEBHOOK_URL",
    "http://localhost:5678/webhook/50287b92-ed6b-4da9-880f-68114802143c/chat",
)
LOGIN_WEBHOOK_URL = os.environ.get(
    "LOGIN_WEBHOOK_URL",
    "http://localhost:5678/webhook/solife-login",
)


@app.route("/")
def index():
    return render_template(
        "index.html",
        chat_webhook_url=CHAT_WEBHOOK_URL,
        login_webhook_url=LOGIN_WEBHOOK_URL,
    )


@app.route("/health")
def health():
    # Petite route utile pour vérifier que le conteneur tourne bien
    # (on s'en servira plus tard avec Docker/GitHub Actions).
    return {"status": "ok"}


if __name__ == "__main__":
    # host="0.0.0.0" est nécessaire pour que Flask soit accessible
    # depuis l'extérieur du conteneur Docker plus tard.
    app.run(host="0.0.0.0", port=5000, debug=True)
