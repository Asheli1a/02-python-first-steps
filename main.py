import json
from datetime import datetime
import random
import shutil
from pathlib import Path
from uuid import uuid4


class Quiz:
    """문제 하나의 데이터와 동작을 관리합니다."""

    def __init__(self, question, choices, answer, hint=""):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def display(self):
        """문제와 선택지를 출력합니다."""
        print(self.question)

        for number, choice in enumerate(self.choices, start=1):
            print(f"{number}. {choice}")

    def check_answer(self, user_answer):
        """입력한 번호가 정답이면 True, 아니면 False를 반환합니다."""
        return user_answer == self.answer

def create_default_quizzes():
    """기본 퀴즈 5개를 새로운 객체 목록으로 만들어 반환합니다."""
    return [
        Quiz(
            question="CPU의 주된 역할은 무엇인가요?",
            choices=[
                "화면에 영상을 표시한다",
                "명령어를 해석하고 연산을 수행한다",
                "종이에 문서를 출력한다",
                "컴퓨터에 전원을 공급한다",
            ],
            answer=2,
            hint="컴퓨터에서 명령을 처리하는 중앙 장치를 생각해 보세요.",
        ),
        Quiz(
            question="일반적인 PC에서 전원을 끄면 저장 내용이 사라지는 메모리는?",
            choices=[
                "SSD",
                "HDD",
                "RAM",
                "USB 플래시 드라이브",
            ],
            answer=3,
            hint="실행 중인 프로그램이 작업 공간으로 사용하는 메모리입니다.",
        ),
        Quiz(
            question="다음 중 운영체제에 해당하는 것은 무엇인가요?",
            choices=[
                "Windows",
                "HDMI",
                "DDR5",
                "PCIe",
            ],
            answer=1,
            hint="다른 선택지는 연결 규격이나 메모리 규격입니다.",
        ),
        Quiz(
            question="다음 중 Python에서 문자열을 나타내는 자료형은?",
            choices=[
                "int",
                "bool",
                "list",
                "str",
            ],
            answer=4,
            hint="영어 string의 앞부분을 생각해 보세요.",
        ),
        Quiz(
            question="Git에서 준비된 변경 사항을 로컬 이력에 기록하는 명령은?",
            choices=[
                "git status",
                "git commit",
                "git diff",
                "git log",
            ],
            answer=2,
            hint="변경 내용을 하나의 이력으로 확정하는 명령입니다.",
        ),
    ]

def parse_state(data):
    """저장 데이터의 구조를 검사하고 퀴즈 객체와 최고 기록을 반환합니다."""
    if not isinstance(data, dict):
        raise ValueError("최상위 데이터는 객체여야 합니다.")

    if "quizzes" not in data or "best_score" not in data:
        raise ValueError("quizzes 또는 best_score가 없습니다.")

    if not isinstance(data["quizzes"], list):
        raise ValueError("quizzes는 목록이어야 합니다.")

    quizzes = []

    for number, item in enumerate(data["quizzes"], start=1):
        if not isinstance(item, dict):
            raise ValueError(f"{number}번 퀴즈는 객체여야 합니다.")

        question = item.get("question")
        choices = item.get("choices")
        answer = item.get("answer")
        hint = item.get("hint", "")

        if not isinstance(hint, str):
            raise ValueError(f"{number}번 힌트는 문자열이어야 합니다.")

        if not isinstance(question, str) or not question.strip():
            raise ValueError(f"{number}번 문제가 비어 있거나 문자열이 아닙니다.")

        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError(f"{number}번 선택지는 4개여야 합니다.")

        if any(
            not isinstance(choice, str) or not choice.strip()
            for choice in choices
        ):
            raise ValueError(f"{number}번 선택지에 잘못된 값이 있습니다.")

        if type(answer) is not int or not 1 <= answer <= 4:
            raise ValueError(f"{number}번 정답은 1~4의 정수여야 합니다.")

        quizzes.append(
            Quiz(
                question=question.strip(),
                choices=[choice.strip() for choice in choices],
                answer=answer,
                hint=hint.strip(),
            )
        )

    best_score = data["best_score"]

    if best_score is not None:
        if not isinstance(best_score, dict):
            raise ValueError("best_score는 객체 또는 null이어야 합니다.")

        correct_count = best_score.get("correct_count")
        total = best_score.get("total")

        if type(correct_count) is not int or type(total) is not int:
            raise ValueError("최고 기록의 정답 수와 문제 수는 정수여야 합니다.")

        if total <= 0 or not 0 <= correct_count <= total:
            raise ValueError("최고 기록의 정답 수 또는 문제 수가 잘못됐습니다.")

        best_score = {
            "correct_count": correct_count,
            "total": total,
        }

    return quizzes, best_score

