# 📊 AI CUSTOMER ASSISTANT FOR SOLIFE — PRÉSENTATION MANAGEMENT

> **Présenté par :** Nefoussi Fedi  
> **Entreprise / Solution :** Vermeg — Solife Life & Health Insurance  
> **Statut :** Présentation optimisée avec visuels HD intégrés, fil conducteur en 3 temps, démo scénarisée et feuille de route stratégique.

---

## 🎯 1. Fil Conducteur de la Présentation (Storytelling en 3 Temps)

1. **La Douleur Métier (Avant)** :
   - Multiplication des écrans et complexité des tableaux financiers.
   - Perte de temps pour les brokers, équipes support et clients.
2. **La Transformation Solife (Pendant)** :
   - Assistant IA RAG qui vulgarise les métriques complexes (Unités de Compte, Fonds Euros, YTD, Arbitrage).
   - Génération de synthèses claires et détection d'alertes proactives.
3. **La Preuve Technique (Après)** :
   - 100% On-Premise (Ollama/DeepSeek, Qdrant, MongoDB, n8n).
   - Déploiement 1-clic avec Docker Compose & CI/CD GitHub Actions.

---

## 🖼️ 2. Diapositives Visuelles HD Remplacées & Intégrées

Les visuels haute définition suivants ont été directement intégrés dans la galerie de présentation (`static/slides/`) :

* 📸 **Slide 4 (Présentation Chatbot NLP)** : [slide_4.png](file:///c:/Users/DELL/Desktop/solife-flask/static/slides/slide_4.png)
  - Visuel 3D et explication du Traitement du Langage Naturel (NLP).
* 📸 **Slide 6 (Cœur du Projet — Comparatif)** : [slide_6.png](file:///c:/Users/DELL/Desktop/solife-flask/static/slides/slide_6.png)
  - Comparatif technique sans titre : *Sans Assistant (Tableau UC/Fonds Euros)* vs *Avec Assistant IA (Synthèse claire + YTD/Arbitrage)*.
* 📸 **Slide 7 (Analyse Proactive & Alertes)** : [slide_7.png](file:///c:/Users/DELL/Desktop/solife-flask/static/slides/slide_7.png)
  - Flux visuel des données de portefeuille générant des alertes d'arbitrage et d'échéance.
* 📸 **Slide 10 (Bénéfices du Chatbot Solife)** : [slide_10.png](file:///c:/Users/DELL/Desktop/solife-flask/static/slides/slide_10.png)
  - Cartes des 3 cibles : *Broker & Support*, *Clients*, *Collaborateurs Internes*.
* 📸 **Slide 13 (Architecture Système Docker)** : [slide_13.png](file:///c:/Users/DELL/Desktop/solife-flask/static/slides/slide_13.png)
  - Schéma bicolore complet montrant Flask, n8n, Qdrant, MongoDB et Gemini/Ollama.

---

## 📊 3. Chiffres Clés d'Ingestion & Performance

- 📄 **59 Documents PDF** d'assurance Santé & Vie indexés.
- 🧩 **1 869 Chunks de texte** découpés avec précision.
- 🔍 **3 075 Points vectoriels** stockés dans la base Qdrant.
- 🔒 **100% Souveraineté des Données** (Aucun envoi à des serveurs tiers).

---

## 🎬 4. Guide de Démonstration en Direct (Scénario 2 Questions)

1. **Question 1 (Client / Portefeuille)** :
   > *"Quelle est la situation de mon contrat ?"*
   - **Objectif** : Démontrer la synthèse automatique, le calcul YTD et l'alerte d'arbitrage.

2. **Question 2 (Support / RAG avec Source)** :
   > *"Comment fonctionne le rebalancing ?"*
   - **Objectif** : Démontrer la précision du RAG et la citation de la documentation officielle VERMEG.

---

## 🚀 5. Perspectives & Feuille de Route Stratégique

* **Aujourd'hui (Réalisé)** : Consultation RAG, sécurité locale, tests unitaires Pytest, Docker Compose 1-clic.
* **Demain (Perspectives Solife)** : Intégration des API transactionnelles Solife pour exécuter des arbitrages directement en langage naturel depuis le chat.
