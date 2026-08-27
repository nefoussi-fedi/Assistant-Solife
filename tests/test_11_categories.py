import sys
import unittest
from app import generate_fallback_chat_response

class Test11Categories(unittest.TestCase):
    def setUp(self):
        self.fedi = {'role': 'client', 'nom': 'Nefoussi Fedi', 'party_id': 'TP-10001', 'username': 'fedi.nefoussi'}
        self.dorra = {'role': 'client', 'nom': 'Ben Salah Dorra', 'party_id': 'TP-10002', 'username': 'dorra.bensalah'}

    def test_category_1_general_info(self):
        q1 = "Quel est mon numéro de contrat ?"
        r1 = generate_fallback_chat_response(q1, self.fedi)
        self.assertIn("SOL-2022-7710", r1)

        q2 = "Qui est le titulaire de mon contrat ?"
        r2 = generate_fallback_chat_response(q2, self.fedi)
        self.assertIn("Nefoussi Fedi", r2)

        q3 = "Quelle est la date d'échéance de mon contrat ?"
        r3 = generate_fallback_chat_response(q3, self.fedi)
        self.assertIn("10/04/2042", r3)

    def test_category_2_valeur_epargne(self):
        q1 = "Quelle est la valeur actuelle de mon contrat ?"
        r1 = generate_fallback_chat_response(q1, self.fedi)
        self.assertIn("117 550", r1)

        q2 = "Combien mon contrat a-t-il rapporté ?"
        r2 = generate_fallback_chat_response(q2, self.fedi)
        self.assertIn("15 695", r2)

        q3 = "Quel est le rendement de mon contrat ?"
        r3 = generate_fallback_chat_response(q3, self.fedi)
        self.assertIn("4,25", r3)

    def test_category_3_versements(self):
        q1 = "Combien ai-je versé sur mon contrat ?"
        r1 = generate_fallback_chat_response(q1, self.fedi)
        self.assertIn("101 855", r1)

        q2 = "Quand ai-je effectué mon dernier versement ?"
        r2 = generate_fallback_chat_response(q2, self.fedi)
        self.assertIn("05/08/2026", r2)

        q3 = "Puis-je effectuer un versement supplémentaire ?"
        r3 = generate_fallback_chat_response(q3, self.dorra)
        self.assertIn("versement", r3.lower())

    def test_category_4_retraits_rachat(self):
        q1 = "Puis-je retirer une partie de mon épargne ?"
        r1 = generate_fallback_chat_response(q1, self.fedi)
        self.assertIn("Rachat Partiel", r1)

        q2 = "Quelle est la différence entre un rachat partiel et total ?"
        r2 = generate_fallback_chat_response(q2, self.fedi)
        self.assertIn("Rachat Total", r2)

    def test_category_5_beneficiaires(self):
        q1 = "Qui sont les bénéficiaires de mon contrat ?"
        r1 = generate_fallback_chat_response(q1, self.fedi)
        self.assertIn("Sarah Nefoussi", r1)
        self.assertIn("Rayan Nefoussi", r1)

        q2 = "Que se passe-t-il si le bénéficiaire décède avant moi ?"
        r2 = generate_fallback_chat_response(q2, self.fedi)
        self.assertIn("prédécès", r2.lower())

    def test_category_6_supports_et_rebalancing(self):
        q1 = "Sur quels supports mon épargne est-elle investie ?"
        r1 = generate_fallback_chat_response(q1, self.fedi)
        self.assertIn("Fonds Euros", r1)
        self.assertIn("Actions Monde ESG", r1)

        q2 = "Qu'est-ce qu'un rebalancing ?"
        r2 = generate_fallback_chat_response(q2, self.fedi)
        self.assertIn("Rebalancing", r2)

    def test_category_7_frais(self):
        q1 = "Quels sont les frais de mon contrat ?"
        r1 = generate_fallback_chat_response(q1, self.fedi)
        self.assertIn("0,00 %", r1)
        self.assertIn("Frais de Gestion", r1)

    def test_category_8_participation_benefices(self):
        q1 = "Qu'est-ce que la participation aux bénéfices ?"
        r1 = generate_fallback_chat_response(q1, self.fedi)
        self.assertIn("Participation aux Bénéfices", r1)
        self.assertIn("3,10 %", r1)

    def test_category_9_documents(self):
        q1 = "Quels documents sont disponibles pour mon contrat ?"
        r1 = generate_fallback_chat_response(q1, self.fedi)
        self.assertIn("Relevé de Situation", r1)
        self.assertIn("Imprimé Fiscal", r1)

    def test_category_10_historique_operations(self):
        q1 = "Quelle est ma dernière opération ?"
        r1 = generate_fallback_chat_response(q1, self.fedi)
        self.assertIn("05/08/2026", r1)

        q2 = "Quelle opération a été effectuée le 15 juin ?"
        r2 = generate_fallback_chat_response(q2, self.fedi)
        self.assertIn("15 juin 2024", r2)
        self.assertIn("8 000,00 €", r2)

        q3 = "Quelle opération a été effectuée le 15 juin ?"
        r3 = generate_fallback_chat_response(q3, self.dorra)
        self.assertIn("15 juin 2025", r3)
        self.assertIn("2 000,00 €", r3)

    def test_category_11_questions_intelligentes(self):
        q1 = "Pourquoi la valeur de mon contrat a-t-elle diminué ce mois-ci ?"
        r1 = generate_fallback_chat_response(q1, self.fedi)
        self.assertIn("Unités de Compte", r1)

        q2 = "Quel est le support qui a le plus contribué à la performance de mon contrat ?"
        r2 = generate_fallback_chat_response(q2, self.fedi)
        self.assertIn("Solife Actions Monde Croissance ESG", r2)

        q3 = "Mon contrat est-il actuellement en moins-value ?"
        r3 = generate_fallback_chat_response(q3, self.fedi)
        self.assertIn("Aucune Moins-Value", r3)

        q4 = "Quelle est la différence entre le montant que j'ai versé et la valeur actuelle de mon contrat ?"
        r4 = generate_fallback_chat_response(q4, self.fedi)
        self.assertIn("+15 695,00 €", r4)

if __name__ == '__main__':
    unittest.main()
