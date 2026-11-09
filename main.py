class Quiz:
    """문제 하나의 데이터와 동작을 관리합니다."""

    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

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
        ),
    ]

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
    print("현재는 실행 중에만 유지되며, 파일 저장은 추후 구현합니다.")

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
    print("=" * 40)


class QuizGame:
    """게임 상태와 메뉴 진행을 관리합니다."""

    def __init__(self):
        self.quizzes = create_default_quizzes()
        self.best_score = None

    def show_menu(self):
        """메뉴를 출력합니다."""
        show_menu()

    def play(self):
        """게임을 진행하고, 완료한 결과로 최고 기록을 갱신합니다."""
        correct_count = play_quizzes(self.quizzes)

        if correct_count is not None:
            self.best_score = update_best_score(
                self.best_score,
                correct_count,
                len(self.quizzes),
            )

        return correct_count

    def add_quiz(self):
        """현재 게임의 퀴즈 목록에 새 문제를 등록합니다."""
        add_quiz(self.quizzes)

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
            choice = input_int("선택: ", 1, 5)

            if choice == 1:
                self.play()

            elif choice == 2:
                self.add_quiz()

            elif choice == 3:
                self.show_quiz_list()

            elif choice == 4:
                self.show_best_score()

            else:
                print("퀴즈 게임을 종료합니다.")
                break


def main():
    """게임 객체를 만들고, 입력 중단 시 안내 후 종료합니다."""
    try:
        game = QuizGame()
        game.run()
    except KeyboardInterrupt:
        print("\n사용자가 실행을 중단했습니다. 종료합니다.")
    except EOFError:
        print("\n입력이 종료되어 프로그램을 종료합니다.")


if __name__ == "__main__":
    main()