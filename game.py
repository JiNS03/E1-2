"""퀴즈 게임 전체 흐름(메뉴, 풀기/추가/목록/점수, 종료)을 관리하는 QuizGame 클래스."""

from default_quizzes import get_default_quizzes
from input_utils import read_int, read_text
from quiz import Quiz

LINE = "=" * 40
THIN_LINE = "-" * 40


class QuizGame:
    def __init__(self):
        # 속성: 게임 상태
        self.quizzes = get_default_quizzes()
        self.best_score = None  # 아직 한 번도 풀지 않았으면 None
        self.best_detail = None  # {"correct": 정답 수, "total": 문제 수}
        self.running = True
        # 메뉴 번호 → (이름, 실행할 메서드). 메뉴 추가 시 이 표만 고치면 된다.
        self.menu = [
            ("퀴즈 풀기", self.play_quiz),
            ("퀴즈 추가", self.add_quiz),
            ("퀴즈 목록", self.list_quizzes),
            ("점수 확인", self.show_score),
            ("종료", self.quit),
        ]

    # ------------------------------------------------------------ 메인 루프
    def run(self):
        """메인 루프. Ctrl+C / 입력 종료(EOF)가 와도 비정상 종료하지 않는다."""
        self.print_title()
        try:
            while self.running:
                self.show_menu()
                choice = read_int("선택: ", 1, len(self.menu))
                self.handle_menu(choice)
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 입력이 중단되어 프로그램을 안전하게 종료합니다.")

    def print_title(self):
        print(LINE)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print(LINE)

    def show_menu(self):
        print()
        for number, (name, _) in enumerate(self.menu, start=1):
            print(f"{number}. {name}")
        print(LINE)

    def handle_menu(self, choice):
        _, action = self.menu[choice - 1]
        action()

    # ------------------------------------------------------------ 퀴즈 풀기
    def play_quiz(self):
        """저장된 퀴즈를 출제하고, 끝나면 결과를 보여준다."""
        if not self.has_quizzes():
            return
        total = len(self.quizzes)
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")
        correct = 0
        for number, quiz in enumerate(self.quizzes, start=1):
            if self.ask_question(number, quiz):
                correct += 1
        self.show_result(correct, total)

    def ask_question(self, number, quiz):
        """한 문제를 출제하고 정답이면 True 를 반환한다."""
        print("\n" + THIN_LINE)
        quiz.display(number)
        answer = read_int(f"정답 입력 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT)
        if quiz.is_correct(answer):
            print("✅ 정답입니다!")
            return True
        print(f"❌ 오답입니다. 정답은 {quiz.answer}번 '{quiz.correct_choice()}' 입니다.")
        return False

    @staticmethod
    def calculate_score(correct, total):
        """정답 수를 100점 만점 점수로 환산한다."""
        return round(correct / total * 100)

    def show_result(self, correct, total):
        """정답 수와 점수를 출력하고 최고 점수를 갱신한다."""
        score = self.calculate_score(correct, total)
        print("\n" + LINE)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if self.update_best_score(score, correct, total):
            print("🎉 새로운 최고 점수입니다!")
        else:
            print(f"   (최고 점수: {self.best_score}점)")
        print(LINE)
        return score

    # ------------------------------------------------------------ 퀴즈 추가 / 목록
    def add_quiz(self):
        """문제, 선택지 4개, 정답 번호를 입력받아 새 퀴즈를 등록한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = read_text("문제를 입력하세요: ")
        choices = self.read_choices()
        answer = read_int(f"정답 번호 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT)
        self.quizzes.append(Quiz(question, choices, answer))
        print(f"\n✅ 퀴즈가 추가되었습니다! (현재 {len(self.quizzes)}개)")

    @staticmethod
    def read_choices():
        """중복 없는 선택지 4개를 입력받는다."""
        choices = []
        while len(choices) < Quiz.CHOICE_COUNT:
            choice = read_text(f"선택지 {len(choices) + 1}: ")
            if choice in choices:
                print("⚠️ 이미 입력한 선택지입니다. 다른 내용을 입력하세요.")
                continue
            choices.append(choice)
        return choices

    def list_quizzes(self):
        """등록된 퀴즈의 문제 목록을 번호와 함께 출력한다."""
        if not self.has_quizzes():
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print(THIN_LINE)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print(THIN_LINE)

    def has_quizzes(self):
        """퀴즈가 하나도 없으면 안내 후 False."""
        if self.quizzes:
            return True
        print("\n📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
        return False

    # ------------------------------------------------------------ 점수
    def update_best_score(self, score, correct, total):
        """이번 점수가 최고 점수보다 높으면 갱신하고 True 를 반환한다."""
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.best_detail = {"correct": correct, "total": total}
            return True
        return False

    def show_score(self):
        """최고 점수를 출력한다. 아직 풀지 않았으면 안내한다."""
        if self.best_score is None:
            print("\n📭 아직 퀴즈를 풀지 않았습니다. 1번 메뉴에서 퀴즈를 풀어 보세요!")
            return
        detail = self.best_detail
        print(
            f"\n🏆 최고 점수: {self.best_score}점 "
            f"({detail['total']}문제 중 {detail['correct']}문제 정답)"
        )

    # ------------------------------------------------------------ 종료
    def quit(self):
        print("\n👋 게임을 종료합니다. 다음에 또 만나요!")
        self.running = False
