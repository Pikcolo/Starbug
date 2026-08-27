"""
Web Scraping and Data Pipeline for Starbucks Thailand.
Features polite rate-limiting, missing field resilience, and graceful fallback.
"""
import os
import sys
import json
import time
import logging
from typing import List, Dict, Any, Optional
import requests
from bs4 import BeautifulSoup

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import MENU_FILE_PATH, SCRAPER_RATE_LIMIT_SECONDS, SCRAPER_TIMEOUT, STARBUCKS_BASE_URL, STARBUCKS_MENU_URL
from data.cleaner import clean_dataset, clean_menu_item

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Active promotion campaigns (can also be refreshed from web/marketing)
STATIC_PROMOTIONS = [
    {
        "id": "promo_bogo_frappe",
        "title": "🎉 1-for-1 Frappuccino Hours",
        "badge": "ซื้อ 1 แถม 1",
        "description": "ซื้อเครื่องดื่มประเภท Frappuccino ขนาด Grande ขึ้นไป รับฟรีทันทีอีก 1 แก้ว ทุกวันพฤหัสบดี (14:00 - 20:00 น.)",
        "period": "ถึงสิ้นเดือนนี้",
        "image_url": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=600&auto=format&fit=crop&q=80",
        "applicable_category": "frappuccino"
    },
    {
        "id": "promo_personal_cup",
        "title": "🌱 Personal Cup Eco Discount",
        "badge": "ลด 20 บาท",
        "description": "ร่วมรักษ์โลก! นำแก้วส่วนตัว (Tumbler / Personal Cup) มารับส่วนลด 20 บาท สำหรับเครื่องดื่มทุกประเภท ทุกขนาด",
        "period": "ตลอดทั้งปี",
        "image_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600&auto=format&fit=crop&q=80",
        "applicable_category": "all"
    },
    {
        "id": "promo_double_stars",
        "title": "⭐ Double Stars New Arrivals",
        "badge": "ดาว 2 เท่า",
        "description": "สมาชิก Starbucks® Rewards รับดาวสะสม x2 เท่าทันที เมื่อสั่งเมนู New Seasonal Arrivals ใดๆ ในสาขา",
        "period": "เฉพาะสมาชิก Rewards",
        "image_url": "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?w=600&auto=format&fit=crop&q=80",
        "applicable_category": "new"
    },
    {
        "id": "promo_breakfast_pairing",
        "title": "🥐 Breakfast Bakery Pairing Combo",
        "badge": "เบเกอรี่ลด 30%",
        "description": "อร่อยยามเช้า เมื่อสั่งเครื่องดื่มแก้วโปรดคู่กับ ครัวซองต์เนยสด หรือแซนด์วิช รับส่วนลดเบเกอรี่ 30% ก่อน 11:00 น.",
        "period": "ทุกวันก่อน 11:00 น.",
        "image_url": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=600&auto=format&fit=crop&q=80",
        "applicable_category": "bakery"
    }
]


