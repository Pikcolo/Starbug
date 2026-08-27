"""
LINE Flex Message Carousel Generator for Starbucks Thailand.
Renders responsive, visually stunning Starbucks-branded product cards.
"""
from typing import List, Dict, Any


def create_product_bubble(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a single Starbucks-themed Flex Message Bubble.
    """
    name_th = item.get("name_th", "สตาร์บัคส์")
    name_en = item.get("name_en", "")
    price = item.get("price", 0)
    image_url = item.get("image_url", "https://www.starbucks.co.th/image-placeholder.png")
    calories = item.get("calories", "")
    desc = item.get("description", "")
    is_new = item.get("is_new", False)
    is_promo = item.get("is_promo", False)
    promo_text = item.get("promo_text", "")

    # Header Badges
    badge_contents = []
    if is_new:
        badge_contents.append({
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "✨ เมนูใหม่",
                    "size": "xxs",
                    "color": "#FFFFFF",
                    "weight": "bold"
                }
            ],
            "backgroundColor": "#CBA258",
            "cornerRadius": "sm",
            "paddingAll": "3px",
            "paddingStart": "6px",
            "paddingEnd": "6px"
        })
    if is_promo:
        badge_contents.append({
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🏷️ มีโปรโมชั่น",
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
        })

    prices_dict = item.get("prices", {})
    has_multiple_sizes = isinstance(prices_dict, dict) and len(prices_dict) > 1

    # Format size text if available
    size_summary = ""
    if has_multiple_sizes:
        size_parts = [f"{sz}: ฿{pr}" for sz, pr in prices_dict.items() if pr > 0]
        size_summary = " • ".join(size_parts)

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "hero": {
            "type": "image",
            "url": image_url,
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "backgroundColor": "#F5F5F5",
            "action": {
                "type": "message",
                "label": "View Image",
                "text": f"ขอดูรายละเอียด {name_th}"
            }
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "paddingAll": "16px",
            "contents": [
                # Badge row
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "contents": badge_contents if badge_contents else [
                        {
                            "type": "text",
                            "text": "STARBUG ภารตะ 👳‍♂️",
                            "size": "xxs",
                            "color": "#006241",
                            "weight": "bold"
                        }
                    ]
                },
                # Product Name Thai
                {
                    "type": "text",
                    "text": name_th,
                    "weight": "bold",
                    "size": "md",
                    "color": "#1E3932",
                    "wrap": True,
                    "maxLines": 2
                },
                # Product Name English
                {
                    "type": "text",
                    "text": name_en,
                    "size": "xs",
                    "color": "#767676",
                    "wrap": True,
                    "maxLines": 1
                },
                # Price & Calories Row
                {
                    "type": "box",
                    "layout": "horizontal",
                    "alignItems": "center",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"฿{price}",
                            "weight": "bold",
                            "size": "lg",
                            "color": "#006241",
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": f"({calories})" if calories else "",
                            "size": "xxs",
                            "color": "#9E9E9E",
                            "margin": "sm",
                            "gravity": "bottom"
                        }
                    ]
                },
                # Size Options breakdown if available
                *(
                    [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"📏 {size_summary}",
                                    "size": "xxs",
                                    "color": "#006241",
                                    "weight": "bold",
                                    "wrap": True
                                }
                            ],
                            "backgroundColor": "#EBF6F2",
                            "paddingAll": "4px",
                            "cornerRadius": "sm",
                            "margin": "xs"
                        }
                    ] if has_multiple_sizes else []
                ),
                # Description excerpt
                {
                    "type": "text",
                    "text": desc,
                    "size": "xxs",
                    "color": "#555555",
                    "wrap": True,
                    "maxLines": 2,
                    "margin": "xs"
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "paddingAll": "12px",
            "contents": [
                {
                    "type": "button",
                    "style": "secondary",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "เลือกขนาด 📏" if has_multiple_sizes else "รายละเอียดจ้ะ",
                        "text": f"ขอดูรายละเอียด {name_th}"
                    },
                    "color": "#EAEAEA"
                },
                {
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "สั่งเลยจ้ะ 🛍️",
                        "text": f"สั่งเมนู {name_th} 1 รายการครับ"
                    },
                    "color": "#006241"
                }
            ]
        }
    }
    return bubble


def create_product_carousel_flex(items: List[Dict[str, Any]], alt_text: str = "เมนูแนะนำจากสตาร์บัคส์") -> Dict[str, Any]:
    """
    Creates a full LINE Carousel Flex Message containing up to 10 product cards.
    """
    bubbles = [create_product_bubble(item) for item in items[:10]]
    if not bubbles:
        return {
            "type": "flex",
            "altText": alt_text,
            "contents": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "ไม่พบเมนูที่ค้นหา ลองค้นหาใหม่อีกครั้งนะครับ ☕",
                            "wrap": True
                        }
                    ]
                }
            }
        }

    return {
        "type": "flex",
        "altText": alt_text,
        "contents": {
            "type": "carousel",
            "contents": bubbles
        }
    }
