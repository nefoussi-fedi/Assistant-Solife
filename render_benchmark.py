import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage, QPainter, QColor, QFont, QPen, QBrush, QLinearGradient, QPainterPath
from PyQt5.QtCore import Qt, QRectF, QPointF

# Initialize Qt App (offscreen)
app = QApplication(sys.argv if sys.argv else [''])

W, H = 1920, 1080
image = QImage(W, H, QImage.Format_ARGB32)
image.fill(QColor("#080c16")) # Deep dark background

painter = QPainter(image)
painter.setRenderHint(QPainter.Antialiasing)
painter.setRenderHint(QPainter.TextAntialiasing)

# ── Background Ambient Glow ──
glow1 = QLinearGradient(0, 0, W, H)
glow1.setColorAt(0.0, QColor(18, 24, 46, 255))
glow1.setColorAt(0.5, QColor(10, 14, 26, 255))
glow1.setColorAt(1.0, QColor(14, 18, 38, 255))
painter.fillRect(0, 0, W, H, QBrush(glow1))

# ── Top Header / Source Citation ──
painter.setPen(QColor("#94a3b8"))
font_source = QFont("Segoe UI", 14, QFont.Bold)
painter.setFont(font_source)
painter.drawText(QRectF(0, 28, W, 30), Qt.AlignCenter, "Source : Artificial Analysis — Benchmark officiel (https://artificialanalysis.ai/models)")

font_title = QFont("Segoe UI", 26, QFont.Bold)
painter.setFont(font_title)
painter.setPen(QColor("#f8fafc"))
painter.drawText(QRectF(0, 62, W, 45), Qt.AlignCenter, "LLM Performance & Cost Benchmark")

# ── Data Definitions ──
# 1. Intelligence
data_intel = [
    ("Claude Opus 5 (max)", 63, "#e06c53", False),
    ("Claude Fable 5 (fb)", 62, "#e06c53", False),
    ("GPT-5.6 Sol (max)", 61, "#475569", False),
    ("Grok 4.6 (high)", 61, "#8b5cf6", False),
    ("Kimi K3 (max)", 60, "#3b82f6", False),
    ("GLM-5.3 (max)", 60, "#0ea5e9", False),
    ("Muse Spark 1.2", 57, "#06b6d4", False),
    ("Gemini 3.7 Flash", 56, "#10b981", True),  # Highlighted
    ("DeepSeek V4 Pro", 53, "#3b82f6", False),
    ("GPT-5.6 Luna", 52, "#475569", False),
    ("Nemotron 3 Ultra", 38, "#84cc16", False),
]

# 2. Speed
data_speed = [
    ("Gemini 3.7 Flash", 365, "#10b981", True), # Highlighted leader
    ("GPT-5.6 Luna", 149, "#475569", False),
    ("Nemotron 3 Ultra", 126, "#84cc16", False),
    ("GLM-5.3 (max)", 93, "#0ea5e9", False),
    ("DeepSeek V4 Pro", 80, "#3b82f6", False),
    ("Claude Fable 5", 75, "#e06c53", False),
    ("GPT-5.6 Sol (max)", 68, "#475569", False),
    ("Grok 4.6 (high)", 63, "#8b5cf6", False),
    ("Claude Opus 5", 59, "#e06c53", False),
    ("Kimi K3 (max)", 39, "#3b82f6", False),
]

# 3. Cost
data_cost = [
    ("GPT-5.6 Luna", 0.05, "$0.05", "#475569", False),
    ("DeepSeek V4 Pro", 0.25, "$0.25", "#3b82f6", False),
    ("Nemotron 3 Ultra", 0.38, "$0.38", "#84cc16", False),
    ("Muse Spark 1.2", 0.40, "$0.40", "#06b6d4", False),
    ("Gemini 3.7 Flash", 0.40, "$0.40", "#10b981", True), # Highlighted
    ("GLM-5.3 (max)", 0.68, "$0.68", "#0ea5e9", False),
    ("Grok 4.6 (high)", 0.84, "$0.84", "#8b5cf6", False),
    ("Kimi K3 (max)", 0.84, "$0.84", "#3b82f6", False),
    ("GPT-5.6 Sol (max)", 1.23, "$1.23", "#475569", False),
    ("Claude Opus 5", 2.34, "$2.34", "#e06c53", False),
    ("Claude Fable 5", 3.14, "$3.14", "#e06c53", False),
]

cards = [
    {
        "title": "Intelligence",
        "sub": "Artificial Analysis Intelligence Index · Higher is better",
        "color": "#8b5cf6",
        "type": "intel",
        "data": data_intel,
        "max_val": 70
    },
    {
        "title": "Speed",
        "sub": "Output tokens per second · Higher is better",
        "color": "#eab308",
        "type": "speed",
        "data": data_speed,
        "max_val": 400
    },
    {
        "title": "Cost per Task",
        "sub": "Weighted average cost (USD) per task · Lower is better",
        "color": "#f97316",
        "type": "cost",
        "data": data_cost,
        "max_val": 3.4
    }
]

