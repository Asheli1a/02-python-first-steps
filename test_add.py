from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from main import add_quiz, create_default_quizzes


def run_add_with_inputs(quizzes, inputs):
    output = StringIO()

    with patch("builtins.input", side_effect=inputs):
        with redirect_stdout(output):
            add_quiz(quizzes)

    return output.getvalue()


def test_add_quiz():
    quizzes = create_default_quizzes()
    original_count = len(quizzes)

    inputs = [
        "  테스트 문제  ",
        "  선택지 A  ",
        "선택지 B",
        "선택지 C",
        "선택지 D",
        " 3 ",
    ]

    output = run_add_with_inputs(quizzes, inputs)

    assert len(quizzes) == original_count + 1

    quiz = quizzes[-1]
    assert quiz.question == "테스트 문제"
    assert quiz.choices == [
        "선택지 A",
        "선택지 B",
        "선택지 C",
        "선택지 D",
    ]
    assert quiz.answer == 3
    assert quiz.check_answer(3) is True
    assert "퀴즈가 추가되었습니다!" in output

    print("정상 등록과 앞뒤 공백 제거: 통과")


def test_invalid_input():
    quizzes = []

    inputs = [
        "", "   ", "테스트 문제",
        "", "선택지 A",
        "   ", "선택지 B",
        "선택지 C",
        "선택지 D",
        "abc", "", "0", "5", "2",
    ]

    output = run_add_with_inputs(quizzes, inputs)

    assert len(quizzes) == 1
    assert quizzes[0].answer == 2
    assert "입력이 비어 있습니다. 내용을 입력하세요." in output
    assert "숫자로 입력하세요." in output
    assert "입력이 비어 있습니다. 숫자를 입력하세요." in output
    assert "1~4 사이의 숫자를 입력하세요." in output

    print("빈 입력과 잘못된 정답 번호 처리: 통과")


def test_interrupted_input():
    for error_type in (KeyboardInterrupt, EOFError):
        quizzes = create_default_quizzes()
        original_quizzes = quizzes.copy()

        # 문제와 첫 선택지를 입력한 뒤 입력 중단을 발생시킵니다.
        inputs = ["작성 중인 문제", "선택지 A", error_type()]

        try:
            run_add_with_inputs(quizzes, inputs)
        except error_type:
            pass
        else:
            raise AssertionError("입력 중단 예외가 전달되지 않았습니다.")

        assert quizzes == original_quizzes

    print("Ctrl+C와 EOF에서 미완성 퀴즈 추가 방지: 통과")


if __name__ == "__main__":
    test_add_quiz()
    test_invalid_input()
    test_interrupted_input()
    print("\n모든 퀴즈 추가 테스트를 통과했습니다.")