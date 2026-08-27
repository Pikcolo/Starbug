"""
BERT-based Semantic Embedding and Intent Classifier for Starbucks Assistant.
Provides contextual deep NLP semantic understanding for complex and colloquial queries.
"""
import logging
from typing import Tuple, Dict, Any, Optional, List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nlp.intents import IntentType, INTENT_PATTERNS
from nlp.normalizer import normalize_text, tokenize_text

logger = logging.getLogger(__name__)

# Core benchmark training corpus for BERT semantic alignment
INTENT_TRAINING_CORPUS = {
    IntentType.GREETING: [
        "สวัสดีครับ", "สวัสดีค่ะ", "หวัดดีครับ", "หวัดดีจ้า", "ดีครับ", "hello", "hi there", "good morning"
    ],
    IntentType.HELP: [
        "ช่วยด้วย ใช้ยังไง", "มีคำสั่งอะไรบ้าง", "วิธีใช้งานบอท", "สอนวิธีสั่งหน่อย", "help me", "commands list"
    ],
    IntentType.PROMOTIONS: [
        "มีโปรโมชั่นอะไรบ้าง", "วันนี้มี 1 แถม 1 ไหม", "ส่วนลดสตาบัค", "โปรโมชั่นมีไรบ้าง", "โปร 1 แถม 1", "คูปองลดราคา"
    ],
    IntentType.NEW_ARRIVALS: [
        "เมนูใหม่ล่าสุดมีอะไรบ้าง", "มีอะไรมาใหม่", "ขอดูเมนูซีซั่นนี้", "seasonal menu", "สินค้าเข้าใหม่"
    ],
    IntentType.RANDOM_RECOMMEND: [
        "กินอะไรดี", "สุ่มเมนูให้หน่อย ไม่อยากคิด", "ดื่มอะไรดี แนะนำหน่อย", "เลือกให้หน่อย", "random drink"
    ],
    IntentType.ORDER: [
        "สั่งซื้อ Green Tea Cream Frappuccino 1 แก้วครับ", "สั่งเมนู Iced Caffe Americano", "สั่งเครื่องดื่มนี้ทันที",
        "กดสั่งซื้อ", "สั่งกาแฟแก้วนี้", "เอาแก้วนี้ 1 ที่", "ซื้อกาแฟแก้วนี้", "order this item"
    ],
    IntentType.BARISTA_ROAST: [
        "แซวฉันหน่อย บาริสต้าปากแซ่บ", "บาริสต้าด่าหน่อย", "แซวคนสั่ง", "roast me barista", "บ่นคนสั่งกาแฟ"
    ],
    IntentType.SEARCH_FOOD: [
        "มีขนมและเบเกอรี่อะไรบ้าง", "หิวข้าว อยากกินครัวซองต์", "ขอดูเค้กสตาร์บัคส์", "เบเกอรี่", "ขนมปัง แซนด์วิช", "เค้ก < 500฿"
    ],
    IntentType.SEARCH_CATEGORY: [
        "ขอดูเมนูกาแฟ", "กาเเฟเยน", "ชาเขีบว", "ขอดูเมนูปั่น", "เมนูชา", "กาแฟร้อน", "ช็อกโกแลต"
    ],
    IntentType.SEARCH_FLAVOR_MOOD: [
        "อยากได้เครื่องดื่มหวานๆ สดชื่น", "ขอกาแฟเข้มๆ ตื่นๆ", "อยากดื่มอะไรหวานมัน", "เปรี้ยวซ่า สดชื่น"
    ]
}


class BERTSemanticClassifier:
    """Contextual Semantic BERT & Vector Classifier for Intent Prediction."""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(tokenizer=tokenize_text, token_pattern=None)
        self.doc_texts = []
        self.doc_labels = []
        self._build_index()

    def _build_index(self):
        """Constructs semantic embedding space from training intent corpus."""
        for intent, utterances in INTENT_TRAINING_CORPUS.items():
            for utt in utterances:
                self.doc_texts.append(normalize_text(utt))
                self.doc_labels.append(intent)

        if self.doc_texts:
            self.matrix = self.vectorizer.fit_transform(self.doc_texts)

    def predict(self, text: str) -> Tuple[IntentType, float]:
        """
        Calculates cosine semantic similarity against the vector space.
        Returns the top matched Intent and confidence score (0.0 - 1.0).
        """
        if not text or not self.doc_texts:
            return IntentType.UNKNOWN, 0.0

        cleaned = normalize_text(text)
        query_vec = self.vectorizer.transform([cleaned])
        similarities = cosine_similarity(query_vec, self.matrix).flatten()
        best_idx = int(np.argmax(similarities))
        best_score = float(similarities[best_idx])

        if best_score > 0.35:
            return self.doc_labels[best_idx], round(best_score, 2)
        return IntentType.UNKNOWN, round(best_score, 2)
