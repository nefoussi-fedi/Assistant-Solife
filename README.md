# Solife Chatbot — Interface Flask

Ce projet fournit l'interface web (Flask + SPA Dark Mode) du chatbot assistant client **Solife** (Life & Health Insurance), connecté aux workflows d'automatisation **n8n** (RAG & Authentification).

---

## 🏗️ Architecture & Composants

```
solife-flask/
├── app.py                 → Serveur Flask (routes '/' et '/health')
├── requirements.txt       → Dépendances (Flask, Gunicorn)
├── Dockerfile             → Image Docker multi-stage (Python 3.12-slim + Gunicorn)
├── docker-compose.yml     → Composition Docker avec réseau externe solife-network
├── n8n-workflows/         → Workflows n8n exportés (principal, embedding, Auth)
├── .github/workflows/     → CI/CD GitHub Actions pour build/push sur Docker Hub
├── templates/
│   └── index.html         → Page unique (Écran Login, Accueil & Widget Chat n8n)
└── static/
    └── solife-hero.png    → Image d'accueil Solife
```

---

## 🚀 Installation en local (sur votre PC)

### 1. Prérequis
- Python 3.10 ou plus récent installé sur votre machine
- Vérifiez avec :
  ```bash
  python --version
  ```

### 2. Installer les dépendances

Ouvrez un terminal dans le dossier du projet, puis :

```bash
pip install -r requirements.txt
```

### 3. Lancer l'application

```bash
python app.py
```

L'application est accessible sur : `http://localhost:5000`

---

## ⚙️ Configuration des Webhooks n8n

Par défaut, l'application utilise les variables d'environnement suivantes pour communiquer avec n8n :

- **Chat (RAG)** : `CHAT_WEBHOOK_URL` (par défaut: `http://localhost:5678/webhook/50287b92-ed6b-4da9-880f-68114802143c/chat`)
- **Authentification** : `LOGIN_WEBHOOK_URL` (par défaut: `http://localhost:5678/webhook/solife-login`)

Pour modifier ces adresses en local sans modifier le code :

```bash
# Sur Windows (Cmd)
set CHAT_WEBHOOK_URL=http://localhost:5678/webhook/xxx/chat
set LOGIN_WEBHOOK_URL=http://localhost:5678/webhook/solife-login
python app.py

# Sur Linux / macOS / PowerShell
export CHAT_WEBHOOK_URL=http://localhost:5678/webhook/xxx/chat
export LOGIN_WEBHOOK_URL=http://localhost:5678/webhook/solife-login
python app.py
```

---

## 🐳 Déploiement Docker & Compose

### Via Docker Compose
```bash
docker-compose up -d --build
```

> **Note :** Le conteneur se connecte au réseau externe `solife-network` afin de communiquer avec les conteneurs n8n, Qdrant et MongoDB.

### Healthcheck Endpoint
- Route de santé : `GET /health` → `{"status": "ok"}`

---

## 🔄 CI/CD Pipeline (GitHub Actions)

À chaque `push` sur la branche `main`, le workflow `.github/workflows/docker-publish.yml` :
1. Prépare Docker Buildx
2. Se connecte à Docker Hub (via secrets `DOCKERHUB_USERNAME` et `DOCKERHUB_TOKEN`)
3. Construit et publie l'image `solife-flask:latest` et `solife-flask:<SHA>`

