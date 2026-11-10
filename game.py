"""퀴즈 게임 전체 흐름(메뉴, 기능 선택, 종료)을 관리한다."""

from default_quizzes import get_default_quizzes
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
        self.quizzes = get_default_quizzes()
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
        if choice == 1:
            self.play_quiz()
        elif choice == len(self.MENU):
            self.quit()
        else:
            print(f"\n🚧 '{self.MENU[choice - 1]}' 기능은 준비 중입니다.")

    def play_quiz(self):
        """저장된 퀴즈를 순서대로 출제하고 정답 수를 센다."""
        if not self.quizzes:
            print("\n📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return
        total = len(self.quizzes)
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")
        correct = 0
        for number, quiz in enumerate(self.quizzes, start=1):
            print("\n" + "-" * 40)
            quiz.display(number)
            answer = read_int(f"정답 입력 (1-{quiz.CHOICE_COUNT}): ", 1, quiz.CHOICE_COUNT)
            if quiz.is_correct(answer):
                correct += 1
                print("✅ 정답입니다!")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번 '{quiz.correct_choice()}' 입니다.")

    def quit(self):
        print("\n👋 게임을 종료합니다. 다음에 또 만나요!")
        self.running = False
