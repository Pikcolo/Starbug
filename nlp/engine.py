"""
Core NLP Processing Engine for Starbucks AI Assistant.
Combines rule-based matching, RapidFuzz fuzzy search, and entity extraction.
"""
import time
from typing import Dict, Any, Optional, Tuple, List
from rapidfuzz import fuzz, process

from nlp.normalizer import normalize_text
from nlp.intents import IntentType, INTENT_PATTERNS
from nlp.entity_extractor import extract_entities
from nlp.bert_classifier import BERTSemanticClassifier
from data.scraper import get_menu_data


class NLPEngine:
    """High-performance NLP classifier combining Rule-based, Fuzzy, and BERT Semantic Embeddings."""

    def __init__(self):
        self.bert = BERTSemanticClassifier()
        self._load_item_index()

    def _load_item_index(self):
        """Indexes item names for fast fuzzy matching."""
        menu = get_menu_data()
        self.item_lookup = {}
        self.search_corpus = []

        for item in menu:
            name_th = normalize_text(item.get("name_th", ""))
            name_en = normalize_text(item.get("name_en", ""))
            
            if name_th:
                self.search_corpus.append(name_th)
                self.item_lookup[name_th] = item
            if name_en:
                self.search_corpus.append(name_en)
                self.item_lookup[name_en] = item

    def classify_intent(self, text: str, entities: Dict[str, Any]) -> Tuple[IntentType, float]:
        """
        Determines the intent and confidence score (0.0 to 1.0) of the user query.
        """
        norm = normalize_text(text)

        # 1. Greetings
        if any(kw == norm or norm.startswith(kw) for kw in INTENT_PATTERNS[IntentType.GREETING]):
            return IntentType.GREETING, 0.98

        # 2. Help & Commands ("คำสั่ง", "วิธีใช้", "ช่วยด้วย")
        if any(kw in norm for kw in INTENT_PATTERNS[IntentType.HELP]):
            return IntentType.HELP, 0.95

        # 3. Order / Purchase Action
        if ("คำสั่ง" not in norm) and (any(norm.startswith(kw) for kw in ["สั่งซื้อ", "สั่งเมนู", "สั่งเครื่องดื่ม", "สั่งแก้วนี้", "สั่ง", "order", "ซื้อ"]) or any(kw in norm for kw in INTENT_PATTERNS[IntentType.ORDER])):
            return IntentType.ORDER, 0.98

        # 4. Sassy Barista Roast (แซว/บ่น/ทายนิสัย)
        if any(kw in norm for kw in INTENT_PATTERNS[IntentType.BARISTA_ROAST]):
            return IntentType.BARISTA_ROAST, 0.95

        # 7. Promotions & Discounts
        if any(kw in norm for kw in INTENT_PATTERNS[IntentType.PROMOTIONS]):
            return IntentType.PROMOTIONS, 0.95

        # 5. New Arrivals & Seasonal
        if any(kw in norm for kw in INTENT_PATTERNS[IntentType.NEW_ARRIVALS]):
            return IntentType.NEW_ARRIVALS, 0.95

        # 6. Random recommendation request
        if any(kw in norm for kw in INTENT_PATTERNS[IntentType.RANDOM_RECOMMEND]):
            return IntentType.RANDOM_RECOMMEND, 0.92

        # 7. Explicit Price constraint
        if entities.get("max_price") is not None or entities.get("min_price") is not None:
            return IntentType.PRICE_FILTER, 0.90

        # 8. Explicit Item Detail / Size selection query (e.g. "ขอดูรายละเอียด คาราเมล แฟรปปูชิโน่", "เลือกขนาด คาเฟ่ ลาเต้")
        if any(kw in norm for kw in ["ขอดูรายละเอียด", "รายละเอียด", "เลือกขนาด", "ดูรายละเอียด", "กี่แคล"]):
            return IntentType.ITEM_DETAIL, 0.98

        # 9. Direct Product Name Fuzzy Match (e.g. "Signature Chocolate Cake", "Iced Caffe Americano", "Green Tea Frappe", "จาวา ชิพ")
        generic_category_queries = {"กาแฟ", "กาแฟเย็น", "กาแฟร้อน", "ขอดูกาแฟ", "เมนูกาแฟ", "ชาเขียว", "ขอดูชาเขียว", "เมนูปั่น", "ขอดูเมนูปั่น", "ปั่น", "เค้ก", "ขนม", "เบเกอรี่", "อาหาร", "มีขนมอะไรบ้าง", "ขอดูขนม"}
        if self.search_corpus and norm not in generic_category_queries:
            best_set = process.extractOne(norm, self.search_corpus, scorer=fuzz.token_set_ratio)
            best_part = process.extractOne(norm, self.search_corpus, scorer=fuzz.partial_ratio)
            chosen_match = best_set if (best_set and best_part and best_set[1] >= best_part[1]) else (best_part or best_set)

            if chosen_match and chosen_match[1] >= 70:
                if len(norm) >= 4 or chosen_match[1] >= 85:
                    return IntentType.ITEM_DETAIL, round(chosen_match[1] / 100.0, 2)

        # 10. Food / Bakery broad query
        if entities.get("is_food_query") or any(kw in norm for kw in INTENT_PATTERNS[IntentType.SEARCH_FOOD]):
            return IntentType.SEARCH_FOOD, 0.90

        if norm in generic_category_queries:
            return IntentType.SEARCH_CATEGORY, 0.90

        # 11. Flavor / Mood
        if entities.get("flavor_moods"):
            return IntentType.SEARCH_FLAVOR_MOOD, 0.90

        # 12. Category / Prep
        if entities.get("categories") or entities.get("prep_types"):
            return IntentType.SEARCH_CATEGORY, 0.88

        # 13. BERT Semantic Embedding Prediction (handles complex phrasing & colloquialisms)
        bert_intent, bert_score = self.bert.predict(text)
        # Safety guard: BARISTA_ROAST requires explicit roast keywords
        if bert_intent == IntentType.BARISTA_ROAST:
            if not any(kw in norm for kw in ["แซว", "ปากแซ่บ", "ด่า", "กวน", "บ่น", "roast", "มุก", "วิจารณ์"]):
                bert_intent = IntentType.UNKNOWN
        if bert_intent != IntentType.UNKNOWN and bert_score >= 0.45:
            return bert_intent, bert_score

        # Fallback to general recommendation
        return IntentType.UNKNOWN, 0.50

    def parse(self, query: str) -> Dict[str, Any]:
        """
        Full NLP parsing pipeline.
        Returns intent, entities, matched items, confidence, and execution latency in ms.
        """
        start_time = time.perf_counter()
        self._load_item_index()

        cleaned_query = normalize_text(query)
        entities = extract_entities(cleaned_query)
        intent, confidence = self.classify_intent(cleaned_query, entities)

        # Find direct matched item if applicable
        matched_item = None
        if self.search_corpus and (intent in (IntentType.ITEM_DETAIL, IntentType.ORDER) or len(cleaned_query) >= 3):
            # Strip ordering & detail keywords to find cleaner product name
            target_text = cleaned_query
            for prefix in ["ขอดูรายละเอียด", "ดูรายละเอียด", "รายละเอียด", "เลือกขนาด", "สั่งซื้อ", "สั่งเมนู", "สั่งเครื่องดื่ม", "สั่งแก้วนี้", "สั่ง", "order", "ซื้อ", "กี่แคล"]:
                target_text = target_text.replace(prefix, "")
            target_text = target_text.replace("1 แก้ว", "").replace("1 ชิ้น", "").replace("ครับ", "").replace("ค่ะ", "").strip()
            
            search_target = target_text if len(target_text) >= 2 else cleaned_query

            # Priority 1: Exact / Substring match sorted by length descending (longest match wins)
            for cand_name in sorted(self.item_lookup.keys(), key=len, reverse=True):
                if len(cand_name) >= 3 and (cand_name in search_target or cand_name in cleaned_query):
                    matched_item = self.item_lookup[cand_name]
                    break

            # Priority 2: Fuzzy matching (token_set_ratio & partial_ratio)
            if not matched_item:
                best_set = process.extractOne(search_target, self.search_corpus, scorer=fuzz.token_set_ratio)
                best_part = process.extractOne(search_target, self.search_corpus, scorer=fuzz.partial_ratio)
                best = best_set if (best_set and best_part and best_set[1] >= best_part[1]) else (best_part or best_set)
                if best and best[1] >= 65:
                    matched_item = self.item_lookup.get(best[0])
                elif not matched_item and intent == IntentType.ORDER:
                    # Fallback to general search on the whole cleaned query
                    best_fallback = process.extractOne(cleaned_query, self.search_corpus, scorer=fuzz.token_set_ratio)
                    if best_fallback and best_fallback[1] >= 50:
                        matched_item = self.item_lookup.get(best_fallback[0])

        latency_ms = (time.perf_counter() - start_time) * 1000.0

        return {
            "query": query,
            "normalized_query": cleaned_query,
            "intent": intent.value,
            "confidence": confidence,
            "entities": entities,
            "matched_item": matched_item,
            "latency_ms": round(latency_ms, 2)
        }


# Singleton engine instance
nlp_engine = NLPEngine()


def parse_user_query(query: str) -> Dict[str, Any]:
    """Helper entry point for parsing user query."""
    return nlp_engine.parse(query)
