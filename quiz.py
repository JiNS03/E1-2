"""개별 퀴즈 한 문제를 표현하는 Quiz 클래스."""


class Quiz:
    CHOICE_COUNT = 4  # 선택지는 4개 고정, 정답은 1~4 번호로 관리

    def __init__(self, question, choices, answer):
        if len(choices) != self.CHOICE_COUNT:
            raise ValueError(f"선택지는 {self.CHOICE_COUNT}개여야 합니다.")
        if not 1 <= answer <= self.CHOICE_COUNT:
            raise ValueError(f"정답 번호는 1~{self.CHOICE_COUNT} 이어야 합니다.")
        self.question = question
        self.choices = list(choices)
        self.answer = answer

    def display(self, number):
        """문제 번호와 함께 문제/선택지를 출력한다."""
        print(f"[문제 {number}]")
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f"  {index}. {choice}")
        print()

    def is_correct(self, user_answer):
        """사용자가 고른 번호가 정답인지 확인한다."""
        return user_answer == self.answer

    def correct_choice(self):
        """정답 번호에 해당하는 선택지 문자열."""
        return self.choices[self.answer - 1]
