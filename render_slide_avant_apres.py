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

# ── Fond sombre élégant ──
bg = QLinearGradient(0, 0, W, H)
bg.setColorAt(0.0, QColor(15, 23, 42, 255))
bg.setColorAt(0.5, QColor(8, 12, 24, 255))
bg.setColorAt(1.0, QColor(13, 17, 34, 255))
painter.fillRect(0, 0, W, H, QBrush(bg))

# ── Titre Principal ──
painter.setPen(QColor("#38bdf8"))
painter.setFont(QFont("Segoe UI", 16, QFont.Bold))
painter.drawText(QRectF(0, 50, W, 30), Qt.AlignCenter, "EXEMPLE CONCRET : RECHERCHE MÉTIER")

painter.setPen(QColor("#ffffff"))
painter.setFont(QFont("Segoe UI", 34, QFont.Bold))
painter.drawText(QRectF(0, 90, W, 50), Qt.AlignCenter, "« Comment fonctionne le Rebalancing ? »")

# ── Dimensions des cartes ──
card_y = 190
card_h = 780
card_w = 780

# ══════════════════════════════════════════════════
# CARTE GAUCHE : AVANT (Ultra Minimaliste)
# ══════════════════════════════════════════════════
cx1 = 120
path1 = QPainterPath()
path1.addRoundedRect(QRectF(cx1, card_y, card_w, card_h), 28, 28)

c1_bg = QLinearGradient(cx1, card_y, cx1, card_y + card_h)
c1_bg.setColorAt(0.0, QColor(32, 18, 26, 245))
c1_bg.setColorAt(1.0, QColor(18, 10, 16, 255))
painter.fillPath(path1, QBrush(c1_bg))
painter.setPen(QPen(QColor(239, 68, 68, 180), 2))
painter.drawPath(path1)

# Badge Titre Gauche
painter.fillRect(QRectF(cx1 + 50, card_y + 45, 22, 22), QBrush(QColor("#ef4444")))
painter.setPen(QColor("#ef4444"))
painter.setFont(QFont("Segoe UI", 26, QFont.Bold))
painter.drawText(cx1 + 85, card_y + 65, "❌ AVANT")

# 1. Action
b1_y = card_y + 120
bp1 = QPainterPath()
bp1.addRoundedRect(QRectF(cx1 + 50, b1_y, card_w - 100, 150), 20, 20)
painter.fillPath(bp1, QBrush(QColor(24, 14, 20, 220)))
painter.setPen(QPen(QColor(239, 68, 68, 90), 1.5))
painter.drawPath(bp1)

painter.setPen(QColor("#fca5a5"))
painter.setFont(QFont("Segoe UI", 20, QFont.Bold))
painter.drawText(cx1 + 80, b1_y + 55, "📂 Fouille Manuelle")
painter.setPen(QColor("#e2e8f0"))
painter.setFont(QFont("Segoe UI", 18))
painter.drawText(cx1 + 80, b1_y + 105, "Recherche dans 59 documents PDF")

# 2. Temps
b2_y = b1_y + 190
bp2 = QPainterPath()
bp2.addRoundedRect(QRectF(cx1 + 50, b2_y, card_w - 100, 150), 20, 20)
painter.fillPath(bp2, QBrush(QColor(24, 14, 20, 220)))
painter.setPen(QPen(QColor(239, 68, 68, 90), 1.5))
painter.drawPath(bp2)

painter.setPen(QColor("#fca5a5"))
painter.setFont(QFont("Segoe UI", 20, QFont.Bold))
painter.drawText(cx1 + 80, b2_y + 55, "⏳ 15 à 20 Minutes")
painter.setPen(QColor("#e2e8f0"))
painter.setFont(QFont("Segoe UI", 18))
painter.drawText(cx1 + 80, b2_y + 105, "Lecture longue et sans réponse directe")

# 3. Résultat
b3_y = b2_y + 190
bp3 = QPainterPath()
bp3.addRoundedRect(QRectF(cx1 + 50, b3_y, card_w - 100, 150), 20, 20)
painter.fillPath(bp3, QBrush(QColor(239, 68, 68, 30)))
painter.setPen(QPen(QColor(239, 68, 68, 160), 2))
painter.drawPath(bp3)

