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


def run_menu():
    """선택한 메뉴에 따라 동작하고, 종료 전까지 반복합니다."""
    while True:
        show_menu()
        choice = input_int("선택: ", 1, 5)

        if choice == 1:
            print("퀴즈 풀기 기능은 준비 중입니다.")
        elif choice == 2:
            print("퀴즈 추가 기능은 준비 중입니다.")
        elif choice == 3:
            print("퀴즈 목록 기능은 준비 중입니다.")
        elif choice == 4:
            print("점수 확인 기능은 준비 중입니다.")
        else:
            print("퀴즈 게임을 종료합니다.")
            break


def main():
    """프로그램을 시작하고, 입력 중단 시 안내 후 종료합니다."""
    try:
        run_menu()
    except KeyboardInterrupt:
        print("\n사용자가 실행을 중단했습니다. 종료합니다.")
    except EOFError:
        print("\n입력이 종료되어 프로그램을 종료합니다.")


if __name__ == "__main__":
    main()