def parse_history(data):
    """기존 파일은 빈 기록으로 읽고, 기록이 있으면 구조를 검사합니다."""
    history = data.get("history", [])

    if not isinstance(history, list):
        raise ValueError("history는 목록이어야 합니다.")

    validated = []

    for number, item in enumerate(history, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"{number}번 게임 기록은 객체여야 합니다.")

        played_at = item.get("played_at")
        correct_count = item.get("correct_count")
        total = item.get("total")
        score = item.get("score")

        if not isinstance(played_at, str):
            raise ValueError(f"{number}번 기록의 시각은 문자열이어야 합니다.")

        recorded_time = datetime.fromisoformat(played_at)

        if recorded_time.utcoffset() is None:
            raise ValueError(f"{number}번 기록에 시간대가 없습니다.")

        if type(correct_count) is not int or type(total) is not int:
            raise ValueError(f"{number}번 기록의 문제 수는 정수여야 합니다.")

        if total <= 0 or not 0 <= correct_count <= total:
            raise ValueError(f"{number}번 기록의 정답 수 또는 문제 수가 잘못됐습니다.")

        if type(score) is not int:
            raise ValueError(f"{number}번 기록의 점수는 정수여야 합니다.")

        expected_score = round(correct_count / total * 100)

        if score != expected_score:
            raise ValueError(f"{number}번 기록의 점수와 정답 수가 일치하지 않습니다.")

        validated.append(
            {
                "played_at": played_at,
                "correct_count": correct_count,
                "total": total,
                "score": score,
            }
        )

    return validated

def input_int(prompt, minimum, maximum):
    """허용 범위 안의 정수를 입력받을 때까지 반복합니다."""
    while True:
        text = input(prompt).strip()

        if text == "":
            print("입력이 비어 있습니다. 숫자를 입력하세요.")
            continue

        try:
            number = int(text)
        except ValueError:
            print("숫자로 입력하세요.")
            continue

        if minimum <= number <= maximum:
            return number

        print(f"{minimum}~{maximum} 사이의 숫자를 입력하세요.")

def input_text(prompt):
    """앞뒤 공백을 제거하고, 비어 있지 않은 문자열을 반환합니다."""
    while True:
        text = input(prompt).strip()

        if text:
            return text

        print("입력이 비어 있습니다. 내용을 입력하세요.")

def add_quiz(quizzes):
    """모든 입력을 완료하면 새 퀴즈를 목록에 추가합니다."""
    print("\n새로운 퀴즈를 추가합니다.")

    question = input_text("문제를 입력하세요: ")

    choices = []

    for number in range(1, 5):
        choice = input_text(f"선택지 {number}: ")
        choices.append(choice)

    answer = input_int("정답 번호 (1~4): ", 1, 4)

    quiz = Quiz(
        question=question,
        choices=choices,
        answer=answer,
    )

    quizzes.append(quiz)

    print(f"퀴즈가 추가되었습니다! 현재 총 {len(quizzes)}개입니다.")

def show_quiz_list(quizzes):
    """등록된 퀴즈의 문제를 번호와 함께 출력합니다."""
    if not quizzes:
        print("\n등록된 퀴즈가 없습니다.")
        return

    print("\n" + "=" * 40)
    print(f"등록된 퀴즈 목록 (총 {len(quizzes)}개)")
    print("-" * 40)

    for number, quiz in enumerate(quizzes, start=1):
        print(f"[{number}] {quiz.question}")

    print("=" * 40)

def delete_quiz(quizzes):
    """삭제를 최종 확인한 경우에만 목록을 변경하고 True를 반환합니다."""
    if not quizzes:
        print("\n삭제할 퀴즈가 없습니다.")
        return False

    show_quiz_list(quizzes)

    number = input_int(
        f"삭제할 문제 번호 (1~{len(quizzes)}, 0: 취소): ",
        0,
        len(quizzes),
    )

    if number == 0:
        print("삭제를 취소했습니다.")
        return False

    quiz = quizzes[number - 1]

    print(f"\n삭제 대상: {quiz.question}")
    confirmation = input_int(
        "정말 삭제할까요? (1: 삭제, 0: 취소): ",
        0,
        1,
    )

    if confirmation == 0:
        print("삭제를 취소했습니다.")
        return False

    deleted_quiz = quizzes.pop(number - 1)

    print(f"퀴즈를 삭제했습니다: {deleted_quiz.question}")
    print(f"현재 총 {len(quizzes)}개입니다.")

    return True

