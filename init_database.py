import os
import sys
import hashlib
from pymongo import MongoClient

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def hash_password(password: str) -> str:
    """Hache le mot de passe en SHA-256 (compatible avec le node Crypto de n8n)"""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def init_db():
    mongo_uri = os.environ.get("MONGO_URI")
    if not mongo_uri:
        mongo_host = os.environ.get("MONGO_HOST", "localhost")
        mongo_port = int(os.environ.get("MONGO_PORT", 27017))
        mongo_uri = f"mongodb://{mongo_host}:{mongo_port}/"

    print(f"[*] Connexion a MongoDB sur {mongo_uri}...")
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    
    # Base de données Solife
    db = client["solife"]
    
    # Vérification connexion
    try:
        client.admin.command('ping')
        print("[+] Connexion a MongoDB reussie !")
    except Exception as e:
        print(f"[-] Impossible de joindre MongoDB : {e}")
        print("Vérifiez que le conteneur mongodb-container est démarré avec 'docker-compose up -d mongodb-container'.")
        return

    # Nettoyage ciblé : On ne touche JAMAIS à chat_histories !
    # Les contrats sont désormais dans la base solife_contracts (voir init_contracts_db.py)
    print("[*] Nettoyage de la collection 'users'...")
    db.users.drop()

    # =========================================================================
    # 1. UTILISATEURS (users)
    # =========================================================================
    users_data = [
        # Collaborateur / Stagiaire
        {
            "username": "collaborateur",
            "password": hash_password("password123"),
            "role": "collaborateur",
            "nom": "Équipe Interne Solife",
            "statut": "actif"
        },
        {
            "username": "admin",
            "password": hash_password("password123"),
            "role": "collaborateur",
            "nom": "Administrateur Solife",
            "statut": "actif"
        },
        # Client 1 : Nefoussi Fedi
        {
            "username": "fedi.nefoussi",
            "password": hash_password("password123"),
            "role": "client",
            "party_id": "TP-10001",
            "nom": "Nefoussi Fedi",
            "email": "fedi.nefoussi@solife.com",
            "telephone": "+33 6 11 22 33 44",
            "adresse": "12 Avenue des Champs-Élysées, 75008 Paris, France",
            "date_naissance": "1988-06-14",
            "statut": "actif"
        },
        # Client 2 : Ben Salah Dorra
        {
            "username": "dorra.bensalah",
            "password": hash_password("password123"),
            "role": "client",
            "party_id": "TP-10002",
            "nom": "Ben Salah Dorra",
            "email": "dorra.bensalah@solife.com",
            "telephone": "+33 6 55 66 77 88",
            "adresse": "45 Rue de la République, 69002 Lyon, France",
            "date_naissance": "1992-11-23",
            "statut": "actif"
        }
    ]
    db.users.insert_many(users_data)
    print(f"[+] {len(users_data)} utilisateurs inseres dans 'users'.")

    # =========================================================================
    # NOTE : Les contrats sont désormais dans la base solife_contracts
    # Exécuter init_contracts_db.py pour initialiser la base des contrats
    # =========================================================================

    # =========================================================================
    # 2. (SUPPRIMÉ — voir init_contracts_db.py)
    # =========================================================================
    contracts_data = [
        # -------------------------------------------------------------
        # CONTRAT 1 (Nefoussi Fedi) : Solife Avenir Épargne
        # -------------------------------------------------------------
        {
            "contract_number": "SOL-2022-7710",
            "produit": {
                "code": "SL-AVENIR",
                "nom": "Solife Avenir Épargne",
                "type": "Multisupport Assurance-Vie",
                "statut": "En vigueur",
                "devise": "EUR"
            },
            "dates": {
                "date_souscription": "2022-04-10",
                "date_effet": "2022-04-11",
                "date_echeance": "2042-04-10",
                "anciennete_annees": 4
            },
            "parties_prenantes": {
                "preneur": { "party_id": "TP-10001", "nom": "Nefoussi Fedi", "qualite": "Souscripteur" },
                "assure": { "party_id": "TP-10001", "nom": "Nefoussi Fedi", "qualite": "Assuré principal" },
                "payeur": { "party_id": "TP-10001", "nom": "Nefoussi Fedi" },
                "clause_beneficiaire": {
                    "texte": "Mon conjoint, à défaut mes enfants nés ou à naître par parts égales, à défaut mes héritiers.",
                    "beneficiaires": [
                        { "nom": "Conjoint", "relation": "Épouse", "part_pourcentage": 100 }
                    ]
                }
            },
            "situation_financiere": {
                "valeur_rachat_totale": 85400.00,
                "cumul_versements_bruts": 72000.00,
                "plus_values_latentes": 13400.00,
                "rendement_annuel": "4.25%",
                "frais_gestion_annuels": "0.75%"
            },
            "versements": {
                "mode": "Programmé mensuel",
                "montant_mensuel": 300.00,
                "jour_prelevement": 5,
                "prochain_prelevement": "2026-09-05"
            },
            "repartition_investissements": {
                "fonds_euros": {
                    "nom": "Solife Actif Général Garanti",
                    "montant": 55510.00,
                    "pourcentage": 65.0,
                    "taux_garanti": "1.00%"
                },
                "unites_de_compte": [
                    {
                        "isin": "FR0010148981",
                        "nom": "Solife Actions Monde Croissance",
                        "montant": 29890.00,
                        "pourcentage": 35.0,
                        "performance_ytd": "+6.8%"
                    }
                ]
            },
            "options_gestion": {
                "rebalancing_automatique": True,
                "frequence_rebalancing": "Semestrielle",
                "securisation_plus_values": True,
                "garantie_plancher_deces": True
            }
        },
        # -------------------------------------------------------------
        # CONTRAT 2 (Nefoussi Fedi) : Solife Plan Retraite Sérénité
        # -------------------------------------------------------------
        {
            "contract_number": "SOL-2024-3320",
            "produit": {
                "code": "SL-RETRAITE",
                "nom": "Solife Plan Retraite Sérénité",
                "type": "PER Assurance-Vie",
                "statut": "En vigueur",
                "devise": "EUR"
            },
            "dates": {
                "date_souscription": "2024-01-15",
                "date_effet": "2024-01-16",
                "date_echeance": "2044-01-15",
                "anciennete_annees": 2
            },
            "parties_prenantes": {
                "preneur": { "party_id": "TP-10001", "nom": "Nefoussi Fedi", "qualite": "Souscripteur" },
                "assure": { "party_id": "TP-10001", "nom": "Nefoussi Fedi", "qualite": "Assuré principal" },
                "payeur": { "party_id": "TP-10001", "nom": "Nefoussi Fedi" },
                "clause_beneficiaire": {
                    "texte": "Mes enfants par parts égales.",
                    "beneficiaires": [
                        { "nom": "Enfants nés ou à naître", "relation": "Enfants", "part_pourcentage": 100 }
                    ]
                }
            },
            "situation_financiere": {
                "valeur_rachat_totale": 32150.00,
                "cumul_versements_bruts": 28000.00,
                "plus_values_latentes": 4150.00,
                "rendement_annuel": "3.90%",
                "frais_gestion_annuels": "0.60%"
            },
            "versements": {
                "mode": "Programmé mensuel",
                "montant_mensuel": 200.00,
                "jour_prelevement": 10,
                "prochain_prelevement": "2026-09-10"
            },
            "repartition_investissements": {
                "fonds_euros": {
                    "nom": "Solife Actif Général Garanti",
                    "montant": 16075.00,
                    "pourcentage": 50.0,
                    "taux_garanti": "1.00%"
                },
                "unites_de_compte": [
                    {
                        "isin": "FR0000295230",
                        "nom": "Solife Éco Responsable ESG",
                        "montant": 16075.00,
                        "pourcentage": 50.0,
                        "performance_ytd": "+5.1%"
                    }
                ]
            },
            "options_gestion": {
                "rebalancing_automatique": False,
                "frequence_rebalancing": "Aucune",
                "securisation_plus_values": False,
                "garantie_plancher_deces": True
            }
        },
        # -------------------------------------------------------------
        # CONTRAT 3 (Ben Salah Dorra) : Solife Sérénité Patrimoine
        # -------------------------------------------------------------
        {
            "contract_number": "SOL-2023-5540",
            "produit": {
                "code": "SL-PATRIMOINE",
                "nom": "Solife Sérénité Patrimoine",
                "type": "Multisupport Haut de Gamme",
                "statut": "En vigueur",
                "devise": "EUR"
            },
            "dates": {
                "date_souscription": "2023-06-20",
                "date_effet": "2023-06-21",
                "date_echeance": "2043-06-20",
                "anciennete_annees": 3
            },
            "parties_prenantes": {
                "preneur": { "party_id": "TP-10002", "nom": "Ben Salah Dorra", "qualite": "Souscripteur" },
                "assure": { "party_id": "TP-10002", "nom": "Ben Salah Dorra", "qualite": "Assuré principal" },
                "payeur": { "party_id": "TP-10002", "nom": "Ben Salah Dorra" },
                "clause_beneficiaire": {
                    "texte": "Mes parents par parts égales, à défaut mes frères et sœurs.",
                    "beneficiaires": [
                        { "nom": "Parents", "relation": "Ascendants", "part_pourcentage": 100 }
                    ]
                }
            },
            "situation_financiere": {
                "valeur_rachat_totale": 62800.00,
                "cumul_versements_bruts": 55000.00,
                "plus_values_latentes": 7800.00,
                "rendement_annuel": "4.80%",
                "frais_gestion_annuels": "0.70%"
            },
            "versements": {
                "mode": "Versements libres",
                "montant_mensuel": 0,
                "jour_prelevement": None,
                "prochain_prelevement": None
            },
            "repartition_investissements": {
                "fonds_euros": {
                    "nom": "Solife Actif Général Garanti",
                    "montant": 25120.00,
                    "pourcentage": 40.0,
                    "taux_garanti": "1.00%"
                },
                "unites_de_compte": [
                    {
                        "isin": "FR0010998877",
                        "nom": "Solife Tech & Intelligence Artificielle",
                        "montant": 25120.00,
                        "pourcentage": 40.0,
                        "performance_ytd": "+9.4%"
                    },
                    {
                        "isin": "FR0000445566",
                        "nom": "Solife Immobilier Premium SCPI",
                        "montant": 12560.00,
                        "pourcentage": 20.0,
                        "performance_ytd": "+3.6%"
                    }
                ]
            },
            "options_gestion": {
                "rebalancing_automatique": True,
                "frequence_rebalancing": "Trimestrielle",
                "securisation_plus_values": True,
                "garantie_plancher_deces": True
            }
        },
        # -------------------------------------------------------------
        # CONTRAT 4 (Ben Salah Dorra) : Solife Protection Santé & Prévoyance
        # -------------------------------------------------------------
        {
            "contract_number": "SOL-2025-1190",
            "produit": {
                "code": "SL-PROTECT",
                "nom": "Solife Protection Santé & Prévoyance",
                "type": "Prévoyance & Capital Décès",
                "statut": "En vigueur",
                "devise": "EUR"
            },
            "dates": {
                "date_souscription": "2025-02-01",
                "date_effet": "2025-02-02",
                "date_echeance": "2045-02-01",
                "anciennete_annees": 1
            },
            "parties_prenantes": {
                "preneur": { "party_id": "TP-10002", "nom": "Ben Salah Dorra", "qualite": "Souscripteur" },
                "assure": { "party_id": "TP-10002", "nom": "Ben Salah Dorra", "qualite": "Assuré principal" },
                "payeur": { "party_id": "TP-10002", "nom": "Ben Salah Dorra" },
                "clause_beneficiaire": {
                    "texte": "Héritiers légaux.",
                    "beneficiaires": [
                        { "nom": "Héritiers légaux", "relation": "Famille", "part_pourcentage": 100 }
                    ]
                }
            },
            "situation_financiere": {
                "valeur_rachat_totale": 18500.00,
                "cumul_versements_bruts": 17000.00,
                "plus_values_latentes": 1500.00,
                "capital_deces_garanti": 100000.00,
                "rendement_annuel": "3.10%",
                "frais_gestion_annuels": "0.50%"
            },
            "versements": {
                "mode": "Programmé mensuel",
                "montant_mensuel": 150.00,
                "jour_prelevement": 1,
                "prochain_prelevement": "2026-09-01"
            },
            "repartition_investissements": {
                "fonds_euros": {
                    "nom": "Solife Actif Général Garanti",
                    "montant": 18500.00,
                    "pourcentage": 100.0,
                    "taux_garanti": "1.50%"
                },
                "unites_de_compte": []
            },
            "options_gestion": {
                "rebalancing_automatique": False,
                "frequence_rebalancing": "Aucune",
                "securisation_plus_values": False,
                "garantie_plancher_deces": True
            }
        }
    ]
    # Note: Les données contrats ci-dessus sont conservées pour référence uniquement.
    # Elles ne sont PAS insérées ici. Utiliser init_contracts_db.py à la place.

    # =========================================================================
    # 3. CRÉATION DES INDEX DE SÉCURITÉ ET RAPIDITÉ
    # =========================================================================
    db.users.create_index("username", unique=True)

    print("\n[+] Initialisation terminee avec succes !")
    print("-------------------------------------------------------------")
    print("Comptes disponibles pour tester :")
    print("  1. Collaborateur : login='collaborateur' / mot de passe='password123'")
    print("  2. Client 1 (Nefoussi Fedi) : login='fedi.nefoussi' / mot de passe='password123'")
    print("  3. Client 2 (Ben Salah Dorra) : login='dorra.bensalah' / mot de passe='password123'")
    print("-------------------------------------------------------------")
    print("[!] N'oubliez pas d'exécuter init_contracts_db.py pour la base solife_contracts !")
    print("-------------------------------------------------------------")

if __name__ == "__main__":
    init_db()
