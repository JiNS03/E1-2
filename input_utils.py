"""사용자 입력을 받고 검증하는 공통 함수 모음.

모든 함수는 입력 앞뒤 공백을 제거한 뒤 검사하고, 잘못된 입력이면
안내 메시지를 출력한 다음 다시 입력을 받는다(재입력 흐름).
KeyboardInterrupt / EOFError 는 여기서 삼키지 않고 호출한 쪽(QuizGame.run)으로
그대로 올려 보내서, 한 곳에서 "저장 후 안전 종료"를 처리한다.
"""


def parse_int(raw, low, high):
    """공백 제거된 문자열을 검사해 (정수, None) 또는 (None, 안내 메시지) 를 반환한다."""
    if raw == "":
        return None, f"⚠️ 입력이 비어 있습니다. {low}-{high} 사이의 숫자를 입력하세요."
    try:
        value = int(raw)
    except ValueError:
        return None, f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요."
    if not low <= value <= high:
        return None, f"⚠️ 범위를 벗어났습니다. {low}-{high} 사이의 숫자를 입력하세요."
    return value, None


def read_int(prompt, low, high):
    """low~high 범위의 정수를 입력받아 반환한다."""
    while True:
        value, error = parse_int(input(prompt).strip(), low, high)
        if error is None:
            return value
        print(error)


def read_text(prompt):
    """비어 있지 않은 문자열을 입력받아 반환한다."""
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print("⚠️ 빈 값은 입력할 수 없습니다. 다시 입력하세요.")


def read_yes_no(prompt):
    """y/n 을 입력받아 True/False 로 반환한다."""
    while True:
        raw = input(prompt).strip().lower()
        if raw in ("y", "yes", "ㅛ"):
            return True
        if raw in ("n", "no", "ㅜ"):
            return False
        print("⚠️ y 또는 n 으로 입력하세요.")
