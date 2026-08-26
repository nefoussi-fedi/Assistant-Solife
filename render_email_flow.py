import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage, QPainter, QColor, QFont, QPen, QBrush, QLinearGradient, QPainterPath
from PyQt5.QtCore import Qt, QRectF, QPointF

app = QApplication(sys.argv if sys.argv else [''])

W, H = 1920, 1080
image = QImage(W, H, QImage.Format_ARGB32)
image.fill(QColor("#080c16"))

painter = QPainter(image)
painter.setRenderHint(QPainter.Antialiasing)
painter.setRenderHint(QPainter.TextAntialiasing)

# Background Ambient Gradient
bg = QLinearGradient(0, 0, W, H)
bg.setColorAt(0.0, QColor(15, 23, 42, 255))
bg.setColorAt(0.5, QColor(8, 12, 22, 255))
bg.setColorAt(1.0, QColor(14, 18, 36, 255))
painter.fillRect(0, 0, W, H, QBrush(bg))

# Top Title
painter.setPen(QColor("#a855f7"))
painter.setFont(QFont("Segoe UI", 14, QFont.Bold))
painter.drawText(QRectF(0, 40, W, 25), Qt.AlignCenter, "SOLIFE AI WORKFLOW")

painter.setPen(QColor("#f8fafc"))
painter.setFont(QFont("Segoe UI", 28, QFont.Bold))
painter.drawText(QRectF(0, 75, W, 45), Qt.AlignCenter, "De la Donnée Complexe à l'E-mail Client Instantané")

# Dimensions
card_y = 170
card_h = 800
card_w = 680

# ── LEFT CARD : Données Complexes & Demande ──
cx1 = 120
path1 = QPainterPath()
path1.addRoundedRect(QRectF(cx1, card_y, card_w, card_h), 24, 24)

card1_bg = QLinearGradient(cx1, card_y, cx1, card_y + card_h)
card1_bg.setColorAt(0.0, QColor(22, 30, 52, 230))
card1_bg.setColorAt(1.0, QColor(13, 17, 32, 245))
painter.fillPath(path1, QBrush(card1_bg))
painter.setPen(QPen(QColor(56, 189, 248, 120), 1.5))
painter.drawPath(path1)

# Left Header
painter.fillRect(QRectF(cx1 + 40, card_y + 40, 16, 16), QBrush(QColor("#38bdf8")))
painter.setPen(QColor("#ffffff"))
painter.setFont(QFont("Segoe UI", 20, QFont.Bold))
painter.drawText(cx1 + 68, card_y + 55, "1. Données Brutes & Demande Client")

# Client Question Bubble
bubble_y = card_y + 95
bubble_path = QPainterPath()
bubble_path.addRoundedRect(QRectF(cx1 + 40, bubble_y, card_w - 80, 85), 16, 16)
painter.fillPath(bubble_path, QBrush(QColor(15, 23, 42, 240)))
painter.setPen(QPen(QColor(56, 189, 248, 180), 1.2))
painter.drawPath(bubble_path)

painter.setPen(QColor("#38bdf8"))
painter.setFont(QFont("Segoe UI", 12, QFont.Bold))
painter.drawText(cx1 + 65, bubble_y + 32, "👤 Client (Question en langage naturel) :")
painter.setPen(QColor("#f1f5f9"))
painter.setFont(QFont("Segoe UI", 15, QFont.DemiBold))
painter.drawText(cx1 + 65, bubble_y + 62, "« Pouvez-vous m'expliquer la situation de mon contrat ? »")

# Complex Table Visualization
tbl_y = card_y + 215
painter.setPen(QColor("#94a3b8"))
painter.setFont(QFont("Segoe UI", 12, QFont.Bold))
painter.drawText(cx1 + 40, tbl_y, "📊 Données internes Solife (Complexes & Denses) :")

tbl_box_y = tbl_y + 15
tbl_path = QPainterPath()
tbl_path.addRoundedRect(QRectF(cx1 + 40, tbl_box_y, card_w - 80, 480), 16, 16)
painter.fillPath(tbl_path, QBrush(QColor(10, 15, 28, 220)))
painter.setPen(QPen(QColor(30, 41, 59, 255), 1.5))
painter.drawPath(tbl_path)

# Draw Table Rows
headers = ["Fonds / Support", "Type", "Alloc.", "Perf. YTD", "Volatilité"]
painter.setFont(QFont("Segoe UI", 11, QFont.Bold))
painter.setPen(QColor("#38bdf8"))
hx = cx1 + 65
col_ws = [150, 110, 80, 95, 90]
for idx, h in enumerate(headers):
    painter.drawText(hx, tbl_box_y + 40, h)
    hx += col_ws[idx]

