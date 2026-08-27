"""
Funny & Creative Interactive Features for Starbug AI Assistant (Indian Chaiwala & Bollywood Style).
Includes Sassy Barista Roast.
"""
import random
from typing import Dict, Any, List

BARISTA_ROASTS = [
    "👳‍♂️ แหม... นายจ๋าสั่งกาแฟหวาน 0% แต่ยืนจ้องตู้เค้กตาเป็นมัน บาริสต้าแอบเห็นนะจ๊ะนายจ๋า! 🤣",
    "😴 นายจ๋าเดินเข้ามาสภาพเหมือนวิญญาณหลุดออกจากร่างไปแล้ว 90% เดี๋ยวบาริสต้าสะบัดกาน้ำชงกาแฟกู้ชีพให้นะจ๊ะ!",
    "🥤 สั่งชาเขียวหวาน 0% แต่นมข้นกับผงมัทฉะในหม้อต้มหวานเจี๊ยบอยู่แล้ว... แต่ไม่เป็นไร บาริสต้าจะไม่บอกเทรนเนอร์ของนายจ๋านะจ๊ะ!",
    "💸 สั่งกาแฟแก้วละเกือบสองร้อยได้สบายๆ แต่ต่อราคาค่ามอเตอร์ไซค์ 5 บาท... เท่ระดับมหาราชาจริงๆ นะจ๊ะนายจ๋า!",
    "📱 ถ่ายรูปแก้วกาแฟลงสตอรี่ IG ไป 8 มุม 15 นาที น้ำแข็งละลายหมดแล้วแต่ฟิลเตอร์สตอรี่ยังไม่เสร็จ! แซวเล่นนะจ๊ะนายจ๋า 💚"
]


def get_random_barista_roast() -> str:
    """Returns a funny Indian chaiwala barista roast."""
    return random.choice(BARISTA_ROASTS)
