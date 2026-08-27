"""
LINE Flex Message for Order Confirmation & Receipt.
Provides a clear, elegant order completed card with order details and website link.
"""
import random
from typing import Dict, Any, Optional


def create_order_confirmation_flex(item: Optional[Dict[str, Any]] = None, order_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Creates an official Starbucks-style Order Completed / Receipt Flex Card.
    """
    if not order_id:
        order_id = f"SBX-{random.randint(1000, 9999)}"

    name_th = item.get("name_th", "เครื่องดื่มสตาร์บัคส์") if item else "เมนูสตาร์บัคส์ที่คุณเลือก"
    name_en = item.get("name_en", "Starbucks Beverage") if item else "Starbucks Order"
    price = item.get("price", 150) if item else 150
    image_url = item.get("image_url") if item and item.get("image_url") else "https://images.unsplash.com/photo-1541167760496-1628856ab772?w=600&auto=format&fit=crop&q=80"
    size_str = item.get("selected_size") if item and item.get("selected_size") else None

    receipt_rows = [
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": "สถานะ:", "size": "xs", "color": "#777777", "flex": 2},
                {"type": "text", "text": "กำลังสะบัดกาน้ำชง 45° ☕", "size": "xs", "color": "#006241", "weight": "bold", "flex": 3}
            ]
        }
    ]
    if size_str:
        receipt_rows.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": "ขนาดที่เลือก:", "size": "xs", "color": "#777777", "flex": 2},
                {"type": "text", "text": f"{size_str} 📏", "size": "xs", "color": "#1E3932", "weight": "bold", "flex": 3}
            ]
        })
    receipt_rows.extend([
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": "เวลารับสินค้า:", "size": "xs", "color": "#777777", "flex": 2},
                {"type": "text", "text": "ประมาณ 10-15 นาที (หรือโรตีสุก 🤣)", "size": "xs", "color": "#333333", "weight": "bold", "flex": 3}
            ]
        },
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": "ยอดรวมทั้งสิ้น:", "size": "xs", "color": "#777777", "flex": 2},
                {"type": "text", "text": f"฿{price}", "size": "sm", "color": "#D9383A", "weight": "bold", "flex": 3}
            ]
        }
    ])

    bubble = {
        "type": "flex",
        "altText": f"✅ สั่งซื้อรายการเสร็จสิ้น: {name_th}",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#006241",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "text",
                        "text": "✅ รับออเดอร์แล้วจ้านายจ๋า 👳‍♂️",
                        "weight": "bold",
                        "size": "md",
                        "color": "#FFFFFF"
                    },
                    {
                        "type": "text",
                        "text": f"รหัสคำสั่งซื้อ: #{order_id}",
                        "size": "xxs",
                        "color": "#D4E9E2",
                        "margin": "xs"
                    }
                ]
            },
            "hero": {
                "type": "image",
                "url": image_url,
                "size": "full",
                "aspectRatio": "20:11",
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "text",
                        "text": name_th,
                        "weight": "bold",
                        "size": "md",
                        "color": "#1E3932",
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "text": name_en,
                        "size": "xs",
                        "color": "#777777",
                        "wrap": True
                    },
                    {"type": "separator", "margin": "md"},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "spacing": "xs",
                        "contents": receipt_rows
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "paddingAll": "12px",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#006241",
                        "height": "sm",
                        "action": {
                            "type": "uri",
                            "label": "🌐 ไปที่หน้าเว็บ Starbug เพื่อชำระเงินนะจ๊ะ",
                            "uri": "https://www.starbucks.co.th/th"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "color": "#F0F0F0",
                        "action": {
                            "type": "message",
                            "label": "ดูเมนูอื่นเพิ่มเติม 📋",
                            "text": "ขอดูเมนูสตาร์บัคส์"
                        }
                    }
                ]
            }
        }
    }
    return bubble
