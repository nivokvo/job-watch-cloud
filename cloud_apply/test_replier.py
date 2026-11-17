"""Предохранители автоответа: python3 test_replier.py. Сеть и Claude подменены."""
import os
os.environ.setdefault("ROUTINE_KEY", "x")
import replier
import sys, tempfile
sys.path.insert(0, os.path.expanduser("~/job-hunt/code"))
try:  # общая память crm.py есть только на маке; в тестах её журнал и кэши временные
    import crm
    crm.JOURNAL, crm.DIR = tempfile.mktemp(), tempfile.mkdtemp()
except ImportError:
    crm = None

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
assert not crm or crm.state("1")["due"] == "2026-11-12T17:00"            # и срок созвона ушёл в журнал (напоминание, пульт)
mem.clear()
if crm:
    open(crm.JOURNAL, "w").write("")
for _ in range(replier.AUTO_PER_CHAT):
    assert run({})["auto"]
assert not run({})["auto"]                                               # четвёртый свой ответ подряд в одном чате

if crm:  # город: один разговор в двух каналах знает одно и то же
    crm.write(key="9", who="closed", need="ушёл в Telegram")
    crm.write(key="9", link="tg5")
    crm.write(key="tg5", event="созвонились, отправил условия 999 ₽")
    assert crm.group("tg5") == {"9", "tg5"} == crm.group("9") and crm.moved() == {"9"}
    seen = []
    replier.ask = lambda text, system=None: seen.append(text) or ({"ok": True} if system else {**GOOD})
    mem.clear()
    c = replier.draft({**T, "chat": "tg5"}, "контекст", "b", "q")
    assert "999 ₽" in seen[0] and "ЖУРНАЛ" in seen[0]                  # журнал из другого канала в промпте
    assert not c["auto"] and c["handoff"]                                # в журнале разговор закрыт: руль у Глеба
    assert any("передал Глебу" in (j.get("event") or "") for j in crm.rows())  # бот сам записал это в журнал
    open(crm.JOURNAL, "w").write("")
    crm.write(key="3", link="tg8")
    mem.clear()
    mem["handoff"] = {"3": 1}
    assert not replier.draft({**T, "chat": "tg8"}, "к", "b", "q")["auto"]  # руль у Глеба на rabota.by = и в Telegram
    assert replier.draft({**T, "chat": "tg77"}, "к", "b", "q")["auto"]   # чужой разговор это не задевает
    crm.write(key="4", who="you", need="созвон", due="2026-11-17T15:00")
    import datetime as dt
    assert [j["key"] for j in crm.due_soon(dt.datetime(2026, 11, 17, 13, 0))] == ["4"] and not crm.due_soon(dt.datetime(2026, 11, 17, 10, 0))
    replier.ask = ask

# кнопка «Отправить»: шлём, только прочитав чат целиком
sent, job = [], {"chat": "7", "vacancy": 5, "name": "v", "company": "c", "status": "approved", "basis": "b", "reply": "Да"}
replier.send = sent.append
replier.api = lambda path, body=None: {"jobs": [job]} if path == "/chat/jobs" else posted.append((path, body)) or {}
replier.run_apply = lambda *a, **k: {"ok": False}
replier.jobs()
assert not sent and ("/chat/done", {"chat": "7", "ok": False}) in posted  # чат не прочитался: не шлём
replier.run_apply = lambda *a, **k: {"ok": True, "messages": [{"mine": False, "text": "Удалёнка?", "id": "b"}]}
replier.jobs()
assert sent == [job]                                                     # прочитали, нового нет: шлём
posted.clear()
replier.run_apply = lambda *a, **k: {"ok": True, "messages": [{"mine": False, "text": "Удалёнка?", "id": "b"}, {"mine": True, "text": "Да", "id": "c"}]}
replier.jobs()
assert sent == [job] and ("/chat/done", {"chat": "7", "ok": True}) in posted  # ответ уже в чате («не ушло» при ушедшем): дубль не шлём

assert not replier.public_url("http://127.0.0.1:37701/") and not replier.public_url("http://localhost/x")  # ссылки работодателя на мак не открываем
replier.api = api
mem.clear()
assert not replier.draft(dict(T), "к\n\nСТРАНИЦА http://x:\nтекст", "b", "q")["auto"]  # чужая страница в промпте: сам не шлём

if crm:  # id вакансии вместо id чата в журнале: пишется под чатом
    import json
    json.dump({"1": {"vacancy": 555, "chat": 777}}, open(os.path.join(crm.DIR, "negotiations.json"), "w"))
    crm.write(key="555", who="you", need="x")
    assert crm.state("777")["need"] == "x"
print("ok")