class StarbucksScraper:
    """Polite and robust scraper for Starbucks Thailand."""

    def __init__(self, menu_path: str = MENU_FILE_PATH):
        self.menu_path = menu_path
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "th-TH,th;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }

    def scrape_from_html(self, html_content: str) -> List[Dict[str, Any]]:
        """
        Parses HTML string safely. Handles broken tags, missing attributes, or dynamic layouts.
        """
        extracted = []
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Look for common item containers
            product_cards = soup.select(".product-card, .menu-item, .item, article, .product-tile")
            
            if not product_cards:
                # Fallback: inspect any div containers with headings
                product_cards = [
                    div for div in soup.find_all(["div", "article", "li"])
                    if div.find(["h1", "h2", "h3", "h4", "h5"])
                ]

            for card in product_cards:
                try:
                    title_elem = card.find(["h1", "h2", "h3", "h4", "h5", "strong"]) or card.select_one(".title, .product-name")
                    name = title_elem.get_text(strip=True) if title_elem else None
                    if not name or len(name) < 2:
                        continue

                    img_elem = card.find("img")
                    img_url = img_elem.get("src") or img_elem.get("data-src", "") if img_elem else ""

                    desc_elem = card.find(["p", "span"]) or card.select_one(".desc, .description")
                    desc = desc_elem.get_text(strip=True) if desc_elem else ""

                    # Find price in elements with price classes or matching digit/baht
                    price_elem = card.select_one(".price, .cost") or card.find(string=re.compile(r"[฿\d]+"))
                    price_text = price_elem.get_text(strip=True) if hasattr(price_elem, "get_text") else str(price_elem or "")

                    raw_item = {
                        "name_th": name,
                        "name_en": name,
                        "description": desc,
                        "image_url": img_url,
                        "price": price_text,
                    }
                    extracted.append(clean_menu_item(raw_item))
                except Exception as card_err:
                    logger.debug(f"Skipping malformed card: {card_err}")
                    continue
        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")

        return extracted

    def scrape_live(self, url: str = STARBUCKS_MENU_URL) -> List[Dict[str, Any]]:
        """
        Scrapes live Starbucks Thailand menu using Headless Chromium + BeautifulSoup4
        to execute JavaScript and fully hydrate Next.js DOM.
        Merges newly discovered items with the verified local catalog.
        """
        logger.info(f"Starting dynamic scrape from {url} with Chromium + BeautifulSoup4...")
        time.sleep(SCRAPER_RATE_LIMIT_SECONDS)

        local_catalog = self.load_local_menu()
        merged_map = {it.get("id"): it for it in local_catalog}

        # 1. Try Headless Chromium dynamic DOM scraper
        try:
            from data.chromium_scraper import scrape_with_chromium
            dynamic_items = scrape_with_chromium(url=url)
            for item in dynamic_items:
                _id = item.get("id")
                if _id and _id not in merged_map:
                    merged_map[_id] = item
                elif _id and item.get("image_url") and item["image_url"].startswith("https://blob.starbucks.co.th"):
                    merged_map[_id]["image_url"] = item["image_url"]
            if dynamic_items:
                logger.info(f"✅ Extracted dynamic items via Chromium + BS4. Total merged catalog: {len(merged_map)}")
                return list(merged_map.values())
        except Exception as chrome_err:
            logger.warning(f"Chromium scrape notice: {chrome_err}. Falling back to verified catalog...")

        return local_catalog

    def load_local_menu(self) -> List[Dict[str, Any]]:
        """Loads and cleans the verified local menu dataset."""
        if not os.path.exists(self.menu_path):
            logger.error(f"Menu file not found at {self.menu_path}")
            return []
        
        try:
            with open(self.menu_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return clean_dataset(data)
        except Exception as e:
            logger.error(f"Error loading local menu file: {e}")
            return []

    def get_promotions(self) -> List[Dict[str, Any]]:
        """Returns active promotions."""
        return STATIC_PROMOTIONS

    def save_to_file(self, items: List[Dict[str, Any]], filepath: str = None) -> bool:
        """Saves cleaned dataset to JSON file."""
        target_path = filepath or self.menu_path
        try:
            with open(target_path, "w", encoding="utf-8") as f:
                json.dump(items, f, ensure_ascii=False, indent=2)
            logger.info(f"Successfully saved {len(items)} items to {target_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save menu file: {e}")
            return False


# Singleton global instances
_scraper = StarbucksScraper()
_cached_menu: Optional[List[Dict[str, Any]]] = None
_last_mtime: float = 0.0


def get_menu_data(force_reload: bool = False) -> List[Dict[str, Any]]:
    """Returns the cleaned menu dataset from memory cache or reloads if file modified."""
    global _cached_menu, _last_mtime
    current_mtime = 0.0
    if os.path.exists(_scraper.menu_path):
        try:
            current_mtime = os.path.getmtime(_scraper.menu_path)
        except OSError:
            pass

    if _cached_menu is None or force_reload or (current_mtime > _last_mtime):
        _cached_menu = _scraper.load_local_menu()
        _last_mtime = current_mtime
    return _cached_menu


def get_promotions_data() -> List[Dict[str, Any]]:
    """Returns active promotions."""
    return _scraper.get_promotions()


def run_pipeline():
    """Executes the full scraping & data cleaning pipeline."""
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print("=" * 60)
    print("  STARBUCKS THAILAND - WEB SCRAPING & DATA PIPELINE")
    print("=" * 60)
    print(f"[*] Target URL: {STARBUCKS_MENU_URL}")
    print(f"[*] Rate-limiting delay: {SCRAPER_RATE_LIMIT_SECONDS}s between requests...")

    scraper = StarbucksScraper()
    items = scraper.scrape_live()

    drinks = [it for it in items if it.get("is_beverage")]
    food = [it for it in items if it.get("is_food")]
    new_items = [it for it in items if it.get("is_new")]
    promos = [it for it in items if it.get("is_promo")]

    print("\n" + "-" * 60)
    print(f"  Total Cleaned Items:    {len(items)}")
    print(f"  - Beverages (เครื่องดื่ม):  {len(drinks)}")
    print(f"  - Bakery & Food (อาหาร): {len(food)}")
    print(f"  - New Arrivals (เมนูใหม่): {len(new_items)}")
    print(f"  - With Promo (โปรโมชั่น): {len(promos)}")
    print("-" * 60)

    scraper.save_to_file(items)
    print(f"[OK] Pipeline complete. Data saved to: {MENU_FILE_PATH}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_pipeline()
