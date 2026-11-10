"""state.json 파일 저장/불러오기를 담당하는 StateStore 클래스.

파일 스키마 (UTF-8, JSON):
{
  "quizzes":     [{"question": str, "choices": [str x4], "answer": 1~4}, ...],
  "best_score":  0~100 정수 또는 null(아직 안 풀었음),
  "best_detail": {"correct": int, "total": int, "hints_used": int} 또는 null,
  "history":     [{"played_at": "YYYY-MM-DD HH:MM:SS", "total": int, "correct": int,
                   "hints_used": int, "score": int}, ...]
}
"""

import json
import os
from datetime import datetime
from pathlib import Path

from default_quizzes import get_default_quizzes
from quiz import Quiz

# 실행 위치(cwd)와 상관없이 항상 "프로젝트 루트/state.json" 을 사용한다.
STATE_PATH = Path(__file__).resolve().parent / "state.json"


class StateStore:
    def __init__(self, path=STATE_PATH):
        self.path = Path(path)

    @staticmethod
    def default_state():
        return {
            "quizzes": get_default_quizzes(),
            "best_score": None,
            "best_detail": None,
            "history": [],
        }

    # ------------------------------------------------------------ 불러오기
    def load(self):
        """(state, 안내 메시지, 복구 저장 필요 여부) 를 반환한다. 어떤 경우에도 예외를 올리지 않는다."""
        if not self.path.exists():
            return self.default_state(), "📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.", False
        try:
            with open(self.path, encoding="utf-8") as file:
                raw = json.load(file)
            state = self.parse(raw)
        except (ValueError, TypeError, KeyError) as error:
            # JSONDecodeError / UnicodeDecodeError 도 ValueError 의 하위 클래스
            backup = self.backup_broken_file()
            message = (
                f"⚠️ state.json 이 손상되어 기본 퀴즈 데이터로 복구합니다. ({type(error).__name__}: {error})"
            )
            if backup:
                message += f"\n   손상된 파일은 {backup.name} 으로 백업했습니다."
            return self.default_state(), message, True
        except OSError as error:
            message = f"⚠️ state.json 을 읽을 수 없어 기본 퀴즈로 시작합니다. ({error.strerror})"
            return self.default_state(), message, False
        best = "-" if state["best_score"] is None else f"{state['best_score']}점"
        message = f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(state['quizzes'])}개, 최고점수 {best})"
        return state, message, False

    @staticmethod
    def parse(raw):
        """JSON 에서 읽은 dict 를 검증하고 Quiz 객체로 변환한다. 형식이 틀리면 ValueError."""
        if not isinstance(raw, dict):
            raise ValueError("최상위 값이 객체({})가 아닙니다")
        if not isinstance(raw["quizzes"], list):
            raise ValueError("quizzes 가 리스트가 아닙니다")
        quizzes = [Quiz.from_dict(item) for item in raw["quizzes"]]

        best_score = raw.get("best_score")
        best_detail = raw.get("best_detail")
        if best_score is not None:
            if isinstance(best_score, bool) or not isinstance(best_score, int) or not 0 <= best_score <= 100:
                raise ValueError("best_score 는 0~100 정수 또는 null 이어야 합니다")
            if not isinstance(best_detail, dict) or not all(
                isinstance(best_detail.get(key), int) for key in ("correct", "total")
            ):
                raise ValueError("best_detail 형식이 올바르지 않습니다")
        else:
            best_detail = None

        history = raw.get("history", [])  # 히스토리 기능 이전 파일에는 키가 없을 수 있다
        record_keys = ("played_at", "total", "correct", "hints_used", "score")
        if not isinstance(history, list) or not all(
            isinstance(record, dict) and all(key in record for key in record_keys)
            for record in history
        ):
            raise ValueError("history 형식이 올바르지 않습니다")
        return {
            "quizzes": quizzes,
            "best_score": best_score,
            "best_detail": best_detail,
            "history": history,
        }

    def backup_broken_file(self):
        """손상된 파일을 state.broken-<시각>.json 으로 옮겨 둔다(원인 분석용)."""
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = self.path.with_name(f"state.broken-{stamp}.json")
        try:
            os.replace(self.path, backup)
            return backup
        except OSError:
            return None

    # ------------------------------------------------------------ 저장
    def save(self, quizzes, best_score, best_detail, history):
        """상태를 state.json 에 저장한다. 성공하면 True, 쓰기 오류면 안내 후 False."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in quizzes],
            "best_score": best_score,
            "best_detail": best_detail,
            "history": history,
        }
        temp_path = self.path.with_name(self.path.name + ".tmp")
        try:
            # 임시 파일에 다 쓴 뒤 교체 → 저장 도중 종료돼도 기존 파일이 깨지지 않는다.
            with open(temp_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
                file.write("\n")
            os.replace(temp_path, self.path)
            return True
        except OSError as error:
            print(f"⚠️ state.json 저장에 실패했습니다. ({error.strerror})")
            return False
