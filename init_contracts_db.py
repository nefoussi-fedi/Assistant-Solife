import os
import sys
from pymongo import MongoClient

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def init_contracts_db():
    mongo_host = os.environ.get("MONGO_HOST", "localhost")
    mongo_port = int(os.environ.get("MONGO_PORT", 27017))
    mongo_uri = f"mongodb://{mongo_host}:{mongo_port}/"

    print(f"[*] Connexion à MongoDB sur {mongo_uri}...")
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)

    # Vérification connexion
    try:
        client.admin.command("ping")
        print("[+] Connexion à MongoDB réussie !")
    except Exception as e:
        print(f"[-] Impossible de joindre MongoDB : {e}")
        return

    # =====================================================================
    # BASES DE DONNÉES : solife_contracts & solife (synchronisées)
    # =====================================================================
    target_dbs = [client["solife_contracts"], client["solife"]]

    collections_to_clean = [
        "contracts", "coverages", "investment_services", "avenants",
        "beneficiaires", "commissions", "bills", "transactions",
        "produits", "fonds", "tarifs", "taxes"
    ]
    for d in target_dbs:
        for col_name in collections_to_clean:
            d[col_name].drop()
    print("[*] Collections nettoyées dans solife_contracts et solife.")

    # =====================================================================
    # 1. PRODUITS — Catalogue des produits Solife
    # =====================================================================
    produits_data = [
        {
            "produit_code": "SL-AVENIR",
            "nom": "Solife Avenir Épargne",
            "type": "Multisupport Assurance-Vie",
            "description": "Contrat d'assurance-vie multisupport combinant fonds en euros garanti et unités de compte pour une gestion patrimoniale diversifiée.",
            "devise": "EUR",
            "pays": "FR",
            "tarif_code": "TAR-AVENIR-2022",
            "statut": "Commercialisé",
            "versement_initial_minimum": 1000.00,
            "versement_programme_minimum": 50.00,
            "fonds_eligibles": ["FND-EURO-001", "FND-UC-001", "FND-UC-002", "FND-UC-003"],
            "options_disponibles": [
                "Rebalancing automatique",
                "Sécurisation des plus-values",
                "Garantie plancher décès",
                "Stop-loss",
                "Dynamisation des intérêts"
            ],
            "duree_recommandee_annees": 8,
            "avantage_fiscal": "Fiscalité avantageuse après 8 ans (abattement de 4 600 € / 9 200 €)"
        },
        {
            "produit_code": "SL-RETRAITE",
            "nom": "Solife Plan Retraite Sérénité",
            "type": "PER Assurance-Vie",
            "description": "Plan d'Épargne Retraite individuel combinant avantage fiscal à l'entrée et sortie en capital ou rente à la retraite.",
            "devise": "EUR",
            "pays": "FR",
            "tarif_code": "TAR-RETRAITE-2024",
            "statut": "Commercialisé",
            "versement_initial_minimum": 500.00,
            "versement_programme_minimum": 50.00,
            "fonds_eligibles": ["FND-EURO-001", "FND-UC-002"],
            "options_disponibles": [
                "Gestion pilotée par horizon",
                "Garantie plancher décès",
                "Sortie en rente viagère"
            ],
            "duree_recommandee_annees": 15,
            "avantage_fiscal": "Déductibilité des versements du revenu imposable (plafond 10% des revenus nets)"
        },
        {
            "produit_code": "SL-PATRIMOINE",
            "nom": "Solife Sérénité Patrimoine",
            "type": "Multisupport Haut de Gamme",
            "description": "Contrat d'assurance-vie haut de gamme avec accès élargi aux unités de compte thématiques (Tech, SCPI, ESG) et gestion patrimoniale personnalisée.",
            "devise": "EUR",
            "pays": "FR",
            "tarif_code": "TAR-PATRIMOINE-2023",
            "statut": "Commercialisé",
            "versement_initial_minimum": 5000.00,
            "versement_programme_minimum": 100.00,
            "fonds_eligibles": ["FND-EURO-001", "FND-UC-001", "FND-UC-002", "FND-UC-003", "FND-UC-004"],
            "options_disponibles": [
                "Rebalancing automatique",
                "Sécurisation des plus-values",
                "Garantie plancher décès",
                "Stop-loss",
                "Mandat de gestion conseillée"
            ],
            "duree_recommandee_annees": 8,
            "avantage_fiscal": "Fiscalité avantageuse après 8 ans (abattement de 4 600 € / 9 200 €)"
        },
        {
            "produit_code": "SL-PROTECT",
            "nom": "Solife Protection Santé & Prévoyance",
            "type": "Prévoyance & Capital Décès",
            "description": "Contrat de prévoyance garantissant un capital décès fixe aux bénéficiaires, avec option d'épargne complémentaire en fonds en euros.",
            "devise": "EUR",
            "pays": "FR",
            "tarif_code": "TAR-PROTECT-2025",
            "statut": "Commercialisé",
            "versement_initial_minimum": 500.00,
            "versement_programme_minimum": 30.00,
            "fonds_eligibles": ["FND-EURO-001"],
            "options_disponibles": [
                "Garantie plancher décès",
                "Doublement accidentel",
                "Rente éducation"
            ],
            "duree_recommandee_annees": 20,
            "avantage_fiscal": "Exonération des capitaux décès (article 990I CGI) selon conditions"
        }
    ]
    db.produits.insert_many(produits_data)
    print(f"[+] {len(produits_data)} produits insérés dans 'produits'.")

    # =====================================================================
    # 2. FONDS — Référentiel des supports d'investissement
    # =====================================================================
    fonds_data = [
        {
            "fonds_code": "FND-EURO-001",
            "nom": "Solife Actif Général Garanti",
            "type": "Fonds en euros",
            "isin": None,
            "devise": "EUR",
            "taux_garanti": 1.00,
            "rendement_2024": 2.80,
            "rendement_2025": 3.10,
            "actif_total": 2500000000.00,
            "gestionnaire": "Solife Gestion d'Actifs",
            "niveau_risque_srri": 1,
            "label_esg": False,
            "statut": "Ouvert"
        },
        {
            "fonds_code": "FND-UC-001",
            "nom": "Solife Actions Monde Croissance",
            "type": "Unité de compte - Actions internationales",
            "isin": "FR0010148981",
            "devise": "EUR",
            "performance_ytd": 6.8,
            "performance_1an": 12.3,
            "performance_3ans": 28.5,
            "performance_5ans": 45.2,
            "niveau_risque_srri": 5,
            "frais_courants": 1.60,
            "gestionnaire": "Solife AM",
            "label_esg": False,
            "statut": "Ouvert"
        },
        {
            "fonds_code": "FND-UC-002",
            "nom": "Solife Éco Responsable ESG",
            "type": "Unité de compte - Actions ESG",
            "isin": "FR0000295230",
            "devise": "EUR",
            "performance_ytd": 5.1,
            "performance_1an": 8.7,
            "performance_3ans": 19.4,
            "niveau_risque_srri": 4,
            "frais_courants": 1.45,
            "gestionnaire": "Solife AM",
            "label_esg": True,
            "labels": ["ISR", "Greenfin"],
            "statut": "Ouvert"
        },
        {
            "fonds_code": "FND-UC-003",
            "nom": "Solife Tech & Intelligence Artificielle",
            "type": "Unité de compte - Actions thématiques",
            "isin": "FR0010998877",
            "devise": "EUR",
            "performance_ytd": 9.4,
            "performance_1an": 18.6,
            "performance_3ans": 42.1,
            "niveau_risque_srri": 6,
            "frais_courants": 1.85,
            "gestionnaire": "Solife AM",
            "label_esg": False,
            "statut": "Ouvert"
        },
        {
            "fonds_code": "FND-UC-004",
            "nom": "Solife Immobilier Premium SCPI",
            "type": "Unité de compte - Immobilier (SCPI)",
            "isin": "FR0000445566",
            "devise": "EUR",
            "performance_ytd": 3.6,
            "performance_1an": 4.2,
            "performance_3ans": 12.8,
            "niveau_risque_srri": 3,
            "frais_courants": 2.10,
            "gestionnaire": "Solife Immobilier",
            "label_esg": False,
            "statut": "Ouvert"
        }
    ]
    db.fonds.insert_many(fonds_data)
    print(f"[+] {len(fonds_data)} fonds insérés dans 'fonds'.")

    # =====================================================================
    # 3. TARIFS — Grilles tarifaires par produit
    # =====================================================================
    tarifs_data = [
        {
            "tarif_code": "TAR-AVENIR-2022", "produit_code": "SL-AVENIR", "version": "2022-V1", "date_effet": "2022-01-01", "statut": "En vigueur",
            "frais": {"frais_entree_max": 3.00, "frais_entree_negocies": 2.00, "frais_gestion_fonds_euros": 0.75, "frais_gestion_uc": 0.90, "frais_arbitrage_en_ligne": 0.00, "frais_arbitrage_papier": 0.50, "frais_sortie": 0.00, "penalite_rachat_avant_4ans": 1.00},
            "baremes_garantie_deces": [{"tranche_age": "18-45", "taux_prime_annuel": 0.12}, {"tranche_age": "46-55", "taux_prime_annuel": 0.25}, {"tranche_age": "56-65", "taux_prime_annuel": 0.55}, {"tranche_age": "66-75", "taux_prime_annuel": 1.20}],
            "commission_distribution": {"taux_entree": 2.00, "taux_recurrent_annuel": 0.30, "taux_encours_uc": 0.10}
        },
        {
            "tarif_code": "TAR-RETRAITE-2024", "produit_code": "SL-RETRAITE", "version": "2024-V1", "date_effet": "2024-01-01", "statut": "En vigueur",
            "frais": {"frais_entree_max": 2.50, "frais_entree_negocies": 1.50, "frais_gestion_fonds_euros": 0.60, "frais_gestion_uc": 0.80, "frais_arbitrage_en_ligne": 0.00, "frais_arbitrage_papier": 0.50, "frais_sortie": 0.00},
            "baremes_garantie_deces": [{"tranche_age": "18-45", "taux_prime_annuel": 0.10}, {"tranche_age": "46-55", "taux_prime_annuel": 0.20}, {"tranche_age": "56-65", "taux_prime_annuel": 0.45}, {"tranche_age": "66-75", "taux_prime_annuel": 1.00}],
            "commission_distribution": {"taux_entree": 1.50, "taux_recurrent_annuel": 0.25, "taux_encours_uc": 0.08}
        },
        {
            "tarif_code": "TAR-PATRIMOINE-2023", "produit_code": "SL-PATRIMOINE", "version": "2023-V1", "date_effet": "2023-01-01", "statut": "En vigueur",
            "frais": {"frais_entree_max": 2.00, "frais_entree_negocies": 1.00, "frais_gestion_fonds_euros": 0.70, "frais_gestion_uc": 0.85, "frais_arbitrage_en_ligne": 0.00, "frais_arbitrage_papier": 0.30, "frais_sortie": 0.00},
            "baremes_garantie_deces": [{"tranche_age": "18-45", "taux_prime_annuel": 0.11}, {"tranche_age": "46-55", "taux_prime_annuel": 0.22}, {"tranche_age": "56-65", "taux_prime_annuel": 0.50}, {"tranche_age": "66-75", "taux_prime_annuel": 1.10}],
            "commission_distribution": {"taux_entree": 1.00, "taux_recurrent_annuel": 0.35, "taux_encours_uc": 0.12}
        },
        {
            "tarif_code": "TAR-PROTECT-2025", "produit_code": "SL-PROTECT", "version": "2025-V1", "date_effet": "2025-01-01", "statut": "En vigueur",
            "frais": {"frais_entree_max": 2.00, "frais_entree_negocies": 1.00, "frais_gestion_fonds_euros": 0.50, "frais_sortie": 0.00},
            "baremes_garantie_deces": [{"tranche_age": "18-45", "taux_prime_annuel": 0.15}, {"tranche_age": "46-55", "taux_prime_annuel": 0.35}, {"tranche_age": "56-65", "taux_prime_annuel": 0.80}, {"tranche_age": "66-75", "taux_prime_annuel": 1.60}],
            "commission_distribution": {"taux_entree": 1.00, "taux_recurrent_annuel": 0.20}
        }
    ]
    db.tarifs.insert_many(tarifs_data)
    print(f"[+] {len(tarifs_data)} tarifs insérés dans 'tarifs'.")

    # =====================================================================
    # 4. TAXES — Régimes fiscaux
    # =====================================================================
    taxes_data = [
        {
            "tax_code": "TAX-FR-AV-2026", "pays": "FR", "type_contrat": "Assurance-Vie", "regime": "Prélèvement Forfaitaire Unique (PFU)", "date_effet": "2026-01-01",
            "regles": {
                "avant_8ans": {"taux_pfu": 30.0, "dont_ir": 12.8, "dont_ps": 17.2},
                "apres_8ans": {"taux_pfu": 24.7, "dont_ir": 7.5, "dont_ps": 17.2, "abattement_celibataire": 4600.00, "abattement_couple": 9200.00},
                "versements_avant_27sept2017": {"option_bareme_progressif": True, "taux_pl_avant_4ans": 35.0, "taux_pl_4_8ans": 15.0, "taux_pl_apres_8ans": 7.5}
            },
            "prelevements_sociaux": {"taux_global": 17.2, "csg": 9.2, "crds": 0.5, "prelevement_solidarite": 7.5}
        },
        {
            "tax_code": "TAX-FR-PER-2026", "pays": "FR", "type_contrat": "PER (Plan Épargne Retraite)", "regime": "Fiscalité PER", "date_effet": "2026-01-01",
            "regles": {
                "phase_epargne": {"deductibilite_versements": True, "plafond_deduction": "10% des revenus nets (max 35 194 €)", "report_plafond_non_utilise": "3 ans"},
                "sortie_capital": {"capital_exonere_si_deduction": False, "imposition_capital": "Barème progressif IR", "imposition_plus_values": "PFU 30% ou barème progressif"},
                "sortie_rente": {"imposition": "Rentes viagères à titre gratuit (barème IR après abattement 10%)"}
            },
            "prelevements_sociaux": {"taux_global": 17.2, "csg": 9.2, "crds": 0.5, "prelevement_solidarite": 7.5}
        }
    ]
    db.taxes.insert_many(taxes_data)
    print(f"[+] {len(taxes_data)} régimes fiscaux insérés dans 'taxes'.")

    # =====================================================================
    # 5. CONTRACTS — Contrats principaux enrichis
    # =====================================================================
    contracts_data = [
        {
            "contract_number": "SOL-2022-7710", "produit_code": "SL-AVENIR", "statut": "En vigueur", "type_contrat": "Multisupport Assurance-Vie", "devise": "EUR", "pays": "FR", "canal_distribution": "Réseau Solife Direct",
            "dates": {"date_souscription": "2022-04-10", "date_effet": "2022-04-11", "date_echeance": "2042-04-10", "date_derniere_modification": "2026-03-15", "anciennete_annees": 4},
            "parties_prenantes": {
                "preneur": {"party_id": "TP-10001", "nom": "Nefoussi Fedi", "qualite": "Souscripteur"},
                "assure": {"party_id": "TP-10001", "nom": "Nefoussi Fedi", "qualite": "Assuré principal", "categorie_risque": "Standard", "fumeur": False},
                "payeur": {"party_id": "TP-10001", "nom": "Nefoussi Fedi", "mode_paiement": "Prélèvement SEPA", "iban_masque": "FR76 **** **** **** **** ***4 12"}
            },
            "situation_financiere": {"valeur_rachat_totale": 85400.00, "cumul_versements_bruts": 72000.00, "cumul_versements_nets": 70560.00, "plus_values_latentes": 13400.00, "rendement_annuel": 4.25, "rendement_cumule": 18.61, "frais_gestion_annuels": 0.75, "frais_entree": 2.00, "frais_sortie": 0.00, "frais_arbitrage": 0.50},
            "versements_programmes": {"mode": "Programmé mensuel", "montant_mensuel": 300.00, "jour_prelevement": 5, "prochain_prelevement": "2026-09-05", "total_versements_annee_en_cours": 2400.00, "date_dernier_versement": "2026-08-05"},
            "options_gestion": {"rebalancing_automatique": True, "frequence_rebalancing": "Semestrielle", "securisation_plus_values": True, "seuil_securisation_pct": 10.0, "garantie_plancher_deces": True, "stop_loss": False, "dynamisation_interets": False},
            "fiscalite": {"regime_fiscal": "Assurance-Vie Droit Français", "tax_code": "TAX-FR-AV-2026", "date_dernier_rachat": "2025-07-10", "abattement_applicable": False, "duree_detention_fiscale_annees": 4}
        },
        {
            "contract_number": "SOL-2024-3320", "produit_code": "SL-RETRAITE", "statut": "En vigueur", "type_contrat": "PER Assurance-Vie", "devise": "EUR", "pays": "FR", "canal_distribution": "Réseau Solife Direct",
            "dates": {"date_souscription": "2024-01-15", "date_effet": "2024-01-16", "date_echeance": "2044-01-15", "date_derniere_modification": "2024-01-15", "anciennete_annees": 2},
            "parties_prenantes": {
                "preneur": {"party_id": "TP-10001", "nom": "Nefoussi Fedi", "qualite": "Souscripteur"},
                "assure": {"party_id": "TP-10001", "nom": "Nefoussi Fedi", "qualite": "Assuré principal", "categorie_risque": "Standard", "fumeur": False},
                "payeur": {"party_id": "TP-10001", "nom": "Nefoussi Fedi", "mode_paiement": "Prélèvement SEPA", "iban_masque": "FR76 **** **** **** **** ***4 12"}
            },
            "situation_financiere": {"valeur_rachat_totale": 32150.00, "cumul_versements_bruts": 28000.00, "cumul_versements_nets": 27580.00, "plus_values_latentes": 4150.00, "rendement_annuel": 3.90, "rendement_cumule": 7.68, "frais_gestion_annuels": 0.60, "frais_entree": 1.50, "frais_sortie": 0.00, "frais_arbitrage": 0.50},
            "versements_programmes": {"mode": "Programmé mensuel", "montant_mensuel": 200.00, "jour_prelevement": 10, "prochain_prelevement": "2026-09-10", "total_versements_annee_en_cours": 1600.00, "date_dernier_versement": "2026-08-10"},
            "options_gestion": {"rebalancing_automatique": False, "frequence_rebalancing": "Aucune", "securisation_plus_values": False, "garantie_plancher_deces": True, "stop_loss": False, "dynamisation_interets": False},
            "fiscalite": {"regime_fiscal": "PER Individuel", "tax_code": "TAX-FR-PER-2026", "date_dernier_rachat": None, "abattement_applicable": False, "duree_detention_fiscale_annees": 2}
        },
        {
            "contract_number": "SOL-2023-5540", "produit_code": "SL-PATRIMOINE", "statut": "En vigueur", "type_contrat": "Multisupport Haut de Gamme", "devise": "EUR", "pays": "FR", "canal_distribution": "Réseau Solife Premium",
            "dates": {"date_souscription": "2023-06-20", "date_effet": "2023-06-21", "date_echeance": "2043-06-20", "date_derniere_modification": "2026-01-10", "anciennete_annees": 3},
            "parties_prenantes": {
                "preneur": {"party_id": "TP-10002", "nom": "Ben Salah Dorra", "qualite": "Souscripteur"},
                "assure": {"party_id": "TP-10002", "nom": "Ben Salah Dorra", "qualite": "Assuré principal", "categorie_risque": "Standard", "fumeur": False},
                "payeur": {"party_id": "TP-10002", "nom": "Ben Salah Dorra", "mode_paiement": "Prélèvement SEPA", "iban_masque": "FR76 **** **** **** **** ***8 55"}
            },
            "situation_financiere": {"valeur_rachat_totale": 62800.00, "cumul_versements_bruts": 55000.00, "cumul_versements_nets": 54450.00, "plus_values_latentes": 7800.00, "rendement_annuel": 4.80, "rendement_cumule": 14.18, "frais_gestion_annuels": 0.70, "frais_entree": 1.00, "frais_sortie": 0.00, "frais_arbitrage": 0.30},
            "versements_programmes": {"mode": "Versements libres", "montant_mensuel": 0, "jour_prelevement": None, "prochain_prelevement": None, "total_versements_annee_en_cours": 10000.00, "date_dernier_versement": "2026-03-15"},
            "options_gestion": {"rebalancing_automatique": True, "frequence_rebalancing": "Trimestrielle", "securisation_plus_values": True, "seuil_securisation_pct": 15.0, "garantie_plancher_deces": True, "stop_loss": False, "dynamisation_interets": False},
            "fiscalite": {"regime_fiscal": "Assurance-Vie Droit Français", "tax_code": "TAX-FR-AV-2026", "date_dernier_rachat": None, "abattement_applicable": False, "duree_detention_fiscale_annees": 3}
        },
        {
            "contract_number": "SOL-2025-1190", "produit_code": "SL-PROTECT", "statut": "En vigueur", "type_contrat": "Prévoyance & Capital Décès", "devise": "EUR", "pays": "FR", "canal_distribution": "Réseau Solife Direct",
            "dates": {"date_souscription": "2025-02-01", "date_effet": "2025-02-02", "date_echeance": "2045-02-01", "date_derniere_modification": "2025-02-01", "anciennete_annees": 1},
            "parties_prenantes": {
                "preneur": {"party_id": "TP-10002", "nom": "Ben Salah Dorra", "qualite": "Souscripteur"},
                "assure": {"party_id": "TP-10002", "nom": "Ben Salah Dorra", "qualite": "Assuré principal", "categorie_risque": "Standard", "fumeur": False},
                "payeur": {"party_id": "TP-10002", "nom": "Ben Salah Dorra", "mode_paiement": "Prélèvement SEPA", "iban_masque": "FR76 **** **** **** **** ***8 55"}
            },
            "situation_financiere": {"valeur_rachat_totale": 18500.00, "cumul_versements_bruts": 17000.00, "cumul_versements_nets": 16830.00, "plus_values_latentes": 1500.00, "capital_deces_garanti": 100000.00, "rendement_annuel": 3.10, "rendement_cumule": 3.10, "frais_gestion_annuels": 0.50, "frais_entree": 1.00, "frais_sortie": 0.00},
            "versements_programmes": {"mode": "Programmé mensuel", "montant_mensuel": 150.00, "jour_prelevement": 1, "prochain_prelevement": "2026-09-01", "total_versements_annee_en_cours": 1200.00, "date_dernier_versement": "2026-08-01"},
            "options_gestion": {"rebalancing_automatique": False, "frequence_rebalancing": "Aucune", "securisation_plus_values": False, "garantie_plancher_deces": True, "stop_loss": False, "dynamisation_interets": False},
            "fiscalite": {"regime_fiscal": "Assurance-Vie Droit Français", "tax_code": "TAX-FR-AV-2026", "date_dernier_rachat": None, "abattement_applicable": False, "duree_detention_fiscale_annees": 1}
        }
    ]
    db.contracts.insert_many(contracts_data)
    print(f"[+] {len(contracts_data)} contrats insérés dans 'contracts'.")

    # =====================================================================
    # 6. COVERAGES — Garanties et couvertures
    # =====================================================================
    coverages_data = [
        {"coverage_id": "COV-7710-001", "contract_number": "SOL-2022-7710", "type_couverture": "Garantie Décès Plancher", "statut": "Active", "date_effet": "2022-04-11", "date_expiration": "2042-04-10", "details": {"capital_garanti": 72000.00, "mode_calcul": "Cumul des versements bruts", "plafond_age_assure": 75, "exclusions": ["Suicide dans les 2 premières années", "Pratique de sports extrêmes non déclarés"], "surprime_applicable": False}, "prime_annuelle": 86.40, "beneficiaires_associes": ["BEN-7710-001", "BEN-7710-002", "BEN-7710-003"]},
        {"coverage_id": "COV-7710-002", "contract_number": "SOL-2022-7710", "type_couverture": "Sécurisation automatique des plus-values", "statut": "Active", "date_effet": "2022-04-11", "details": {"seuil_declenchement": "10% de plus-values latentes", "fonds_destination": "FND-EURO-001", "frequence_controle": "Mensuelle"}, "prime_annuelle": 0.00},
        {"coverage_id": "COV-3320-001", "contract_number": "SOL-2024-3320", "type_couverture": "Garantie Décès Plancher", "statut": "Active", "date_effet": "2024-01-16", "date_expiration": "2044-01-15", "details": {"capital_garanti": 28000.00, "mode_calcul": "Cumul des versements bruts", "plafond_age_assure": 75, "exclusions": ["Suicide dans les 2 premières années"], "surprime_applicable": False}, "prime_annuelle": 28.00, "beneficiaires_associes": ["BEN-3320-001"]},
        {"coverage_id": "COV-5540-001", "contract_number": "SOL-2023-5540", "type_couverture": "Garantie Décès Plancher", "statut": "Active", "date_effet": "2023-06-21", "date_expiration": "2043-06-20", "details": {"capital_garanti": 55000.00, "mode_calcul": "Cumul des versements bruts", "plafond_age_assure": 75, "exclusions": ["Suicide dans les 2 premières années"], "surprime_applicable": False}, "prime_annuelle": 60.50, "beneficiaires_associes": ["BEN-5540-001", "BEN-5540-002"]},
        {"coverage_id": "COV-1190-001", "contract_number": "SOL-2025-1190", "type_couverture": "Capital Décès Toutes Causes", "statut": "Active", "date_effet": "2025-02-02", "date_expiration": "2045-02-01", "details": {"capital_garanti": 100000.00, "mode_calcul": "Capital fixe", "franchise_jours": 0, "conditions_speciales": "Doublement du capital en cas de décès accidentel (200 000 €)", "exclusions": ["Suicide dans la première année", "Guerre et actes terroristes", "Pratique aérienne non commerciale"], "surprime_applicable": False}, "prime_annuelle": 420.00, "beneficiaires_associes": ["BEN-1190-001"]},
        {"coverage_id": "COV-1190-002", "contract_number": "SOL-2025-1190", "type_couverture": "Rente Éducation", "statut": "Active", "date_effet": "2025-02-02", "details": {"montant_rente_annuelle": 6000.00, "duree_versement": "Jusqu'au 25ème anniversaire de chaque enfant", "beneficiaires": "Enfants à charge au moment du décès", "conditions": "Versée trimestriellement"}, "prime_annuelle": 180.00}
    ]
    db.coverages.insert_many(coverages_data)
    print(f"[+] {len(coverages_data)} couvertures insérées dans 'coverages'.")

    # =====================================================================
    # 7. INVESTMENT_SERVICES — Portefeuille d'investissement
    # =====================================================================
    investment_data = [
        {
            "investment_id": "INV-7710-001", "contract_number": "SOL-2022-7710", "profil_investisseur": "Équilibré", "horizon_placement": "Long terme (> 8 ans)", "date_derniere_allocation": "2026-06-15",
            "allocation": [
                {"fonds_code": "FND-EURO-001", "nom": "Solife Actif Général Garanti", "type": "Fonds en euros", "montant": 55510.00, "pourcentage": 65.0, "taux_garanti": 1.00, "rendement_2025": 3.10},
                {"fonds_code": "FND-UC-001", "nom": "Solife Actions Monde Croissance", "type": "Unité de compte - Actions", "isin": "FR0010148981", "montant": 29890.00, "pourcentage": 35.0, "performance_ytd": 6.8, "performance_1an": 12.3, "niveau_risque_srri": 5, "frais_courants": 1.60}
            ],
            "historique_arbitrages": [
                {"date": "2025-12-10", "type": "Rebalancing automatique", "montant": 3200.00, "de_fonds": "FND-UC-001", "vers_fonds": "FND-EURO-001", "motif": "Rééquilibrage semestriel — UC surperformantes"},
                {"date": "2025-06-12", "type": "Rebalancing automatique", "montant": 1800.00, "de_fonds": "FND-EURO-001", "vers_fonds": "FND-UC-001", "motif": "Rééquilibrage semestriel — correction de marché"}
            ]
        },
        {
            "investment_id": "INV-3320-001", "contract_number": "SOL-2024-3320", "profil_investisseur": "Prudent", "horizon_placement": "Très long terme (retraite)", "date_derniere_allocation": "2024-01-16",
            "allocation": [
                {"fonds_code": "FND-EURO-001", "nom": "Solife Actif Général Garanti", "type": "Fonds en euros", "montant": 16075.00, "pourcentage": 50.0, "taux_garanti": 1.00, "rendement_2025": 3.10},
                {"fonds_code": "FND-UC-002", "nom": "Solife Éco Responsable ESG", "type": "Unité de compte - ESG", "isin": "FR0000295230", "montant": 16075.00, "pourcentage": 50.0, "performance_ytd": 5.1, "niveau_risque_srri": 4, "frais_courants": 1.45}
            ],
            "historique_arbitrages": []
        },
        {
            "investment_id": "INV-5540-001", "contract_number": "SOL-2023-5540", "profil_investisseur": "Dynamique", "horizon_placement": "Long terme (> 8 ans)", "date_derniere_allocation": "2026-03-15",
            "allocation": [
                {"fonds_code": "FND-EURO-001", "nom": "Solife Actif Général Garanti", "type": "Fonds en euros", "montant": 25120.00, "pourcentage": 40.0, "taux_garanti": 1.00, "rendement_2025": 3.10},
                {"fonds_code": "FND-UC-003", "nom": "Solife Tech & Intelligence Artificielle", "type": "Unité de compte - Actions thématiques", "isin": "FR0010998877", "montant": 25120.00, "pourcentage": 40.0, "performance_ytd": 9.4, "niveau_risque_srri": 6, "frais_courants": 1.85},
                {"fonds_code": "FND-UC-004", "nom": "Solife Immobilier Premium SCPI", "type": "Unité de compte - SCPI", "isin": "FR0000445566", "montant": 12560.00, "pourcentage": 20.0, "performance_ytd": 3.6, "niveau_risque_srri": 3, "frais_courants": 2.10}
            ],
            "historique_arbitrages": [{"date": "2026-01-10", "type": "Rebalancing automatique", "montant": 4500.00, "de_fonds": "FND-UC-003", "vers_fonds": "FND-EURO-001", "motif": "Rééquilibrage trimestriel — sécurisation des gains Tech"}]
        },
        {
            "investment_id": "INV-1190-001", "contract_number": "SOL-2025-1190", "profil_investisseur": "Sécuritaire", "horizon_placement": "Très long terme (prévoyance)", "date_derniere_allocation": "2025-02-02",
            "allocation": [{"fonds_code": "FND-EURO-001", "nom": "Solife Actif Général Garanti", "type": "Fonds en euros", "montant": 18500.00, "pourcentage": 100.0, "taux_garanti": 1.50, "rendement_2025": 3.10}],
            "historique_arbitrages": []
        }
    ]
    db.investment_services.insert_many(investment_data)
    print(f"[+] {len(investment_data)} services d'investissement insérés dans 'investment_services'.")

    # =====================================================================
    # 8. BENEFICIAIRES
    # =====================================================================
    beneficiaires_data = [
        {"beneficiaire_id": "BEN-7710-001", "contract_number": "SOL-2022-7710", "rang": 1, "nom": "Nefoussi Sarah", "relation": "Épouse", "date_naissance": "1990-03-22", "part_pourcentage": 100, "type_designation": "Nominative", "clause_texte": "Mon conjoint, Mme Sarah Nefoussi", "acceptation": False, "date_designation": "2025-01-20"},
        {"beneficiaire_id": "BEN-7710-002", "contract_number": "SOL-2022-7710", "rang": 2, "nom": "Enfants nés ou à naître", "relation": "Enfants", "part_pourcentage": 100, "type_designation": "Générique", "clause_texte": "À défaut, mes enfants nés ou à naître, par parts égales entre eux", "condition": "En cas de prédécès du bénéficiaire de rang 1", "date_designation": "2025-01-20"},
        {"beneficiaire_id": "BEN-7710-003", "contract_number": "SOL-2022-7710", "rang": 3, "nom": "Héritiers légaux", "relation": "Héritiers", "part_pourcentage": 100, "type_designation": "Légale", "clause_texte": "À défaut, mes héritiers", "condition": "En cas de prédécès de tous les bénéficiaires précédents", "date_designation": "2022-04-10"},
        {"beneficiaire_id": "BEN-3320-001", "contract_number": "SOL-2024-3320", "rang": 1, "nom": "Enfants nés ou à naître", "relation": "Enfants", "part_pourcentage": 100, "type_designation": "Générique", "clause_texte": "Mes enfants, nés ou à naître, par parts égales entre eux", "date_designation": "2024-01-15"},
        {"beneficiaire_id": "BEN-3320-002", "contract_number": "SOL-2024-3320", "rang": 2, "nom": "Héritiers légaux", "relation": "Héritiers", "part_pourcentage": 100, "type_designation": "Légale", "clause_texte": "À défaut, mes héritiers", "date_designation": "2024-01-15"},
        {"beneficiaire_id": "BEN-5540-001", "contract_number": "SOL-2023-5540", "rang": 1, "nom": "Ben Salah Ahmed & Ben Salah Fatma", "relation": "Parents (Ascendants)", "part_pourcentage": 100, "type_designation": "Nominative", "clause_texte": "Mes parents, M. Ahmed Ben Salah et Mme Fatma Ben Salah, par parts égales", "acceptation": False, "date_designation": "2023-06-20"},
        {"beneficiaire_id": "BEN-5540-002", "contract_number": "SOL-2023-5540", "rang": 2, "nom": "Frères et sœurs", "relation": "Collatéraux", "part_pourcentage": 100, "type_designation": "Générique", "clause_texte": "À défaut, mes frères et sœurs par parts égales", "condition": "En cas de prédécès des bénéficiaires de rang 1", "date_designation": "2023-06-20"},
        {"beneficiaire_id": "BEN-1190-001", "contract_number": "SOL-2025-1190", "rang": 1, "nom": "Héritiers légaux", "relation": "Famille", "part_pourcentage": 100, "type_designation": "Légale", "clause_texte": "Mes héritiers légaux", "date_designation": "2025-02-01"}
    ]
    db.beneficiaires.insert_many(beneficiaires_data)
    print(f"[+] {len(beneficiaires_data)} bénéficiaires insérés dans 'beneficiaires'.")

    # =====================================================================
    # 9. AVENANTS
    # =====================================================================
    avenants_data = [
        {"avenant_id": "AVN-7710-001", "contract_number": "SOL-2022-7710", "type": "Versement complémentaire", "date_effet": "2023-03-15", "date_demande": "2023-03-10", "statut": "Appliqué", "details": {"montant": 5000.00, "fonds_destination": "FND-EURO-001", "mode_paiement": "Virement bancaire"}, "traite_par": "Système automatique"},
        {"avenant_id": "AVN-7710-002", "contract_number": "SOL-2022-7710", "type": "Versement complémentaire", "date_effet": "2024-06-15", "date_demande": "2024-06-10", "statut": "Appliqué", "details": {"montant": 8000.00, "fonds_destination": "FND-UC-001", "mode_paiement": "Virement bancaire"}, "traite_par": "Système automatique"},
        {"avenant_id": "AVN-7710-003", "contract_number": "SOL-2022-7710", "type": "Modification clause bénéficiaire", "date_effet": "2025-01-20", "date_demande": "2025-01-15", "statut": "Appliqué", "details": {"ancienne_clause": "Mon conjoint, à défaut mes héritiers.", "nouvelle_clause": "Mon conjoint, Mme Sarah Nefoussi, à défaut mes enfants nés ou à naître par parts égales, à défaut mes héritiers.", "document_reference": "AVN-CB-2025-0120"}, "traite_par": "Marie Dupont (Collaborateur)"},
        {"avenant_id": "AVN-7710-004", "contract_number": "SOL-2022-7710", "type": "Modification versement programmé", "date_effet": "2023-09-01", "date_demande": "2023-08-20", "statut": "Appliqué", "details": {"ancien_montant": 250.00, "nouveau_montant": 300.00, "motif": "Augmentation volontaire du client"}, "traite_par": "Système automatique"},
        {"avenant_id": "AVN-7710-005", "contract_number": "SOL-2022-7710", "type": "Rachat partiel", "date_effet": "2025-07-10", "date_demande": "2025-07-05", "statut": "Appliqué", "details": {"montant_brut": 3000.00, "montant_net_fiscal": 2820.00, "prelevement_social": 180.00, "fonds_source": "FND-EURO-001", "motif": "Besoin de trésorerie"}, "traite_par": "Système automatique"},
        {"avenant_id": "AVN-7710-006", "contract_number": "SOL-2022-7710", "type": "Arbitrage", "date_effet": "2024-03-20", "date_demande": "2024-03-18", "statut": "Appliqué", "details": {"montant": 8000.00, "de_fonds": "FND-EURO-001", "vers_fonds": "FND-UC-001", "frais_arbitrage": 40.00, "motif": "Diversification vers les actions"}, "traite_par": "Client (en ligne)"},
        {"avenant_id": "AVN-7710-007", "contract_number": "SOL-2022-7710", "type": "Activation option de gestion", "date_effet": "2022-04-11", "date_demande": "2022-04-10", "statut": "Appliqué", "details": {"option": "Sécurisation des plus-values", "seuil": "10%", "fonds_cible": "FND-EURO-001"}, "traite_par": "Souscription initiale"},
        {"avenant_id": "AVN-5540-001", "contract_number": "SOL-2023-5540", "type": "Versement complémentaire", "date_effet": "2024-12-10", "date_demande": "2024-12-05", "statut": "Appliqué", "details": {"montant": 10000.00, "repartition": {"FND-UC-003": 60, "FND-UC-004": 40}, "mode_paiement": "Virement bancaire"}, "traite_par": "Système automatique"},
        {"avenant_id": "AVN-5540-002", "contract_number": "SOL-2023-5540", "type": "Versement complémentaire", "date_effet": "2026-03-15", "date_demande": "2026-03-10", "statut": "Appliqué", "details": {"montant": 10000.00, "repartition": {"FND-EURO-001": 50, "FND-UC-003": 50}, "mode_paiement": "Chèque"}, "traite_par": "Système automatique"},
        {"avenant_id": "AVN-5540-003", "contract_number": "SOL-2023-5540", "type": "Arbitrage", "date_effet": "2025-09-05", "date_demande": "2025-09-03", "statut": "Appliqué", "details": {"montant": 5000.00, "de_fonds": "FND-UC-003", "vers_fonds": "FND-UC-004", "frais_arbitrage": 15.00, "motif": "Diversification vers l'immobilier"}, "traite_par": "Client (en ligne)"},
        {"avenant_id": "AVN-1190-001", "contract_number": "SOL-2025-1190", "type": "Versement complémentaire", "date_effet": "2025-06-15", "date_demande": "2025-06-10", "statut": "Appliqué", "details": {"montant": 2000.00, "fonds_destination": "FND-EURO-001", "mode_paiement": "Virement bancaire"}, "traite_par": "Système automatique"},
        {"avenant_id": "AVN-1190-002", "contract_number": "SOL-2025-1190", "type": "Ajout couverture", "date_effet": "2025-02-02", "date_demande": "2025-02-01", "statut": "Appliqué", "details": {"couverture_ajoutee": "Rente Éducation", "montant_rente": 6000.00, "prime_supplementaire": 180.00}, "traite_par": "Souscription initiale"}
    ]
    db.avenants.insert_many(avenants_data)
    print(f"[+] {len(avenants_data)} avenants insérés dans 'avenants'.")

    # =====================================================================
    # 10. COMMISSIONS
    # =====================================================================
    commissions_data = [
        {"commission_id": "COMM-7710-001", "contract_number": "SOL-2022-7710", "type": "Commission d'entrée", "taux": 2.00, "montant": 1440.00, "beneficiaire_commission": "Réseau Solife Direct", "date_application": "2022-04-10", "statut": "Versée"},
        {"commission_id": "COMM-7710-002", "contract_number": "SOL-2022-7710", "type": "Commission de gestion récurrente", "taux": 0.30, "montant_annuel": 256.20, "beneficiaire_commission": "Réseau Solife Direct", "frequence": "Annuelle", "derniere_date_versement": "2026-04-10"},
        {"commission_id": "COMM-7710-003", "contract_number": "SOL-2022-7710", "type": "Commission sur encours UC", "taux": 0.10, "montant_annuel": 29.89, "beneficiaire_commission": "Réseau Solife Direct", "fonds_concerne": "FND-UC-001"},
        {"commission_id": "COMM-3320-001", "contract_number": "SOL-2024-3320", "type": "Commission d'entrée", "taux": 1.50, "montant": 420.00, "beneficiaire_commission": "Réseau Solife Direct", "date_application": "2024-01-15", "statut": "Versée"},
        {"commission_id": "COMM-3320-002", "contract_number": "SOL-2024-3320", "type": "Commission de gestion récurrente", "taux": 0.25, "montant_annuel": 80.38, "beneficiaire_commission": "Réseau Solife Direct", "frequence": "Annuelle", "derniere_date_versement": "2026-01-15"},
        {"commission_id": "COMM-5540-001", "contract_number": "SOL-2023-5540", "type": "Commission d'entrée", "taux": 1.00, "montant": 550.00, "beneficiaire_commission": "Réseau Solife Premium", "date_application": "2023-06-20", "statut": "Versée"},
        {"commission_id": "COMM-5540-002", "contract_number": "SOL-2023-5540", "type": "Commission de gestion récurrente", "taux": 0.35, "montant_annuel": 219.80, "beneficiaire_commission": "Réseau Solife Premium", "frequence": "Annuelle", "derniere_date_versement": "2026-06-20"},
        {"commission_id": "COMM-5540-003", "contract_number": "SOL-2023-5540", "type": "Commission sur encours UC", "taux": 0.12, "montant_annuel": 45.22, "beneficiaire_commission": "Réseau Solife Premium", "fonds_concerne": "FND-UC-003"},
        {"commission_id": "COMM-5540-004", "contract_number": "SOL-2023-5540", "type": "Commission sur encours UC", "taux": 0.12, "montant_annuel": 15.07, "beneficiaire_commission": "Réseau Solife Premium", "fonds_concerne": "FND-UC-004"},
        {"commission_id": "COMM-1190-001", "contract_number": "SOL-2025-1190", "type": "Commission d'entrée", "taux": 1.00, "montant": 170.00, "beneficiaire_commission": "Réseau Solife Direct", "date_application": "2025-02-01", "statut": "Versée"},
        {"commission_id": "COMM-1190-002", "contract_number": "SOL-2025-1190", "type": "Commission de gestion récurrente", "taux": 0.20, "montant_annuel": 37.00, "beneficiaire_commission": "Réseau Solife Direct", "frequence": "Annuelle", "derniere_date_versement": "2026-02-01"}
    ]
    db.commissions.insert_many(commissions_data)
    print(f"[+] {len(commissions_data)} commissions insérées dans 'commissions'.")

    # =====================================================================
    # 11. BILLS — Factures et quittances
    # =====================================================================
    bills_data = []
    for m, pay_date, statut in [("2026-05", "2026-05-05", "Payée"), ("2026-06", "2026-06-05", "Payée"), ("2026-07", "2026-07-05", "Payée"), ("2026-08", "2026-08-05", "Payée"), ("2026-09", None, "En attente")]:
        bills_data.append({"bill_id": f"BILL-7710-{m}", "contract_number": "SOL-2022-7710", "type": "Prélèvement mensuel programmé", "montant_ttc": 300.00, "devise": "EUR", "date_emission": f"{m}-01", "date_echeance": f"{m}-05", "date_paiement": pay_date, "statut": statut, "mode_paiement": "Prélèvement SEPA"})
    bills_data.append({"bill_id": "BILL-7710-2026-FG", "contract_number": "SOL-2022-7710", "type": "Frais de gestion annuels", "montant_ttc": 640.50, "devise": "EUR", "date_emission": "2026-04-10", "date_paiement": "2026-04-10", "statut": "Prélevée sur encours", "mode_paiement": "Déduction automatique sur le contrat"})
    bills_data.append({"bill_id": "BILL-7710-2026-GD", "contract_number": "SOL-2022-7710", "type": "Prime garantie décès plancher", "montant_ttc": 86.40, "devise": "EUR", "date_emission": "2026-04-10", "date_paiement": "2026-04-10", "statut": "Prélevée sur encours", "mode_paiement": "Déduction automatique sur le contrat"})
    for m, pay_date, statut in [("2026-06", "2026-06-10", "Payée"), ("2026-07", "2026-07-10", "Payée"), ("2026-08", "2026-08-10", "Payée"), ("2026-09", None, "En attente")]:
        bills_data.append({"bill_id": f"BILL-3320-{m}", "contract_number": "SOL-2024-3320", "type": "Prélèvement mensuel programmé", "montant_ttc": 200.00, "devise": "EUR", "date_emission": f"{m}-01", "date_echeance": f"{m}-10", "date_paiement": pay_date, "statut": statut, "mode_paiement": "Prélèvement SEPA"})
    for m, pay_date, statut in [("2026-06", "2026-06-01", "Payée"), ("2026-07", "2026-07-01", "Payée"), ("2026-08", "2026-08-01", "Payée"), ("2026-09", None, "En attente")]:
        bills_data.append({"bill_id": f"BILL-1190-{m}", "contract_number": "SOL-2025-1190", "type": "Prélèvement mensuel programmé", "montant_ttc": 150.00, "devise": "EUR", "date_emission": f"{m}-01", "date_echeance": f"{m}-01", "date_paiement": pay_date, "statut": statut, "mode_paiement": "Prélèvement SEPA"})
    bills_data.append({"bill_id": "BILL-1190-2026-CD", "contract_number": "SOL-2025-1190", "type": "Prime capital décès toutes causes", "montant_ttc": 420.00, "devise": "EUR", "date_emission": "2026-02-01", "date_paiement": "2026-02-01", "statut": "Prélevée sur encours", "mode_paiement": "Déduction automatique"})
    db.bills.insert_many(bills_data)
    print(f"[+] {len(bills_data)} factures insérées dans 'bills'.")

    # =====================================================================
    # 12. TRANSACTIONS — Mouvements financiers
    # =====================================================================
    transactions_data = [
        {"transaction_id": "TXN-7710-20260605", "contract_number": "SOL-2022-7710", "type": "Versement programmé", "sens": "Crédit", "montant_brut": 300.00, "frais": 6.00, "montant_net": 294.00, "devise": "EUR", "date_valeur": "2026-06-05", "fonds_impacte": "FND-EURO-001", "statut": "Exécutée"},
        {"transaction_id": "TXN-7710-20260705", "contract_number": "SOL-2022-7710", "type": "Versement programmé", "sens": "Crédit", "montant_brut": 300.00, "frais": 6.00, "montant_net": 294.00, "devise": "EUR", "date_valeur": "2026-07-05", "fonds_impacte": "FND-EURO-001", "statut": "Exécutée"},
        {"transaction_id": "TXN-7710-20260805", "contract_number": "SOL-2022-7710", "type": "Versement programmé", "sens": "Crédit", "montant_brut": 300.00, "frais": 6.00, "montant_net": 294.00, "devise": "EUR", "date_valeur": "2026-08-05", "fonds_impacte": "FND-EURO-001", "statut": "Exécutée"},
        {"transaction_id": "TXN-7710-20250710", "contract_number": "SOL-2022-7710", "type": "Rachat partiel", "sens": "Débit", "montant_brut": 3000.00, "prelevement_social": 180.00, "montant_net": 2820.00, "devise": "EUR", "date_valeur": "2025-07-10", "fonds_impacte": "FND-EURO-001", "statut": "Exécutée"},
        {"transaction_id": "TXN-7710-20240320-A", "contract_number": "SOL-2022-7710", "type": "Arbitrage - Sortie", "sens": "Débit", "montant_brut": 8000.00, "frais": 40.00, "montant_net": 7960.00, "devise": "EUR", "date_valeur": "2024-03-20", "fonds_impacte": "FND-EURO-001", "statut": "Exécutée"},
        {"transaction_id": "TXN-7710-20240320-B", "contract_number": "SOL-2022-7710", "type": "Arbitrage - Entrée", "sens": "Crédit", "montant_brut": 7960.00, "frais": 0.00, "montant_net": 7960.00, "devise": "EUR", "date_valeur": "2024-03-20", "fonds_impacte": "FND-UC-001", "statut": "Exécutée"},
        {"transaction_id": "TXN-7710-20230315", "contract_number": "SOL-2022-7710", "type": "Versement complémentaire", "sens": "Crédit", "montant_brut": 5000.00, "frais": 100.00, "montant_net": 4900.00, "devise": "EUR", "date_valeur": "2023-03-15", "fonds_impacte": "FND-EURO-001", "statut": "Exécutée"},
        {"transaction_id": "TXN-7710-20240615", "contract_number": "SOL-2022-7710", "type": "Versement complémentaire", "sens": "Crédit", "montant_brut": 8000.00, "frais": 160.00, "montant_net": 7840.00, "devise": "EUR", "date_valeur": "2024-06-15", "fonds_impacte": "FND-UC-001", "statut": "Exécutée"},
        {"transaction_id": "TXN-3320-20260710", "contract_number": "SOL-2024-3320", "type": "Versement programmé", "sens": "Crédit", "montant_brut": 200.00, "frais": 3.00, "montant_net": 197.00, "devise": "EUR", "date_valeur": "2026-07-10", "fonds_impacte": "FND-EURO-001", "statut": "Exécutée"},
        {"transaction_id": "TXN-3320-20260810", "contract_number": "SOL-2024-3320", "type": "Versement programmé", "sens": "Crédit", "montant_brut": 200.00, "frais": 3.00, "montant_net": 197.00, "devise": "EUR", "date_valeur": "2026-08-10", "fonds_impacte": "FND-EURO-001", "statut": "Exécutée"},
        {"transaction_id": "TXN-5540-20260315", "contract_number": "SOL-2023-5540", "type": "Versement complémentaire", "sens": "Crédit", "montant_brut": 10000.00, "frais": 100.00, "montant_net": 9900.00, "devise": "EUR", "date_valeur": "2026-03-15", "fonds_impacte": "Répartition multiple", "statut": "Exécutée"},
        {"transaction_id": "TXN-5540-20250905-A", "contract_number": "SOL-2023-5540", "type": "Arbitrage - Sortie", "sens": "Débit", "montant_brut": 5000.00, "frais": 15.00, "montant_net": 4985.00, "devise": "EUR", "date_valeur": "2025-09-05", "fonds_impacte": "FND-UC-003", "statut": "Exécutée"},
        {"transaction_id": "TXN-5540-20250905-B", "contract_number": "SOL-2023-5540", "type": "Arbitrage - Entrée", "sens": "Crédit", "montant_brut": 4985.00, "frais": 0.00, "montant_net": 4985.00, "devise": "EUR", "date_valeur": "2025-09-05", "fonds_impacte": "FND-UC-004", "statut": "Exécutée"},
        {"transaction_id": "TXN-1190-20260701", "contract_number": "SOL-2025-1190", "type": "Versement programmé", "sens": "Crédit", "montant_brut": 150.00, "frais": 1.50, "montant_net": 148.50, "devise": "EUR", "date_valeur": "2026-07-01", "fonds_impacte": "FND-EURO-001", "statut": "Exécutée"},
        {"transaction_id": "TXN-1190-20260801", "contract_number": "SOL-2025-1190", "type": "Versement programmé", "sens": "Crédit", "montant_brut": 150.00, "frais": 1.50, "montant_net": 148.50, "devise": "EUR", "date_valeur": "2026-08-01", "fonds_impacte": "FND-EURO-001", "statut": "Exécutée"},
        {"transaction_id": "TXN-1190-20250615", "contract_number": "SOL-2025-1190", "type": "Versement complémentaire", "sens": "Crédit", "montant_brut": 2000.00, "frais": 20.00, "montant_net": 1980.00, "devise": "EUR", "date_valeur": "2025-06-15", "fonds_impacte": "FND-EURO-001", "statut": "Exécutée"}
    ]
    db.transactions.insert_many(transactions_data)
    print(f"[+] {len(transactions_data)} transactions insérées dans 'transactions'.")

    # =====================================================================
    # CRÉATION DES INDEX
    # =====================================================================
    print("\n[*] Création des index de performance...")
    db.contracts.create_index("contract_number", unique=True)
    db.contracts.create_index("produit_code")
    db.contracts.create_index("parties_prenantes.preneur.party_id")
    db.contracts.create_index("parties_prenantes.assure.party_id")
    db.contracts.create_index("statut")
    db.coverages.create_index("coverage_id", unique=True)
    db.coverages.create_index("contract_number")
    db.investment_services.create_index("investment_id", unique=True)
    db.investment_services.create_index("contract_number")
    db.avenants.create_index("avenant_id", unique=True)
    db.avenants.create_index("contract_number")
    db.avenants.create_index("type")
    db.beneficiaires.create_index("beneficiaire_id", unique=True)
    db.beneficiaires.create_index("contract_number")
    db.commissions.create_index("commission_id", unique=True)
    db.commissions.create_index("contract_number")
    db.bills.create_index("bill_id", unique=True)
    db.bills.create_index("contract_number")
    db.bills.create_index("statut")
    db.transactions.create_index("transaction_id", unique=True)
    db.transactions.create_index("contract_number")
    db.transactions.create_index("type")
    db.produits.create_index("produit_code", unique=True)
    db.fonds.create_index("fonds_code", unique=True)
    db.tarifs.create_index("tarif_code", unique=True)
    db.tarifs.create_index("produit_code")
    db.taxes.create_index("tax_code", unique=True)
    print("[+] Tous les index créés avec succès.")

    # =====================================================================
    # RÉSUMÉ
    # =====================================================================
    print("\n" + "=" * 65)
    print("  BASE DE DONNÉES solife_contracts INITIALISÉE AVEC SUCCÈS")
    print("=" * 65)
    cols = ["produits", "fonds", "tarifs", "taxes", "contracts", "coverages", "investment_services", "beneficiaires", "avenants", "commissions", "bills", "transactions"]
    total = 0
    for c in cols:
        count = db[c].count_documents({})
        print(f"  📦 {c:25s} : {count:3d} documents")
        total += count
    print(f"  {'─' * 40}")
    print(f"  📊 TOTAL                    : {total:3d} documents")
    print("=" * 65)


if __name__ == "__main__":
    init_contracts_db()
