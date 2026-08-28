"""
Contextual Quick Reply generator for LINE Bot.
Provides quick-action chips for easy NLP interaction.
"""
from typing import List, Dict, Any


def get_default_quick_replies() -> Dict[str, Any]:
    """
    Returns concise, essential Starbug quick reply options (5 focused chips).
    """
    return {
        "items": [
            {
                "type": "action",
                "action": {
                    "type": "message",
                    "label": "⭐ เมนูแนะนำวันนี้",
                    "text": "ขอดูเมนูแนะนำวันนี้"
                }
            },
            {
                "type": "action",
                "action": {
                    "type": "message",
                    "label": "☕ เมนูกาแฟสด",
                    "text": "ขอดูเมนูกาแฟสดและลาเต้"
                }
            },
            {
                "type": "action",
                "action": {
                    "type": "message",
                    "label": "🥐 เบเกอรี่ & เค้ก",
                    "text": "มีขนมและเบเกอรี่อะไรบ้าง"
                }
            },
            {
                "type": "action",
                "action": {
                    "type": "message",
                    "label": "🏷️ โปรโมชั่นเด็ด",
                    "text": "มีโปรโมชั่นส่วนลดอะไรบ้าง"
                }
            },
            {
                "type": "action",
                "action": {
                    "type": "message",
                    "label": "📖 วิธีการใช้งาน",
                    "text": "วิธีการใช้งาน"
                }
            },
            {
                "type": "action",
                "action": {
                    "type": "message",
                    "label": "🤣 บาริสต้าปากแซ่บ",
                    "text": "แซวฉันหน่อย บาริสต้าปากแซ่บ"
                }
            }
        ]
    }