card_w = 570
card_h = 880
start_x = 55
gap = 35
card_y = 135

for idx, card in enumerate(cards):
    cx = start_x + idx * (card_w + gap)
    cy = card_y

    # Draw Card Background (Glassmorphism)
    path = QPainterPath()
    path.addRoundedRect(QRectF(cx, cy, card_w, card_h), 20, 20)
    
    card_bg = QLinearGradient(cx, cy, cx, cy + card_h)
    card_bg.setColorAt(0.0, QColor(20, 26, 45, 230))
    card_bg.setColorAt(1.0, QColor(12, 16, 30, 240))
    painter.fillPath(path, QBrush(card_bg))
    
    painter.setPen(QPen(QColor(42, 54, 86, 200), 1.5))
    painter.drawPath(path)

    # Square Icon + Title
    icon_color = QColor(card["color"])
    painter.fillRect(QRectF(cx + 26, cy + 28, 18, 18), QBrush(icon_color))

    painter.setPen(QColor("#ffffff"))
    painter.setFont(QFont("Segoe UI", 18, QFont.Bold))
    painter.drawText(cx + 52, cy + 44, card["title"])

    # Subtitle
    painter.setPen(QColor("#94a3b8"))
    painter.setFont(QFont("Segoe UI", 10))
    painter.drawText(cx + 26, cy + 72, card["sub"])

    # Dotted Grid Lines
    grid_top = cy + 120
    grid_bottom = cy + 620
    grid_height = grid_bottom - grid_top

    painter.setPen(QPen(QColor(51, 65, 85, 100), 1, Qt.DashLine))
    for step in range(4):
        gy = grid_top + (step * grid_height / 3.0)
        painter.drawLine(int(cx + 26), int(gy), int(cx + card_w - 26), int(gy))

    # Draw Bars
    items = card["data"]
    n_items = len(items)
    plot_w = card_w - 60
    bar_slot = plot_w / n_items
    bar_width = bar_slot * 0.72

    for i, item in enumerate(items):
        name = item[0]
        val = item[1]
        val_str = str(val) if card["type"] != "cost" else item[2]
        color_hex = item[2] if card["type"] != "cost" else item[3]
        is_highlight = item[3] if card["type"] != "cost" else item[4]

        # Calculate height
        bh = (val / card["max_val"]) * grid_height
        bx = cx + 30 + i * bar_slot + (bar_slot - bar_width) / 2.0
        by = grid_bottom - bh

        # Bar Shape
        bar_path = QPainterPath()
        bar_path.addRoundedRect(QRectF(bx, by, bar_width, bh), 5, 5)

        base_color = QColor(color_hex)
        if is_highlight:
            # Glowing highlight for Gemini / Key Choice
            bar_grad = QLinearGradient(bx, by, bx, grid_bottom)
            bar_grad.setColorAt(0.0, QColor("#34d399"))
            bar_grad.setColorAt(1.0, QColor("#059669"))
            painter.fillPath(bar_path, QBrush(bar_grad))
            painter.setPen(QPen(QColor("#a7f3d0"), 2))
            painter.drawPath(bar_path)
        else:
            bar_grad = QLinearGradient(bx, by, bx, grid_bottom)
            bar_grad.setColorAt(0.0, base_color.lighter(115))
            bar_grad.setColorAt(1.0, base_color.darker(110))
            painter.fillPath(bar_path, QBrush(bar_grad))
            painter.setPen(Qt.NoPen)
            painter.drawPath(bar_path)

        # Value text inside/above bar
        painter.setFont(QFont("Segoe UI", 9, QFont.Bold))
        if is_highlight:
            painter.setPen(QColor("#ffffff"))
        else:
            painter.setPen(QColor("#e2e8f0"))

        if bh > 28:
            painter.drawText(QRectF(bx - 10, by + 6, bar_width + 20, 20), Qt.AlignCenter, val_str)
        else:
            painter.drawText(QRectF(bx - 10, by - 20, bar_width + 20, 20), Qt.AlignCenter, val_str)

        # Rotated Label below bar
        painter.save()
        painter.translate(bx + bar_width / 2.0, grid_bottom + 15)
        painter.rotate(65)
        painter.setFont(QFont("Segoe UI", 9, QFont.Bold if is_highlight else QFont.Normal))
        if is_highlight:
            painter.setPen(QColor("#34d399"))
        else:
            painter.setPen(QColor("#cbd5e1"))
        painter.drawText(0, 0, name)
        painter.restore()

# Save rendered image
out_path = r"c:\Users\DELL\Desktop\solife-flask\static\slides\slide_benchmark_exact.png"
image.save(out_path, "PNG")
image.save(r"c:\Users\DELL\Desktop\solife-flask\static\slide_benchmark_exact.png", "PNG")
print("Successfully generated exact high-res benchmark slide!")
