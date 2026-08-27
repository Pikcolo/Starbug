import unittest
import time
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from nlp.engine import NLPEngine
from nlp.intents import IntentType


TEST_SUITE = [
    # 1. Greetings & Help
    {"query": "สวัสดีครับ", "expected_intent": IntentType.GREETING.value},
    {"query": "หวัดดีจ้า", "expected_intent": IntentType.GREETING.value},
    {"query": "ช่วยด้วย ใช้ยังไง", "expected_intent": IntentType.HELP.value},
    {"query": "มีคำสั่งอะไรบ้าง", "expected_intent": IntentType.HELP.value},

    # 2. Promotions & Discounts
    {"query": "มีโปรโมชั่นอะไรบ้าง", "expected_intent": IntentType.PROMOTIONS.value},
    {"query": "วันนี้มี 1 แถม 1 ไหม", "expected_intent": IntentType.PROMOTIONS.value},
    {"query": "ส่วนลดสตาบัค", "expected_intent": IntentType.PROMOTIONS.value},
    {"query": "โปโมชั่นมีไรบ้าง", "expected_intent": IntentType.PROMOTIONS.value},  # Typo test

    # 3. New Arrivals & Seasonal
    {"query": "เมนูใหม่ล่าสุดมีอะไรบ้าง", "expected_intent": IntentType.NEW_ARRIVALS.value},
    {"query": "มีอะไรมาใหม่", "expected_intent": IntentType.NEW_ARRIVALS.value},
    {"query": "ขอดูเมนูซีซั่นนี้", "expected_intent": IntentType.NEW_ARRIVALS.value},

    # 4. Random Recommendation
    {"query": "กินอะไรดี", "expected_intent": IntentType.RANDOM_RECOMMEND.value},
    {"query": "สุ่มเมนูให้หน่อย ไม่อยากคิด", "expected_intent": IntentType.RANDOM_RECOMMEND.value},
    {"query": "ดื่มอะไรดี แนะนำหน่อย", "expected_intent": IntentType.RANDOM_RECOMMEND.value},

    # 5. Price filtering & Budget
    {"query": "งบไม่เกิน 150 บาท", "expected_intent": IntentType.PRICE_FILTER.value, "max_price": 150},
    {"query": "ราคาต่ำกว่า 170", "expected_intent": IntentType.PRICE_FILTER.value, "max_price": 170},
    {"query": "มีเมนูไม่เกิน 140 ไหม", "expected_intent": IntentType.PRICE_FILTER.value, "max_price": 140},

    # 6. Categories & Typo tolerance
    {"query": "ขอดูเมนูกาแฟ", "expected_intent": IntentType.SEARCH_CATEGORY.value, "category": "espresso"},
    {"query": "กาเเฟเยน", "expected_intent": IntentType.SEARCH_CATEGORY.value, "category": "espresso", "prep": "iced"},  # Typo
    {"query": "ชาเขีบว", "expected_intent": IntentType.SEARCH_CATEGORY.value, "category": "tea"},  # Typo
    {"query": "มัทฉะลาเต้เย็น", "expected_intent": IntentType.ITEM_DETAIL.value},
    {"query": "ขอดูเมนูปั่น", "expected_intent": IntentType.SEARCH_CATEGORY.value, "prep": "frappuccino"},

    # 7. Food & Bakery
    {"query": "มีขนมและเบเกอรี่อะไรบ้าง", "expected_intent": IntentType.SEARCH_FOOD.value},
    {"query": "หิวข้าว อยากกินครัวซองต์", "expected_intent": IntentType.SEARCH_FOOD.value},
    {"query": "ขอดูเค้กสตาร์บัคส์", "expected_intent": IntentType.SEARCH_FOOD.value},

    # 8. Complex multi-criteria
    {"query": "อยากกินกาแฟปั่นราคาไม่เกิน 170 บาท", "expected_intent": IntentType.PRICE_FILTER.value, "max_price": 170, "prep": "frappuccino"},
    {"query": "อยากได้เครื่องดื่มหวานๆ สดชื่น", "expected_intent": IntentType.SEARCH_FLAVOR_MOOD.value},
    {"query": "ขอกาแฟเข้มๆ ตื่นๆ", "expected_intent": IntentType.SEARCH_FLAVOR_MOOD.value},

    # 9. Specific Product Detail query
    {"query": "Iced Caffe Americano กี่แคล", "expected_intent": IntentType.ITEM_DETAIL.value},
    {"query": "จาวา ชิพ แฟรปปูชิโน่", "expected_intent": IntentType.ITEM_DETAIL.value},
    {"query": "Green Tea Cream Frappuccino", "expected_intent": IntentType.ITEM_DETAIL.value},

    # 10. Order / Purchase Action
    {"query": "สั่งซื้อ Green Tea Cream Frappuccino 1 แก้วครับ", "expected_intent": IntentType.ORDER.value},
    {"query": "สั่งเมนู Iced Caffe Americano", "expected_intent": IntentType.ORDER.value},
    {"query": "สั่งเครื่องดื่มนี้ทันที", "expected_intent": IntentType.ORDER.value},

    # 11. Funny & Interactive Features
    {"query": "แซวฉันหน่อย บาริสต้าปากแซ่บ", "expected_intent": IntentType.BARISTA_ROAST.value}
]


class TestNLPBenchmark(unittest.TestCase):

    def setUp(self):
        self.engine = NLPEngine()

    def test_nlp_accuracy_and_latency(self):
        """Runs all test utterances and asserts accuracy > 85% and latency < 1500ms."""
        total_queries = len(TEST_SUITE)
        correct_intents = 0
        latencies_ms = []

        print("\n" + "=" * 65)
        print("  STARBUCKS NLP ENGINE BENCHMARK & ACCURACY REPORT")
        print("=" * 65)

        for tc in TEST_SUITE:
            q = tc["query"]
            expected = tc["expected_intent"]

            parsed = self.engine.parse(q)
            lat = parsed["latency_ms"]
            latencies_ms.append(lat)

            # Check intent match
            is_match = (parsed["intent"] == expected)
            if is_match:
                correct_intents += 1

            status_icon = "[PASS]" if is_match else "[FAIL]"
            print(f"{status_icon} Query: '{q}' -> Intent: {parsed['intent']} (Expected: {expected}) | {lat:.2f}ms")

            # Verify latency under strict 1500ms limit
            self.assertLess(lat, 1500, f"Query '{q}' exceeded latency threshold ({lat}ms)")

            # Check entity constraints if specified
            if "max_price" in tc:
                self.assertEqual(parsed["entities"]["max_price"], tc["max_price"])
            if "prep" in tc:
                self.assertIn(tc["prep"], parsed["entities"]["prep_types"])

        accuracy_pct = (correct_intents / total_queries) * 100.0
        avg_latency = sum(latencies_ms) / len(latencies_ms)
        max_latency = max(latencies_ms)

        print("-" * 65)
        print(f"Total Test Cases:      {total_queries}")
        print(f"Accuracy Rate:         {accuracy_pct:.2f}% (Target: > 85.0%)")
        print(f"Average Latency:       {avg_latency:.2f} ms (Target: < 1500 ms)")
        print(f"Max Peak Latency:      {max_latency:.2f} ms")
        print("=" * 65 + "\n")

        self.assertGreaterEqual(accuracy_pct, 85.0, "NLP accuracy fell below the 85% requirement")


if __name__ == "__main__":
    unittest.main()
