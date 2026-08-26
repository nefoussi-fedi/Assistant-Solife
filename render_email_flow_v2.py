import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage, QPainter, QColor, QFont, QPen, QBrush, QLinearGradient, QPainterPath
from PyQt5.QtCore import Qt, QRectF

app = QApplication(sys.argv if sys.argv else [''])

W, H = 1920, 1080
image = QImage(W, H, QImage.Format_ARGB32)
image.fill(QColor("#080c16"))

painter = QPainter(image)
painter.setRenderHint(QPainter.Antialiasing)
painter.setRenderHint(QPainter.TextAntialiasing)

# ── Fond sombre avec dégradé subtil ──
bg = QLinearGradient(0, 0, W, H)
bg.setColorAt(0.0, QColor(15, 23, 42, 255))
bg.setColorAt(0.5, QColor(8, 12, 24, 255))
bg.setColorAt(1.0, QColor(13, 17, 34, 255))
painter.fillRect(0, 0, W, H, QBrush(bg))

# ── Titre Principal ──
painter.setPen(QColor("#38bdf8"))
painter.setFont(QFont("Segoe UI", 16, QFont.Bold))
painter.drawText(QRectF(0, 45, W, 30), Qt.AlignCenter, "AUTOMATISATION DE LA RELATION CLIENT")

painter.setPen(QColor("#ffffff"))
painter.setFont(QFont("Segoe UI", 32, QFont.Bold))
painter.drawText(QRectF(0, 80, W, 50), Qt.AlignCenter, "De 50 données brutes à un E-mail clair en 1 seconde")

# ── Dimensions des cartes ──
card_y = 175
card_h = 810
card_w = 700

# ══════════════════════════════════════════════════
# CARTE GAUCHE : COMPLEXITÉ DES DONNÉES
# ══════════════════════════════════════════════════
cx1 = 110
path1 = QPainterPath()
path1.addRoundedRect(QRectF(cx1, card_y, card_w, card_h), 24, 24)

c1_bg = QLinearGradient(cx1, card_y, cx1, card_y + card_h)
c1_bg.setColorAt(0.0, QColor(20, 26, 46, 240))
c1_bg.setColorAt(1.0, QColor(12, 16, 28, 250))
painter.fillPath(path1, QBrush(c1_bg))
painter.setPen(QPen(QColor(56, 189, 248, 120), 1.5))
painter.drawPath(path1)

# Header Gauche
painter.fillRect(QRectF(cx1 + 45, card_y + 40, 18, 18), QBrush(QColor("#38bdf8")))
painter.setPen(QColor("#ffffff"))
painter.setFont(QFont("Segoe UI", 22, QFont.Bold))
painter.drawText(cx1 + 75, card_y + 57, "1. Données Brutes & Demande")

# Question Client (Bulle bien lisible)
bq_y = card_y + 95
bq_path = QPainterPath()
bq_path.addRoundedRect(QRectF(cx1 + 45, bq_y, card_w - 90, 95), 16, 16)
painter.fillPath(bq_path, QBrush(QColor(15, 23, 42, 240)))
painter.setPen(QPen(QColor(56, 189, 248, 180), 1.5))
painter.drawPath(bq_path)

painter.setPen(QColor("#38bdf8"))
painter.setFont(QFont("Segoe UI", 13, QFont.Bold))
painter.drawText(cx1 + 70, bq_y + 35, "👤 Question du Client :")
painter.setPen(QColor("#f8fafc"))
painter.setFont(QFont("Segoe UI", 17, QFont.DemiBold))
painter.drawText(cx1 + 70, bq_y + 70, "« Bonjour, où en est mon contrat d'assurance ? »")

# Tableau Dense (Données complexes)
tbl_y = card_y + 225
painter.setPen(QColor("#94a3b8"))
painter.setFont(QFont("Segoe UI", 13, QFont.Bold))
painter.drawText(cx1 + 45, tbl_y, "📊 Données internes Solife (Complexes à lire pour le client) :")

tbl_box_y = tbl_y + 20
tbl_path = QPainterPath()
tbl_path.addRoundedRect(QRectF(cx1 + 45, tbl_box_y, card_w - 90, 480), 16, 16)
painter.fillPath(tbl_path, QBrush(QColor(10, 14, 26, 230)))
painter.setPen(QPen(QColor(30, 41, 59, 255), 1.5))
painter.drawPath(tbl_path)

# Lignes du tableau
headers = ["Fonds / Support", "Type", "Alloc.", "Perf. YTD"]
painter.setFont(QFont("Segoe UI", 13, QFont.Bold))
painter.setPen(QColor("#38bdf8"))
hx = cx1 + 70
col_ws = [220, 130, 90, 110]
for idx, h in enumerate(headers):
    painter.drawText(hx, tbl_box_y + 45, h)
    hx += col_ws[idx]

