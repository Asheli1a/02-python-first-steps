from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from main import Quiz, QuizGame


def make_game():
    game = QuizGame()
    game.quizzes = [
        Quiz(
            question=f"테스트 문제 {number}",
            choices=["A", "B", "C", "D"],
            answer=2,
        )
        for number in range(1, 6)
    ]
    return game


def test_selected_count_and_record():
    game = make_game()
    original_quizzes = game.quizzes.copy()
    output = StringIO()

    # 3문제 선택 후 모두 정답
    inputs = ["3", "2", "2", "2"]

    with patch("builtins.input", side_effect=inputs):
        with redirect_stdout(output):
            result = game.play_selected()

    assert result == 3
    assert game.best_score == {
        "correct_count": 3,
        "total": 3,
    }
    assert "총 3문제" in output.getvalue()
    assert game.quizzes == original_quizzes

    print("선택한 문제 수·최고 기록·원본 목록 유지: 통과")


def test_sampling_without_replacement():
    game = make_game()
    original_quizzes = game.quizzes.copy()

    with patch("main.play_quizzes", return_value=0) as mocked_play:
        with patch("builtins.input", return_value="4"):
            with redirect_stdout(StringIO()):
                game.play_selected()

    selected = mocked_play.call_args.args[0]

    assert len(selected) == 4
    assert len({id(quiz) for quiz in selected}) == 4
    assert all(
        any(quiz is original for original in original_quizzes)
        for quiz in selected
    )
    assert selected is not game.quizzes
    assert game.quizzes == original_quizzes

    print("중복 위치 없이 선정하고 원본 순서 보존: 통과")


def test_invalid_count():
    game = make_game()

    # 잘못된 문제 수 입력 후 2문제 선택
    inputs = ["abc", "", "0", "6", " 2 ", "2", "2"]
    output = StringIO()

    with patch("builtins.input", side_effect=inputs):
        with redirect_stdout(output):
            result = game.play_selected()

    assert result == 2
    assert game.best_score["total"] == 2

    text = output.getvalue()
    assert "숫자로 입력하세요." in text
    assert "입력이 비어 있습니다." in text
    assert "1~5 사이의 숫자를 입력하세요." in text

    print("잘못된 문제 수와 공백 입력 처리: 통과")


def test_empty_quizzes():
    game = make_game()
    game.quizzes = []
    output = StringIO()

    with patch("builtins.input") as mocked_input:
        with redirect_stdout(output):
            result = game.play_selected()

    assert result is None
    assert game.best_score is None
    mocked_input.assert_not_called()
    assert "등록된 퀴즈가 없습니다." in output.getvalue()

    print("빈 퀴즈 목록에서 입력 없이 안내: 통과")


def test_interrupted_selection():
    for error_type in (KeyboardInterrupt, EOFError):
        game = make_game()
        record = {"correct_count": 4, "total": 5}
        game.best_score = record

        with patch("builtins.input", side_effect=error_type()):
            with redirect_stdout(StringIO()):
                try:
                    game.play_selected()
                except error_type:
                    pass
                else:
                    raise AssertionError("중단 예외가 전달되지 않았습니다.")

        assert game.best_score is record

    print("문제 수 선택 중 중단 시 기록 유지: 통과")


def test_menu_connection():
    game = make_game()

    # 1번 메뉴 → 2문제 선택 → 모두 정답 → 5번 종료
    inputs = ["1", "2", "2", "2", "5"]

    with patch("builtins.input", side_effect=inputs):
        with redirect_stdout(StringIO()):
            game.run()

    assert game.best_score == {
        "correct_count": 2,
        "total": 2,
    }

    print("메뉴에서 문제 수 선택과 랜덤 플레이 연결: 통과")


if __name__ == "__main__":
    test_selected_count_and_record()
    test_sampling_without_replacement()
    test_invalid_count()
    test_empty_quizzes()
    test_interrupted_selection()
    test_menu_connection()

    print("\n모든 랜덤 출제·문제 수 선택 테스트를 통과했습니다.")