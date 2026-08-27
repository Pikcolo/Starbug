"""
Multi-criteria product filtering engine.
"""
from typing import List, Dict, Any
from data.scraper import get_menu_data
from nlp.intents import IntentType


def filter_menu(nlp_result: Dict[str, Any], catalog: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Filters the Starbucks catalog against intent and extracted entities.
    """
    if catalog is None:
        catalog = get_menu_data()

    intent = nlp_result.get("intent")
    entities = nlp_result.get("entities", {})
    matched_item = nlp_result.get("matched_item")

    # 1. Direct Item Detail match
    if intent == IntentType.ITEM_DETAIL.value and matched_item:
        return [matched_item]

    filtered = list(catalog)

    # 2. Intent-specific filtering
    if intent == IntentType.NEW_ARRIVALS.value:
        filtered = [item for item in filtered if item.get("is_new")]
        if not filtered:
            # Fallback to latest beverages
            filtered = list(catalog)[:5]
        return filtered

    if intent == IntentType.PROMOTIONS.value:
        promo_items = [item for item in filtered if item.get("is_promo")]
        if promo_items:
            filtered = promo_items

    if intent == IntentType.SEARCH_FOOD.value:
        filtered = [item for item in filtered if item.get("is_food")]

    # 3. Entity Filters
    # Price filtering
    max_p = entities.get("max_price")
    min_p = entities.get("min_price")
    if max_p is not None:
        filtered = [item for item in filtered if item.get("price", 0) <= max_p]
    if min_p is not None:
        filtered = [item for item in filtered if item.get("price", 0) >= min_p]

    # Category filtering
    categories = entities.get("categories", [])
    if categories:
        cat_filtered = []
        for item in filtered:
            item_cat = item.get("category", "").lower()
            item_sub = item.get("subcategory", "").lower()
            if any(c in item_cat or c in item_sub for c in categories):
                cat_filtered.append(item)
            elif "bakery" in categories and item.get("is_food"):
                cat_filtered.append(item)
        if cat_filtered:
            filtered = cat_filtered

    # Prep type filtering (hot / iced / frappuccino)
    preps = entities.get("prep_types", [])
    if preps:
        prep_filtered = []
        for item in filtered:
            item_preps = item.get("prep_types", [])
            if any(p in item_preps for p in preps):
                prep_filtered.append(item)
        if prep_filtered:
            filtered = prep_filtered

    # Flavor / Mood filtering
    flavors = entities.get("flavor_moods", [])
    if flavors:
        flavor_filtered = []
        for item in filtered:
            item_flavors = item.get("flavor_notes", [])
            if any(f in item_flavors for f in flavors):
                flavor_filtered.append(item)
        if flavor_filtered:
            filtered = flavor_filtered

    # If filtered list is empty, fallback to catalog gracefully
    if not filtered:
        filtered = catalog

    return filtered
