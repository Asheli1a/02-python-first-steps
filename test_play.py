from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from main import create_default_quizzes, play_quizzes


def run_game_with_answers(answers):
    """키보드 입력 대신 준비된 답을 전달하고 출력도 수집합니다."""
    output = StringIO()

    with patch("builtins.input", side_effect=answers):
        with redirect_stdout(output):
            result = play_quizzes(create_default_quizzes())

    return result, output.getvalue()


def test_all_correct():
    quizzes = create_default_quizzes()
    answers = [str(quiz.answer) for quiz in quizzes]

    result, output = run_game_with_answers(answers)

    assert result == len(quizzes)
    assert "100점" in output
    print("모두 정답인 경우: 통과")


def test_all_wrong():
    quizzes = create_default_quizzes()

    # 각 문제의 정답과 반드시 다른 번호를 만듭니다.
    answers = [str(quiz.answer % 4 + 1) for quiz in quizzes]

    result, output = run_game_with_answers(answers)

    assert result == 0
    assert "(0점)" in output
    assert output.count("오답입니다.") == len(quizzes)
    print("모두 오답인 경우: 통과")


def test_invalid_input():
    quizzes = create_default_quizzes()
    answers = ["abc", "", "0", "5"]
    answers += [f" {quiz.answer} " for quiz in quizzes]

    result, output = run_game_with_answers(answers)

    assert result == len(quizzes)
    assert "숫자로 입력하세요." in output
    assert "입력이 비어 있습니다." in output
    assert "1~4 사이의 숫자를 입력하세요." in output
    print("잘못된 입력 후 재입력: 통과")


def test_empty_quizzes():
    output = StringIO()

    with redirect_stdout(output):
        result = play_quizzes([])

    assert result is None
    assert "등록된 퀴즈가 없습니다." in output.getvalue()
    print("퀴즈가 없는 경우: 통과")


if __name__ == "__main__":
    test_all_correct()
    test_all_wrong()
    test_invalid_input()
    test_empty_quizzes()
    print("\n모든 플레이 테스트를 통과했습니다.")