def play_quizzes(quizzes):
    """퀴즈를 차례로 출제하고 최종 정답 수를 반환합니다."""
    if not quizzes:
        print("등록된 퀴즈가 없습니다.")
        return None

    correct_count = 0
    total = len(quizzes)

    print(f"\n퀴즈를 시작합니다! (총 {total}문제)")

    for number, quiz in enumerate(quizzes, start=1):
        print("\n" + "-" * 40)
        print(f"[문제 {number}/{total}]")
        quiz.display()

        user_answer = input_int("정답 입력 (1~4): ", 1, 4)

        if quiz.check_answer(user_answer):
            print("정답입니다!")
            correct_count += 1
        else:
            correct_choice = quiz.choices[quiz.answer - 1]
            print("오답입니다.")
            print(f"정답: {quiz.answer}. {correct_choice}")

    score = correct_count / total * 100

    print("\n" + "=" * 40)
    print(f"결과: {total}문제 중 {correct_count}문제 정답! ({score:.0f}점)")
    print("=" * 40)

    return correct_count

def update_best_score(best_score, correct_count, total):
    """더 높은 정답률이면 새 기록을 반환하고, 아니면 기존 기록을 유지합니다."""
    if best_score is None:
        is_new_record = True
    else:
        # 나눗셈 대신 교차 곱으로 정답률을 비교합니다.
        is_new_record = (
            correct_count * best_score["total"]
            > best_score["correct_count"] * total
        )

    if is_new_record:
        print("새로운 최고 기록입니다!")

        return {
            "correct_count": correct_count,
            "total": total,
        }

    return best_score

def show_best_score(best_score):
    """최고 기록을 출력합니다."""
    if best_score is None:
        print("\n아직 완료한 게임이 없습니다.")
        return

    correct_count = best_score["correct_count"]
    total = best_score["total"]
    score = correct_count / total * 100

    print("\n" + "=" * 40)
    print(f"최고 점수: {score:.0f}점")
    print(f"당시 {total}문제 중 {correct_count}문제 정답")
    print("=" * 40)

def show_menu():
    """메뉴를 화면에 출력합니다."""
    print()
    print("=" * 40)
    print("           나만의 퀴즈 게임")
    print("=" * 40)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("6. 퀴즈 삭제")
    print("7. 게임 기록")
    print("=" * 40)


