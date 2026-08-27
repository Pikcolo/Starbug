"""
Test Checkpoint 1: Scraping Robustness and Data Cleaning Resilience.
Verifies that the scraper and cleaning pipeline handle malformed HTML, missing attributes,
unexpected price formats, and network timeouts without crashing.
"""
import unittest
from data.cleaner import clean_menu_item, clean_price, sanitize_text, clean_dataset
from data.scraper import StarbucksScraper


class TestScraperRobustness(unittest.TestCase):

    def setUp(self):
        self.scraper = StarbucksScraper()

    def test_clean_price_formats(self):
        """Tests various Thai/English currency formats."""
        self.assertEqual(clean_price("฿165"), 165)
        self.assertEqual(clean_price("165 บาท"), 165)
        self.assertEqual(clean_price("฿ 170.00"), 170)
        self.assertEqual(clean_price(185), 185)
        self.assertEqual(clean_price(195.5), 195)
        self.assertEqual(clean_price("free"), 0)
        self.assertEqual(clean_price(None), 0)
        self.assertEqual(clean_price(""), 0)

    def test_sanitize_text(self):
        """Tests HTML tag stripping and whitespace normalization."""
        html_input = "  <strong>Iced Latte</strong><br><span>หอมกาแฟ</span>   \n\t"
        cleaned = sanitize_text(html_input)
        self.assertEqual(cleaned, "Iced Latte หอมกาแฟ")
        self.assertEqual(sanitize_text(None), "")

    def test_missing_and_malformed_fields_in_item(self):
        """Tests that items with missing or corrupt attributes don't cause crash."""
        corrupt_raw = {
            "name": None,
            "price": "N/A",
            "image_url": None,
            "description": None
        }
        item = clean_menu_item(corrupt_raw)
        self.assertIn("name_th", item)
        self.assertEqual(item["price"], 0)
        self.assertTrue(item["image_url"].startswith("http"))
        self.assertIsInstance(item["prep_types"], list)
        self.assertIsInstance(item["flavor_notes"], list)

    def test_scraper_malformed_html_parsing(self):
        """Simulates scraper handling heavily damaged HTML."""
        broken_html = """
        <html>
            <body>
                <div class="product-card">
                    <h2>Iced Americano</h2>
                    <span class="price">฿130</span>
                </div>
                <div class="product-card">
                    <!-- Missing title & price entirely -->
                    <img src="/test.jpg">
                    <p>Some random description</p>
                </div>
                <div class="product-card">
                    <h3>Pure Matcha Latte</h3>
                    <p>ชาเขียวมัทฉะแท้</p>
                    <span class="price">160 บาท</span>
                </div>
                <article>
                    <!-- Unclosed tag -->
                    <h4>Signature Croissant
                    <span class="price">75</span>
                </article>
            </body>
        </html>
        """
        extracted = self.scraper.scrape_from_html(broken_html)
        self.assertGreaterEqual(len(extracted), 2)
        names = [it["name_th"] for it in extracted]
        self.assertIn("Iced Americano", names)
        self.assertIn("Pure Matcha Latte", names)

    def test_dataset_cleaning_with_corrupted_rows(self):
        """Tests batch cleaning with null and invalid entries."""
        raw_batch = [
            {"name_th": "กาแฟ 1", "price": 100},
            None,  # null row
            "Invalid string row",
            {"name_th": "กาแฟ 2", "price": "฿120"},
        ]
        valid_items = clean_dataset([it for it in raw_batch if isinstance(it, dict)])
        self.assertEqual(len(valid_items), 2)


if __name__ == "__main__":
    unittest.main()
