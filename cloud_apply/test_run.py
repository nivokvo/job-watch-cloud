"""Облачный цикл откликов: python3 test_run.py. Воркер, Opus и браузер подменены."""
import os, sys
os.environ.setdefault("ROUTINE_KEY", "x")
sys.argv = ["run.py"]
import run

applied, verdict = [], []
replies = iter([{"ok": True}, {"ok": False, "reason": "captcha"}, {"ok": True}])
queue = [{"id": i, "name": "v", "sal": ""} for i in (1, 2, 3, 4)]


def curl(path, body=None):
    if path == "/queue":
        return [dict(v, manager="Анна") for v in queue]
    if path == "/cloudstat":
        return {"applied_today": 0, "mac_today": 0}
    verdict.append(body)
    return {"done": []}


run.curl, run.time.sleep = curl, lambda s: None
run.score = lambda vs: {v["id"]: {"score": 9, "letter": "письмо", "resume": run.RESUMES[0]} for v in vs}
run.apply = lambda v, sc: applied.append(v["id"]) or next(replies)
run.main()
assert applied == [1, 2], applied                                    # после капчи дальше не откликаемся
assert [r["applied"] for r in verdict[0]] == [True, False]             # вердикт ушёл по обеим, остальные ждут следующего прогона
assert verdict[0][1]["apply_reason"] == "captcha"

applied.clear(), verdict.clear()
replies = iter([{"ok": True}] * 9)
run.CLOUD_PER_DAY = 3
run.main()
assert applied == [1, 2, 3], applied                                 # дневной лимит облака
assert verdict[0][3]["apply_reason"] == "дневной лимит облачных откликов"
print("ok")
