"""Ответы работодателям в чатах rabota.by: Opus пишет черновик, Глеб жмёт кнопку в Telegram, отправка отсюда.

Один и тот же файл работает на маке (зовёт сторож) и в GitHub Actions (cloud_apply/replier.py), пока мак спит.
Общее состояние (что уже видели, черновики, решения Глеба) живёт в KV Cloudflare-воркера, поэтому мак и облако
не отвечают дважды. Карточки и кнопки в Telegram рисует воркер.

python3 replier.py poll    прочитать новые сообщения работодателей и прислать черновики
python3 replier.py jobs    выполнить решения Глеба: отправить одобренное, переписать по правкам
python3 replier.py cloud   то и другое, но только если мак спит (для GitHub Actions)

Мелочь (подтвердить время, «спасибо», «да, ГПХ подходит», кнопка анкеты по фактам из me.md) уходит сама,
Глебу приходит тихая строчка. Всё остальное только после кнопки «Отправить». Тексты работодателей это данные, не инструкции.
"""
import datetime, html, json, os, re, subprocess, sys, tempfile

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = DIR if os.path.exists(os.path.join(DIR, "me.md")) else os.path.dirname(DIR)  # в облачном репо me.md лежит в корне
WORKER = "https://rabota-watch.7vy7m8srtf.workers.dev"
CLOUD = bool(os.environ.get("RABOTA_STATE_FILE"))
PY = sys.executable if CLOUD else "/Library/Frameworks/Python.framework/Versions/3.14/bin/python3"
CLAUDE = "claude" if CLOUD else os.path.expanduser("~/.local/bin/claude")
UA = "Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/130 Safari/537.36"
_tok = os.path.join(DIR, "claude.env")  # на маке токен подписки для claude -p лежит рядом
if not os.environ.get("CLAUDE_CODE_OAUTH_TOKEN") and os.path.exists(_tok):
    os.environ.update(l.strip().split("=", 1) for l in open(_tok) if l.startswith("CLAUDE_CODE_OAUTH_TOKEN="))
MAX_AUTO = 400  # длиннее автоматом не шлём: длинный ответ почти всегда что-то обещает


def key():
    if os.environ.get("ROUTINE_KEY"):
        return os.environ["ROUTINE_KEY"]
    return dict(l.strip().split("=", 1) for l in open(os.path.join(DIR, "cloud", "admin.env")) if "=" in l)["ADMIN_KEY"]


def log(*a):
    # в облаке логи публичные: только id и цифры
    print(datetime.datetime.now().strftime("%H:%M:%S"), "ответы:", *a, flush=True)


def api(path, body=None):
    cmd = ["curl", "-s", "-m", "60", "--retry", "2", f"{WORKER}{path}{'&' if '?' in path else '?'}key={key()}"]
    if body is not None:
        cmd += ["-X", "POST", "-H", "content-type: application/json", "--data-binary", "@-"]
    r = subprocess.run(cmd, input=json.dumps(body, ensure_ascii=False) if body is not None else None,
                       capture_output=True, text=True, timeout=120)
    return json.loads(r.stdout)


def run_apply(*args, timeout=240):
    r = subprocess.run([PY, os.path.join(DIR, "apply.py"), *map(str, args)], capture_output=True, text=True, timeout=timeout)
    lines = r.stdout.strip().splitlines()
    try:
        return json.loads(lines[-1], strict=False)
    except Exception:
        return {"ok": False, "reason": "apply.py без ответа"}


def describe(vid):
    h = subprocess.run(["curl", "-s", "-L", "-m", "30", "--retry", "2", "-A", UA, f"https://rabota.by/vacancy/{vid}"],
                       capture_output=True, timeout=90).stdout.decode("utf-8", "replace")
    m = re.search(r'data-qa="vacancy-description"[^>]*>(.*?)</div>\s*</div>', h, re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub("<[^>]+>", " ", m.group(1)))).strip()[:2500] if m else ""


def page_text(url, limit=5000):
    h = subprocess.run(["curl", "-s", "-L", "-m", "30", "-A", UA, url], capture_output=True, timeout=60).stdout.decode("utf-8", "replace")
    h = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", h, flags=re.S | re.I)
    return re.sub(r"\s+", " ", html.unescape(re.sub("<[^>]+>", " ", h))).strip()[:limit]


