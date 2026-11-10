"""퀴즈 게임 전체 흐름(메뉴, 기능 선택, 종료)을 관리한다."""

from input_utils import read_int

LINE = "=" * 40


class QuizGame:
    MENU = (
        "퀴즈 풀기",
        "퀴즈 추가",
        "퀴즈 목록",
        "점수 확인",
        "종료",
    )

    def __init__(self):
        self.running = True

    def run(self):
        """메인 루프. Ctrl+C / 입력 종료(EOF)가 와도 비정상 종료하지 않는다."""
        self.print_title()
        try:
            while self.running:
                self.show_menu()
                choice = read_int("선택: ", 1, len(self.MENU))
                self.handle_menu(choice)
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 입력이 중단되어 프로그램을 안전하게 종료합니다.")

    def print_title(self):
        print(LINE)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print(LINE)

    def show_menu(self):
        print()
        for number, name in enumerate(self.MENU, start=1):
            print(f"{number}. {name}")
        print(LINE)

    def handle_menu(self, choice):
        if choice == len(self.MENU):
            self.quit()
        else:
            print(f"\n🚧 '{self.MENU[choice - 1]}' 기능은 준비 중입니다.")

    def quit(self):
        print("\n👋 게임을 종료합니다. 다음에 또 만나요!")
        self.running = False
