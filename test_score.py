from contextlib import redirect_stdout
from io import StringIO

from main import show_best_score, update_best_score


def update_quietly(best_score, correct_count, total):
    with redirect_stdout(StringIO()):
        return update_best_score(best_score, correct_count, total)


def capture_best_score(best_score):
    output = StringIO()

    with redirect_stdout(output):
        show_best_score(best_score)

    return output.getvalue()


def test_no_record():
    output = capture_best_score(None)

    assert "아직 완료한 게임이 없습니다." in output
    print("아직 완료한 게임이 없는 경우: 통과")


def test_first_zero_score():
    best = update_quietly(None, 0, 5)

    assert best == {"correct_count": 0, "total": 5}

    output = capture_best_score(best)
    assert "최고 점수: 0점" in output
    assert "당시 5문제 중 0문제 정답" in output

    print("첫 게임이 0점인 경우: 통과")


def test_higher_score():
    best = {"correct_count": 4, "total": 5}
    updated = update_quietly(best, 5, 6)

    assert updated == {"correct_count": 5, "total": 6}
    assert best == {"correct_count": 4, "total": 5}

    print("문제 수가 달라도 높은 정답률로 갱신: 통과")


def test_lower_score():
    best = {"correct_count": 4, "total": 5}

    # 정답 개수는 늘었지만 정답률은 낮아졌습니다.
    updated = update_quietly(best, 5, 10)

    assert updated is best
    print("정답 개수가 많아도 낮은 정답률이면 유지: 통과")


def test_equal_score():
    best = {"correct_count": 4, "total": 5}
    updated = update_quietly(best, 8, 10)

    assert updated is best
    print("동일한 정답률이면 기존 기록 유지: 통과")


def test_record_display():
    best = {"correct_count": 5, "total": 6}
    output = capture_best_score(best)

    assert "최고 점수: 83점" in output
    assert "당시 6문제 중 5문제 정답" in output
    print("최고 점수와 당시 문제 수 표시: 통과")


if __name__ == "__main__":
    test_no_record()
    test_first_zero_score()
    test_higher_score()
    test_lower_score()
    test_equal_score()
    test_record_display()

    print("\n모든 최고 점수 테스트를 통과했습니다.")