from main import Quiz, create_default_quizzes


def test_quiz():
    quiz = Quiz(
        question="테스트 문제: 두 번째 선택지를 고르세요.",
        choices=["첫 번째", "두 번째", "세 번째", "네 번째"],
        answer=2,
    )

    print("=== 문제 출력 테스트 ===")
    quiz.display()

    print("\n=== 데이터 확인 테스트 ===")
    assert quiz.question == "테스트 문제: 두 번째 선택지를 고르세요."
    assert len(quiz.choices) == 4
    assert quiz.answer == 2

    print("\n=== 정답 확인 테스트 ===")
    assert quiz.check_answer(2) is True
    assert quiz.check_answer(1) is False
    assert quiz.check_answer(3) is False
    assert quiz.check_answer(4) is False

    print("Quiz 클래스 테스트를 통과했습니다.")


def test_default_quizzes():
    print("\n=== 기본 퀴즈 데이터 테스트 ===")

    quizzes = create_default_quizzes()

    assert isinstance(quizzes, list), "퀴즈 목록은 list여야 합니다."
    assert len(quizzes) >= 5, "기본 퀴즈는 5개 이상이어야 합니다."

    for number, quiz in enumerate(quizzes, start=1):
        assert isinstance(quiz, Quiz), f"{number}번은 Quiz 객체여야 합니다."

        assert isinstance(quiz.question, str), (
            f"{number}번 문제는 문자열이어야 합니다."
        )
        assert quiz.question.strip(), f"{number}번 문제가 비어 있습니다."

        assert isinstance(quiz.choices, list), (
            f"{number}번 선택지는 list여야 합니다."
        )
        assert len(quiz.choices) == 4, (
            f"{number}번 선택지는 4개여야 합니다."
        )

        for choice in quiz.choices:
            assert isinstance(choice, str), (
                f"{number}번 선택지는 문자열이어야 합니다."
            )
            assert choice.strip(), f"{number}번에 빈 선택지가 있습니다."

        assert type(quiz.answer) is int, (
            f"{number}번 정답 번호는 정수여야 합니다."
        )
        assert 1 <= quiz.answer <= 4, (
            f"{number}번 정답 번호는 1~4여야 합니다."
        )

        for answer in range(1, 5):
            expected = answer == quiz.answer
            assert quiz.check_answer(answer) is expected, (
                f"{number}번 문제의 정답 판정이 잘못됐습니다."
            )

        print(f"{number}번 검사 통과: {quiz.question}")

    print(f"기본 퀴즈 {len(quizzes)}개의 데이터 검사를 통과했습니다.")


if __name__ == "__main__":
    test_quiz()
    test_default_quizzes()
    print("\n모든 테스트를 통과했습니다.")