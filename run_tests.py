"""기존 테스트 스크립트를 각각 별도 프로세스로 실행합니다."""

import subprocess
import sys
from pathlib import Path


TEST_SCRIPTS = (
    "test_quiz.py",
    "test_play.py",
    "test_add.py",
    "test_list.py",
    "test_score.py",
    "test_game.py",
    "test_storage.py",
    "test_random_selection.py",
    "test_delete.py",
    "test_history.py",
    "test_hints.py",
    "test_hint_play.py",
    "test_storage_feedback.py",
)


def run_tests(project_root=None, scripts=TEST_SCRIPTS):
    """전체 결과를 요약하고 성공 0, 실패 1, 사용자 중단 130을 반환합니다."""
    root = (
        Path(project_root).resolve()
        if project_root is not None
        else Path(__file__).resolve().parent
    )
    if not sys.executable:
        print("Python 실행 파일 경로를 확인할 수 없습니다.", flush=True)
        return 1

    print(f"Python: {sys.version.split()[0]}", flush=True)
    print(f"실행 파일: {sys.executable}", flush=True)
    print(f"프로젝트: {root}", flush=True)
    print(f"테스트 스크립트: {len(scripts)}종", flush=True)

    results = []
    interrupted = False

    for number, name in enumerate(scripts, start=1):
        print(f"\n[{number}/{len(scripts)}] {name}", flush=True)
        print("-" * 60, flush=True)
        path = root / name

        if not path.is_file():
            results.append((name, "FAIL", "파일 없음"))
            print("실패: 테스트 파일이 없습니다.", flush=True)
            continue

        try:
            completed = subprocess.run(
                [sys.executable, "-u", str(path)],
                cwd=root,
                check=False,
            )
        except KeyboardInterrupt:
            results.append((name, "INTERRUPTED", "사용자 중단"))
            interrupted = True
            print("\n사용자가 통합 테스트 실행을 중단했습니다.", flush=True)
            break
        except OSError as error:
            results.append((name, "FAIL", f"실행 오류: {error}"))
            print(f"실패: {error}", flush=True)
            continue

        if completed.returncode == 0:
            results.append((name, "PASS", "종료 코드 0"))
        else:
            results.append((name, "FAIL", f"종료 코드 {completed.returncode}"))

    print("\n" + "=" * 60, flush=True)
    print("테스트 스크립트 결과 요약", flush=True)
    for name, status, detail in results:
        print(f"{status:11} {name} ({detail})", flush=True)

    passed = sum(status == "PASS" for _, status, _ in results)
    failed = sum(status == "FAIL" for _, status, _ in results)
    stopped = sum(status == "INTERRUPTED" for _, status, _ in results)
    not_run = len(scripts) - len(results)
    print(
        f"총 {len(scripts)}종 | 통과 {passed} | 실패 {failed} | "
        f"중단 {stopped} | 미실행 {not_run}",
        flush=True,
    )
    print("개별 테스트 개수가 아니라 스크립트 단위 집계입니다.", flush=True)

    if interrupted:
        return 130
    if failed or not_run:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(run_tests())
