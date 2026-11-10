import json
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from main import Quiz, QuizGame, create_default_quizzes, parse_state


def test_optional_hint():
    old_style = Quiz("문제", ["A", "B", "C", "D"], 2)
    with_hint = Quiz(
        "문제",
        ["A", "B", "C", "D"],
        2,
        hint="두 번째 선택지입니다.",
    )

    assert old_style.hint == ""
    assert with_hint.hint == "두 번째 선택지입니다."
    assert with_hint.check_answer(2) is True

    print("기존 생성 방식과 힌트 속성: 통과")


def test_default_hints():
    quizzes = create_default_quizzes()

    assert len(quizzes) >= 5
    assert all(isinstance(quiz.hint, str) for quiz in quizzes)
    assert all(quiz.hint.strip() for quiz in quizzes)

    print("기본 퀴즈의 힌트 구성: 통과")


def test_old_data_and_validation():
    old_quiz = {
        "question": "기존 문제",
        "choices": ["A", "B", "C", "D"],
        "answer": 2,
    }

    quizzes, _ = parse_state(
        {
            "quizzes": [old_quiz],
            "best_score": None,
        }
    )
    assert quizzes[0].hint == ""

    quizzes, _ = parse_state(
        {
            "quizzes": [{**old_quiz, "hint": "  한글 힌트  "}],
            "best_score": None,
        }
    )
    assert quizzes[0].hint == "한글 힌트"

    for invalid_hint in (None, 123, True, [], {}):
        try:
            parse_state(
                {
                    "quizzes": [{**old_quiz, "hint": invalid_hint}],
                    "best_score": None,
                }
            )
        except ValueError:
            pass
        else:
            raise AssertionError("문자열이 아닌 힌트를 허용했습니다.")

    print("기존 데이터 호환과 힌트 형식 검증: 통과")


def test_hint_round_trip():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "state.json"

        with redirect_stdout(StringIO()):
            first = QuizGame(state_path=path)

        first.quizzes = [
            Quiz(
                "한글 문제",
                ["가", "나", "다", "라"],
                2,
                hint="두 번째 선택지입니다.",
            )
        ]
        first.best_score = {"correct_count": 1, "total": 1}
        first.history = [
            {
                "played_at": "2026-11-10T16:27:17+09:00",
                "correct_count": 1,
                "total": 1,
                "score": 100,
            }
        ]

        assert first.save_state() is True

        with redirect_stdout(StringIO()):
            restored = QuizGame(state_path=path)

        assert restored.quizzes[0].hint == "두 번째 선택지입니다."
        assert restored.best_score == first.best_score
        assert restored.history == first.history

        saved = json.loads(path.read_text(encoding="utf-8"))
        assert saved["quizzes"][0]["hint"] == "두 번째 선택지입니다."

    print("힌트 저장·복원과 기존 기록 유지: 통과")


def test_old_file_upgrade():
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
            "best_score": None,
            "history": [],
        }
        path.write_text(
            json.dumps(old_data, ensure_ascii=False),
            encoding="utf-8",
        )

        with redirect_stdout(StringIO()):
            game = QuizGame(state_path=path)

        assert game.quizzes[0].question == "기존 문제"
        assert game.quizzes[0].hint == ""
        assert game.save_state() is True

        saved = json.loads(path.read_text(encoding="utf-8"))
        assert saved["quizzes"][0]["hint"] == ""
        assert not list(Path(directory).glob("*.bak"))

    print("기존 파일을 손상 처리 없이 새 형식으로 저장: 통과")


if __name__ == "__main__":
    test_optional_hint()
    test_default_hints()
    test_old_data_and_validation()
    test_hint_round_trip()
    test_old_file_upgrade()

    print("\n모든 힌트 데이터 테스트를 통과했습니다.")