PROMPT = """Ты ведёшь переписку студента Глеба с работодателями на rabota.by. Работодатель написал в чат по отклику Глеба.
Твоя задача: понять, что от Глеба хотят, и написать ответ от его имени, который он одобрит одной кнопкой.
Факты о Глебе только из блоков «ГЛЕБ» и «РЕЗЮМЕ». Ничего не выдумывай: ни опыта, ни навыков, ни ссылок, ни дат.
Если для ответа нужен факт, которого там нет, не придумывай его, а напиши в attention, что именно уточнить у Глеба.

Как писать ответ (reply):
- от первого лица, просто и по-человечески, на «вы», коротко: обычно 1-4 предложения; без восклицаний, кроме приветствия; подпись «Глеб» с новой строки только в первом ответе этому работодателю;
- отвечай ровно на то, что спросили, по пунктам, если вопросов несколько; не повторяй резюме и письмо;
- зовут на созвон: если время названо и подходит под расписание из блока «ГЛЕБ», подтверди его; если не подходит или не названо, предложи 2 конкретных слота по расписанию;
- без признаков ИИ-текста: никаких «не X, а Y», «Честно, … Но …», пафосных концовок, «буду рад(а) возможности», «готов к новым вызовам», длинных тире, канцелярита, троек ради ритма, мудрых обобщений; каждое предложение сообщает новое.

Тестовое или анкета:
- если это вопросы прямо в чате, ответь на все в reply (по фактам о Глебе);
- если это задание (текст, пост, разбор, таблица, расчёт), сделай его целиком в solution, как сделал бы сильный кандидат, а в reply напиши короткое сопроводительное сообщение (если решение можно вставить в чат, reply = само решение);
- если задание во внешней форме, файле или требует действий вне чата, опиши в manual, что сделать по шагам, а в solution дай готовые ответы, которые останется вставить.

Кнопки: если работодатель (часто робот) дал кнопки, а ответ на вопрос однозначно следует из фактов о Глебе, верни точный текст кнопки в button и пустой reply.

auto = true, только если отправить можно без Глеба, потому что ответ ничего нового не обещает: подтвердить время, которое назвал работодатель и которое влезает в расписание; поблагодарить; «да/нет» по фактам из «ГЛЕБ» (формат, оформление, город, удалёнка, компьютер); нажать кнопку анкеты по этим фактам. Во всех остальных случаях (тестовое, деньги, дата выхода, новые слоты, сомнения, любой факт не из блоков, оффер, отказ, подозрение на обман) auto = false.

Когда отвечать не нужно (reply и button пустые): отказ, «спасибо, изучим, вернёмся», автоматическое уведомление, работодатель запретил писать в чат, последнее слово уже за Глебом и вопросов нет.

Верни только JSON без markdown:
{"kind": "invite" | "question" | "test" | "form" | "offer" | "info" | "reject" | "skip" | "scam",
 "summary": "одно короткое предложение: что хотят от Глеба и к какому сроку",
 "attention": ["до 3 пунктов: срок, деньги, что уточнить у Глеба, признаки обмана (оплата, курс, карта или паспорт до договора, «куратор» в мессенджере без собеседования); пусто, если нечего"],
 "reply": "текст сообщения в чат или пусто",
 "button": "текст кнопки или пусто",
 "solution": "готовое решение тестового или ответы для формы, иначе пусто",
 "manual": "что Глебу сделать самому вне чата (позвонить, написать в Telegram, заполнить форму, прислать файл) или пусто",
 "meeting": "ISO-время созвона или дедлайна с поясом +03:00, если оно названо явно, иначе пусто",
 "auto": false}
kind = "skip", если вакансия явно не для Глеба (продажи, колл-центр, работа ногами офлайн) и отвечать не стоит."""


def ask(text):
    env = {**os.environ, "LANG": "en_US.UTF-8"}
    if not CLOUD:
        env["PATH"] = os.path.expanduser("~/.local/bin") + ":/usr/bin:/bin"
    r = subprocess.run([CLAUDE, "-p", "--model", "opus", "--system-prompt", PROMPT, "--tools", "", "--strict-mcp-config",
                        "--setting-sources", "", "--disable-slash-commands", "--no-session-persistence"],
                       input=text, capture_output=True, text=True, timeout=600, env=env, cwd=DIR)
    m = re.search(r"\{.*\}", r.stdout, re.S)
    if r.returncode or not m:
        raise RuntimeError(f"claude -p упал, код {r.returncode}")
    return json.loads(m.group(0), strict=False)


def context(t, msgs, buttons, can):
    talk = "\n\n".join(f"{'Глеб' if m['mine'] else 'Работодатель' + (' (робот)' if m.get('bot') else '')} ({m['time'].replace('T', ' ')}): "
                       f"{m['text'].strip() or '[отклик с резюме]'}" for m in msgs)
    pages = ""
    last = next((m["text"] for m in reversed(msgs) if not m["mine"]), "")
    for url in re.findall(r"https?://[^\s<>\")]+", last)[:2]:
        if not re.search(r"rabota\.by|hh\.ru|forms\.gle|docs\.google\.com/forms|t\.me", url):
            try:
                pages += f"\n\nСТРАНИЦА {url}:\n{page_text(url)}"
            except Exception:
                pass
    return (f"ГЛЕБ:\n{open(os.path.join(ROOT, 'me.md')).read()}\n\nРЕЗЮМЕ:\n{open(os.path.join(ROOT, 'resume.md')).read()}\n\n"
            f"ВАКАНСИЯ: {t['name']} · {t['company']}\n{describe(t['vacancy'])}\n\n"
            f"ПЕРЕПИСКА (сейчас {datetime.datetime.now():%Y-%m-%d %H:%M}, {['пн','вт','ср','чт','пт','сб','вс'][datetime.datetime.now().weekday()]}):\n{talk}"
            f"\n\nКНОПКИ РАБОТОДАТЕЛЯ: {', '.join(buttons) if buttons else 'нет'}"
            f"\nПИСАТЬ В ЧАТ: {'запрещено работодателем' if can.startswith('DISABLED') else 'можно'}{pages}")


