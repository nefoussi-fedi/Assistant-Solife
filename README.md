# Solife Chatbot — Interface Flask

## Installation (en local, sur votre PC)

### 1. Prérequis
- Python 3.10 ou plus récent installé sur votre machine
- Vérifiez avec :
  ```
  python --version
  ```

### 2. Installer les dépendances

Ouvrez un terminal dans le dossier du projet, puis :

```
pip install -r requirements.txt
```

### 3. Lancer l'application

```
python app.py
```

Vous devriez voir un message indiquant que le serveur tourne sur `http://127.0.0.1:5000` (ou `0.0.0.0:5000`).

### 4. Ouvrir dans le navigateur

Allez sur :
```
http://localhost:5000
```

Vous devriez voir l'écran de connexion Solife.

## Configuration des webhooks n8n

Par défaut, l'application utilise ces adresses (celles de votre n8n en local) :
- Chat : `http://localhost:5678/webhook/50287b92-ed6b-4da9-880f-68114802143c/chat`
- Login : `http://localhost:5678/webhook/solife-login`

Si besoin de les changer sans modifier le code, définissez ces variables d'environnement avant de lancer `python app.py` :

```
set CHAT_WEBHOOK_URL=http://localhost:5678/webhook/xxx/chat
set LOGIN_WEBHOOK_URL=http://localhost:5678/webhook/solife-login
python app.py
```

*(Sur Mac/Linux, remplacez `set` par `export`.)*

## Structure du projet

```
solife-flask/
├── app.py                 → l'application Flask
├── requirements.txt       → dépendances Python à installer
├── templates/
│   └── index.html         → la page (écran de connexion, accueil, chat)
└── static/
    └── solife-hero.png    → image d'accueil (à remplacer par la vraie si besoin)
```

## Prochaine étape

Une fois que ça fonctionne en local, on passera à la dockerisation (Dockerfile) pour préparer la mise en production.
