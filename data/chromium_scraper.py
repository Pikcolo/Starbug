"""
Chromium-based Dynamic Web Scraper for Starbucks Thailand.
Extracts products from Starbucks Thailand Next.js pages and merges with verified catalog.
"""
import os
import sys
import json
import time
import re
import logging
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import MENU_FILE_PATH, STARBUCKS_MENU_URL
from data.cleaner import clean_dataset, clean_menu_item

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def scrape_with_chromium(url: str = STARBUCKS_MENU_URL, headless: bool = True) -> List[Dict[str, Any]]:
    """
    Launches Headless Chromium to extract dynamic items and blob images.
    """
    logger.info(f"🚀 Launching Headless Chromium to scrape: {url}")
    scraped_items = []

    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800},
                locale="th-TH"
            )
            page = context.new_page()
            
            # Scrape menu page
            page.goto(url, wait_until="domcontentloaded", timeout=25000)
            try:
                page.wait_for_load_state("networkidle", timeout=8000)
            except Exception:
                pass

            # Scroll to trigger lazy loading
            page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
            time.sleep(1)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)

            html_content = page.content()
            browser.close()
            logger.info(f"✅ Extracted rendered HTML ({len(html_content)} bytes). Parsing with BeautifulSoup4...")

            soup = BeautifulSoup(html_content, "html.parser")
            
            # Find all product cards or specific item elements with valid names
            generic_ignore = {"เครื่องดื่ม", "อาหาร", "กาแฟ", "เมนู", "starbucks", "สตาร์บัคส์", "beverage", "food"}
            
            for elem in soup.find_all(["div", "article", "section"]):
                title_elem = elem.find(["h2", "h3", "h4", "strong"])
                if not title_elem:
                    continue
                name = title_elem.get_text(strip=True)
                if not name or len(name) < 3 or name.lower() in generic_ignore:
                    continue

                img_elem = elem.find("img")
                img_url = img_elem.get("src", "") if img_elem else ""
                if not img_url.startswith("http"):
                    continue

                desc_elem = elem.find(["p", "span"])
                desc = desc_elem.get_text(strip=True) if desc_elem else ""
                if "ราคาและสินค้า" in desc and len(desc) < 60:
                    desc = ""

                price_match = re.search(r"(\d{2,3})\s*(?:บาท|฿)", elem.get_text())
                price = int(price_match.group(1)) if price_match else 150

                raw_item = {
                    "name_th": name,
                    "name_en": name,
                    "description": desc,
                    "image_url": img_url,
                    "price": price
                }
                cleaned = clean_menu_item(raw_item)
                if cleaned and cleaned["name_th"] and cleaned["name_th"].lower() not in generic_ignore:
                    scraped_items.append(cleaned)

    except Exception as err:
        logger.warning(f"Chromium scrape notice: {err}")

    return scraped_items