painter.setPen(QPen(QColor(51, 65, 85, 120), 1))
painter.drawLine(cx1 + 55, tbl_box_y + 55, cx1 + card_w - 55, tbl_box_y + 55)

rows = [
    ("Actions Monde ESG", "UC Actions", "45%", "+8.90%", "14.2%"),
    ("Immobilier Euro", "UC SCPI", "25%", "+4.20%", "5.1%"),
    ("Fonds Garanti 2026", "Fonds Euros", "30%", "+2.10%", "0.4%"),
    ("Arbitrage Récents", "Transaction", "3 op.", "Validé", "Auto"),
    ("Profil Investisseur", "Audit KYC", "Équilibré", "Conforme", "Niveau 3"),
    ("Historique Prélèvements", "Mensuel", "300 €", "Actif", "OK"),
]

ry = tbl_box_y + 90
painter.setFont(QFont("Segoe UI", 11))
for r in rows:
    rx = cx1 + 65
    painter.setPen(QColor("#cbd5e1"))
    for idx, val in enumerate(r):
        if idx == 3 and "+" in val:
            painter.setPen(QColor("#34d399"))
        elif idx == 0:
            painter.setPen(QColor("#f8fafc"))
        else:
            painter.setPen(QColor("#94a3b8"))
        painter.drawText(rx, ry, val)
        rx += col_ws[idx]
    
    painter.setPen(QPen(QColor(30, 41, 59, 100), 1))
    painter.drawLine(cx1 + 55, ry + 15, cx1 + card_w - 55, ry + 15)
    ry += 52

# Table footer note
painter.setPen(QColor("#64748b"))
painter.setFont(QFont("Segoe UI", 10, QFont.Normal))
painter.drawText(cx1 + 60, tbl_box_y + 450, "+ 12 tables relationnelles & 50+ métriques techniques")


# ── CENTER AI CONNECTOR ──
center_x = 960
center_y = card_y + (card_h / 2.0)

# Circuit Lines
painter.setPen(QPen(QColor(168, 85, 247, 180), 2, Qt.DashLine))
painter.drawLine(cx1 + card_w, int(center_y), cx1 + card_w + 140, int(center_y))

# AI Core Chip
ai_chip_path = QPainterPath()
ai_chip_path.addRoundedRect(QRectF(center_x - 55, center_y - 55, 110, 110), 22, 22)
ai_grad = QLinearGradient(center_x - 55, center_y - 55, center_x + 55, center_y + 55)
ai_grad.setColorAt(0.0, QColor(168, 85, 247, 240))
ai_grad.setColorAt(1.0, QColor(59, 130, 246, 240))
painter.fillPath(ai_chip_path, QBrush(ai_grad))
painter.setPen(QPen(QColor("#f3e8ff"), 2.5))
painter.drawPath(ai_chip_path)

painter.setFont(QFont("Segoe UI", 20, QFont.Bold))
painter.setPen(QColor("#ffffff"))
painter.drawText(QRectF(center_x - 55, center_y - 55, 110, 110), Qt.AlignCenter, "IA\nRAG")


# ── RIGHT CARD : E-mail Synthétique Pré-généré ──
cx2 = 1120
path2 = QPainterPath()
path2.addRoundedRect(QRectF(cx2, card_y, card_w, card_h), 24, 24)

card2_bg = QLinearGradient(cx2, card_y, cx2, card_y + card_h)
card2_bg.setColorAt(0.0, QColor(24, 28, 50, 235))
card2_bg.setColorAt(1.0, QColor(14, 16, 32, 245))
painter.fillPath(path2, QBrush(card2_bg))
painter.setPen(QPen(QColor(168, 85, 247, 160), 1.5))
painter.drawPath(path2)

# Right Header
painter.fillRect(QRectF(cx2 + 40, card_y + 40, 16, 16), QBrush(QColor("#c084fc")))
painter.setPen(QColor("#ffffff"))
painter.setFont(QFont("Segoe UI", 20, QFont.Bold))
painter.drawText(cx2 + 68, card_y + 55, "2. E-mail Synthétique & Vulgarisé")

# Email Window Card
em_y = card_y + 95
em_path = QPainterPath()
em_path.addRoundedRect(QRectF(cx2 + 40, em_y, card_w - 80, 640), 18, 18)
painter.fillPath(em_path, QBrush(QColor(15, 19, 36, 240)))
painter.setPen(QPen(QColor(168, 85, 247, 100), 1.5))
painter.drawPath(em_path)

