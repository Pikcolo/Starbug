"""
Intent definitions and rule-based semantic matcher patterns for Starbucks AI Assistant.
"""
from enum import Enum
from typing import List, Dict, Any


class IntentType(str, Enum):
    GREETING = "GREETING"
    HELP = "HELP"
    PROMOTIONS = "PROMOTIONS"
    NEW_ARRIVALS = "NEW_ARRIVALS"
    RANDOM_RECOMMEND = "RANDOM_RECOMMEND"
    PRICE_FILTER = "PRICE_FILTER"
    SEARCH_CATEGORY = "SEARCH_CATEGORY"
    SEARCH_FLAVOR_MOOD = "SEARCH_FLAVOR_MOOD"
    SEARCH_FOOD = "SEARCH_FOOD"
    ITEM_DETAIL = "ITEM_DETAIL"
    ORDER = "ORDER"
    FORTUNE = "FORTUNE"
    SECRET_RECIPE = "SECRET_RECIPE"
    BARISTA_ROAST = "BARISTA_ROAST"
    UNKNOWN = "UNKNOWN"


# Patterns mapping for high precision matching
INTENT_PATTERNS: Dict[IntentType, List[str]] = {
    IntentType.FORTUNE: [
        "ดูดวง", "ทำนายดวง", "ดวง", "กาแฟทำนายดวง", "ดวงวันนี้", "ดวงการงาน", "ดวงความรัก", "ดวงการเงิน", "หมอดู", "เซียมซี", "fortune", "horoscope"
    ],
    IntentType.SECRET_RECIPE: [
        "สูตรลับ", "เมนูแปลก", "เมนูลับ", "สูตรพิสดาร", "เมนูป่วน", "secret menu", "สูตรกวน", "เมนูในตำนาน", "custom แปลก"
    ],
    IntentType.BARISTA_ROAST: [
        "แซวหน่อย", "บ่นหน่อย", "บาริสต้าปากแซ่บ", "ด่าหน่อย", "ทายนิสัย", "แซวฉันหน่อย", "roast", "แซว"
    ],
    IntentType.ORDER: [
        "สั่งซื้อ", "สั่งเมนู", "สั่งเครื่องดื่ม", "สั่งแก้วนี้", "สั่ง", "order", "ซื้อ", "เช็คบิล", "ชำระเงิน", "checkout"
    ],
    IntentType.GREETING: [
        "สวัสดี", "หวัดดี", "ฮัลโหล", "hello", "hi", "hey", "ดีครับ", "ดีค่ะ", "เริ่ม", "start"
    ],
    IntentType.HELP: [
        "ช่วยด้วย", "วิธีใช้", "ทำอะไรได้บ้าง", "คู่มือ", "คำสั่ง", "help", "เมนูหลัก", "ใช้ยังไง"
    ],
    IntentType.PROMOTIONS: [
        "โปร", "โปรโมชั่น", "ส่วนลด", "ลดราคา", "1แถม1", "1 แถม 1", "ซื้อ 1 แถม 1", "promotion", "discount", "คุ้ม", "deal", "สิทธิพิเศษ", "ดาว"
    ],
    IntentType.NEW_ARRIVALS: [
        "ใหม่", "เมนูใหม่", "มาใหม่", "มีอะไรใหม่", "สินค้าใหม่", "new", "seasonal", "ซีซั่น", "ล่าสุด"
    ],
    IntentType.RANDOM_RECOMMEND: [
        "เมนูแนะนำวันนี้", "ขอดูเมนูแนะนำวันนี้", "แนะนำวันนี้", "เมนูแนะนำ", "สุ่ม", "กินอะไรดี", "ดื่มอะไรดี", "แนะนำ", "เลือกให้หน่อย", "ไม่รู้จะกินอะไร", "จัดให้หน่อย", "อะไรก็ได้", "random", "recommend", "surpise"
    ],
    IntentType.SEARCH_FOOD: [
        "ขนม", "ของกิน", "อาหาร", "เค้ก", "ครัวซองต์", "แซนด์วิช", "เบเกอรี่", "muffin", "bakery", "food", "bread", "cake", "หิว"
    ]
}