class QuizGame:
    """게임 상태와 메뉴 진행을 관리합니다."""

    def __init__(self, state_path=None):
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.history = []
        self.state_path = (
            Path(state_path) if state_path is not None else None
        )
        self.storage_writable = True

        if self.state_path is not None:
            self.load_state()

    def load_state(self):
        """파일을 읽고, 검증을 통과한 데이터만 적용합니다."""
        if self.state_path is None:
            return

        try:
            with self.state_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            quizzes, best_score = parse_state(data)
            history = parse_history(data)

        except FileNotFoundError:
            print("저장 파일이 없어 기본 퀴즈로 시작합니다.")

        except (ValueError, UnicodeError) as error:
            print(f"저장 파일이 손상되었습니다: {error}")
            self.backup_damaged_state()
            print("기본 퀴즈와 초기 기록으로 시작합니다.")

        except OSError as error:
            self.storage_writable = False
            print(f"저장 파일을 읽을 수 없습니다: {error}")
            print("원본 보호를 위해 이번 실행에서는 파일 저장을 중지합니다.")

        else:
            self.quizzes = quizzes
            self.best_score = best_score
            self.history = history
            print(f"저장된 데이터를 불러왔습니다. 퀴즈 {len(quizzes)}개")

    def backup_damaged_state(self):
        """손상된 원본을 복사하고, 백업 실패 시 덮어쓰기를 막습니다."""
        backup_path = self.state_path.with_name(
            f"{self.state_path.name}.corrupt-{uuid4().hex}.bak"
        )

        try:
            shutil.copyfile(self.state_path, backup_path)
            print(f"손상 파일 백업: {backup_path.name}")
        except OSError as error:
            self.storage_writable = False
            print(f"손상 파일을 백업할 수 없습니다: {error}")
            print("원본 보호를 위해 이번 실행에서는 파일 저장을 중지합니다.")

    def save_state(self):
        """임시 파일에 저장한 뒤 기존 파일을 교체합니다."""
        if self.state_path is None:
            return False

        if not self.storage_writable:
            print("원본 보호를 위해 파일 저장을 건너뜁니다.")
            return False

        data = {
            "quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer,
                    "hint": quiz.hint,
                }
                for quiz in self.quizzes
            ],
            "best_score": self.best_score,
            "history": self.history,
        }

        temporary_path = self.state_path.with_name(
            self.state_path.name + ".tmp"
        )

        try:
            # 잘못된 메모리 데이터를 파일에 기록하지 않도록 검사합니다.
            parse_state(data)
            parse_history(data)

            with temporary_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
                file.write("\n")

            temporary_path.replace(self.state_path)

        except (OSError, ValueError, TypeError, UnicodeError) as error:
            print(f"데이터 저장에 실패했습니다: {error}")
            return False

        return True

    def show_menu(self):
        """메뉴를 출력합니다."""
        show_menu()

    def play(self, selected_quizzes=None):
        """완료한 게임의 최고 기록과 히스토리를 갱신하고 저장합니다."""
        if selected_quizzes is None:
            selected_quizzes = self.quizzes

        correct_count = play_quizzes(selected_quizzes)

        if correct_count is not None:
            total = len(selected_quizzes)

            self.best_score = update_best_score(
                self.best_score,
                correct_count,
                total,
            )

            self.history.append(
                {
                    "played_at": datetime.now().astimezone().isoformat(
                        timespec="seconds"
                    ),
                    "correct_count": correct_count,
                    "total": total,
                    "score": round(correct_count / total * 100),
                }
            )

            self.save_state()

        return correct_count

    def play_selected(self):
        """문제 수를 입력받아 무작위로 선정한 뒤 플레이합니다."""
        if not self.quizzes:
            return self.play([])

        total = len(self.quizzes)

        print(f"\n등록된 퀴즈는 총 {total}개입니다.")
        question_count = input_int(
            f"몇 문제를 풀까요? (1~{total}): ",
            1,
            total,
        )

        selected_quizzes = random.sample(
            self.quizzes,
            k=question_count,
        )

        print(f"{question_count}문제를 무작위로 선정했습니다.")

        return self.play(selected_quizzes)

    def add_quiz(self):
        """퀴즈 등록을 완료하면 파일에 저장합니다."""
        add_quiz(self.quizzes)

        if self.save_state():
            print("추가한 퀴즈를 파일에 저장했습니다.")

    def delete_quiz(self):
        """삭제가 완료된 경우 변경된 목록을 저장합니다."""
        deleted = delete_quiz(self.quizzes)

        if not deleted:
            return False

        if self.state_path is None:
            print("파일 저장을 사용하지 않는 실행입니다.")
        elif self.save_state():
            print("삭제 결과를 파일에 저장했습니다.")
        else:
            print("현재 목록에서는 삭제됐지만 파일 저장은 완료되지 않았습니다.")

        return True

    def show_quiz_list(self):
        """현재 게임의 퀴즈 목록을 출력합니다."""
        show_quiz_list(self.quizzes)

    def show_best_score(self):
        """현재 게임의 최고 기록을 출력합니다."""
        show_best_score(self.best_score)

    def run(self):
        """종료를 선택할 때까지 메뉴를 반복합니다."""
        while True:
            self.show_menu()
            choice = input_int("선택: ", 1, 7)

            if choice == 1:
                self.play_selected()

            elif choice == 2:
                self.add_quiz()

            elif choice == 3:
                self.show_quiz_list()

            elif choice == 4:
                self.show_best_score()

            elif choice == 5:
                print("퀴즈 게임을 종료합니다.")
                break

            elif choice == 6:
                self.delete_quiz()
            elif choice == 7:
                self.show_history()

    def show_history(self):
        """최근 게임부터 기록을 출력합니다."""
        if not self.history:
            print("\n아직 완료한 게임 기록이 없습니다.")
            return

        print(f"\n게임 기록 (총 {len(self.history)}회, 최근 기록부터)")
        print("-" * 60)

        for number, record in enumerate(reversed(self.history), start=1):
            print(
                f"[{number}] {record['played_at']} | "
                f"{record['total']}문제 중 "
                f"{record['correct_count']}문제 정답 | "
                f"{record['score']}점"
            )


def main():
    """프로젝트 루트의 저장 파일을 사용하고 종료 시 저장을 시도합니다."""
    game = None

    try:
        state_path = Path(__file__).resolve().parent / "state.json"
        game = QuizGame(state_path=state_path)
        game.run()

    except KeyboardInterrupt:
        print("\n사용자가 실행을 중단했습니다. 종료합니다.")

    except EOFError:
        print("\n입력이 종료되어 프로그램을 종료합니다.")

    finally:
        if game is not None:
            if game.save_state():
                print("데이터를 저장했습니다.")


if __name__ == "__main__":
    main()