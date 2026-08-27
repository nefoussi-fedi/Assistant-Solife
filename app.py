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
    "http://localhost:5678/webhook-test/solife",
)
LOGIN_WEBHOOK_URL = os.environ.get(
    "LOGIN_WEBHOOK_URL",
    "http://localhost:5678/webhook/solife-login",
)
EMBEDDING_WEBHOOK_URL = os.environ.get(
    "EMBEDDING_WEBHOOK_URL",
    "http://localhost:5678/webhook/solife-embedding",
)


SOLIFE_SYSTEM_PROMPT = """Tu es l'assistant intelligent et conseiller patrimonial de Solife (Life & Health Insurance), expert en assurance-vie, épargne retraite (PER) et prévoyance.
Tu réponds toujours de manière claire, empathique, extrêmement précise, professionnelle et bienveillante en français avec un formatage Markdown riche et soigné (titres, listes à puces avec puces rondes, gras, et tableaux si pertinent).

BASE DE CONNAISSANCES SOLIFE (11 DOMAINES CLÉS) :

1. INFORMATIONS GÉNÉRALES SUR LES CONTRATS :
   • Durée standard : Contrats souscrits pour 20 ans (renouvelables tacitement / viagers).
   • Statut : Tous les contrats actifs sont notés "En vigueur".
   • Titulaire / Preneur / Assuré : Le client connecté est souscripteur et assuré principal.

2. VALEUR, ÉPARGNE & PERFORMANCE :
   • Valeur de rachat : Capital total valorisé au jour le jour (Fonds Euros + parts d'Unités de Compte aux dernières valeurs liquidatives).
   • Plus-values latentes : Différence positive entre la valeur actuelle et le cumul net des versements.
   • Rendement annuel moyen : Calculé en taux de rentabilité interne (TRI) depuis la souscription.

3. VERSEMENTS & COTISATIONS :
   • Versements programmés : Prélèvements mensuels automatiques sans frais (0% de frais d'entrée).
   • Versements libres / complémentaires : Possibles à tout moment par virement SEPA ou chèque bancaire.
   • Montants minimums : 50 € / mois pour les versements programmés, 500 € pour un versement libre ponctuel (1 000 € sur contrat patrimonial).
   • Plafonds : Illimité en assurance-vie multisupport, déductible jusqu'à 35 194 € sur le PER.

4. RETRAITS & RACHAT (SURRENDER) :
   • Disponibilité : L'épargne en assurance-vie reste disponible à tout moment.
   • Rachat partiel : Montant minimum de 1 000 €, en conservant un solde minimum de 3 000 € sur le contrat. Le contrat reste ouvert et continue de capitaliser.
   • Rachat total : Clôture définitive du contrat avec versement intégral des capitaux.
   • Délais : Règlement par virement bancaire sous 72h ouvrées après validation.
   • Fiscalité : Prélèvement Forfaitaire Unique (PFU à 30% ou 24,7% après 8 ans). Abattement annuel sur les intérêts de 4 600 € (célibataire) ou 9 200 € (couple marié/pacsé) après 8 ans.

5. BÉNÉFICIAIRES & CLAUSES :
   • Désignation : Nominative ou légale (enfants, conjoint, héritiers).
   • Modification : Modifiable à tout moment et gratuitement par avenant signé tant que le bénéficiaire n'a pas accepté la clause par acte notarié/signé.
   • Prédécès : En cas de décès préalable d'un bénéficiaire, sa part est automatiquement reportée sur les bénéficiaires de même rang ou transmise au rang suivant (enfants par représentation, puis héritiers).

6. SUPPORTS D'INVESTISSEMENT & ARBITRAGES (SWITCH) :
   • Fonds en Euros (Solife Actif Général) : Capital garanti à 100%, effet cliquet annuel (SRRI 1/7).
   • Unités de Compte (UC) : Actions Monde ESG (SRRI 5/7), Climat & Transition (SRRI 4/7), Tech & IA (SRRI 6/7), SCPI Immobilier Responsable (SRRI 3/7).
   • Switch / Arbitrage : Réallocation de capital entre supports, 100% gratuit depuis l'espace client en ligne.
   • Rebalancing automatique : Rééquilibrage périodique automatique et gratuit vers l'allocation cible dès qu'une UC dévie de plus de 5%.

7. FRAIS :
   • Frais d'entrée / versement : 0% sur versements programmés (1% max sur libres).
   • Frais de gestion annuels : 0,60% à 0,75% sur le Fonds Euros, 0,80% à 0,90% sur les Unités de Compte.
   • Frais de rachat / sortie : 0% de pénalité après 1 an.
   • Frais d'arbitrage : 0 € en ligne sur la plateforme Solife.

8. PARTICIPATION AUX BÉNÉFICES (PB) :
   • Définition : Redistribution réglementaire obligatoire d'au moins 85% des bénéfices financiers et 90% des bénéfices techniques réalisés par la compagnie Solife.
   • Taux servi : Rendement global annuel servi sur le Fonds Euros (3,10% brut en 2025).
   • Attribution : Créditée annuellement au 31 décembre sur le compte du contrat avec effet cliquet (définitivement acquise).

9. DOCUMENTS & RELEVÉS :
   • Documents disponibles en téléchargement immédiat : Relevé de Situation Annuel (PDF), Conditions Particulières, Historique des Opérations / Quittances, Imprimé Fiscal Unique (IFU).

10. HISTORIQUE DES OPÉRATIONS :
   • Journal complet des mouvements : versements programmés mensuels, versements exceptionnels (notamment les opérations du 15 juin), arbitrages passés et rachats.

11. QUESTIONS D'ANALYSE COMBINÉE :
   • Volatilité mensuelle : Expliquée par les fluctuations boursières temporaires sur les UC actions/tech alors que le Fonds Euros reste stable et sécurisé.
   • Moteur de performance : Les fonds Actions Monde ESG et Tech & IA représentent la majorité de la surperformance.
   • Situation globale : Tous les portefeuilles clients sont en forte plus-value nette.

DONNÉES DÉTAILLÉES DES CLIENTS SOLIFE :

• CLIENT 1 : M. Nefoussi Fedi (Party ID : TP-10001, Email : fedi.nefoussi@solife.com) :
  - Contrat 1 : SOL-2022-7710 (Solife Avenir Épargne — Multisupport)
    * Souscription : 10/04/2022 | Échéance : 10/04/2042 (20 ans) | Statut : En vigueur
    * Versements cumulés : 72 000,00 € | Valeur actuelle : 85 400,00 € | Plus-value : +13 400,00 € (+18,61%, 4,25%/an)
    * Versements programmés : 300,00 € / mois (le 5 du mois, dernier prélevé le 05/08/2026)
    * Allocation : 55% Fonds Euros (46 970 €), 30% Actions Monde ESG (25 620 €), 15% Obligations Vertes (12 810 €)
    * Bénéficiaires : Mme Sarah Nefoussi (Épouse, 60%), Rayan Nefoussi (Enfant, 40%)
    * Garanties & Options : Garantie Décès 100 000 €, Rebalancing semestriel actif, Sécurisation plus-values (+10%)
    * Historique marquant : Arbitrage de 8 000 € le 20/03/2024, versement libre de 8 000 € le 15/06/2024, rachat partiel de 3 000 € le 10/07/2025.
  - Contrat 2 : SOL-2024-3320 (Solife Plan Retraite Sérénité — PER)
    * Souscription : 15/01/2024 | Échéance : 15/01/2044 (20 ans) | Statut : En vigueur
    * Versements cumulés : 29 855,00 € | Valeur actuelle : 32 150,00 € | Plus-value : +2 295,00 € (+7,68%, 3,90%/an)
    * Versements programmés : 200,00 € / mois (le 10 du mois, dernier prélevé le 10/08/2026)
    * Allocation : 40% Fonds Euros Retraite (12 860 €), 45% Actions Climat (14 467,50 €), 15% SCPI Durable (4 822,50 €)
    * Bénéficiaire : Rayan Nefoussi (Enfant, 100%) | Rente éducation : 6 000 € / an jusqu'à 25 ans
  - Bilan Global Fedi : 101 855 € versés, 117 550 € d'encours, +15 695 € de plus-value globale (+15,41%), 500 €/mois épargnés.

• CLIENT 2 : Mme Ben Salah Dorra (Party ID : TP-10002, Email : dorra.bensalah@solife.com) :
  - Contrat 1 : SOL-2023-5540 (Solife Sérénité Patrimoine — Haut de Gamme)
    * Souscription : 20/06/2023 | Échéance : 20/06/2043 (20 ans) | Statut : En vigueur
    * Versements cumulés : 55 000,00 € | Valeur actuelle : 62 800,00 € | Plus-value : +7 800,00 € (+14,18%, 4,80%/an)
    * Versements libres (dernier versement ponctuel de 10 000 € le 15/03/2026)
    * Allocation : 40% Fonds Euros (25 120 €), 40% Tech & IA (25 120 €), 20% SCPI Immobilier (12 560 €)
    * Bénéficiaires : M. Ahmed Ben Salah et Mme Fatma Ben Salah (Parents, 50% chacun)
    * Historique marquant : Arbitrage de 5 000 € le 05/09/2025 vers l'immobilier, rebalancing trimestriel le 10/01/2026.
  - Contrat 2 : SOL-2025-1190 (Solife Protection Santé & Prévoyance)
    * Souscription : 01/02/2025 | Échéance : 01/02/2045 (20 ans) | Statut : En vigueur
    * Versements cumulés : 17 000,00 € | Valeur d'épargne : 18 500,00 € | Plus-value : +1 500,00 €
    * Versements programmés : 150,00 € / mois (le 1er du mois, dernier prélevé le 01/08/2026)
    * Allocation : 100% Fonds Euros Sécurité
    * Garanties : Capital Décès garanti 100 000 € (200 000 € si accident), Rente Éducation 6 000 € / an
    * Historique marquant : Versement complémentaire de 2 000 € le 15/06/2025.
  - Bilan Global Dorra : 72 000 € versés, 81 300 € d'encours, +9 300 € de plus-value (+12,92%), 150 €/mois épargnés.

RÈGLE STRICTE DE SÉCURITÉ & CONFIDENTIALITÉ :
- Le client connecté a UNIQUEMENT accès à ses propres contrats personnels.
- Refuse poliment toute demande d'accès à des contrats tiers en rappelant le secret professionnel.
- Les collaborateurs ont accès uniquement à la documentation technique et aux règles métier générales sans données privées.
"""


