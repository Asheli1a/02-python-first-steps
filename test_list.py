from contextlib import redirect_stdout
from io import StringIO

from main import Quiz, create_default_quizzes, show_quiz_list


def capture_list_output(quizzes):
    """목록 출력 내용을 문자열로 수집합니다."""
    output = StringIO()

    with redirect_stdout(output):
        show_quiz_list(quizzes)

    return output.getvalue()


def test_default_list():
    quizzes = create_default_quizzes()
    original_quizzes = quizzes.copy()

    output = capture_list_output(quizzes)

    assert f"등록된 퀴즈 목록 (총 {len(quizzes)}개)" in output

    for number, quiz in enumerate(quizzes, start=1):
        assert f"[{number}] {quiz.question}" in output

    assert quizzes == original_quizzes
    print("기본 퀴즈 목록과 번호 표시: 통과")


def test_added_quiz():
    quizzes = create_default_quizzes()

    quiz = Quiz(
        question="추가된 테스트 문제",
        choices=["A", "B", "C", "D"],
        answer=1,
    )
    quizzes.append(quiz)

    output = capture_list_output(quizzes)

    assert f"등록된 퀴즈 목록 (총 {len(quizzes)}개)" in output
    assert f"[{len(quizzes)}] 추가된 테스트 문제" in output
    print("추가된 퀴즈의 목록 반영: 통과")


def test_empty_list():
    output = capture_list_output([])

    assert "등록된 퀴즈가 없습니다." in output
    assert "등록된 퀴즈 목록" not in output
    print("퀴즈가 없는 경우: 통과")


if __name__ == "__main__":
    test_default_list()
    test_added_quiz()
    test_empty_list()
    print("\n모든 퀴즈 목록 테스트를 통과했습니다.")