// Script d'initialisation MongoDB directement exécutable via mongosh ou Docker
const dbInstance = db.getSiblingDB("solife");

print("🧹 Nettoyage des collections 'users' et 'contracts'...");
dbInstance.users.drop();
dbInstance.contracts.drop();

// 1. UTILISATEURS (users)
// Note: mot de passe "password123" haché en SHA-256 : 
// "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f"
const passwordHash = "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f";

dbInstance.users.insertMany([
  {
    "username": "collaborateur",
    "password": passwordHash,
    "role": "collaborateur",
    "nom": "Équipe Interne Solife",
    "statut": "actif"
  },
  {
    "username": "admin",
    "password": passwordHash,
    "role": "collaborateur",
    "nom": "Administrateur Solife",
    "statut": "actif"
  },
  {
    "username": "fedi.nefoussi",
    "password": passwordHash,
    "role": "client",
    "party_id": "TP-10001",
    "nom": "Nefoussi Fedi",
    "email": "fedi.nefoussi@solife.com",
    "telephone": "+33 6 11 22 33 44",
    "statut": "actif"
  },
  {
    "username": "dorra.bensalah",
    "password": passwordHash,
    "role": "client",
    "party_id": "TP-10002",
    "nom": "Ben Salah Dorra",
    "email": "dorra.bensalah@solife.com",
    "telephone": "+33 6 55 66 77 88",
    "statut": "actif"
  }
]);
print("✅ Utilisateurs insérés avec succès.");

// 2. CONTRATS (contracts)
dbInstance.contracts.insertMany([
  // Contrat 1 (Nefoussi Fedi)
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
      "rebalancing_automatique": true,
      "frequence_rebalancing": "Semestrielle",
      "securisation_plus_values": true,
      "garantie_plancher_deces": true
    }
  },
  // Contrat 2 (Nefoussi Fedi)
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
      "rebalancing_automatique": false,
      "frequence_rebalancing": "Aucune",
      "securisation_plus_values": false,
      "garantie_plancher_deces": true
    }
  },
  // Contrat 3 (Ben Salah Dorra)
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
      "jour_prelevement": null,
      "prochain_prelevement": null
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
      "rebalancing_automatique": true,
      "frequence_rebalancing": "Trimestrielle",
      "securisation_plus_values": true,
      "garantie_plancher_deces": true
    }
  },
  // Contrat 4 (Ben Salah Dorra)
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
      "rebalancing_automatique": false,
      "frequence_rebalancing": "Aucune",
      "securisation_plus_values": false,
      "garantie_plancher_deces": true
    }
  }
]);

print("✅ Contrats insérés avec succès.");
print("🚀 Base de données Solife prête !");
