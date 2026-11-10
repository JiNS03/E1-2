"""기본 퀴즈 데이터: 주제 = 개발자 작업실 기초 (터미널·Docker·Git·Python).

state.json 이 없거나 손상되었을 때 이 데이터로 게임을 시작/복구한다.
"""

from quiz import Quiz


def get_default_quizzes():
    """기본 퀴즈를 Quiz 인스턴스 리스트로 만들어 반환한다 (매번 새 객체)."""
    return [
        Quiz(
            "리눅스에서 현재 작업 중인 디렉터리의 절대 경로를 출력하는 명령어는?",
            ["ls", "pwd", "cd", "whoami"],
            2,
            "print working directory 의 약자입니다.",
        ),
        Quiz(
            "파일 권한 755 를 기호로 바르게 나타낸 것은?",
            ["rwxr-xr-x", "rw-r--r--", "rwxrwxrwx", "rwx------"],
            1,
            "r=4, w=2, x=1 을 더해 자리별로 계산하세요.",
        ),
        Quiz(
            "docker run -p 8080:80 nginx 에서 8080 이 의미하는 것은?",
            ["컨테이너 내부 포트", "호스트(내 PC) 포트", "이미지 버전", "컨테이너 ID"],
            2,
            "-p 호스트포트:컨테이너포트 순서입니다.",
        ),
        Quiz(
            "컨테이너를 삭제해도 데이터를 유지하기 위해 Docker 가 관리하는 저장 공간은?",
            ["이미지 레이어", "볼륨(Volume)", "포트 매핑", "환경 변수"],
            2,
            "docker volume create 로 만들 수 있습니다.",
        ),
        Quiz(
            "원격 저장소의 변경사항을 가져와 현재 브랜치에 병합하는 Git 명령어는?",
            ["git push", "git clone", "git pull", "git commit"],
            3,
            "fetch + merge 를 한 번에 합니다.",
        ),
        Quiz(
            "Python 에서 키(key)와 값(value)의 쌍으로 데이터를 저장하는 자료형은?",
            ["list", "tuple", "str", "dict"],
            4,
            "중괄호 {} 로 만듭니다.",
        ),
        Quiz(
            "Python 에서 json.loads() 가 잘못된 JSON 문자열을 만났을 때 발생하는 예외는?",
            ["KeyError", "json.JSONDecodeError", "IndexError", "ZeroDivisionError"],
            2,
            "JSON 'Decode' 실패를 뜻하는 이름입니다.",
        ),
    ]
