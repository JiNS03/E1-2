"""개별 퀴즈 한 문제를 표현하는 Quiz 클래스."""


class Quiz:
    CHOICE_COUNT = 4  # 선택지는 4개 고정, 정답은 1~4 번호로 관리

    def __init__(self, question, choices, answer, hint=None):
        if len(choices) != self.CHOICE_COUNT:
            raise ValueError(f"선택지는 {self.CHOICE_COUNT}개여야 합니다.")
        if not 1 <= answer <= self.CHOICE_COUNT:
            raise ValueError(f"정답 번호는 1~{self.CHOICE_COUNT} 이어야 합니다.")
        self.question = question
        self.choices = list(choices)
        self.answer = answer
        self.hint = hint or None  # 빈 문자열도 "힌트 없음"으로 통일

    def has_hint(self):
        return self.hint is not None

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

    def to_dict(self):
        """JSON 으로 저장할 수 있는 dict 로 변환한다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data):
        """state.json 의 dict 한 개를 검증해서 Quiz 객체로 만든다. 형식이 틀리면 ValueError."""
        if not isinstance(data, dict):
            raise ValueError("퀴즈 항목이 객체가 아닙니다")
        question = data["question"]
        choices = data["choices"]
        answer = data["answer"]
        if not isinstance(question, str) or not question.strip():
            raise ValueError("question 은 비어 있지 않은 문자열이어야 합니다")
        if not isinstance(choices, list) or not all(isinstance(c, str) for c in choices):
            raise ValueError("choices 는 문자열 리스트여야 합니다")
        if isinstance(answer, bool) or not isinstance(answer, int):
            raise ValueError("answer 는 정수여야 합니다")
        hint = data.get("hint")  # 힌트 기능 이전에 저장된 파일에는 hint 키가 없을 수 있다
        if hint is not None and not isinstance(hint, str):
            raise ValueError("hint 는 문자열 또는 null 이어야 합니다")
        return cls(question, choices, answer, hint)
