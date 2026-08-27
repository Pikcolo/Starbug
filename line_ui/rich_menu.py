"""
LINE Rich Menu Generator and Uploader for Starbug Assistant.
Generates an official 2500x1686 6-grid Rich Menu image and configures LINE API.
"""
import os
import json
import logging
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

RICH_MENU_IMG_PATH = "web/static/images/rich_menu_starbug.png"


def generate_rich_menu_image(output_path: str = RICH_MENU_IMG_PATH):
    """
    Generates a 2500x1686 PNG image with 6 rich interactive cards for LINE Rich Menu.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    width, height = 2500, 1686
    img = Image.new("RGB", (width, height), color="#006241")
    draw = ImageDraw.Draw(img)

    # 6 Grid configuration: 3 columns x 2 rows
    cols, rows = 3, 2
    cell_w = width // cols
    cell_h = height // rows

    cards = [
        # Row 1
        {"title": "เมนูกาแฟ & ชา", "sub": "Coffee & Tea", "icon": "☕", "bg": "#006241", "accent": "#CBA258"},
        {"title": "เครื่องดื่มปั่น", "sub": "Frappuccino", "icon": "🥤", "bg": "#1E3932", "accent": "#D4E9E2"},
        {"title": "เบเกอรี่ & เค้ก", "sub": "Bakery & Cake", "icon": "🥐", "bg": "#006241", "accent": "#CBA258"},
        # Row 2
        {"title": "โปรโมชั่นเด็ด", "sub": "Flash Deals", "icon": "🏷️", "bg": "#D9383A", "accent": "#FFFFFF"},
        {"title": "เมนูแนะนำวันนี้", "sub": "Today's Picks", "icon": "⭐", "bg": "#1E3932", "accent": "#CBA258"},
        {"title": "บาริสต้าปากแซ่บ", "sub": "Sassy Roast", "icon": "🤣", "bg": "#006241", "accent": "#FFFFFF"},
    ]

    # Try loading Thai font or fallback to default
    try:
        font_title = ImageFont.truetype("tahoma.ttf", 68)
        font_sub = ImageFont.truetype("tahoma.ttf", 42)
        font_icon = ImageFont.truetype("seguiemj.ttf", 110)
    except Exception:
        try:
            font_title = ImageFont.truetype("arial.ttf", 68)
            font_sub = ImageFont.truetype("arial.ttf", 42)
            font_icon = font_title
        except Exception:
            font_title = ImageFont.load_default()
            font_sub = font_title
            font_icon = font_title

    idx = 0
    for r in range(rows):
        for c in range(cols):
            x1 = c * cell_w
            y1 = r * cell_h
            x2 = x1 + cell_w
            y2 = y1 + cell_h

            card = cards[idx]
            idx += 1

            # Card background
            draw.rectangle([x1 + 12, y1 + 12, x2 - 12, y2 - 12], fill=card["bg"], outline="#CBA258", width=4)

            # Draw card contents
            center_x = x1 + cell_w // 2
            center_y = y1 + cell_h // 2

            # Title & Subtitle
            draw.text((center_x, center_y - 80), card["icon"], fill=card["accent"], font=font_icon, anchor="mm")
            draw.text((center_x, center_y + 60), card["title"], fill="#FFFFFF", font=font_title, anchor="mm")
            draw.text((center_x, center_y + 140), card["sub"], fill=card["accent"], font=font_sub, anchor="mm")

    # Save generated image
    img.save(output_path, "PNG")
    logger.info(f"Rich menu image generated at: {output_path}")
    return output_path


def get_rich_menu_payload() -> dict:
    """
    Returns the LINE Rich Menu JSON schema with 6 touch bounds.
    """
    return {
        "size": {"width": 2500, "height": 1686},
        "selected": True,
        "name": "Starbug Official Rich Menu",
        "chatBarText": "เมนู Starbug",
        "areas": [
            {
                "bounds": {"x": 0, "y": 0, "width": 833, "height": 843},
                "action": {"type": "message", "text": "ขอดูเมนูกาแฟสดและลาเต้"}
            },
            {
                "bounds": {"x": 833, "y": 0, "width": 833, "height": 843},
                "action": {"type": "message", "text": "แนะนำเมนูปั่น Frappuccino"}
            },
            {
                "bounds": {"x": 1666, "y": 0, "width": 834, "height": 843},
                "action": {"type": "message", "text": "มีขนมและเบเกอรี่อะไรบ้าง"}
            },
            {
                "bounds": {"x": 0, "y": 843, "width": 833, "height": 843},
                "action": {"type": "message", "text": "มีโปรโมชั่นอะไรบ้าง"}
            },
            {
                "bounds": {"x": 833, "y": 843, "width": 833, "height": 843},
                "action": {"type": "message", "text": "ขอดูเมนูแนะนำวันนี้"}
            },
            {
                "bounds": {"x": 1666, "y": 843, "width": 834, "height": 843},
                "action": {"type": "message", "text": "แซวฉันหน่อย บาริสต้าปากแซ่บ"}
            }
        ]
    }
