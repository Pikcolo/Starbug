"""
LINE Flex Message for Promotions and Special Deals.
"""
from typing import List, Dict, Any


def create_promotions_carousel(promos: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Renders promotional cards with badges and detailed terms.
    """
    bubbles = []
    for p in promos:
        bubble = {
            "type": "bubble",
            "size": "kilo",
            "hero": {
                "type": "image",
                "url": p.get("image_url", "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600&auto=format&fit=crop&q=80"),
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": p.get("badge", "PROMOTION"),
                                "size": "xxs",
                                "color": "#FFFFFF",
                                "weight": "bold"
                            }
                        ],
                        "backgroundColor": "#D9383A",
                        "cornerRadius": "sm",
                        "paddingAll": "3px",
                        "paddingStart": "6px",
                        "paddingEnd": "6px"
                    },
                    {
                        "type": "text",
                        "text": p.get("title", "โปรโมชั่นสตาร์บัคส์"),
                        "weight": "bold",
                        "size": "md",
                        "color": "#1E3932",
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "text": p.get("description", ""),
                        "size": "xs",
                        "color": "#555555",
                        "wrap": True,
                        "maxLines": 3
                    },
                    {
                        "type": "text",
                        "text": f"⏳ ระยะเวลา: {p.get('period', 'จำกัดเวลา')}",
                        "size": "xxs",
                        "color": "#888888",
                        "margin": "sm"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#006241",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "ดูเมนูที่ร่วมรายการ",
                            "text": f"ขอดูเมนูหมวด {p.get('applicable_category', 'all')}"
                        }
                    }
                ]
            }
        }
        bubbles.append(bubble)

    return {
        "type": "flex",
        "altText": "โปรโมชั่นและสิทธิพิเศษจากสตาร์บัคส์ 🏷️",
        "contents": {
            "type": "carousel",
            "contents": bubbles
        }
    }
