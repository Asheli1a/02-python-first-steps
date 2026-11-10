import json
from contextlib import redirect_stdout
from datetime import datetime
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from main import Quiz, QuizGame, parse_history


def make_game():
    game = QuizGame()
    game.quizzes = [
        Quiz("문제 A", ["A", "B", "C", "D"], 2),
        Quiz("문제 B", ["A", "B", "C", "D"], 2),
    ]
    return game


def play_with_answers(game, answers, selected=None):
    with patch("builtins.input", side_effect=answers):
        with redirect_stdout(StringIO()):
            return game.play(selected)


def test_completed_games():
    game = make_game()

    play_with_answers(game, ["2", "1"])
    play_with_answers(game, ["1", "1"])

    assert len(game.history) == 2

    first, second = game.history
    assert first["correct_count"] == 1
    assert first["total"] == 2
    assert first["score"] == 50
    assert second["score"] == 0

    for record in game.history:
        assert datetime.fromisoformat(record["played_at"]).utcoffset() is not None

    print("완료한 게임과 0점 및 시간대 기록: 통과")

def test_selected_count():
    game = make_game()

    play_with_answers(game, ["2"], selected=game.quizzes[:1])

    assert len(game.history) == 1
    assert game.history[0]["total"] == 1
    assert game.history[0]["score"] == 100

    print("실제 출제 수 기준 기록: 통과")


def test_no_record_for_empty_or_interrupted():
    game = make_game()

    with redirect_stdout(StringIO()):
        assert game.play([]) is None

    assert game.history == []

    for error_type in (KeyboardInterrupt, EOFError):
        with patch("builtins.input", side_effect=["2", error_type()]):
            with redirect_stdout(StringIO()):
                try:
                    game.play()
                except error_type:
                    pass
                else:
                    raise AssertionError("중단 예외가 전달되지 않았습니다.")

        assert game.history == []

    print("빈 목록과 게임 중단 시 미기록: 통과")


def test_old_file_and_round_trip():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "state.json"

        old_data = {
            "quizzes": [
                {
                    "question": "기존 문제",
                    "choices": ["A", "B", "C", "D"],
                    "answer": 2,
                }
            ],
            "best_score": {"correct_count": 4, "total": 5},
        }
        path.write_text(
            json.dumps(old_data, ensure_ascii=False),
            encoding="utf-8",
        )

        with redirect_stdout(StringIO()):
            game = QuizGame(state_path=path)

        assert game.history == []
        assert game.best_score == old_data["best_score"]
        assert game.quizzes[0].question == "기존 문제"

        play_with_answers(game, ["1"])

        with redirect_stdout(StringIO()):
            restored = QuizGame(state_path=path)

        assert restored.history == game.history
        assert len(restored.history) == 1
        assert restored.history[0]["score"] == 0
        assert restored.best_score == old_data["best_score"]

    print("기존 파일 호환과 기록 저장·복원: 통과")


def test_history_display_and_menu():
    game = make_game()
    output = StringIO()

    # 7번에서 빈 기록 확인 → 1번에서 1문제 → 정답 → 기록 조회 → 종료
    inputs = ["7", "1", "1", "2", "7", "5"]

    with patch("builtins.input", side_effect=inputs):
        with redirect_stdout(output):
            game.run()

    text = output.getvalue()

    assert "아직 완료한 게임 기록이 없습니다." in text
    assert "게임 기록 (총 1회" in text
    assert "1문제 중 1문제 정답 | 100점" in text
    assert len(game.history) == 1

    print("빈 기록 안내와 7번 메뉴 연결: 통과")


def test_delete_keeps_history():
    game = make_game()
    play_with_answers(game, ["2", "1"])
    original_history = [record.copy() for record in game.history]

    with patch("builtins.input", side_effect=["1", "1"]):
        with redirect_stdout(StringIO()):
            game.delete_quiz()

    assert len(game.quizzes) == 1
    assert game.history == original_history

    print("퀴즈 삭제 후 과거 기록 유지: 통과")


def test_invalid_history():
    valid = {
        "played_at": "2026-11-10T15:00:00+09:00",
        "correct_count": 1,
        "total": 2,
        "score": 50,
    }

    invalid_histories = [
        None,
        "wrong",
        [123],
        [{**valid, "played_at": "날짜 아님"}],
        [{**valid, "played_at": "2026-11-10T15:00:00"}],
        [{**valid, "total": 0}],
        [{**valid, "correct_count": True}],
        [{**valid, "score": 100}],
    ]

    for history in invalid_histories:
        try:
            parse_history({"history": history})
        except ValueError:
            pass
        else:
            raise AssertionError("잘못된 기록을 허용했습니다.")

    assert parse_history({}) == []
    print("기록 구조·시각·범위·점수 일관성 검사: 통과")


if __name__ == "__main__":
    test_completed_games()
    test_selected_count()
    test_no_record_for_empty_or_interrupted()
    test_old_file_and_round_trip()
    test_history_display_and_menu()
    test_delete_keeps_history()
    test_invalid_history()

    print("\n모든 게임 기록 테스트를 통과했습니다.")