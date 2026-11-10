"""표준 라이브러리 unittest 로 핵심 로직을 검증한다: python3 -m unittest -v"""

import builtins
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from game import QuizGame
from input_utils import parse_int
from quiz import Quiz
from storage import StateStore


class QuizTest(unittest.TestCase):
    def test_is_correct(self):
        quiz = Quiz("q", ["a", "b", "c", "d"], 3)
        self.assertTrue(quiz.is_correct(3))
        self.assertFalse(quiz.is_correct(1))
        self.assertEqual(quiz.correct_choice(), "c")

    def test_invalid_quiz_raises(self):
        with self.assertRaises(ValueError):
            Quiz("q", ["a", "b"], 1)
        with self.assertRaises(ValueError):
            Quiz("q", ["a", "b", "c", "d"], 5)

    def test_dict_round_trip(self):
        quiz = Quiz("q", ["a", "b", "c", "d"], 2, "hint")
        again = Quiz.from_dict(quiz.to_dict())
        self.assertEqual(again.to_dict(), quiz.to_dict())

    def test_from_dict_rejects_bool_answer(self):
        with self.assertRaises(ValueError):
            Quiz.from_dict({"question": "q", "choices": list("abcd"), "answer": True})


class ParseIntTest(unittest.TestCase):
    def test_cases(self):
        self.assertEqual(parse_int("3", 1, 5), (3, None))
        for raw in ("", "abc", "9", "0", "1.5"):
            value, error = parse_int(raw, 1, 5)
            self.assertIsNone(value, raw)
            self.assertIsNotNone(error, raw)


class StateStoreTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "state.json"
        self.store = StateStore(self.path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_missing_file_uses_defaults(self):
        state, _, needs_save = self.store.load()
        self.assertGreaterEqual(len(state["quizzes"]), 5)
        self.assertIsNone(state["best_score"])
        self.assertFalse(needs_save)

    def test_save_then_load_keeps_data(self):
        quizzes = [Quiz("한글 문제", ["가", "나", "다", "라"], 4)]
        detail = {"correct": 1, "total": 1, "hints_used": 0}
        self.assertTrue(self.store.save(quizzes, 100, detail, []))
        self.assertIn("한글 문제", self.path.read_text(encoding="utf-8"))  # ensure_ascii=False
        state, _, _ = self.store.load()
        self.assertEqual(state["quizzes"][0].question, "한글 문제")
        self.assertEqual(state["best_score"], 100)

    def test_broken_file_is_backed_up_and_recovered(self):
        self.path.write_text("{ not json", encoding="utf-8")
        state, message, needs_save = self.store.load()
        self.assertTrue(needs_save)
        self.assertIn("손상", message)
        self.assertGreaterEqual(len(state["quizzes"]), 5)
        self.assertEqual(len(list(self.path.parent.glob("state.broken-*.json"))), 1)

    def test_wrong_schema_is_treated_as_broken(self):
        self.path.write_text(json.dumps({"quizzes": "x"}), encoding="utf-8")
        _, _, needs_save = self.store.load()
        self.assertTrue(needs_save)


class QuizGameTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = StateStore(Path(self.tmp.name) / "state.json")
        self.game = QuizGame(self.store)

    def tearDown(self):
        self.tmp.cleanup()

    def test_score_with_hint_penalty(self):
        self.assertEqual(QuizGame.calculate_score(4, 5), 80)
        self.assertEqual(QuizGame.calculate_score(2, 2, hints_used=1), 75)

    def test_best_score_only_increases(self):
        self.assertTrue(self.game.update_best_score(60, 3, 5))
        self.assertFalse(self.game.update_best_score(40, 2, 5))
        self.assertEqual(self.game.best_score, 60)

    def test_play_all_correct_updates_and_persists(self):
        answers = iter(["2"] + [str(q.answer) for q in self.game.quizzes])  # 문제 수 2
        picked = []
        original_sample = __import__("random").sample

        def fake_input(_prompt=""):
            return next(answers) if not picked else str(picked.pop(0).answer)

        import game as game_module

        def sample(population, k):
            result = original_sample(population, k)
            picked.extend(result)
            return result

        game_module.random.sample, saved_sample = sample, game_module.random.sample
        builtins.input, saved_input = fake_input, builtins.input
        try:
            with redirect_stdout(StringIO()):
                self.game.play_quiz()
        finally:
            builtins.input = saved_input
            game_module.random.sample = saved_sample
        self.assertEqual(self.game.best_score, 100)
        reloaded = QuizGame(self.store)
        self.assertEqual(reloaded.best_score, 100)
        self.assertEqual(len(reloaded.history), 1)

    def test_empty_quiz_list_is_handled(self):
        self.game.quizzes = []
        out = StringIO()
        with redirect_stdout(out):
            self.game.play_quiz()
            self.game.list_quizzes()
        self.assertEqual(out.getvalue().count("등록된 퀴즈가 없습니다"), 2)


if __name__ == "__main__":
    unittest.main()
