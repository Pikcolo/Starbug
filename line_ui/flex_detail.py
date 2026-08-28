"""
Single Product Detail Flex Message Bubble.
"""
from typing import Dict, Any


def create_product_detail_flex(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Renders an in-depth product specification card with prices per size,
    dietary/customization options, and calorie info.
    """
    name_th = item.get("name_th", "สตาร์บัคส์")
    name_en = item.get("name_en") or name_th
    price = item.get("price", 0)
    prices = item.get("prices", {"Tall": price, "Grande": price + 15, "Venti": price + 30}) if item.get("prices") else {"Standard": price}
    image_url = item.get("image_url") or "https://www.starbucks.co.th/image-placeholder.png"
    calories = item.get("calories") or "ข้อมูลมาตรฐาน"
    desc = item.get("description") or "เมนูคุณภาพคัดสรรพิเศษจาก Starbug สดใหม่พร้อมเสิร์ฟ"
    promo_text = item.get("promo_text", "")
    
    prep_list = item.get("prep_types") or []
    prep_types = ", ".join(prep_list) if prep_list else ("เบเกอรี่ & ขนมอบ 🥐" if item.get("is_food") else "พร้อมเสิร์ฟ ☕")

    price_rows = []
    for sz, p in prices.items():
        price_rows.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": f"ขนาด {sz}", "size": "sm", "color": "#555555", "flex": 3},
                {"type": "text", "text": f"฿{p}", "size": "sm", "color": "#006241", "weight": "bold", "align": "end", "flex": 2}
            ]
        })

    # Generate quick size selection buttons if multiple sizes exist
    size_buttons = []
    if len(prices) > 1:
        for sz, p in prices.items():
            if p > 0:
                size_buttons.append({
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "color": "#006241",
                    "action": {
                        "type": "message",
                        "label": f"สั่ง {sz} (฿{p})",
                        "text": f"สั่งซื้อ {name_th} ขนาด {sz}"
                    }
                })

    single_size_label = list(prices.keys())[0] if prices else "Standard"
    single_size_price = list(prices.values())[0] if prices else price

    bubble = {
        "type": "flex",
        "altText": f"รายละเอียดสินค้า: {name_th}",
        "contents": {
            "type": "bubble",
            "size": "mega",
            "hero": {
                "type": "image",
                "url": image_url,
                "size": "full",
                "aspectRatio": "16:9",
                "aspectMode": "cover",
                "backgroundColor": "#F5F5F5"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": name_th,
                        "weight": "bold",
                        "size": "xl",
                        "color": "#1E3932",
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "text": name_en,
                        "size": "xs",
                        "color": "#888888",
                        "wrap": True
                    },
                    {"type": "separator", "margin": "sm"},
                    {
                        "type": "text",
                        "text": desc,
                        "size": "sm",
                        "color": "#444444",
                        "wrap": True
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "spacing": "sm",
                        "backgroundColor": "#F7F7F7",
                        "paddingAll": "12px",
                        "cornerRadius": "md",
                        "contents": price_rows
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "🔥 แคลอรี่:", "size": "xs", "color": "#777777", "flex": 2},
                            {"type": "text", "text": str(calories), "size": "xs", "color": "#222222", "weight": "bold", "flex": 3}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "☕ รูปแบบ:", "size": "xs", "color": "#777777", "flex": 2},
                            {"type": "text", "text": prep_types, "size": "xs", "color": "#222222", "weight": "bold", "flex": 3}
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    # Size selection row if available
                    *(
                        [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "spacing": "xs",
                                "contents": size_buttons
                            }
                        ] if size_buttons else [
                            {
                                "type": "button",
                                "style": "primary",
                                "color": "#006241",
                                "height": "sm",
                                "action": {
                                    "type": "message",
                                    "label": f"สั่งซื้อทันที ฿{single_size_price} 🛍️",
                                    "text": f"สั่งซื้อ {name_th} ขนาด {single_size_label}"
                                }
                            }
                        ]
                    ),
                    {
                        "type": "button",
                        "style": "secondary",
                        "color": "#F0F0F0",
                        "height": "sm",
                        "action": {
                            "type": "uri",
                            "label": "🌐 สั่งซื้อผ่านเว็บ Starbucks",
                            "uri": "https://www.starbucks.co.th/th"
                        }
                    }
                ]
            }
        }
    }
    return bubble
