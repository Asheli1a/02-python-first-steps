from main import Quiz


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

    print("모든 테스트를 통과했습니다.")


if __name__ == "__main__":
    test_quiz()