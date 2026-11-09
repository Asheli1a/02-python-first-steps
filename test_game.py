from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from main import QuizGame


def test_initial_state():
    game = QuizGame()

    assert len(game.quizzes) >= 5
    assert game.best_score is None

    print("게임 초기 상태: 통과")


def test_independent_games():
    first = QuizGame()
    second = QuizGame()

    assert first.quizzes is not second.quizzes
    assert first.quizzes[0] is not second.quizzes[0]

    second_count = len(second.quizzes)
    first.quizzes.pop()

    assert len(second.quizzes) == second_count

    first.best_score = {"correct_count": 1, "total": 5}
    assert second.best_score is None

    print("게임 객체 간 상태 분리: 통과")


def test_play_updates_record():
    game = QuizGame()
    answers = [str(quiz.answer) for quiz in game.quizzes]

    with patch("builtins.input", side_effect=answers):
        with redirect_stdout(StringIO()):
            result = game.play()

    assert result == len(game.quizzes)
    assert game.best_score == {
        "correct_count": len(game.quizzes),
        "total": len(game.quizzes),
    }

    print("플레이 결과의 최고 기록 반영: 통과")


def test_empty_play_keeps_record():
    game = QuizGame()
    game.quizzes = []
    record = {"correct_count": 4, "total": 5}
    game.best_score = record

    with redirect_stdout(StringIO()):
        result = game.play()

    assert result is None
    assert game.best_score is record

    print("빈 퀴즈 플레이 시 기존 기록 유지: 통과")


def test_interrupted_play_keeps_record():
    for error_type in (KeyboardInterrupt, EOFError):
        game = QuizGame()
        record = {"correct_count": 4, "total": 5}
        game.best_score = record

        with patch("builtins.input", side_effect=error_type()):
            with redirect_stdout(StringIO()):
                try:
                    game.play()
                except error_type:
                    pass
                else:
                    raise AssertionError("중단 예외가 전달되지 않았습니다.")

        assert game.best_score is record

    print("게임 중단 시 기존 기록 유지: 통과")


def test_menu_add_and_list():
    game = QuizGame()
    original_count = len(game.quizzes)

    inputs = [
        "2",
        "메뉴 연동 테스트 문제",
        "A",
        "B",
        "C",
        "D",
        "2",
        "3",
        "4",
        "5",
    ]

    output = StringIO()

    with patch("builtins.input", side_effect=inputs):
        with redirect_stdout(output):
            game.run()

    assert len(game.quizzes) == original_count + 1
    assert game.quizzes[-1].question == "메뉴 연동 테스트 문제"
    assert game.quizzes[-1].answer == 2

    text = output.getvalue()
    assert f"[{original_count + 1}] 메뉴 연동 테스트 문제" in text
    assert "아직 완료한 게임이 없습니다." in text
    assert "퀴즈 게임을 종료합니다." in text

    print("메뉴의 등록·목록·점수 조회·종료 연결: 통과")


if __name__ == "__main__":
    test_initial_state()
    test_independent_games()
    test_play_updates_record()
    test_empty_play_keeps_record()
    test_interrupted_play_keeps_record()
    test_menu_add_and_list()

    print("\n모든 QuizGame 테스트를 통과했습니다.")