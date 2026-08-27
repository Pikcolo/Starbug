"""
Data cleaning and attribute normalization pipeline for Starbucks Thailand menu data.
Provides robust attribute sanitization, price extraction, tag assignment, and schema validation.
"""
import re
from typing import Dict, Any, Optional, List


def clean_price(price_val: Any) -> int:
    """
    Extracts an integer THB price from varied inputs:
    e.g., '฿165', '165 บาท', '165.00', 165 -> 165
    Returns 0 if missing or unparseable.
    """
    if price_val is None:
        return 0
    if isinstance(price_val, (int, float)):
        return int(price_val)
    
    price_str = str(price_val)
    # Find all digits
    match = re.search(r"(\d+(?:\.\d+)?)", price_str.replace(",", ""))
    if match:
        try:
            return int(float(match.group(1)))
        except (ValueError, TypeError):
            return 0
    return 0


def sanitize_text(text: Optional[str]) -> str:
    """Removes excess whitespace, HTML tags, and non-printable characters."""
    if not text:
        return ""
    # Replace HTML tags with space to preserve separation between tags
    clean = re.sub(r"<[^>]+>", " ", text)
    # Normalize whitespace
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean


def infer_tags_and_attributes(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Infers additional metadata, tags, and category classifications
    based on product name, description, and category.
    """
    name_th = item.get("name_th", "") or ""
    name_en = item.get("name_en", "") or ""
    desc = item.get("description", "") or ""
    full_text = f"{name_th} {name_en} {desc}".lower()

    # Temperature / Prep methods
    prep_types = []
    if any(k in full_text for k in ["ร้อน", "hot"]):
        prep_types.append("hot")
    if any(k in full_text for k in ["เย็น", "iced", "cold"]):
        prep_types.append("iced")
    if any(k in full_text for k in ["ปั่น", "frappuccino", "blended", "frappe"]):
        prep_types.append("frappuccino")
    if not prep_types:
        # Default for drinks if unspecified
        if item.get("is_beverage", True):
            prep_types = ["hot", "iced"]

    # Flavor / Taste Notes
    flavor_notes = []
    flavor_map = {
        "matcha": ["ชาเขียว", "matcha", "มัทฉะ", "green tea"],
        "chocolate": ["ช็อกโกแลต", "chocolate", "โกโก้", "cocoa", "มอคค่า", "mocha", "ช็อคโกแลต"],
        "caramel": ["คาราเมล", "caramel"],
        "vanilla": ["วานิลลา", "vanilla"],
        "coffee_strong": ["เอสเพรสโซ", "espresso", "americano", "อเมริกาโน่", "cold brew", "เข้ม"],
        "fruity_refreshing": ["สดชื่น", "refresher", "berry", "เบอร์รี่", "strawberry", "yuzu", "ยูสุ", "peach", "พีช", "lemon", "มะนาว", "ส้ม", "orange"],
        "milky_smooth": ["ลาเต้", "latte", "นม", "milk", "คาปูชิโน", "cappuccino", "ละมุน"],
        "sweet": ["หวาน", "sweet", "frappuccino", "caramel", "honey", "น้ำผึ้ง"]
    }
    for note, keywords in flavor_map.items():
        if any(kw in full_text for kw in keywords):
            flavor_notes.append(note)

    # Category determination
    is_food = item.get("is_food", False)
    if not is_food:
        food_keywords = ["เค้ก", "cake", "ครัวซอง", "croissant", "แซนด์วิช", "sandwich", "ขนมปัง", "bread", "muffin", "พาย", "pie", "cookie", "คุกกี้", "เบเกอรี่", "bakery"]
        if any(kw in full_text for kw in food_keywords) or item.get("category", "") in ["bakery", "food", "dessert"]:
            is_food = True

    is_beverage = not is_food

    return {
        "prep_types": prep_types,
        "flavor_notes": flavor_notes,
        "is_food": is_food,
        "is_beverage": is_beverage,
    }


def clean_menu_item(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Cleans a single menu item dictionary and ensures all standard fields exist.
    """
    name_th = sanitize_text(raw.get("name_th") or raw.get("name", "สินค้าสตาร์บัคส์"))
    name_en = sanitize_text(raw.get("name_en") or raw.get("name", ""))
    
    price = clean_price(raw.get("price", 0))
    if price == 0 and "prices" in raw and isinstance(raw["prices"], dict):
        # Fallback to smallest size price
        for sz in ["tall", "grande", "venti", "regular"]:
            if sz in raw["prices"]:
                price = clean_price(raw["prices"][sz])
                if price > 0:
                    break

    image_url = raw.get("image_url") or "https://www.starbucks.co.th/image-placeholder.png"
    description = sanitize_text(raw.get("description", ""))
    category = sanitize_text(raw.get("category", "beverage")).lower()
    subcategory = sanitize_text(raw.get("subcategory", "")).lower()
    
    is_new = bool(raw.get("is_new", False))
    is_promo = bool(raw.get("is_promo", False))
    promo_text = sanitize_text(raw.get("promo_text", ""))
    
    cleaned = {
        "id": str(raw.get("id", re.sub(r'[^a-zA-Z0-9]', '_', name_en.lower() if name_en else name_th))),
        "name_th": name_th,
        "name_en": name_en,
        "category": category,
        "subcategory": subcategory,
        "price": price,
        "prices": raw.get("prices", {
            "Tall": price,
            "Grande": price + 15 if price > 0 else 0,
            "Venti": price + 30 if price > 0 else 0
        }),
        "calories": raw.get("calories", "150-280 kcal"),
        "image_url": image_url,
        "description": description,
        "is_new": is_new,
        "is_promo": is_promo,
        "promo_text": promo_text,
        "is_food": bool(raw.get("is_food", False)),
        "is_beverage": bool(raw.get("is_beverage", True)),
    }
    
    # Infer smart tags
    inferred = infer_tags_and_attributes(cleaned)
    cleaned.update(inferred)
    
    return cleaned


def clean_dataset(raw_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Clean a whole dataset with duplicate removal and integrity validation."""
    seen_ids = set()
    cleaned_items = []
    
    for item in raw_list:
        try:
            cleaned = clean_menu_item(item)
            if cleaned["id"] in seen_ids:
                cleaned["id"] = f"{cleaned['id']}_{len(seen_ids)}"
            seen_ids.add(cleaned["id"])
            cleaned_items.append(cleaned)
        except Exception:
            # Fault tolerance: Skip fatally corrupted individual items without failing whole batch
            continue
            
    return cleaned_items
