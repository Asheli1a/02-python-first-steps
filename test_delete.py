from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from main import Quiz, QuizGame, delete_quiz


def make_quizzes():
    return [
        Quiz("문제 A", ["A", "B", "C", "D"], 1),
        Quiz("문제 B", ["A", "B", "C", "D"], 2),
        Quiz("문제 C", ["A", "B", "C", "D"], 3),
    ]


def run_delete(quizzes, inputs):
    with patch("builtins.input", side_effect=inputs):
        with redirect_stdout(StringIO()):
            return delete_quiz(quizzes)


def test_delete_selected():
    quizzes = make_quizzes()
    first = quizzes[0]
    last = quizzes[2]

    result = run_delete(quizzes, ["2", "1"])

    assert result is True
    assert quizzes == [first, last]

    print("선택한 번호의 문제만 삭제: 통과")

def test_cancel():
    for inputs in (["0"], ["2", "0"]):
        quizzes = make_quizzes()
        original = quizzes.copy()

        result = run_delete(quizzes, inputs)

        assert result is False
        assert quizzes == original

    print("번호 선택과 최종 확인에서 취소: 통과")


def test_invalid_input():
    quizzes = make_quizzes()

    inputs = [
        "abc", "", "-1", "4", " 2 ",
        "abc", "", "2", "1",
    ]

    result = run_delete(quizzes, inputs)

    assert result is True
    assert [quiz.question for quiz in quizzes] == ["문제 A", "문제 C"]

    print("잘못된 입력 후 재입력과 공백 처리: 통과")


def test_empty_list():
    with patch("builtins.input") as mocked_input:
        with redirect_stdout(StringIO()):
            result = delete_quiz([])

    assert result is False
    mocked_input.assert_not_called()

    print("빈 목록에서 입력 없이 안내: 통과")


def test_interrupted_input():
    for error_type in (KeyboardInterrupt, EOFError):
        for prefix in ([], ["2"]):
            quizzes = make_quizzes()
            original = quizzes.copy()
            inputs = prefix + [error_type()]

            try:
                run_delete(quizzes, inputs)
            except error_type:
                pass
            else:
                raise AssertionError("중단 예외가 전달되지 않았습니다.")

            assert quizzes == original

    print("번호·확인 입력 중 중단 시 원본 유지: 통과")


def test_persistence_and_best_record():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "state.json"

        with redirect_stdout(StringIO()):
            game = QuizGame(state_path=path)

        game.quizzes = make_quizzes()
        record = {"correct_count": 4, "total": 5}
        game.best_score = record.copy()

        with patch("builtins.input", side_effect=["2", "1"]):
            with redirect_stdout(StringIO()):
                result = game.delete_quiz()

        assert result is True

        with redirect_stdout(StringIO()):
            restored = QuizGame(state_path=path)

        assert [q.question for q in restored.quizzes] == [
            "문제 A", "문제 C"
        ]
        assert restored.best_score == record

    print("삭제 후 재실행 복원과 과거 최고 기록 유지: 통과")


def test_delete_last_quiz():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "state.json"

        with redirect_stdout(StringIO()):
            game = QuizGame(state_path=path)

        game.quizzes = make_quizzes()[:1]

        with patch("builtins.input", side_effect=["1", "1"]):
            with redirect_stdout(StringIO()):
                game.delete_quiz()

        with redirect_stdout(StringIO()):
            restored = QuizGame(state_path=path)

        assert restored.quizzes == []

    print("마지막 문제 삭제 후 빈 목록 유지: 통과")


def test_save_failure():
    game = QuizGame()
    game.quizzes = make_quizzes()
    game.state_path = Path("not-used-state.json")
    output = StringIO()

    with patch.object(game, "save_state", return_value=False):
        with patch("builtins.input", side_effect=["1", "1"]):
            with redirect_stdout(output):
                result = game.delete_quiz()

    assert result is True
    assert len(game.quizzes) == 2
    assert "파일 저장은 완료되지 않았습니다." in output.getvalue()

    print("저장 실패 시 메모리 변경과 미저장 안내: 통과")


def test_menu_connection():
    game = QuizGame()
    game.quizzes = make_quizzes()

    # 6번 메뉴 → 2번 문제 → 삭제 확인 → 5번 종료
    with patch("builtins.input", side_effect=["6", "2", "1", "5"]):
        with redirect_stdout(StringIO()):
            game.run()

    assert [q.question for q in game.quizzes] == ["문제 A", "문제 C"]

    print("삭제 메뉴 연결과 기존 5번 종료 유지: 통과")


if __name__ == "__main__":
    test_delete_selected()
    test_cancel()
    test_invalid_input()
    test_empty_list()
    test_interrupted_input()
    test_persistence_and_best_record()
    test_delete_last_quiz()
    test_save_failure()
    test_menu_connection()

    print("\n모든 퀴즈 삭제 테스트를 통과했습니다.")