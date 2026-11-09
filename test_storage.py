import json
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from main import Quiz, QuizGame, parse_state


def test_missing_file():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "state.json"
        game = QuizGame(state_path=path)

        assert len(game.quizzes) >= 5
        assert game.best_score is None
        assert game.save_state() is True
        assert path.is_file()

    print("파일 없는 첫 실행과 최초 저장: 통과")


def test_round_trip():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "state.json"
        first = QuizGame(state_path=path)

        first.quizzes.append(
            Quiz("한글 저장 테스트", ["가", "나", "다", "라"], 3)
        )
        first.best_score = {"correct_count": 0, "total": 6}

        assert first.save_state() is True

        second = QuizGame(state_path=path)

        assert len(second.quizzes) == len(first.quizzes)
        assert second.quizzes[-1].question == "한글 저장 테스트"
        assert second.quizzes[-1].choices == ["가", "나", "다", "라"]
        assert second.quizzes[-1].answer == 3
        assert second.best_score == {"correct_count": 0, "total": 6}
        assert "한글 저장 테스트" in path.read_text(encoding="utf-8")

    print("퀴즈·0점 기록·UTF-8 저장 후 복원: 통과")


def test_corrupted_files():
    contents = [
        "{broken",
        json.dumps({"quizzes": "wrong", "best_score": None}),
    ]

    for content in contents:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            path.write_text(content, encoding="utf-8")

            game = QuizGame(state_path=path)

            assert len(game.quizzes) >= 5
            assert game.best_score is None

            backups = list(Path(directory).glob("state.json.corrupt-*.bak"))
            assert len(backups) == 1
            assert backups[0].read_text(encoding="utf-8") == content

            assert game.save_state() is True
            parse_state(json.loads(path.read_text(encoding="utf-8")))

    print("JSON 문법·구조 손상 시 백업과 초기화: 통과")


def test_invalid_values():
    invalid_quiz = {
        "question": "문제",
        "choices": ["A", "B", "C", "D"],
        "answer": True,
    }

    invalid_states = [
        {"quizzes": [invalid_quiz], "best_score": None},
        {
            "quizzes": [],
            "best_score": {"correct_count": 0, "total": 0},
        },
        {
            "quizzes": [],
            "best_score": {"correct_count": 6, "total": 5},
        },
        {"quizzes": []},
    ]

    for data in invalid_states:
        try:
            parse_state(data)
        except ValueError:
            pass
        else:
            raise AssertionError("잘못된 데이터를 허용했습니다.")

    print("필드 누락·잘못된 정답·최고 기록 범위 거부: 통과")


def test_read_error():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "state.json"

        with patch.object(Path, "open", side_effect=PermissionError("테스트")):
            game = QuizGame(state_path=path)

        assert game.storage_writable is False
        assert game.save_state() is False
        assert not path.exists()

    print("읽기 오류 시 원본 덮어쓰기 방지: 통과")


def test_failed_replace():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "state.json"
        game = QuizGame(state_path=path)
        assert game.save_state() is True

        original = path.read_bytes()
        game.best_score = {"correct_count": 1, "total": 5}

        with patch.object(
            Path, "replace", side_effect=PermissionError("테스트")
        ):
            assert game.save_state() is False

        assert path.read_bytes() == original

    print("파일 교체 실패 시 기존 데이터 보존: 통과")


def test_failed_backup():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "state.json"
        path.write_text("{broken", encoding="utf-8")

        with patch(
            "main.shutil.copyfile",
            side_effect=PermissionError("테스트"),
        ):
            game = QuizGame(state_path=path)

        assert game.storage_writable is False
        assert game.save_state() is False
        assert path.read_text(encoding="utf-8") == "{broken"

    print("백업 실패 시 손상 원본 보존: 통과")


def test_empty_quizzes():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "state.json"
        first = QuizGame(state_path=path)
        first.quizzes = []

        assert first.save_state() is True

        second = QuizGame(state_path=path)
        assert second.quizzes == []

    print("빈 퀴즈 목록도 그대로 복원: 통과")


if __name__ == "__main__":
    tests = [
        test_missing_file,
        test_round_trip,
        test_corrupted_files,
        test_invalid_values,
        test_read_error,
        test_failed_replace,
        test_failed_backup,
        test_empty_quizzes,
    ]

    for test in tests:
        output = StringIO()

        with redirect_stdout(output):
            test()

        print(output.getvalue().strip().splitlines()[-1])

    print("\n모든 저장 테스트를 통과했습니다.")