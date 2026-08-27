import unittest
import sys
from collections import Counter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from recommender.fair_randomizer import FairRandomizer
from data.scraper import get_menu_data


class TestRandomizationFairness(unittest.TestCase):

    def setUp(self):
        self.randomizer = FairRandomizer(history_window_size=10)
        self.catalog = get_menu_data()

    def test_anti_repetition_consecutive_queries(self):
        """
        Tests that two consecutive Top-5 recommendations for the same user
        do not yield the exact identical 5 items if the candidate pool is larger than 5.
        """
        session = "test_user_session_1"
        self.randomizer.clear_history(session)

        first_top_5 = self.randomizer.select_top_5(self.catalog, session_id=session, is_random_intent=True)
        first_ids = {it["id"] for it in first_top_5}

        second_top_5 = self.randomizer.select_top_5(self.catalog, session_id=session, is_random_intent=True)
        second_ids = {it["id"] for it in second_top_5}

        # They must not be 100% identical sets
        overlap = first_ids.intersection(second_ids)
        self.assertLess(
            len(overlap), 5,
            f"Consecutive recommendations yielded 100% identical items (overlap={len(overlap)})"
        )

    def test_distribution_fairness_monte_carlo(self):
        """
        Simulates 200 user recommendation calls across a session.
        Verifies that every item in the catalog is sampled fairly without starvation.
        """
        session = "test_monte_carlo_user"
        self.randomizer.clear_history(session)

        item_counts = Counter()
        iterations = 150

        for _ in range(iterations):
            selected = self.randomizer.select_top_5(self.catalog, session_id=session, is_random_intent=True)
            self.assertEqual(len(selected), min(5, len(self.catalog)))
            for it in selected:
                item_counts[it["id"]] += 1

        total_catalog_items = len(self.catalog)
        sampled_distinct_items = len(item_counts)

        print("\n" + "=" * 60)
        print("  RANDOMIZATION FAIRNESS & DISTRIBUTION AUDIT")
        print("=" * 60)
        print(f"Total Catalog Items:      {total_catalog_items}")
        print(f"Distinct Items Sampled:   {sampled_distinct_items}")
        print(f"Sample Coverage Rate:     {(sampled_distinct_items / total_catalog_items) * 100:.1f}%")
        print(f"Min Item Appearances:     {min(item_counts.values())}")
        print(f"Max Item Appearances:     {max(item_counts.values())}")
        print("=" * 60 + "\n")

        # 100% of the catalog items must have been sampled at least once
        self.assertEqual(
            sampled_distinct_items, total_catalog_items,
            f"Some items were starved: only {sampled_distinct_items}/{total_catalog_items} sampled"
        )


if __name__ == "__main__":
    unittest.main()
