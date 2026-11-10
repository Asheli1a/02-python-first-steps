import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from main import (
    Quiz, QuizGame, input_answer, parse_state, parse_history,
    play_quizzes, score_value, update_best_score,
)


def make_quiz(hint="힌트 내용"):
    return Quiz("문제", ["A", "B", "C", "D"], 2, hint=hint)


def quiet_call(function, inputs=None, *args, **kwargs):
    with redirect_stdout(io.StringIO()):
        if inputs is None:
            return function(*args, **kwargs)
        with patch("builtins.input", side_effect=inputs):
            return function(*args, **kwargs)


class HintPlayTests(unittest.TestCase):
    def test_01_hint_once_and_input_validation(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=[" H ", "h", "", "abc", "0", "5", " 2 "]):
            with redirect_stdout(output):
                answer, used = input_answer(make_quiz())
        self.assertEqual(answer, 2)
        self.assertTrue(used)
        self.assertEqual(output.getvalue().count("10점 감점됩니다."), 1)
        self.assertIn("추가 감점하지 않습니다.", output.getvalue())

    def test_02_missing_hint_is_free(self):
        self.assertEqual(quiet_call(input_answer, ["h", "2"], make_quiz("")), (2, False))

    def test_03_legacy_return_and_unassisted_record(self):
        self.assertEqual(quiet_call(play_quizzes, ["2"], [make_quiz()]), 1)
        result = quiet_call(update_best_score, None, None, 1, 1)
        self.assertEqual(result, {"correct_count": 1, "total": 1})

    def test_04_penalty_and_zero_floor(self):
        self.assertEqual(score_value(1, 1, 1), 90)
        self.assertEqual(score_value(1, 2, 1), 40)
        self.assertEqual(score_value(0, 2, 2), 0)
        self.assertEqual(score_value(1, 20, 1), 0)
        for hints in (-1, 3, True):
            with self.assertRaises(ValueError):
                score_value(1, 2, hints)

    def test_05_best_score_uses_final_score(self):
        old = {"correct_count": 19, "total": 20}
        kept = quiet_call(update_best_score, None, old, 1, 1, 1)
        self.assertIs(kept, old)
        assisted = {"correct_count": 1, "total": 1, "hints_used": 1, "hint_penalty": 10}
        updated = quiet_call(update_best_score, None, assisted, 1, 1)
        self.assertEqual(updated, {"correct_count": 1, "total": 1})
        tied = quiet_call(update_best_score, None, assisted, 9, 10)
        self.assertIs(tied, assisted)

    def test_06_record_round_trip(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            game = quiet_call(QuizGame, None, state_path=path)
            game.quizzes = [make_quiz()]
            self.assertEqual(quiet_call(game.play, ["h", "h", "2"]), 1)
            self.assertEqual(game.history[-1]["score"], 90)
            self.assertEqual(game.history[-1]["hints_used"], 1)
            restored = quiet_call(QuizGame, None, state_path=path)
            self.assertEqual(restored.history, game.history)
            self.assertEqual(restored.best_score, game.best_score)
            self.assertEqual(restored.quizzes[0].hint, "힌트 내용")

    def test_07_old_file_keeps_data(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            old = {
                "quizzes": [{"question": "기존 문제", "choices": ["A", "B", "C", "D"], "answer": 2}],
                "best_score": {"correct_count": 4, "total": 5},
                "history": [{"played_at": "2026-11-10T16:27:17+09:00", "correct_count": 4, "total": 5, "score": 80}],
            }
            path.write_text(json.dumps(old), encoding="utf-8")
            game = quiet_call(QuizGame, None, state_path=path)
            self.assertEqual(game.best_score, old["best_score"])
            self.assertEqual(game.history, old["history"])
            self.assertEqual(game.quizzes[0].hint, "")
            self.assertTrue(game.save_state())
            self.assertEqual(list(Path(directory).glob("*.bak")), [])

    def test_08_bad_records_are_rejected(self):
        valid = {"played_at": "2026-11-10T16:27:17+09:00", "correct_count": 1, "total": 1,
                 "score": 90, "hints_used": 1, "hint_penalty": 10}
        self.assertEqual(parse_history({"history": [valid]}), [valid])
        for fields in ({"score": 100}, {"hints_used": 2}, {"hints_used": True},
                       {"hint_penalty": -1}, {"hint_penalty": "10"}):
            with self.assertRaises(ValueError):
                parse_history({"history": [{**valid, **fields}]})
        with self.assertRaises(ValueError):
            parse_state({"quizzes": [], "best_score": {"correct_count": 1, "total": 1, "hints_used": 2}})

    def test_09_interrupt_does_not_record(self):
        for error in (KeyboardInterrupt, EOFError):
            game = QuizGame()
            game.quizzes = [make_quiz()]
            for inputs in (["h", error()], [error()]):
                with self.assertRaises(error):
                    quiet_call(game.play, inputs)
                self.assertEqual(game.history, [])
                self.assertIsNone(game.best_score)

    def test_10_empty_and_setting_cancel(self):
        game = QuizGame()
        game.quizzes = []
        with patch("builtins.input") as mocked:
            self.assertIsNone(quiet_call(game.play))
            self.assertFalse(quiet_call(game.set_hint))
            mocked.assert_not_called()
        game.quizzes = [make_quiz()]
        self.assertFalse(quiet_call(game.set_hint, ["0"]))
        self.assertEqual(game.quizzes[0].hint, "힌트 내용")
        with self.assertRaises(EOFError):
            quiet_call(game.set_hint, ["1", EOFError()])
        self.assertEqual(game.quizzes[0].hint, "힌트 내용")

    def test_11_menu_setting_and_play(self):
        game = QuizGame()
        game.quizzes = [make_quiz("")]
        quiet_call(game.run, ["8", "1", " 새 힌트 ", "1", "1", "h", "2", "7", "4", "5"])
        self.assertEqual(game.quizzes[0].hint, "새 힌트")
        self.assertEqual(game.history[0]["score"], 90)
        self.assertEqual(game.best_score["hints_used"], 1)

    def test_12_remove_hint(self):
        game = QuizGame()
        game.quizzes = [make_quiz()]
        self.assertTrue(quiet_call(game.set_hint, ["1", "   "]))
        self.assertEqual(game.quizzes[0].hint, "")

    def test_13_stored_penalty_is_respected(self):
        record = {"played_at": "2026-11-10T16:27:17+09:00", "correct_count": 1, "total": 1,
                  "score": 80, "hints_used": 1, "hint_penalty": 20}
        self.assertEqual(parse_history({"history": [record]}), [record])

    def test_14_setting_failure_reports_unsaved(self):
        game = QuizGame()
        game.quizzes = [make_quiz()]
        game.state_path = Path("unused-test-path.json")
        output = io.StringIO()
        with patch.object(game, "save_state", return_value=False):
            with patch("builtins.input", side_effect=["1", "새 힌트"]):
                with redirect_stdout(output):
                    game.set_hint()
        self.assertEqual(game.quizzes[0].hint, "새 힌트")
        self.assertIn("파일 저장은 완료되지 않았습니다.", output.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
