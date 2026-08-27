"""
LINE Flex Message UI for Funny Features (Fortune Teller, Secret Recipes, Wealth Calculator).
"""
from typing import Dict, Any


def create_fortune_flex(fortune_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Renders Starbucks Fortune Teller Flex Card.
    """
    topic = fortune_data.get("topic", "🔮 ดวงชะตากาแฟวันนี้")
    fortune = fortune_data.get("fortune", "")
    lucky_drink = fortune_data.get("lucky_drink", "กาแฟสตาร์บัคส์")
    tip = fortune_data.get("tip", "")
    img_url = fortune_data.get("image_url", "https://blob.starbucks.co.th/publicproduct26/home-banner-1784217494661.jpg")

    bubble = {
        "type": "flex",
        "altText": f"🔮 คำทำนายดวงชะตา: {topic}",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#1E3932",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "text",
                        "text": "🔮 หมอดูบาริสต้าทำนายดวง",
                        "weight": "bold",
                        "size": "md",
                        "color": "#CBA258"
                    },
                    {
                        "type": "text",
                        "text": topic,
                        "size": "xs",
                        "color": "#FFFFFF",
                        "margin": "xs"
                    }
                ]
            },
            "hero": {
                "type": "image",
                "url": img_url,
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
                        "text": fortune,
                        "size": "sm",
                        "color": "#333333",
                        "wrap": True
                    },
                    {"type": "separator", "margin": "md"},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "spacing": "xs",
                        "backgroundColor": "#F4F7F5",
                        "paddingAll": "10px",
                        "cornerRadius": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": "☕ เมนูเครื่องดื่มเสริมดวง:",
                                "size": "xs",
                                "color": "#006241",
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": lucky_drink,
                                "size": "sm",
                                "color": "#1E3932",
                                "weight": "bold",
                                "wrap": True
                            },
                            {
                                "type": "text",
                                "text": f"💡 เคล็ดลับ: {tip}",
                                "size": "xxs",
                                "color": "#666666",
                                "wrap": True,
                                "margin": "xs"
                            }
                        ]
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
                            "type": "message",
                            "label": f"สั่งเมนูเสริมดวงนี้ทันที ☕",
                            "text": f"สั่งซื้อ {lucky_drink}"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "color": "#F0F0F0",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "🎲 สุ่มดูดวงใหม่อีกรอบ",
                            "text": "ดูดวงกาแฟให้หน่อย"
                        }
                    }
                ]
            }
        }
    }
    return bubble


def create_secret_recipe_flex(recipe: Dict[str, Any]) -> Dict[str, Any]:
    """
    Renders Secret/Chaos Custom Recipe Flex Card.
    """
    title = recipe.get("title", "สูตรลับในตำนาน")
    base = recipe.get("base", "")
    custom = recipe.get("custom", "")
    price = recipe.get("price_est", 200)
    effect = recipe.get("effect", "")
    script = recipe.get("script_to_order", "")
    img_url = recipe.get("image_url", "https://blob.starbucks.co.th/publicproduct26/home-banner-1784517024412.png")

    bubble = {
        "type": "flex",
        "altText": f"🧪 {title}",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#D9383A",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "text",
                        "text": "🧪 สูตรลับในตำนานสาย Custom",
                        "weight": "bold",
                        "size": "xs",
                        "color": "#FFFFFF"
                    },
                    {
                        "type": "text",
                        "text": title,
                        "size": "md",
                        "weight": "bold",
                        "color": "#FFFFFF",
                        "wrap": True,
                        "margin": "xs"
                    }
                ]
            },
            "hero": {
                "type": "image",
                "url": img_url,
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
                        "text": f"📌 ฐานเมนู: {base}",
                        "size": "xs",
                        "color": "#222222",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f"🪄 สั่งเพิ่ม: {custom}",
                        "size": "xs",
                        "color": "#006241",
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "text": f"✨ สรรพคุณ: {effect}",
                        "size": "xxs",
                        "color": "#666666",
                        "wrap": True,
                        "margin": "xs"
                    },
                    {"type": "separator", "margin": "sm"},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": "#FFF8E7",
                        "paddingAll": "8px",
                        "cornerRadius": "sm",
                        "margin": "sm",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🗣️ โพยพูดสั่งหน้าร้าน:",
                                "size": "xxs",
                                "color": "#A05A00",
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": f'"{script}"',
                                "size": "xs",
                                "color": "#333333",
                                "style": "italic",
                                "wrap": True
                            }
                        ]
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
                            "label": "🌐 ไปที่หน้าเว็บสั่งซื้อ Starbucks",
                            "uri": "https://www.starbucks.co.th/th"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "color": "#F0F0F0",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "🧪 สุ่มสูตรลับอื่นอีก",
                            "text": "ขอสูตรลับสตาร์บัคส์หน่อย"
                        }
                    }
                ]
            }
        }
    }
    return bubble