painter.setPen(QPen(QColor(51, 65, 85, 150), 1.5))
painter.drawLine(cx1 + 65, tbl_box_y + 65, cx1 + card_w - 65, tbl_box_y + 65)

raw_rows = [
    ("Actions Monde ESG", "UC Actions", "45%", "+8.90%"),
    ("Immobilier Euro SCPI", "UC SCPI", "25%", "+4.20%"),
    ("Fonds Garanti 2026", "Fonds Euros", "30%", "+2.10%"),
    ("Audit Profil Risque", "KYC", "Niveau 3", "Conforme"),
    ("Historique Prélèvements", "Mensuel", "300 € / m", "Actif"),
    ("Rachat Partiel Possible", "Fiscalité", "Exonéré", "Disponible"),
]

ry = tbl_box_y + 110
for r in raw_rows:
    rx = cx1 + 70
    for idx, val in enumerate(r):
        painter.setFont(QFont("Segoe UI", 12, QFont.Bold if idx == 0 or idx == 3 else QFont.Normal))
        if idx == 3 and "+" in val:
            painter.setPen(QColor("#34d399"))
        elif idx == 0:
            painter.setPen(QColor("#f8fafc"))
        else:
            painter.setPen(QColor("#94a3b8"))
        painter.drawText(rx, ry, val)
        rx += col_ws[idx]
    
    painter.setPen(QPen(QColor(30, 41, 59, 120), 1))
    painter.drawLine(cx1 + 65, ry + 16, cx1 + card_w - 65, ry + 16)
    ry += 58


# ══════════════════════════════════════════════════
# CONNECTEUR IA CENTRAL
# ══════════════════════════════════════════════════
center_x = 960
center_y = card_y + (card_h / 2.0)

ai_chip = QPainterPath()
ai_chip.addRoundedRect(QRectF(center_x - 50, center_y - 50, 100, 100), 20, 20)
ai_grad = QLinearGradient(center_x - 50, center_y - 50, center_x + 50, center_y + 50)
ai_grad.setColorAt(0.0, QColor("#a855f7"))
ai_grad.setColorAt(1.0, QColor("#3b82f6"))
painter.fillPath(ai_chip, QBrush(ai_grad))
painter.setPen(QPen(QColor("#ffffff"), 2))
painter.drawPath(ai_chip)

painter.setFont(QFont("Segoe UI", 18, QFont.Bold))
painter.setPen(QColor("#ffffff"))
painter.drawText(QRectF(center_x - 50, center_y - 50, 100, 100), Qt.AlignCenter, "IA\nRAG")


# ══════════════════════════════════════════════════
# CARTE DROITE : E-MAIL ULTRA CLAIR & LISIBLE
# ══════════════════════════════════════════════════
cx2 = 1110
path2 = QPainterPath()
path2.addRoundedRect(QRectF(cx2, card_y, card_w, card_h), 24, 24)

c2_bg = QLinearGradient(cx2, card_y, cx2, card_y + card_h)
c2_bg.setColorAt(0.0, QColor(25, 30, 56, 245))
c2_bg.setColorAt(1.0, QColor(14, 17, 36, 255))
painter.fillPath(path2, QBrush(c2_bg))
painter.setPen(QPen(QColor(168, 85, 247, 180), 2))
painter.drawPath(path2)

# Header Droite
painter.fillRect(QRectF(cx2 + 45, card_y + 40, 18, 18), QBrush(QColor("#c084fc")))
painter.setPen(QColor("#ffffff"))
painter.setFont(QFont("Segoe UI", 22, QFont.Bold))
painter.drawText(cx2 + 75, card_y + 57, "2. E-mail Généré (Clair & Prêt)")

# Fenêtre E-mail (Haute lisibilité)
em_y = card_y + 95
em_path = QPainterPath()
em_path.addRoundedRect(QRectF(cx2 + 45, em_y, card_w - 90, 650), 18, 18)
painter.fillPath(em_path, QBrush(QColor(17, 24, 48, 255)))
painter.setPen(QPen(QColor(168, 85, 247, 140), 1.5))
painter.drawPath(em_path)

# Email window dots
painter.setPen(Qt.NoPen)
painter.setBrush(QColor("#ef4444"))
painter.drawEllipse(cx2 + 70, em_y + 25, 12, 12)
painter.setBrush(QColor("#f59e0b"))
painter.drawEllipse(cx2 + 90, em_y + 25, 12, 12)
painter.setBrush(QColor("#10b981"))
painter.drawEllipse(cx2 + 110, em_y + 25, 12, 12)

