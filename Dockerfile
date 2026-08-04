# On part d'une image Python légère (bonne pratique : évite d'alourdir l'image finale)
FROM python:3.12-slim

# Dossier de travail à l'intérieur du conteneur
WORKDIR /app

# On copie d'abord uniquement requirements.txt : Docker peut ainsi réutiliser
# cette étape (plus rapide) tant que les dépendances ne changent pas,
# même si on modifie le code ensuite.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# On copie le reste du projet (app.py, templates/, static/)
COPY . .

# Port sur lequel l'application écoute à l'intérieur du conteneur
EXPOSE 5000

# En production, on utilise gunicorn (plus robuste que le serveur de dev Flask)
# --bind 0.0.0.0:5000 : accessible depuis l'extérieur du conteneur
# app:app : fichier app.py, variable "app" (l'objet Flask)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