# Email window dots (mac style)
painter.setPen(Qt.NoPen)
painter.setBrush(QColor("#ef4444"))
painter.drawEllipse(cx2 + 65, em_y + 24, 12, 12)
painter.setBrush(QColor("#f59e0b"))
painter.drawEllipse(cx2 + 85, em_y + 24, 12, 12)
painter.setBrush(QColor("#10b981"))
painter.drawEllipse(cx2 + 105, em_y + 24, 12, 12)

# Email Meta fields
painter.setPen(QColor("#94a3b8"))
painter.setFont(QFont("Segoe UI", 11))
painter.drawText(cx2 + 65, em_y + 65, "À : client.martin@email.com")
painter.drawText(cx2 + 65, em_y + 90, "Objet : Synthèse de votre contrat d'assurance-vie Solife")

painter.setPen(QPen(QColor(51, 65, 85, 120), 1))
painter.drawLine(cx2 + 60, em_y + 110, cx2 + card_w - 60, em_y + 110)

# Email Content (Clean, Structured, Jargon-Free)
ey = em_y + 145
painter.setPen(QColor("#f8fafc"))
painter.setFont(QFont("Segoe UI", 13, QFont.DemiBold))
painter.drawText(cx2 + 65, ey, "Bonjour M. Martin,")

ey += 35
painter.setPen(QColor("#cbd5e1"))
painter.setFont(QFont("Segoe UI", 12))
painter.drawText(cx2 + 65, ey, "Voici le résumé clair de votre contrat au 20 Août 2026 :")

# Bullet 1 (Gains)
ey += 45
bullet1_path = QPainterPath()
bullet1_path.addRoundedRect(QRectF(cx2 + 65, ey - 20, card_w - 130, 60), 12, 12)
painter.fillPath(bullet1_path, QBrush(QColor(16, 185, 129, 25)))
painter.setPen(QPen(QColor(52, 211, 153, 100), 1))
painter.drawPath(bullet1_path)

painter.setPen(QColor("#34d399"))
painter.setFont(QFont("Segoe UI", 12, QFont.Bold))
painter.drawText(cx2 + 85, ey + 15, "📈 Performance globale : +6,40 % (Croissance positive)")

# Bullet 2 (Allocation)
ey += 80
bullet2_path = QPainterPath()
bullet2_path.addRoundedRect(QRectF(cx2 + 65, ey - 20, card_w - 130, 60), 12, 12)
painter.fillPath(bullet2_path, QBrush(QColor(59, 130, 246, 25)))
painter.setPen(QPen(QColor(96, 165, 250, 100), 1))
painter.drawPath(bullet2_path)

painter.setPen(QColor("#60a5fa"))
painter.setFont(QFont("Segoe UI", 12, QFont.Bold))
painter.drawText(cx2 + 85, ey + 15, "🛡️ Répartition : 70% Unités de Compte / 30% Fonds Euros")

# Bullet 3 (Conseil)
ey += 80
bullet3_path = QPainterPath()
bullet3_path.addRoundedRect(QRectF(cx2 + 65, ey - 20, card_w - 130, 60), 12, 12)
painter.fillPath(bullet3_path, QBrush(QColor(168, 85, 247, 25)))
painter.setPen(QPen(QColor(192, 132, 252, 100), 1))
painter.drawPath(bullet3_path)

painter.setPen(QColor("#c084fc"))
painter.setFont(QFont("Segoe UI", 12, QFont.Bold))
painter.drawText(cx2 + 85, ey + 15, "💡 Conseil : Opportunité d'arbitrage pour sécuriser vos gains.")

# Email Signoff
ey += 85
painter.setPen(QColor("#94a3b8"))
painter.setFont(QFont("Segoe UI", 11))
painter.drawText(cx2 + 65, ey, "Votre conseiller reste à votre entière disposition.")
ey += 24
painter.setPen(QColor("#e2e8f0"))
painter.setFont(QFont("Segoe UI", 12, QFont.Bold))
painter.drawText(cx2 + 65, ey, "Bien cordialement, L'équipe Solife — Vermeg")

# Save Slide
out_file = r"c:\Users\DELL\Desktop\solife-flask\static\slides\slide_email_flow.png"
image.save(out_file, "PNG")
image.save(r"c:\Users\DELL\Desktop\solife-flask\static\slide_email_flow.png", "PNG")
print("Successfully generated slide_email_flow.png!")