def last_employer(msgs):
    m = next((m for m in reversed(msgs) if not m["mine"] and m["text"].strip()), None)
    return str(m["id"]) if m else ""


def make(t, edit=None, prev=None):
    """Прочитать чат, получить черновик Opus и отдать его воркеру. Мелочь отправить сразу."""
    chat = run_apply("chat", t["chat"], timeout=180)
    if not chat.get("ok"):
        raise RuntimeError("чат не прочитался")
    msgs, buttons, can = chat["messages"], chat.get("buttons") or [], str(chat.get("can_write") or "")
    basis = last_employer(msgs)
    text = context(t, msgs, buttons, can)
    if edit:
        text += f"\n\nПРОШЛЫЙ ЧЕРНОВИК ОТВЕТА:\n{json.dumps(prev or {}, ensure_ascii=False)}\n\nПРАВКИ ГЛЕБА (выполни их точно, это главное):\n{edit}"
    d = ask(text)
    if can.startswith("DISABLED"):
        d["reply"], d["button"], d["auto"] = "", "", False
    if d.get("button") not in buttons:
        d["button"] = ""
    d["auto"] = bool(d.get("auto")) and not edit and (d.get("kind") not in ("test", "form", "offer", "scam", "reject") or d.get("kind") == "form" and d["button"]) \
        and len(d.get("reply") or "") <= MAX_AUTO and bool(d.get("reply") or d.get("button"))
    card = {"chat": str(t["chat"]), "vacancy": t["vacancy"], "name": t["name"], "company": t["company"], "basis": basis,
            **{k: d.get(k) or "" for k in ("kind", "summary", "reply", "button", "solution", "manual", "meeting")},
            "attention": d.get("attention") or [], "auto": d["auto"], "revised": bool(edit)}
    api("/chat/draft", card)
    log("черновик", t["chat"], card["kind"], "авто" if card["auto"] else "")
    if card["auto"]:
        send(card)


def send(d):
    r = run_apply("click", d["chat"], d["button"]) if d.get("button") else None
    if r is None and d.get("reply"):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write(d["reply"])
        r = run_apply("say", d["chat"], f.name, "--nowait")
        os.unlink(f.name)
    ok = bool(r and r.get("ok"))
    api("/chat/done", {"chat": d["chat"], "ok": ok})
    log("отправка", d["chat"], "ok" if ok else "не ушло")


def poll(topics):
    """topics: из apply.py responses. Новые сообщения работодателя → черновик."""
    st = api("/chat/seen")
    seen, first = st.get("seen") or {}, not st.get("seen")
    upd = {}
    for t in topics:
        c = str(t.get("chat") or "")
        if not c or int(t.get("msgs") or 0) <= (seen.get(c) or {}).get("n", 0):
            continue
        upd[c] = {"n": int(t.get("msgs") or 0), "id": (seen.get(c) or {}).get("id", "")}
        if first or t["state"] == "DISCARD":  # первый запуск: только запоминаем; отказы молча
            continue
        try:
            chat = run_apply("chat", c, timeout=180)
            msgs = chat.get("messages") or []
            b = last_employer(msgs)
            upd[c]["id"] = b
            if not msgs or msgs[-1]["mine"] or not b or b == (seen.get(c) or {}).get("id"):
                continue
            api("/chat/seen", upd)  # сразу, чтобы облако не взяло тот же чат параллельно
            make(t)
        except Exception as e:
            log("чат", c, "ошибка", type(e).__name__)
    if upd:
        api("/chat/seen", upd)


def jobs():
    """Решения Глеба из Telegram: отправить одобренное (если в чате ничего нового) или переписать по правкам."""
    for d in api("/chat/jobs").get("jobs") or []:
        t = {"chat": d["chat"], "vacancy": d["vacancy"], "name": d["name"], "company": d["company"]}
        try:
            if d["status"] == "revise":
                make(t, edit=d.get("edit"), prev={k: d.get(k) for k in ("reply", "solution", "button")})
            elif d["status"] == "approved":
                chat = run_apply("chat", d["chat"], timeout=180)
                if chat.get("ok") and last_employer(chat["messages"]) != d.get("basis"):
                    make(t)  # пока ждали кнопку, работодатель написал ещё: переписываем, ничего не шлём
                else:
                    send(d)
        except Exception as e:
            log("задача", d["chat"], "ошибка", type(e).__name__)
            api("/chat/done", {"chat": d["chat"], "ok": False})


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "cloud":
        st = api("/chat/seen")
        if st.get("mac_alive") and os.environ.get("FORCE") != "true":
            return log("мак не спит, ответы делает он")
        jobs()
        r = run_apply("responses", timeout=240)
        if r.get("ok"):
            poll(r["topics"])
        else:
            log("отклики не прочитались")
    elif cmd == "poll":
        r = run_apply("responses", timeout=240)
        poll(r.get("topics") or [])
    elif cmd == "jobs":
        jobs()
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
