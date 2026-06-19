import random
import unittest
from collections import Counter

import memory_logic as logic


# These tests check rules that do not need a Pygame window.
# They use unittest, so they run with Python's built-in test runner.


class TestMemoryLogic(unittest.TestCase):
    def test_create_board_has_16_cards_and_8_pairs(self):
        board = logic.create_board()

        self.assertEqual(len(board), 16)
        self.assertEqual(sorted(Counter(board).values()), [2] * 8)

    def test_reset_starts_a_new_unfinished_game(self):
        logic.reset()

        self.assertEqual(len(logic.board), 16)
        self.assertEqual(logic.revealed, [False] * 16)
        self.assertEqual(logic.matched, [False] * 16)
        self.assertEqual(logic.moves, 0)
        self.assertEqual(logic.score, 0)
        self.assertIn(logic.mode, ("menu", "gui", "text"))
        self.assertFalse(logic.show_popup)

    def test_auto_solver_returns_known_unmatched_pair_when_memory_has_one(self):
        logic.reset()
        logic.board = list("AABBCCDDEEFFGGHH")
        logic.matched = [False] * 16
        logic.auto_memory = {0: "A", 1: "A"}

        original_random = random.random
        random.random = lambda: 0.0
        try:
            self.assertEqual(logic.auto_pick_pair(), (0, 1))
        finally:
            random.random = original_random

    def test_auto_solver_returns_none_when_less_than_two_unmatched_cards(self):
        logic.reset()
        logic.matched = [True] * 16
        logic.matched[0] = False

        self.assertIsNone(logic.auto_pick_pair())

    def test_cli_log_keeps_only_last_six_lines(self):
        logic.cli_log = []

        for index in range(8):
            logic.cli_log_append(f"line {index}")

        self.assertEqual(
            logic.cli_log,
            [
                "line 2",
                "line 3",
                "line 4",
                "line 5",
                "line 6",
                "line 7",
            ],
        )


if __name__ == "__main__":
    unittest.main()