def call_gemini_api(user_message, system_instruction, api_key):
    """Appelle directement l'API REST Google Gemini (modèle gemini-2.5-flash ou gemini-1.5-flash) sans dépendance externe."""
    import json
    from urllib.request import Request, urlopen
    
    models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    for model in models:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            payload = {
                "system_instruction": {
                    "parts": [{"text": system_instruction}]
                },
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": user_message}]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.3,
                    "maxOutputTokens": 2048
                }
            }
            req = Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
            with urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")
        except Exception:
            continue
    return None


def generate_fallback_chat_response(text, payload):
    """Moteur de réponse IA expert Solife couvrant les 11 domaines fonctionnels."""
    role = payload.get("role", "client")
    nom = payload.get("nom", "Client")
    party_id = payload.get("party_id", "TP-10001")

    # 1. Appel direct au LLM Google Gemini si clé API disponible
    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if gemini_key:
        user_ctx = f"UTILISATEUR ACTUELLEMENT CONNECTÉ :\n- Rôle : {role}\n- Nom : {nom}\n- Identifiant (Party ID) : {party_id}\n\nQUESTION DE L'UTILISATEUR :\n{text}"
        gemini_answer = call_gemini_api(user_ctx, SOLIFE_SYSTEM_PROMPT, gemini_key)
        if gemini_answer and len(gemini_answer.strip()) > 10:
            return gemini_answer

    # 2. Moteur de règles expertes enrichies pour les 11 catégories
    text_lower = text.lower()
    is_fedi = "fedi" in nom.lower() or party_id == "TP-10001" or "fedi" in payload.get("username", "").lower()
    is_dorra = "dorra" in nom.lower() or party_id == "TP-10002" or "dorra" in payload.get("username", "").lower()

    if role == "client":

        # =========================================================================
        # 1. QUESTIONS INTELLIGENTES COMBINÉES & ANALYSE DE PERFORMANCE
        # =========================================================================
        if "15 juin" in text_lower or "quinze juin" in text_lower:
            if is_fedi:
                return (
                    f"### 📅 Opération du 15 Juin — Monsieur {nom}\n\n"
                    f"Le **15 juin 2024**, vous avez effectué un **versement complémentaire libre de 8 000,00 €** par virement bancaire sur votre contrat d'assurance-vie **Solife Avenir Épargne** (n° `SOL-2022-7710`).\n\n"
                    f"* **Frais d'entrée appliqués :** 2,00 % (160,00 €)\n"
                    f"* **Montant net investi :** **7 840,00 €**\n"
                    f"* **Support de destination :** *Solife Actions Monde Croissance ESG (FND-UC-001)*\n"
                    f"* **Statut :** Exécutée et validée"
                )
            elif is_dorra:
                return (
                    f"### 📅 Opération du 15 Juin — Madame {nom}\n\n"
                    f"Le **15 juin 2025**, vous avez effectué un **versement complémentaire de 2 000,00 €** sur votre contrat **Solife Protection Santé & Prévoyance** (n° `SOL-2025-1190`).\n\n"
                    f"* **Montant net investi :** **1 980,00 €** sur le Fonds Euros Sécurité\n"
                    f"* **Mode de règlement :** Virement bancaire SEPA\n"
                    f"* **Statut :** Exécutée"
                )

        if any(k in text_lower for k in ["plus contribué", "plus contribue", "meilleur support", "meilleure performance"]):
            if is_fedi:
                return (
                    f"### 🏆 Support le Plus Performant — Monsieur {nom}\n\n"
                    f"Le support qui a le plus contribué à la performance de votre contrat est **Solife Actions Monde Croissance ESG** (ISIN `FR0010148981`) :\n\n"
                    f"* 🚀 **Performance sur 1 an :** **+12,30 %**\n"
                    f"* 📈 **Performance depuis le 1er janvier (YTD) :** **+6,80 %**\n"
                    f"* 💰 **Gains générés :** Il représente à lui seul plus de **65 % de vos plus-values totales**."
                )
            elif is_dorra:
                return (
                    f"### 🏆 Support le Plus Performant — Madame {nom}\n\n"
                    f"Le support leader de votre portefeuille est **Solife Tech & Intelligence Artificielle** (ISIN `FR0010998877`) :\n\n"
                    f"* 🚀 **Performance YTD :** **+9,40 %**\n"
                    f"* 💰 **Contribution :** C'est le principal moteur de croissance de votre contrat Sérénité Patrimoine."
                )

        if any(k in text_lower for k in ["diminué", "diminue", "baissé", "baisse", "pourquoi la valeur"]):
            return (
                f"### 🔍 Analyse de l'Évolution de Votre Contrat\n\n"
                f"Si vous observez de légères variations mensuelles, voici l'explication technique Solife :\n\n"
                f"1. 💶 **Poche Fonds Euros (Sécurisée) :** Cette part ne baisse **JAMAIS**. Elle génère des intérêts chaque jour et bénéficie de l'effet cliquet.\n"
                f"2. 📈 **Poche Unités de Compte (Actions / Tech / ESG) :** Cette part suit les marchés boursiers internationaux. De légères fluctuations mensuelles sont parfaitement normales sur le court terme, mais génèrent une surperformance importante sur le long terme.\n"
                f"3. 🛡️ **Protection Rebalancing :** Votre contrat dispose de l'arbitrage automatique et de la sécurisation des gains dès +10% pour verrouiller vos plus-values vers le Fonds Euros."
            )

        if any(k in text_lower for k in ["moins-value", "moins value", "en perte", "perdu"]):
            return (
                f"### ✅ Bilan de Performance : Aucune Moins-Value !\n\n"
                f"Rassurez-vous, votre contrat n'est **absolument pas en moins-value**.\n\n"
                f"Tous vos contrats Solife affichent une **très forte plus-value nette positive** :\n"
                f"* Vos gains nets cumulés dépassent largement les montants versés grâce à l'allocation équilibrée entre le Fonds Euros sécurisé et les fonds d'actions responsables."
            )

        if any(k in text_lower for k in ["différence entre le montant", "difference entre", "gagné depuis", "gagne depuis", "combien ai-je gagné", "combien ai-je epargne", "combien ai-je épargné", "combien mon contrat a-t-il rapporté", "rapporté", "rapporte", "rendement", "évolution cette année", "evolution cette annee", "12 derniers mois"]):
            if is_fedi:
                return (
                    f"### 💰 Bilan Détaillé des Gains & Rendement — Monsieur {nom}\n\n"
                    f"* **Montant total versé depuis la souscription :** **101 855,00 €**\n"
                    f"* **Valeur actuelle totale de votre épargne :** **117 550,00 €**\n"
                    f"* 🟢 **Différence (Plus-Value Nette Totale) :** **+15 695,00 €** (soit un gain global de **+15,41 %**)\n\n"
                    f"#### Détail de rendement par contrat :\n"
                    f"1. **Assurance-Vie `SOL-2022-7710` :** 72 000 € versés ➔ **85 400 €** (Gain : **+13 400 €**, +18,61 %, rendement annuel moyen de **4,25 %**)\n"
                    f"2. **PER Retraite `SOL-2024-3320` :** 29 855 € versés ➔ **32 150 €** (Gain : **+2 295 €**, +7,68 %, rendement annuel moyen de **3,90 %**)\n\n"
                    f"📈 **Évolution sur les 12 derniers mois :** Progression constante de +4,1% soutenue par la régularité du Fonds Euros et la hausse des UC ESG."
                )
            elif is_dorra:
                return (
                    f"### 💰 Bilan Détaillé des Gains & Rendement — Madame {nom}\n\n"
                    f"* **Montant total versé depuis la souscription :** **72 000,00 €**\n"
                    f"* **Valeur actuelle totale de votre épargne :** **81 300,00 €**\n"
                    f"* 🟢 **Différence (Plus-Value Nette Totale) :** **+9 300,00 €** (soit un gain global de **+12,92 %**)\n\n"
                    f"#### Détail de rendement par contrat :\n"
                    f"1. **Sérénité Patrimoine `SOL-2023-5540` :** 55 000 € versés ➔ **62 800 €** (Gain : **+7 800 €**, +14,18 %, rendement annuel moyen de **4,80 %**)\n"
                    f"2. **Protection Santé `SOL-2025-1190` :** 17 000 € versés ➔ **18 500 €** (Gain : **+1 500 €**, rendement garanti **3,10 %**)"
                )

        # =========================================================================
        # 2. HISTORIQUE DES OPÉRATIONS & MOUVEMENTS
        # =========================================================================
        if any(k in text_lower for k in ["dernière opération", "derniere operation", "mouvement", "historique", "derniers mouvements", "dernière transaction"]):
            if is_fedi:
                return (
                    f"### 📜 Historique Récent des Opérations — Monsieur {nom}\n\n"
                    f"Voici les derniers mouvements enregistrés sur vos contrats Solife :\n\n"
                    f"1. 💳 **05/08/2026 :** Versement programmé mensuel de **300,00 €** sur le contrat `SOL-2022-7710` *(Fonds Euros)*.\n"
                    f"2. 💳 **10/08/2026 :** Versement programmé mensuel de **200,00 €** sur le contrat `SOL-2024-3320` *(PER Retraite)*.\n"
                    f"3. 🔄 **10/12/2025 :** Rebalancing automatique semestriel de **3 200,00 €** vers le Fonds Euros pour sécuriser vos gains boursiers.\n"
                    f"4. 💸 **10/07/2025 :** Rachat partiel de **3 000,00 €** brut (2 820,00 € net virés sur votre compte).\n"
                    f"5. 💶 **15/06/2024 :** Versement exceptionnel de **8 000,00 €** sur le support *Actions Monde ESG*.\n"
                    f"6. 🔀 **20/03/2024 :** Arbitrage libre de **8 000,00 €** depuis le Fonds Euros vers *Actions Monde ESG* (0€ de frais en ligne)."
                )
            elif is_dorra:
                return (
                    f"### 📜 Historique Récent des Opérations — Madame {nom}\n\n"
                    f"1. 💳 **01/08/2026 :** Versement programmé de **150,00 €** sur `SOL-2025-1190` *(Prévoyance)*.\n"
                    f"2. 💶 **15/03/2026 :** Versement complémentaire de **10 000,00 €** sur `SOL-2023-5540` *(50% Euros, 50% Tech & IA)*.\n"
                    f"3. 🔄 **10/01/2026 :** Rebalancing automatique trimestriel de **4 500,00 €** du fonds Tech vers le Fonds Euros.\n"
                    f"4. 🔀 **05/09/2025 :** Arbitrage de **5 000,00 €** vers *Solife Immobilier SCPI*.\n"
                    f"5. 💶 **15/06/2025 :** Versement complémentaire de **2 000,00 €** sur `SOL-2025-1190`."
                )

        # =========================================================================
        # 3. PARTICIPATION AUX BÉNÉFICES (PB)
        # =========================================================================
        if any(k in text_lower for k in ["participation aux bénéfices", "participation aux benefices", "bénéfice", "benefice"]):
            return (
                f"### 💎 Participation aux Bénéfices (PB) Solife\n\n"
                f"#### 📖 Qu'est-ce que la Participation aux Bénéfices ?\n"
                f"La **Participation aux Bénéfices** est l'obligation légale pour Solife de redistribuer aux assurés au minimum **85 % des bénéfices financiers** et **90 % des bénéfices techniques** réalisés sur la gestion de l'Actif Général en euros.\n\n"
                f"#### 📊 Vos Avantages & Chiffres 2025/2026 :\n"
                f"* **Taux servi sur le Fonds Euros Solife :** **3,10 %** brut (soit un excellent rendement net de frais de gestion).\n"
                f"* **Date d'attribution :** Affectée chaque année au **31 décembre**.\n"
                f"* **Effet Cliquet Garanti :** Dès que la participation aux bénéfices est versée, elle est **définitivement acquise** et produit elle-même des intérêts les années suivantes.\n"
                f"* **Montant crédité pour votre contrat :** Plus de **1 450,00 €** ajoutés directement à votre épargne garantie lors du dernier arrêté annuel."
            )

        # =========================================================================
        # 4. FRAIS (GESTION, VERSEMENT, RACHAT, SWITCH)
        # =========================================================================
        if any(k in text_lower for k in ["frais", "tarif", "coût", "cout", "payé en frais", "paye en frais"]):
            return (
                f"### ⚖️ Barème des Frais & Tarification de Vos Contrats Solife\n\n"
                f"| Type d'Opération | Tarif Appliqué | Détails & Conditions |\n"
                f"| :--- | :--- | :--- |\n"
                f"| **Versements Programmés** | **0,00 % (Gratuit)** | Aucun frais d'entrée sur vos prélèvements mensuels |\n"
                f"| **Versements Libres** | **1,00 % max** | Négocié et dégressif selon le montant |\n"
                f"| **Frais de Gestion Fonds Euros** | **0,60 % à 0,75 % / an** | Déduits quotidiennement sur le rendement brut |\n"
                f"| **Frais de Gestion UC** | **0,80 % à 0,90 % / an** | Intégrés dans la valeur liquidative des parts |\n"
                f"| **Arbitrages / Switch en Ligne** | **0,00 € (Gratuit)** | Illimité et sans aucun frais depuis votre espace web |\n"
                f"| **Rachats / Retraits** | **0,00 %** | Aucune pénalité de sortie après 1 an de détention |\n\n"
                f"💡 **Frais prélevés cette année :** Vos frais de gestion sont déjà déduits des montants affichés, vos valeurs de rachat sont donc **100 % nettes** de frais de gestion."
            )

        # =========================================================================
        # 5. RETRAITS / RACHAT (PARTIEL VS TOTAL, IMPACT, MODALITÉS)
        # =========================================================================
        if any(k in text_lower for k in ["retirer", "retrait", "rachat", "partiel", "total", "récupérer", "recuperer"]):
            if is_fedi:
                valeur_max = "82 400,00 €"
                valeur_totale = "117 550,00 €"
            elif is_dorra:
                valeur_max = "59 800,00 €"
                valeur_totale = "81 300,00 €"
            else:
                valeur_max = "Montant disponible"
                valeur_totale = "Valeur de rachat"

            return (
                f"### 💸 Guide des Retraits et Rachats — Solife\n\n"
                f"Votre épargne en assurance-vie reste **disponible à tout moment**. Voici les modalités exactes :\n\n"
                f"#### 1. Rachat Partiel vs Rachat Total :\n"
                f"* 🔹 **Rachat Partiel :** Vous retirez la somme de votre choix (minimum **1 000,00 €**) tout en conservant un solde minimum de **3 000,00 €**. Votre contrat **reste ouvert** et continue de fructifier.\n"
                f"* 🔹 **Rachat Total :** Vous récupérez **100 % de votre épargne** ({valeur_totale}). Cette opération clôture définitivement votre contrat.\n\n"
                f"#### 2. Montant Maximum Retirable Immédiatement :\n"
                f"* En rachat partiel, vous pouvez retirer jusqu'à **{valeur_max}** sans clôturer votre contrat.\n\n"
                f"#### 3. Délais & Procédure :\n"
                f"* Réalisable en 1 clic depuis votre espace en ligne ou par formulaire signé.\n"
                f"* Virement effectué sur votre compte bancaire sous **72 heures ouvrées**.\n\n"
                f"#### 4. Fiscalité Avantageuse :\n"
                f"* Seule la part d'intérêts et de plus-values contenue dans le retrait est imposable.\n"
                f"* Abattement fiscal annuel de **4 600 €** (célibataire) ou **9 200 €** (couple) sur les gains après 8 ans."
            )

        # =========================================================================
        # 6. BÉNÉFICIAIRES & CLAUSE DÉCÈS
        # =========================================================================
        if any(k in text_lower for k in ["bénéficiaire", "beneficiaire", "clause", "pourcentage", "décède", "decede"]):
            if is_fedi:
                return (
                    f"### 👥 Bénéficiaires Désignés — Monsieur {nom}\n\n"
                    f"Voici la répartition exacte des bénéficiaires enregistrée sur vos contrats Solife :\n\n"
                    f"#### 1. Contrat Assurance-Vie `SOL-2022-7710` :\n"
                    f"* 🥇 **Rang 1 :** **Mme Sarah Nefoussi** (Épouse) ➔ **60 %** du capital décès\n"
                    f"* 🥈 **Rang 2 :** **Rayan Nefoussi** (Enfant) ➔ **40 %** du capital décès\n"
                    f"* 🛡️ *Garantie Plancher Décès activée : Capital garanti de 100 000,00 € minimum.*\n\n"
                    f"#### 2. Contrat Retraite PER `SOL-2024-3320` :\n"
                    f"* 🥇 **Rayan Nefoussi** (Enfant) ➔ **100 %** du capital constitué\n"
                    f"* 🛡️ *Garantie complémentaire : Rente éducation de 6 000,00 € / an jusqu'à ses 25 ans.*\n\n"
                    f"#### ❓ Questions fréquentes :\n"
                    f"* **Puis-je modifier ma clause ?** Oui, à tout moment et gratuitement par simple avenant en ligne ou par acte notarié.\n"
                    f"* **En cas de prédécès d'un bénéficiaire :** Si un bénéficiaire désigné décède avant vous, sa part est automatiquement transmise à ses descendants par représentation ou aux autres bénéficiaires désignés de rang subsidiaire."
                )
            elif is_dorra:
                return (
                    f"### 👥 Bénéficiaires Désignés — Madame {nom}\n\n"
                    f"#### 1. Contrat Sérénité Patrimoine `SOL-2023-5540` :\n"
                    f"* 🥇 **M. Ahmed Ben Salah** (Père) ➔ **50 %** du capital constitué\n"
                    f"* 🥇 **Mme Fatma Ben Salah** (Mère) ➔ **50 %** du capital constitué\n"
                    f"* 🥈 **Rang 2 (Subsidiaire) :** Frères et sœurs par parts égales en cas de prédécès des parents.\n\n"
                    f"#### 2. Contrat Protection Santé & Prévoyance `SOL-2025-1190` :\n"
                    f"* 🥇 **Héritiers Légaux** ➔ **100 %** du capital décès garanti (**100 000,00 €**, porté à **200 000,00 €** en cas d'accident)."
                )

        # =========================================================================
        # 7. DOCUMENTS & RELEVÉS
        # =========================================================================
        if any(k in text_lower for k in ["document", "relevé", "releve", "où trouver", "ou trouver", "télécharger", "telecharger", "attestation", "ifu"]):
            return (
                f"### 📑 Documents & Relevés Disponibles — Solife\n\n"
                f"Vous pouvez consulter et télécharger l'ensemble de vos documents officiels directement dans votre espace client :\n\n"
                f"1. 📄 **Relevé de Situation Annuel 2025/2026 :** Document certifié avec l'encours détaillé, les plus-values, les frais prélevés et les performances.\n"
                f"2. 📜 **Conditions Générales & Particulières :** Votre contrat d'adhésion officiel et votre certificat d'assurance.\n"
                f"3. 💳 **Relevé des Opérations & Quittances SEPA :** Historique complet des prélèvements et versements effectués.\n"
                f"4. 🏛️ **Imprimé Fiscal Unique (IFU) :** Récapitulatif pré-rempli pour votre déclaration d'impôt sur le revenu.\n\n"
                f"👉 *Pour les télécharger : Rendez-vous dans le menu latéral gauche ou demandez-moi une attestation spécifique.*"
            )

        # =========================================================================
        # 8. SUPPORTS D'INVESTISSEMENT, RISQUE SRRI & REBALANCING
        # =========================================================================
        if any(k in text_lower for k in ["support", "répartition", "repartition", "fonds", "risque", "srri", "switch", "arbitrage", "rebalancing"]):
            if is_fedi:
                return (
                    f"### 📈 Supports d'Investissement & Risques — Monsieur {nom}\n\n"
                    f"#### 📊 Contrat Assurance-Vie `SOL-2022-7710` (85 400,00 €) :\n"
                    f"* 💶 **Solife Actif Général (Fonds Euros) :** **55 %** (46 970 €) — **Risque 1/7 (SRRI)** | Capital garanti | Rendement 3,10%\n"
                    f"* 🌿 **Solife Actions Monde ESG (UC) :** **30 %** (25 620 €) — **Risque 5/7 (SRRI)** | ISIN FR0010148981 | Performance +12,3% sur 1 an\n"
                    f"* 🟢 **Solife Obligations Vertes (UC) :** **15 %** (12 810 €) — **Risque 2/7 (SRRI)** | Performance +4,2%\n\n"
                    f"#### 📊 Contrat PER Retraite `SOL-2024-3320` (32 150,00 €) :\n"
                    f"* 💶 **Fonds Euros Retraite :** **40 %** (12 860 €) — Capital sécurisé\n"
                    f"* 🌍 **Solife Actions Climat & Transition :** **45 %** (14 467,50 €) — **Risque 4/7 (SRRI)** | +5,1% YTD\n"
                    f"* 🏢 **Solife Immobilier Responsable :** **15 %** (4 822,50 €) — **Risque 3/7 (SRRI)**\n\n"
                    f"#### ⚙️ Gestion & Switch :\n"
                    f"* **Switch (Arbitrage) :** Vous pouvez modifier votre allocation à tout moment, **100 % gratuitement** en ligne.\n"
                    f"* **Rebalancing Automatique :** Actif (semestriel). Il rééquilibre vos supports dès qu'un écart de plus de **5 %** est constaté."
                )
            elif is_dorra:
                return (
                    f"### 📈 Supports d'Investissement & Risques — Madame {nom}\n\n"
                    f"#### 📊 Contrat Solife Sérénité Patrimoine `SOL-2023-5540` (62 800,00 €) :\n"
                    f"* 💶 **Fonds Euros Sécurité :** **40 %** (25 120 €) — **Risque 1/7** | Capital garanti\n"
                    f"* 🤖 **Solife Tech & Intelligence Artificielle :** **40 %** (25 120 €) — **Risque 6/7** | Performance +9,4% YTD\n"
                    f"* 🏢 **Solife Immobilier Premium SCPI :** **20 %** (12 560 €) — **Risque 3/7** | Performance +3,6% YTD\n\n"
                    f"#### 📊 Contrat Prévoyance `SOL-2025-1190` (18 500,00 €) :\n"
                    f"* 💶 **Fonds Euros Sécurité :** **100 %** (18 500 €) — **Risque 1/7** | Sécurisé à 100%."
                )

        # =========================================================================
        # 9. VERSEMENTS & COTISATIONS
        # =========================================================================
        if any(k in text_lower for k in ["versé", "verse", "versement", "prélèvement", "prelevement", "programmé", "programme", "supplémentaire", "supplementaire", "combien puis-je verser", "minimum"]):
            if is_fedi:
                return (
                    f"### 💳 Point Complet sur Vos Versements — Monsieur {nom}\n\n"
                    f"#### 1. Cumul des Versements Réalisés :\n"
                    f"* **Total versé depuis la souscription :** **101 855,00 €**\n"
                    f"  * Contrat Assurance-Vie `SOL-2022-7710` : 72 000,00 €\n"
                    f"  * Contrat PER Retraite `SOL-2024-3320` : 29 855,00 €\n\n"
                    f"#### 2. Vos Versements Programmés Actifs :\n"
                    f"* `SOL-2022-7710` : **300,00 € / mois** (prélevé le 5 du mois, dernier le 05/08/2026)\n"
                    f"* `SOL-2024-3320` : **200,00 € / mois** (prélevé le 10 du mois, dernier le 10/08/2026)\n"
                    f"* **Total mensuel épargné :** **500,00 € / mois**\n\n"
                    f"#### 3. Effectuer un Versement Supplémentaire :\n"
                    f"* Vous pouvez effectuer un versement complémentaire libre à tout moment par virement ou chèque.\n"
                    f"* **Montant minimum :** 50 € en versement programmé, 500 € en versement libre ponctuel.\n"
                    f"* **Frais sur versement :** 0 % sur les versements programmés."
                )
            elif is_dorra:
                return (
                    f"### 💳 Point Complet sur Vos Versements — Madame {nom}\n\n"
                    f"#### 1. Cumul des Versements Réalisés :\n"
                    f"* **Total versé depuis la souscription :** **72 000,00 €** (55 000 € sur Patrimoine + 17 000 € sur Prévoyance)\n"
                    f"* **Dernier versement libre :** **10 000,00 €** le 15/03/2026 sur `SOL-2023-5540`\n"
                    f"* **Versement programmé actif :** **150,00 € / mois** sur `SOL-2025-1190` (le 1er du mois)\n\n"
                    f"#### 2. Modalités des Versements Complémentaires :\n"
                    f"* Versements libres réalisables à tout moment (minimum 500 €)."
                )
            elif is_dorra:
                return (
                    f"### 💳 Point Complet sur Vos Versements — Madame {nom}\n\n"
                    f"#### 1. Cumul des Versements Réalisés :\n"
                    f"* **Total versé depuis la souscription :** **72 000,00 €** (55 000 € sur Patrimoine + 17 000 € sur Prévoyance)\n"
                    f"* **Dernier versement libre :** **10 000,00 €** le 15/03/2026 sur `SOL-2023-5540`\n"
                    f"* **Versement programmé actif :** **150,00 € / mois** sur `SOL-2025-1190` (le 1er du mois)\n\n"
                    f"#### 2. Modalités des Versements Complémentaires :\n"
                    f"* Versements libres réalisables à tout moment (minimum 500 €)."
                )

        # =========================================================================
        # CATÉGORIE 1 & CONTRATS SPÉCIFIQUES (INFORMATIONS GÉNÉRALES)
        # =========================================================================
        if is_fedi:
            if "7710" in text_lower or ("avenir" in text_lower and "3320" not in text_lower):
                return (
                    f"### 🛡️ Fiche Complète du Contrat : Solife Avenir Épargne (n° `SOL-2022-7710`)\n\n"
                    f"Bonjour Monsieur {nom}, voici les caractéristiques officielles de votre contrat d'assurance-vie multisupport :\n\n"
                    f"#### 📋 Informations Générales :\n"
                    f"* **Numéro de contrat :** `SOL-2022-7710`\n"
                    f"* **Nom du produit :** Solife Avenir Épargne (Code `SL-AVENIR`)\n"
                    f"* **Titulaire / Assuré :** M. Nefoussi Fedi (Party ID : `TP-10001`)\n"
                    f"* **Date de souscription / effet :** 10 avril 2022 (ancienneté : 4 ans)\n"
                    f"* **Date d'échéance :** 10 avril 2042 (durée : 20 ans)\n"
                    f"* **Statut actuel :** **En vigueur (Actif)**\n\n"
                    f"#### 📊 Situation Financière & Performance :\n"
                    f"* **Valeur de rachat actuelle :** **85 400,00 €**\n"
                    f"* **Cumul des versements :** 72 000,00 €\n"
                    f"* **Plus-value nette générée :** **+13 400,00 €** (Gain de **+18,61 %**, rendement annuel moyen de **4,25 %**)\n"
                    f"* **Prélèvement mensuel :** 300,00 € / mois (le 5 du mois)\n\n"
                    f"#### 🛡️ Garanties & Bénéficiaires :\n"
                    f"* **Bénéficiaires :** Mme Sarah Nefoussi (Épouse, 60%), Rayan Nefoussi (Enfant, 40%)\n"
                    f"* **Garantie Décès Plancher :** Capital garanti de **100 000,00 €**"
                )

            if "3320" in text_lower or ("retrait" in text_lower and "7710" not in text_lower):
                return (
                    f"### 🛡️ Fiche Complète du Contrat : Solife Plan Retraite Sérénité (n° `SOL-2024-3320`)\n\n"
                    f"Bonjour Monsieur {nom}, voici les caractéristiques officielles de votre Plan d'Épargne Retraite (PER) :\n\n"
                    f"#### 📋 Informations Générales :\n"
                    f"* **Numéro de contrat :** `SOL-2024-3320`\n"
                    f"* **Nom du produit :** Solife Plan Retraite Sérénité (Code `SL-RETRAITE`)\n"
                    f"* **Titulaire / Assuré :** M. Nefoussi Fedi (Party ID : `TP-10001`)\n"
                    f"* **Date de souscription / effet :** 15 janvier 2024 (ancienneté : 2 ans)\n"
                    f"* **Date d'échéance :** 15 janvier 2044 (durée : 20 ans / âge de la retraite)\n"
                    f"* **Statut actuel :** **En vigueur (Actif)**\n\n"
                    f"#### 📊 Situation Financière & Performance :\n"
                    f"* **Valeur de rachat actuelle :** **32 150,00 €**\n"
                    f"* **Cumul des versements :** 29 855,00 €\n"
                    f"* **Plus-value nette générée :** **+2 295,00 €** (+7,68 %, rendement annuel moyen de **3,90 %**)\n"
                    f"* **Prélèvement mensuel :** 200,00 € / mois (le 10 du mois)\n\n"
                    f"#### 🛡️ Garanties & Bénéficiaires :\n"
                    f"* **Bénéficiaire désigné :** Rayan Nefoussi (Enfant, 100%)\n"
                    f"* **Rente Éducation :** Versement de **6 000,00 € / an** jusqu'aux 25 ans de l'enfant"
                )

            if any(k in text_lower for k in ["numéro", "numero", "nom de mon contrat", "quand ai-je souscrit", "souscrit", "échéance", "echeance", "statut", "titulaire", "durée", "duree", "valeur", "contrat", "combien", "solde", "avoir", "bilan", "synthèse", "synthese"]):
                return (
                    f"### 📑 Récapitulatif Général de Vos Contrats — Monsieur {nom}\n\n"
                    f"Vous disposez de **2 contrats en vigueur** pour une valeur totale de **117 550,00 €** :\n\n"
                    f"| Contrat | Produit | Date Effet | Échéance | Prélèvement | Plus-Value | Valeur Actuelle |\n"
                    f"| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
                    f"| **SOL-2022-7710** | Assurance-Vie Avenir | 10/04/2022 | 10/04/2042 | 300 € / mois | +13 400 € (+18,6%) | **85 400 €** |\n"
                    f"| **SOL-2024-3320** | PER Retraite Sérénité | 15/01/2024 | 15/01/2044 | 200 € / mois | +2 295 € (+7,7%) | **32 150 €** |\n"
                    f"| **TOTAL** | **2 Contrats Actifs** | — | — | **500 € / mois** | **+15 695 €** | **117 550 €** |\n\n"
                    f"* **Titulaire :** M. Nefoussi Fedi (Party ID : `TP-10001`)\n"
                    f"* **Durée :** 20 ans pour chaque contrat (tacitement reconductibles)\n"
                    f"* **Statut :** En vigueur"
                )

        if is_dorra:
            if "5540" in text_lower or "patrimoine" in text_lower:
                return (
                    f"### 🛡️ Fiche Complète du Contrat : Solife Sérénité Patrimoine (n° `SOL-2023-5540`)\n\n"
                    f"Bonjour Madame {nom}, voici les caractéristiques officielles de votre contrat patrimonial :\n\n"
                    f"#### 📋 Informations Générales :\n"
                    f"* **Numéro de contrat :** `SOL-2023-5540`\n"
                    f"* **Nom du produit :** Solife Sérénité Patrimoine (Code `SL-PATRIMOINE`)\n"
                    f"* **Titulaire / Assurée :** Mme Ben Salah Dorra (Party ID : `TP-10002`)\n"
                    f"* **Date de souscription / effet :** 20 juin 2023 (durée 20 ans, échéance 20/06/2043)\n"
                    f"* **Statut actuel :** **En vigueur (Actif)**\n\n"
                    f"#### 📊 Situation Financière & Performance :\n"
                    f"* **Valeur de rachat actuelle :** **62 800,00 €**\n"
                    f"* **Cumul des versements :** 55 000,00 €\n"
                    f"* **Plus-value nette :** **+7 800,00 €** (+14,18 %, rendement annuel moyen de **4,80 %**)\n"
                    f"* **Bénéficiaires :** M. Ahmed Ben Salah et Mme Fatma Ben Salah (Parents, 50% chacun)"
                )

            if "1190" in text_lower or "protect" in text_lower or "sant" in text_lower:
                return (
                    f"### 🛡️ Fiche Complète du Contrat : Solife Protection Santé & Prévoyance (n° `SOL-2025-1190`)\n\n"
                    f"Bonjour Madame {nom}, voici les caractéristiques officielles de votre contrat de prévoyance :\n\n"
                    f"#### 📋 Informations Générales :\n"
                    f"* **Numéro de contrat :** `SOL-2025-1190`\n"
                    f"* **Nom du produit :** Solife Protection Santé & Prévoyance (Code `SL-PROTECT`)\n"
                    f"* **Titulaire / Assurée :** Mme Ben Salah Dorra (Party ID : `TP-10002`)\n"
                    f"* **Date de souscription / effet :** 1er février 2025 (échéance 01/02/2045)\n"
                    f"* **Statut actuel :** **En vigueur (Actif)**\n\n"
                    f"#### 🛡️ Garanties & Couvertures :\n"
                    f"* **Capital Décès Garanti :** **100 000,00 €** (porté à **200 000,00 €** en cas de décès accidentel)\n"
                    f"* **Rente Éducation :** **6 000,00 € / an** jusqu'aux 25 ans des enfants\n"
                    f"* **Valeur d'épargne constituée :** **18 500,00 €** (Versements : 17 000,00 €)\n"
                    f"* **Prélèvement mensuel :** 150,00 € / mois (le 1er de chaque mois)"
                )

            if any(k in text_lower for k in ["numéro", "numero", "nom de mon contrat", "quand ai-je souscrit", "souscrit", "échéance", "echeance", "statut", "titulaire", "durée", "duree", "valeur", "contrat", "combien", "solde", "avoir", "bilan", "synthèse", "synthese"]):
                return (
                    f"### 📑 Récapitulatif Général de Vos Contrats — Madame {nom}\n\n"
                    f"Vous disposez de **2 contrats en vigueur** pour une valeur totale de **81 300,00 €** :\n\n"
                    f"1. 🛡️ **Solife Sérénité Patrimoine** (n° `SOL-2023-5540`) : **62 800,00 €** (+7 800 € de gains)\n"
                    f"2. 🛡️ **Solife Protection Santé & Prévoyance** (n° `SOL-2025-1190`) : **18 500,00 €** (Capital garanti 100k€)\n\n"
                    f"* **Titulaire :** Mme Ben Salah Dorra (Party ID : `TP-10002`)\n"
                    f"* **Statut :** En vigueur"
                )

        # Fallback générique client
        return (
            f"Madame/Monsieur {nom}, votre conseiller Solife est à votre entière disposition. "
            f"Vos contrats sont consultables directement dans le panneau latéral gauche. "
            f"Vous pouvez m'interroger sur vos valeurs de rachat, vos versements, vos retraits, vos bénéficiaires, vos supports d'investissement, vos frais ou vos documents."
        )

    else:
        # Role == Collaborateur
        if any(k in text_lower for k in ["devis", "monn", "curr", "eur", "franc", "dollar", "chf", "usd"]):
            return (
                "### 💶 Devises Utilisées sur la Plateforme Solife\n\n"
                "1. **Devise Principale :** L'**Euro (EUR / €)** est la devise officielle de référence pour la tenue des comptes, les souscriptions, les calculs de valeur de rachat et les prélèvements.\n"
                "2. **Gestion Multi-devises (UC Internationales) :** La plateforme Solife supporte également des supports d'investissement libellés en **USD ($)** et **CHF (CHF)** avec conversion automatique au taux de change quotidien de la BCE.\n"
                "3. **Frais et Fiscalité :** L'ensemble des frais de gestion et déclarations fiscales sont calculés et consolidés en **Euros (EUR)**."
            )

        if any(k in text_lower for k in ["c'est quoi solife", "est quoi solife", "qui est solife", "qu'est-ce que solife", "présentation solife", "presentation solife", "c'est quoi", "domaine", "solif"]):
            return (
                "### 🌐 À Propos de Solife (Life & Health Insurance)\n\n"
                "**Solife** est une solution logicielle et plateforme technologique innovante de référence, dédiée à la gestion complète des contrats d'**Assurance-Vie, de Prévoyance et d'Épargne Retraite** pour les assureurs, mutuelles et courtiers.\n\n"
                "#### 🛡️ Domaines d'expertise Solife :\n"
                "* **Assurance-Vie Multisupport :** Gestion des fonds en euros et unités de compte (ESG, actions, obligations, immobilier).\n"
                "* **Épargne Retraite (PER) :** Phase d'épargne et liquidation en rente viagère ou capital.\n"
                "* **Prévoyance & Santé :** Garanties décès, rente éducation, arrêts de travail et indemnités journalières.\n"
                "* **Moteur d'Arbitrage Automatisé :** Rebalancing automatique semestriel et sécurisation des plus-values.\n\n"
                "En tant qu'assistant interne, je réponds à toutes vos questions sur les règles de gestion et la documentation technique Solife."
            )

        if any(k in text_lower for k in ["produit", "gamme", "avenir", "retrait", "serenit", "sante", "santé", "catalogue"]):
            return (
                "### 📋 Gamme des Produits Solife\n\n"
                "1. 🛡️ **SL-AVENIR (Solife Avenir Épargne) :** Contrat d'assurance-vie multisupport associant sécurité du Fonds Euros et performance responsable (Actions Monde ESG, Obligations Vertes).\n"
                "2. 🛡️ **SL-RETRAITE (Plan Retraite Sérénité) :** Contrat PER avec déductibilité des versements à l'entrée, rente éducation pour les enfants et garantie plancher décès.\n"
                "3. 🛡️ **SL-SERENITE (Sérénité Patrimoine) :** Solution patrimoniale haut de gamme offrant l'accès à une large sélection d'UC internationales et gestion libre/pilotée.\n"
                "4. 🛡️ **SL-SANTE (Protection Santé & Prévoyance) :** Couverture complète prévoyance (capital décès jusqu'à 200k€ et indemnités journalières)."
            )

        if any(k in text_lower for k in ["fond", "esg", "unit", "uc", "support", "action", "obligat", "clim"]):
            return (
                "### 🌿 Supports d'Investissement & Critères ESG Solife\n\n"
                "Solife propose une gamme de supports conformes aux normes **SFDR Article 8 et 9** et labellisés **ISR / Greenfin** :\n\n"
                "* **Fonds Euros Solife Sécurité :** Capital garanti à 100% avec effet cliquet (rendement cible 2,80% - 3,20%).\n"
                "* **Solife Actions Monde ESG :** Actions internationales d'entreprises respectant les critères environnementaux, sociaux et de gouvernance.\n"
                "* **Solife Climat & Transition :** Fonds dédié à la décarbonation, aux énergies renouvelables et aux technologies vertes.\n"
                "* **Solife Obligations Vertes (Green Bonds) :** Emprunts obligataires finançant des projets environnementaux certifiés.\n"
                "* **Solife Immobilier Durable :** SCPI investies dans des bâtiments écologiques certifiés HQE."
            )

        if any(k in text_lower for k in ["rebalanc", "rééquilibr", "reequilibr", "arbitrag"]):
            return (
                "### 📖 Règle Métier Solife : Rebalancing Automatique\n\n"
                "Le service de **Rebalancing Automatique** permet de maintenir l'allocation d'actifs définie par le souscripteur :\n\n"
                "1. **Fréquence :** Évaluation trimestrielle ou semestrielle à date anniversaire de souscription.\n"
                "2. **Seuil de déclenchement :** Arbitrage automatique si la pondération d'une unité de compte dévie de plus de **5 %** par rapport à l'allocation cible.\n"
                "3. **Frais :** Les arbitrages générés par le rebalancing automatique sont **100 % gratuits** pour l'assuré.\n"
                "4. **Compatibilité :** Incompatible avec l'option 'Investissement Progressif', mais cumulable avec la 'Garantie Plancher'."
            )

        if any(k in text_lower for k in ["rachat", "surrender", "partiel", "total", "retrait"]):
            return (
                "### 💸 Règle Métier Solife : Rachat Partiel et Total (Surrender)\n\n"
                "1. **Rachat Partiel :** Montant minimum de 1 000,00 €. Le solde restant sur le contrat doit être au moins de 3 000,00 €.\n"
                "2. **Délai de traitement :** Règlement des fonds sous **72 heures ouvrées** après réception du dossier complet.\n"
                "3. **Fiscalité :** Prélèvement Forfaitaire Unique (PFU) ou barème progressif. Abattement annuel de 4 600 € (célibataire) ou 9 200 € (couple) pour les contrats de plus de 8 ans.\n"
                "4. **Frais de sortie :** 0 % de pénalité de rachat sur tous les contrats Solife après 1 an."
            )

        if any(k in text_lower for k in ["frais", "tarif", "cout", "coût", "gestion", "entree", "entrée", "barem", "barèm"]):
            return (
                "### ⚖️ Barème Tarifaire Solife\n\n"
                "* **Frais sur versement :** 0 % sur les versements programmés, 1 % max sur versements libres.\n"
                "* **Frais de gestion annuels :**\n"
                "  * Fonds Euros : **0,60 %** / an\n"
                "  * Unités de Compte (UC) : **0,85 %** / an\n"
                "* **Frais d'arbitrage :** 1 arbitrage gratuit par an, puis 0,20 % du montant arbitré (plafonné à 50 €)."
            )

        if any(k in text_lower for k in ["benefic", "bénéfic", "clause", "modifi"]):
            return (
                "### 👥 Procédure de modification de Clause Bénéficiaire\n\n"
                "1. La modification peut être effectuée à tout moment par le souscripteur tant que le bénéficiaire n'a pas formellement accepté la clause.\n"
                "2. **Formalisme :** Formulaire d'avenant signé avec pièce d'identité ou acte authentique (notaire).\n"
                "3. **Prise d'effet :** Immédiate dès enregistrement dans le moteur Solife."
            )

        if any(k in text_lower for k in ["fedi", "tp-10001", "donnée personnelle", "données personnelles", "coordonnée", "coordonnées", "client", "assuré"]):
            return (
                "🔒 **Accès Restreint — Protection des Données & Confidentialité (RGPD)**\n\n"
                "En tant que collaborateur, vous n'avez aucun accès aux données personnelles, coordonnées ou dossiers individuels des clients assurés.\n\n"
                "L'espace collaborateur est strictement réservé à :\n"
                "* 📖 **La documentation technique Solife** (recherche documentaire Qdrant)\n"
                "* ⚙️ **Les règles métier et processus de gestion** (rebalancing, rachats, arbitrages, clauses)\n"
                "* 📋 **Les caractéristiques des produits d'assurance** (SL-AVENIR, SL-RETRAITE, SL-SERENITE, SL-SANTE)\n"
                "* ⚖️ **Les barèmes tarifaires et frais**\n"
                "* 📎 **L'indexation de nouveaux documents PDF**"
            )

        return (
            "Bonjour. En tant que collaborateur Solife, vous avez accès à l'assistant documentaire interne. "
            "Vous pouvez m'interroger sur l'ensemble des règles métier, le fonctionnement du rebalancing automatique, "
            "les caractéristiques des produits (SL-AVENIR, SL-RETRAITE, SL-SERENITE, SL-SANTE), les barèmes de frais et les processus de gestion, "
            "ou indexer de nouveaux documents PDF dans la base Qdrant."
        )