# Email Header Fields (Grosses écritures nettes)
painter.setPen(QColor("#94a3b8"))
painter.setFont(QFont("Segoe UI", 12, QFont.DemiBold))
painter.drawText(cx2 + 70, em_y + 68, "À : client.martin@email.com")

painter.setPen(QColor("#e2e8f0"))
painter.setFont(QFont("Segoe UI", 14, QFont.Bold))
painter.drawText(cx2 + 70, em_y + 98, "Objet : Synthèse de votre contrat d'assurance-vie Solife")

painter.setPen(QPen(QColor(51, 65, 85, 160), 1.5))
painter.drawLine(cx2 + 65, em_y + 118, cx2 + card_w - 65, em_y + 118)

# Contenu Email (Grandes polices très claires)
ey = em_y + 155
painter.setPen(QColor("#ffffff"))
painter.setFont(QFont("Segoe UI", 16, QFont.Bold))
painter.drawText(cx2 + 70, ey, "Bonjour M. Martin,")

ey += 35
painter.setPen(QColor("#cbd5e1"))
painter.setFont(QFont("Segoe UI", 14))
painter.drawText(cx2 + 70, ey, "Voici l'état de votre épargne en 3 points essentiels :")

# ── CARTOUCHE 1 : PERFORMANCE (Vert Fluo / Émeraudes) ──
ey += 40
b1 = QPainterPath()
b1.addRoundedRect(QRectF(cx2 + 70, ey, card_w - 140, 75), 14, 14)
painter.fillPath(b1, QBrush(QColor(16, 185, 129, 35)))
painter.setPen(QPen(QColor(52, 211, 153, 220), 1.5))
painter.drawPath(b1)

painter.setPen(QColor("#34d399"))
painter.setFont(QFont("Segoe UI", 16, QFont.Bold))
painter.drawText(cx2 + 95, ey + 32, "📈 Performance Globale : +6,40 %")
painter.setPen(QColor("#e2e8f0"))
painter.setFont(QFont("Segoe UI", 12))
painter.drawText(cx2 + 95, ey + 56, "Votre capital progresse grâce au dynamisme des Unités de Compte.")

# ── CARTOUCHE 2 : RÉPARTITION (Bleu Électrique) ──
ey += 95
b2 = QPainterPath()
b2.addRoundedRect(QRectF(cx2 + 70, ey, card_w - 140, 75), 14, 14)
painter.fillPath(b2, QBrush(QColor(59, 130, 246, 35)))
painter.setPen(QPen(QColor(96, 165, 250, 220), 1.5))
painter.drawPath(b2)

painter.setPen(QColor("#60a5fa"))
painter.setFont(QFont("Segoe UI", 16, QFont.Bold))
painter.drawText(cx2 + 95, ey + 32, "🛡️ Répartition : 70% Dynamique / 30% Sécurisé")
painter.setPen(QColor("#e2e8f0"))
painter.setFont(QFont("Segoe UI", 12))
painter.drawText(cx2 + 95, ey + 56, "Votre épargne reste parfaitement équilibrée et conforme à votre profil.")

# ── CARTOUCHE 3 : CONSEIL (Violet Néon) ──
ey += 95
b3 = QPainterPath()
b3.addRoundedRect(QRectF(cx2 + 70, ey, card_w - 140, 75), 14, 14)
painter.fillPath(b3, QBrush(QColor(168, 85, 247, 35)))
painter.setPen(QPen(QColor(192, 132, 252, 220), 1.5))
painter.drawPath(b3)

painter.setPen(QColor("#c084fc"))
painter.setFont(QFont("Segoe UI", 16, QFont.Bold))
painter.drawText(cx2 + 95, ey + 32, "💡 Conseil : Sécurisation des Plus-Values")
painter.setPen(QColor("#e2e8f0"))
painter.setFont(QFont("Segoe UI", 12))
painter.drawText(cx2 + 95, ey + 56, "Un arbitrage vers le Fonds Garanti est possible en 1 clic.")

# Signature Email
ey += 115
painter.setPen(QColor("#94a3b8"))
painter.setFont(QFont("Segoe UI", 13))
painter.drawText(cx2 + 70, ey, "Votre conseiller reste à votre entière disposition.")
ey += 26
painter.setPen(QColor("#ffffff"))
painter.setFont(QFont("Segoe UI", 14, QFont.Bold))
painter.drawText(cx2 + 70, ey, "L'équipe Solife — Vermeg")

# Enregistrement
out_file = r"c:\Users\DELL\Desktop\solife-flask\static\slides\slide_email_flow.png"
image.save(out_file, "PNG")
image.save(r"c:\Users\DELL\Desktop\solife-flask\static\slide_email_flow.png", "PNG")
print("Slide email flow v2 générée avec succès !")