painter.setPen(QColor("#ef4444"))
painter.setFont(QFont("Segoe UI", 20, QFont.Bold))
painter.drawText(cx1 + 80, b3_y + 55, "⚠️ Goulet d'Étranglement")
painter.setPen(QColor("#ffffff"))
painter.setFont(QFont("Segoe UI", 18, QFont.DemiBold))
painter.drawText(cx1 + 80, b3_y + 105, "Surcharge support & attente client")


# ══════════════════════════════════════════════════
# CARTE DROITE : APRÈS (Ultra Minimaliste)
# ══════════════════════════════════════════════════
cx2 = 1020
path2 = QPainterPath()
path2.addRoundedRect(QRectF(cx2, card_y, card_w, card_h), 28, 28)

c2_bg = QLinearGradient(cx2, card_y, cx2, card_y + card_h)
c2_bg.setColorAt(0.0, QColor(14, 30, 26, 245))
c2_bg.setColorAt(1.0, QColor(8, 18, 16, 255))
painter.fillPath(path2, QBrush(c2_bg))
painter.setPen(QPen(QColor(16, 185, 129, 200), 2))
painter.drawPath(path2)

# Badge Titre Droite
painter.fillRect(QRectF(cx2 + 50, card_y + 45, 22, 22), QBrush(QColor("#10b981")))
painter.setPen(QColor("#34d399"))
painter.setFont(QFont("Segoe UI", 26, QFont.Bold))
painter.drawText(cx2 + 85, card_y + 65, "✅ APRÈS (Chatbot IA)")

# 1. Action
r1_y = card_y + 120
rp1 = QPainterPath()
rp1.addRoundedRect(QRectF(cx2 + 50, r1_y, card_w - 100, 150), 20, 20)
painter.fillPath(rp1, QBrush(QColor(10, 26, 22, 220)))
painter.setPen(QPen(QColor(16, 185, 129, 90), 1.5))
painter.drawPath(rp1)

painter.setPen(QColor("#6ee7b7"))
painter.setFont(QFont("Segoe UI", 20, QFont.Bold))
painter.drawText(cx2 + 80, r1_y + 55, "💬 1 Simple Question")
painter.setPen(QColor("#e2e8f0"))
painter.setFont(QFont("Segoe UI", 18))
painter.drawText(cx2 + 80, r1_y + 105, "En langage naturel dans le chat")

# 2. Temps
r2_y = r1_y + 190
rp2 = QPainterPath()
rp2.addRoundedRect(QRectF(cx2 + 50, r2_y, card_w - 100, 150), 20, 20)
painter.fillPath(rp2, QBrush(QColor(10, 26, 22, 220)))
painter.setPen(QPen(QColor(16, 185, 129, 90), 1.5))
painter.drawPath(rp2)

painter.setPen(QColor("#6ee7b7"))
painter.setFont(QFont("Segoe UI", 20, QFont.Bold))
painter.drawText(cx2 + 80, r2_y + 55, "⚡ Moins de 1 Seconde")
painter.setPen(QColor("#e2e8f0"))
painter.setFont(QFont("Segoe UI", 18))
painter.drawText(cx2 + 80, r2_y + 105, "Synthèse claire + Document source cité")

# 3. Résultat
r3_y = r2_y + 190
rp3 = QPainterPath()
rp3.addRoundedRect(QRectF(cx2 + 50, r3_y, card_w - 100, 150), 20, 20)
painter.fillPath(rp3, QBrush(QColor(16, 185, 129, 30)))
painter.setPen(QPen(QColor(16, 185, 129, 180), 2))
painter.drawPath(rp3)

painter.setPen(QColor("#34d399"))
painter.setFont(QFont("Segoe UI", 20, QFont.Bold))
painter.drawText(cx2 + 80, r3_y + 55, "🚀 Réponse Immédiate & Fiable")
painter.setPen(QColor("#ffffff"))
painter.setFont(QFont("Segoe UI", 18, QFont.DemiBold))
painter.drawText(cx2 + 80, r3_y + 105, "Gain de temps massif & 100% autonome")

# ══════════════════════════════════════════════════
# ENREGISTREMENT
# ══════════════════════════════════════════════════
out_slide = r"c:\Users\DELL\Desktop\solife-flask\static\slides\slide_avant_apres.png"
image.save(out_slide, "PNG")
image.save(r"c:\Users\DELL\Desktop\solife-flask\static\slide_avant_apres.png", "PNG")
print("Slide minimaliste générée avec succès !")