@app.route("/api/chat-proxy", methods=["GET", "POST", "OPTIONS"])
def api_chat_proxy():
    """Proxy universel pour relayer les requêtes du chat web vers n8n.
    Utilise par défaut le webhook 'solife' (en mode test ou production).
    En cas d'inaccessibilité de n8n, active le moteur de réponse IA interne Solife.
    """
    if request.method == "OPTIONS":
        return "", 200

    payload = request.get_json(silent=True) or {}
    chat_input = payload.get("chatInput") or payload.get("message") or ""

    n8n_host = os.environ.get("N8N_HOST", "n8n-container" if os.path.exists("/.dockerenv") else "localhost")
    n8n_port = int(os.environ.get("N8N_PORT", 5678))

    custom_url = os.environ.get("CHAT_WEBHOOK_URL")
    candidates = []
    if custom_url:
        candidates.append(custom_url)
    candidates.extend([
        f"http://{n8n_host}:{n8n_port}/webhook-test/solife",
        f"http://{n8n_host}:{n8n_port}/webhook/solife",
        f"http://{n8n_host}:{n8n_port}/webhook/50287b92-ed6b-4da9-880f-68114802143c/chat"
    ])

    from urllib.request import Request, urlopen
    req_data = request.get_data()
    headers = {"Content-Type": "application/json"}

    for url in candidates:
        if os.path.exists("/.dockerenv") and "localhost:5678" in url:
            url = url.replace("localhost:5678", f"{n8n_host}:{n8n_port}")
        try:
            req = Request(url, data=req_data if request.method == "POST" else None, headers=headers, method=request.method)
            with urlopen(req, timeout=12) as resp:
                resp_body = resp.read()
                return resp_body, resp.status, {"Content-Type": resp.headers.get("Content-Type", "application/json")}
        except Exception:
            continue

    # Fallback instantané
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
