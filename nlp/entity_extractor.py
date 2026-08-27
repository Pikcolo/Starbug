"""
Entity Extraction engine for parsing prices, categories, preparation types, and flavor/mood tags.
"""
import re
from typing import Dict, Any, Optional, List
from nlp.normalizer import normalize_text


CATEGORY_KEYWORDS = {
    "espresso": ["กาแฟ", "เอสเพรสโซ่", "ลาเต้", "อเมริกาโน่", "คาปูชิโน่", "มอคค่า", "มัคคิอาโต", "coffee", "latte", "americano", "espresso", "cappuccino", "mocha", "macchiato"],
    "tea": ["ชาเขียว", "มัทฉะ", "ชา", "กรีนที", "tea", "matcha", "green tea", "hibiscus", "ฮิบิสคัส"],
    "frappuccino": ["ปั่น", "แฟรปปูชิโน่", "frappuccino", "frappe", "blended"],
    "cold_brew": ["โคลด์ บรูว์", "สกัดเย็น", "cold brew", "coldbrew"],
    "refresher": ["รีเฟรชเชอร์", "สดชื่น", "ผลไม้", "สตรอเบอร์รี่", "อาซาอิ", "มะม่วง", "แก้วมังกร", "pink drink", "dragon drink", "refresher", "lemonade", "เลมอนเนด"],
    "bakery": ["ขนม", "เบเกอรี่", "ครัวซองต์", "มัฟฟิน", "เค้ก", "แซนด์วิช", "เบเกิล", "บริออช", "bakery", "cake", "croissant", "sandwich", "bread", "pastry"]
}

PREP_TYPE_KEYWORDS = {
    "hot": ["ร้อน", "hot", "อุ่น"],
    "iced": ["เย็น", "iced", "cold", "ใส่น้ำแข็ง"],
    "frappuccino": ["ปั่น", "frappe", "frappuccino", "blended"]
}

FLAVOR_MOOD_KEYWORDS = {
    "matcha": ["ชาเขียว", "มัทฉะ", "matcha", "green tea"],
    "chocolate": ["ช็อกโกแลต", "โกโก้", "มอคค่า", "chocolate", "cocoa", "mocha"],
    "caramel": ["คาราเมล", "caramel"],
    "vanilla": ["วานิลลา", "vanilla"],
    "coffee_strong": ["เข้ม", "ตื่น", "กาแฟดำ", "เข้มข้น", "strong", "dark"],
    "fruity_refreshing": ["สดชื่น", "เปรี้ยว", "ผลไม้", "เลมอน", "สดใส", "refreshing", "fruity", "berry"],
    "milky_smooth": ["นม", "นุ่ม", "ละมุน", "มัน", "smooth", "milky"],
    "sweet": ["หวาน", "หวานๆ", "sweet"]
}


def extract_price_range(text: str) -> Dict[str, Optional[int]]:
    """
    Extracts minimum and maximum price constraints from text.
    Handles:
    - 'ไม่เกิน 150 บาท', 'งบ 160', 'ต่ำกว่า 170', 'ไม่เกิน 160', '< 150'
    - '100 - 150 บาท'
    - 'มากกว่า 100', '120 ขึ้นไป'
    """
    clean = normalize_text(text)
    result = {"min_price": None, "max_price": None}

    # Range pattern: e.g. "100-150", "100 ถึง 150"
    range_match = re.search(r'(\d+)\s*(?:-|ถึง|to)\s*(\d+)', clean)
    if range_match:
        p1 = int(range_match.group(1))
        p2 = int(range_match.group(2))
        result["min_price"] = min(p1, p2)
        result["max_price"] = max(p1, p2)
        return result

    # Max price patterns: "ไม่เกิน 150", "ต่ำกว่า 150", "งบ 150", "ราคาไม่เกิน 170", "งบไม่เกิน 200"
    max_match = re.search(r'(?:ไม่เกิน|ต่ำกว่า|งบ|งบไม่เกิน|ราคาไม่เกิน|น้อยกว่า|budget|under|below|max)\s*(\d+)', clean)
    if max_match:
        result["max_price"] = int(max_match.group(1))
        return result

    # Suffix pattern: "150 บาทลงไป", "150 บ. พอ"
    suffix_max = re.search(r'(\d+)\s*(?:บาทลงไป|บาทพอ|บ\.)', clean)
    if suffix_max:
        result["max_price"] = int(suffix_max.group(1))
        return result

    # Min price patterns: "มากกว่า 100", "120 ขึ้นไป"
    min_match = re.search(r'(?:มากกว่า|เกิน|ขั้นต่ำ|อย่างน้อย|above|more than)\s*(\d+)', clean)
    if min_match:
        result["min_price"] = int(min_match.group(1))
        return result
        
    suffix_min = re.search(r'(\d+)\s*(?:บาทขึ้นไป|ขึ้นไป)', clean)
    if suffix_min:
        result["min_price"] = int(suffix_min.group(1))
        return result

    return result


def extract_size(text: str) -> Optional[str]:
    """Extracts requested drink size: Tall, Grande, Venti."""
    clean = normalize_text(text).lower()
    if any(k in clean for k in ["venti", "เวนติ", "เวนตี้", "แก้วใหญ่", "ขนาดใหญ่", "ใหญ่"]):
        return "Venti"
    if any(k in clean for k in ["grande", "แกรนเด", "แกรนด์", "แก้วกลาง", "ขนาดกลาง", "กลาง"]):
        return "Grande"
    if any(k in clean for k in ["tall", "ทอล", "ทอลล์", "แก้วเล็ก", "ขนาดเล็ก", "เล็ก"]):
        return "Tall"
    if any(k in clean for k in ["doppio", "ดอปปิโอ", "ด๊อปปิโอ", "ดับเบิ้ลช็อต"]):
        return "Doppio"
    if any(k in clean for k in ["solo", "โซโล", "ซิงเกิ้ลช็อต"]):
        return "Solo"
    if any(k in clean for k in ["short", "ชอร์ต"]):
        return "Short"
    return None


def extract_entities(text: str) -> Dict[str, Any]:
    """
    Extracts all relevant entities:
    - categories
    - prep_types
    - flavor_moods
    - price constraints
    - selected_size
    - specific search keyword
    """
    normalized = normalize_text(text)
    
    # 1. Prices
    prices = extract_price_range(normalized)
    
    # 2. Categories
    detected_categories = []
    for cat, kws in CATEGORY_KEYWORDS.items():
        if any(kw in normalized for kw in kws):
            detected_categories.append(cat)
            
    # 3. Preparation types
    detected_preps = []
    for prep, kws in PREP_TYPE_KEYWORDS.items():
        if any(kw in normalized for kw in kws):
            detected_preps.append(prep)
            
    # 4. Flavor and Moods
    detected_flavors = []
    for flavor, kws in FLAVOR_MOOD_KEYWORDS.items():
        if any(kw in normalized for kw in kws):
            detected_flavors.append(flavor)

    # 5. Food vs Beverage preference
    is_food_query = any(kw in normalized for kw in ["ขนม", "เค้ก", "อาหาร", "เบเกอรี่", "ครัวซองต์", "แซนด์วิช", "กิน", "หิว"])
    
    # 6. Selected Size
    selected_size = extract_size(normalized)

    return {
        "raw_query": text,
        "normalized_query": normalized,
        "min_price": prices["min_price"],
        "max_price": prices["max_price"],
        "categories": detected_categories,
        "prep_types": detected_preps,
        "flavor_moods": detected_flavors,
        "is_food_query": is_food_query,
        "selected_size": selected_size
    }
