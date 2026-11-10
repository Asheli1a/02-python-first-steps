import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import main as main_module
from main import Quiz, QuizGame, parse_history


ADD_UNSAVED = (
    "현재 목록에는 퀴즈가 추가됐지만 "
    "파일 저장은 완료되지 않았습니다."
)
PLAY_UNSAVED = (
    "이번 결과는 현재 실행의 기록에 반영됐지만 "
    "파일 저장은 완료되지 않았습니다."
)


class StorageFeedbackTests(unittest.TestCase):
    def setUp(self):
        self.output = io.StringIO()
        self.redirect = redirect_stdout(self.output)
        self.redirect.__enter__()
        self.addCleanup(self.redirect.__exit__, None, None, None)
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "state.json"

    def make_game(self, persistent=True):
        game = QuizGame()
        game.quizzes = [
            Quiz("두 번째 선택지를 고르세요.", ["A", "B", "C", "D"], 2,
                 hint="두 번째입니다.")
        ]
        if persistent:
            game.state_path = self.path
        return game

    def add_inputs(self):
        return ["새 문제", "첫째", "둘째", "셋째", "넷째", "2"]

    def test_01_add_failure_keeps_memory_and_reports_unsaved(self):
        game = self.make_game()
        with patch.object(game, "save_state", return_value=False) as save:
            with patch("builtins.input", side_effect=self.add_inputs()):
                game.add_quiz()
        save.assert_called_once_with()
        self.assertEqual(len(game.quizzes), 2)
        self.assertEqual(game.quizzes[-1].question, "새 문제")
        self.assertIn(ADD_UNSAVED, self.output.getvalue())
        self.assertNotIn("추가한 퀴즈를 파일에 저장했습니다.", self.output.getvalue())

    def test_02_add_success_keeps_success_message(self):
        game = self.make_game()
        with patch.object(game, "save_state", return_value=True):
            with patch("builtins.input", side_effect=self.add_inputs()):
                game.add_quiz()
        self.assertIn("추가한 퀴즈를 파일에 저장했습니다.", self.output.getvalue())
        self.assertNotIn(ADD_UNSAVED, self.output.getvalue())

    def test_03_play_failure_keeps_assisted_result(self):
        game = self.make_game()
        with patch.object(game, "save_state", return_value=False) as save:
            with patch("builtins.input", side_effect=["h", "2"]):
                correct_count = game.play()
        save.assert_called_once_with()
        self.assertEqual(correct_count, 1)
        self.assertEqual(len(game.history), 1)
        self.assertEqual(game.history[0]["score"], 90)
        self.assertEqual(game.history[0]["hints_used"], 1)
        self.assertEqual(game.best_score["hints_used"], 1)
        self.assertIn(PLAY_UNSAVED, self.output.getvalue())

    def test_04_play_failure_keeps_better_old_record(self):
        game = self.make_game()
        old_best = {"correct_count": 2, "total": 2}
        game.best_score = old_best
        with patch.object(game, "save_state", return_value=False):
            with patch("builtins.input", side_effect=["h", "2"]):
                game.play()
        self.assertIs(game.best_score, old_best)
        self.assertEqual(len(game.history), 1)
        self.assertEqual(game.history[0]["score"], 90)
        self.assertIn(PLAY_UNSAVED, self.output.getvalue())

    def test_05_memory_only_execution_has_no_failure_notice(self):
        game = self.make_game(persistent=False)
        with patch("builtins.input", side_effect=self.add_inputs()):
            game.add_quiz()
        with patch("builtins.input", side_effect=["2"]):
            game.play([game.quizzes[0]])
        self.assertEqual(len(game.quizzes), 2)
        self.assertEqual(len(game.history), 1)
        self.assertNotIn(ADD_UNSAVED, self.output.getvalue())
        self.assertNotIn(PLAY_UNSAVED, self.output.getvalue())
        self.assertFalse(self.path.exists())

    def test_06_score_mismatch_mentions_hint_information(self):
        record = {
            "played_at": "2026-11-10T18:59:24+09:00",
            "correct_count": 1,
            "total": 1,
            "score": 100,
            "hints_used": 1,
            "hint_penalty": 10,
        }
        with self.assertRaises(ValueError) as caught:
            parse_history({"history": [record]})
        self.assertEqual(
            str(caught.exception),
            "1번 기록의 점수가 정답 수와 "
            "힌트 감점 정보에 따른 계산 결과와 일치하지 않습니다.",
        )
        record["score"] = 90
        self.assertEqual(parse_history({"history": [record]}), [record])

    def test_07_real_write_failure_preserves_old_file_and_retry(self):
        game = self.make_game()
        self.assertTrue(game.save_state())
        before = self.path.read_bytes()
        with patch.object(Path, "replace", side_effect=OSError("교체 실패 테스트")):
            with patch("builtins.input", side_effect=["h", "2"]):
                game.play()
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(len(game.history), 1)
        self.assertIn("데이터 저장에 실패했습니다:", self.output.getvalue())
        self.assertIn(PLAY_UNSAVED, self.output.getvalue())
        self.assertTrue(game.save_state())
        self.assertTrue(game.save_state())
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(len(data["history"]), 1)
        self.assertEqual(data["history"][0]["score"], 90)
        restored = QuizGame(state_path=self.path)
        self.assertEqual(restored.history, game.history)
        self.assertEqual(restored.best_score, game.best_score)

    def test_08_main_finally_retries_without_duplicate_history(self):
        game = self.make_game()
        self.assertTrue(game.save_state())
        original_replace = Path.replace
        calls = []

        def fail_once_then_replace(source, target):
            calls.append((source, target))
            if len(calls) == 1:
                raise OSError("초기 교체만 실패")
            return original_replace(source, target)

        with patch("main.QuizGame", return_value=game):
            with patch.object(game, "run", side_effect=game.play):
                with patch("builtins.input", side_effect=["2"]):
                    with patch.object(
                        Path, "replace", autospec=True,
                        side_effect=fail_once_then_replace,
                    ):
                        main_module.main()
        self.assertEqual(len(calls), 2)
        self.assertEqual(len(game.history), 1)
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(len(data["history"]), 1)
        self.assertEqual(data["history"][0]["score"], 100)
        self.assertIn(PLAY_UNSAVED, self.output.getvalue())
        self.assertIn("데이터를 저장했습니다.", self.output.getvalue())

    def test_09_play_success_has_no_failure_notice(self):
        game = self.make_game()
        with patch("builtins.input", side_effect=["2"]):
            game.play()
        self.assertTrue(self.path.exists())
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(len(data["history"]), 1)
        self.assertNotIn(PLAY_UNSAVED, self.output.getvalue())

    def test_10_add_real_failure_preserves_old_file(self):
        game = self.make_game()
        self.assertTrue(game.save_state())
        before = self.path.read_bytes()
        with patch.object(Path, "replace", side_effect=OSError("등록 저장 실패")):
            with patch("builtins.input", side_effect=self.add_inputs()):
                game.add_quiz()
        self.assertEqual(len(game.quizzes), 2)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertIn(ADD_UNSAVED, self.output.getvalue())
        self.assertTrue(game.save_state())
        restored = QuizGame(state_path=self.path)
        self.assertEqual(len(restored.quizzes), 2)
        self.assertEqual(restored.quizzes[-1].question, "새 문제")


if __name__ == "__main__":
    unittest.main(verbosity=2)
