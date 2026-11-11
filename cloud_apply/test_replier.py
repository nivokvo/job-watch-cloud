"""Предохранители автоответа: python3 test_replier.py. Сеть и Claude подменены."""
import os
os.environ.setdefault("ROUTINE_KEY", "x")
import replier

mem, posted = {}, []
answer = {}


def api(path, body=None):
    if path == "/chat/mem":
        if body:
            mem.update(body)
        return dict(mem)
    posted.append((path, body))
    return {}


def ask(text, system=None):
    return {"ok": answer.get("critic", True), "why": "факт не подтверждён"} if system else dict(answer["opus"])


replier.api, replier.ask = api, ask
T = {"chat": "1", "vacancy": 5, "name": "v", "company": "c"}
GOOD = {"kind": "question", "reply": "Да, удалённо из Минска.", "auto": True, "attention": [], "need": "", "manual": "", "meeting": ""}


def run(opus, critic=True, **kw):
    answer.update(opus={**GOOD, **opus}, critic=critic)
    return replier.draft(dict(T), "контекст", "b", "q", **kw)


assert run({})["auto"]                                                   # обычный вопрос, проверка пройдена: шлём сами
assert mem["autos"] == {"1": 1}
assert not run({}, critic=False)["auto"]                                 # проверяющий против: карточка
assert not run({"auto": False})["auto"]                                  # Opus не уверен
assert not run({"need": "Есть ли ИП?", "reply": ""})["auto"]             # не хватает факта: вопрос Глебу
assert not run({"attention": ["просят паспорт"]})["auto"]
assert not run({"manual": "заполнить форму"})["auto"]
assert not run({"reply": "я" * 701})["auto"]
assert not run({}, auto_ok=False)["auto"]                                # Telegram: только кнопка
assert not run({}, edit="короче")["auto"]                                # обычные правки: снова карточка
assert run({}, edit="ИП нет", fact=True)["auto"]                         # ответ на вопрос бота: можно слать
for kind in ("invite", "offer", "test", "scam"):                         # позвали: руль у Глеба, и дальше тоже
    mem.clear()
    c = run({"kind": kind})
    assert not c["auto"] and c["handoff"] and mem["handoff"] == {"1": 1}
    assert not run({})["auto"]
mem.clear()
assert not run({}, invited=True)["auto"]                                 # статус отклика «приглашение»
mem.clear()
assert not run({"meeting": "2026-11-12T17:00:00+03:00"})["auto"]         # назначают время
mem.clear()
for _ in range(replier.AUTO_PER_CHAT):
    assert run({})["auto"]
assert not run({})["auto"]                                               # четвёртый свой ответ подряд в одном чате
print("ok")
