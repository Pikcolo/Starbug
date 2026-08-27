"""
Fair Top-5 Recommendation and Randomization Algorithm with Anti-Repetition Buffer.
"""
import random
from typing import List, Dict, Any, Optional
from collections import defaultdict


class FairRandomizer:
    """
    Manages session-based recommendation history to guarantee diverse,
    non-repetitive Top-5 selections across consecutive user interactions.
    """

    def __init__(self, history_window_size: int = 10):
        self.history_window_size = history_window_size
        # Map user_id / session_id -> list of recently shown item IDs
        self.user_history: Dict[str, List[str]] = defaultdict(list)

    def record_history(self, session_id: str, item_ids: List[str]):
        """Records recently shown item IDs to the user's sliding history window."""
        history = self.user_history[session_id]
        for i_id in item_ids:
            if i_id not in history:
                history.append(i_id)
        # Trim history if exceeding window size
        if len(history) > self.history_window_size:
            self.user_history[session_id] = history[-self.history_window_size:]

    def clear_history(self, session_id: str):
        """Clears recommendation history for a session."""
        if session_id in self.user_history:
            del self.user_history[session_id]

    def select_top_5(
        self,
        candidate_items: List[Dict[str, Any]],
        session_id: str = "default_user",
        limit: int = 5,
        is_random_intent: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Picks up to `limit` (default 5) items from candidates with fair randomization
        and anti-repetition weighting.
        """
        if not candidate_items:
            return []

        if len(candidate_items) <= limit:
            # If total candidates are <= 5, return all candidates (shuffled if random intent)
            result = list(candidate_items)
            if is_random_intent:
                random.shuffle(result)
            self.record_history(session_id, [it["id"] for it in result])
            return result

        recent_ids = set(self.user_history[session_id])

        # Partition candidates into:
        # 1. Unseen items (not shown in recent queries)
        # 2. Recently seen items
        unseen_items = [it for it in candidate_items if it["id"] not in recent_ids]
        seen_items = [it for it in candidate_items if it["id"] in recent_ids]

        # Shuffle both candidate pools
        random.shuffle(unseen_items)
        random.shuffle(seen_items)

        selected = []
        # Priority 1: Fill from unseen items
        if len(unseen_items) >= limit:
            selected = unseen_items[:limit]
        else:
            selected = list(unseen_items)
            needed = limit - len(selected)
            selected.extend(seen_items[:needed])

        # Record selected items to session history
        self.record_history(session_id, [it["id"] for it in selected])

        return selected


# Singleton instance
global_randomizer = FairRandomizer()


def get_top_5_recommendations(
    candidate_items: List[Dict[str, Any]],
    session_id: str = "default_user",
    is_random_intent: bool = False
) -> List[Dict[str, Any]]:
    """Helper entry point for Top 5 recommendation."""
    return global_randomizer.select_top_5(candidate_items, session_id, limit=5, is_random_intent=is_random_intent)
