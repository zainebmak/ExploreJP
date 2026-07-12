import unittest

from explorejp.pages.explore_cities import get_favorite_button_label


class ExploreCitiesPageTests(unittest.TestCase):
    def test_favorite_button_label_for_non_favorite_city(self):
        self.assertEqual(
            get_favorite_button_label(7, {3, 5}),
            "🤍 Add to My Japan",
        )

    def test_favorite_button_label_for_favorite_city(self):
        self.assertEqual(
            get_favorite_button_label(7, {3, 7}),
            "💖 Remove from My Japan",
        )


if __name__ == "__main__":
    unittest.main()
