"""Облачный Opus для сторожа rabota.by: запускается из GitHub Actions, пока мак спит.

1. Забирает из Cloudflare-воркера вакансии, которые облако нашло и Gemini оценил на 5+.
2. Opus (Claude Code с токеном подписки) оценивает их по rubric.md и пишет письмо для 7+.
3. Для 7+ откликается через скрытый браузер с сессией rabota.by (не больше CLOUD_PER_DAY в день).
   Без письма не отправляет никогда, эти проверки в apply.py.
4. Отдаёт вердикт воркеру: тот правит карточку в Telegram, а мак после пробуждения не откликается повторно.
"""
import json, os, re, subprocess, sys, tempfile

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(DIR)
CLOUD = "https://rabota-watch.7vy7m8srtf.workers.dev"
KEY = os.environ["ROUTINE_KEY"]
MIN_SCORE = 7
CLOUD_PER_DAY = 7  # с 12.10: мак днём часто закрыт (пары), облако должно успевать за будним потоком
RESERVE_8 = 2  # последние слоты дня держим только для 8+, чтобы семёрки не съели место хорошей вакансии
TOTAL_PER_DAY = 10  # как APPLY_PER_DAY на маке
DRY = "--dry" in sys.argv or any(a.startswith("--vid=") for a in sys.argv)
RESUMES = ["Специалист по сбору и обработке данных (Python, Excel), удалённо", "Оператор ПК, оператор базы данных (удалённо)",
           "Контент-менеджер (наполнение сайта, карточки товаров), удалённо", "Ассистент менеджера маркетплейсов (Wildberries, Ozon)",
           "Аудитор, специалист по мониторингу цен и наличия (удалённо, подработка)"]
FORMAT = """

Верни только JSON-массив без markdown: [{"id": число, "score": 0-10, "why": "до 15 слов почему", "how": "до 20 слов как автоматизировать", "you": "до 15 слов что останется руками"}]
Только для вакансий с оценкой 7+ добавь в объект поля "resume" и "letter" по правилам письма, чтобы отклик ушёл сразу."""


def curl(path, body=None):
    cmd = ["curl", "-s", "-m", "60", f"{CLOUD}{path}{'&' if '?' in path else '?'}key={KEY}"]
    if body is not None:
        cmd += ["-X", "POST", "-H", "content-type: application/json", "--data-binary", "@-"]
    r = subprocess.run(cmd, input=json.dumps(body, ensure_ascii=False) if body is not None else None,
                       capture_output=True, text=True, timeout=90)
    return json.loads(r.stdout)


def brief(v):
    return (f"id={v['id']} | {v['name']} | {v.get('company', '')} | зп: {v.get('sal') or 'не указана'} | опыт: {v.get('exp') or ''} "
            f"| часы: {','.join(v.get('hours') or [])} | требования: {(v.get('req') or '')[:250]} "
            f"| обязанности: {(v.get('duty') or v.get('resp_text') or '')[:250]} | описание: {(v.get('desc') or '')[:1500]}")


def score(vs):
    system = open(os.path.join(ROOT, "rubric.md")).read() + FORMAT
    text = f"РЕЗЮМЕ:\n{open(os.path.join(ROOT, 'resume.md')).read()}\n\nВАКАНСИИ:\n" + "\n\n".join(map(brief, vs))
    r = subprocess.run(["claude", "-p", "--model", "opus", "--system-prompt", system, "--tools", "", "--strict-mcp-config",
                        "--setting-sources", "", "--disable-slash-commands", "--no-session-persistence"],
                       input=text, capture_output=True, text=True, timeout=900)
    m = re.search(r"\[.*\]", r.stdout, re.S)
    if r.returncode or not m:
        raise RuntimeError((r.stdout + r.stderr).strip()[:300])
    out = {int(x["id"]): x for x in json.loads(m.group(0), strict=False)}
    for x in out.values():
        if x.get("letter") and x.get("resume") not in RESUMES:
            x["resume"] = RESUMES[0]
    return out


def apply(v, sc):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write(sc["letter"])
    args = [sys.executable, os.path.join(DIR, "apply.py"), "apply", str(v["id"]), sc["resume"], f.name] + (["--dry"] if DRY else [])
    r = subprocess.run(args, capture_output=True, text=True, timeout=300)
    lines = r.stdout.strip().splitlines()
    try:
        return json.loads(lines[-1])
    except Exception:
        return {"ok": False, "reason": (r.stdout + r.stderr).strip()[-200:]}


def vacancy(vid):
    """Для проверки руками: вакансия прямо со страницы rabota.by."""
    import html as h
    t = subprocess.run(["curl", "-s", "-L", "-m", "30", "-A", "Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/130 Safari/537.36",
                        f"https://rabota.by/vacancy/{vid}"], capture_output=True, text=True).stdout
    def qa(name):
        m = re.search(rf'data-qa="{name}"[^>]*>(.*?)</(?:h1|span|div|a|p)>', t, re.S)
        return re.sub(r"\s+", " ", h.unescape(re.sub("<[^>]+>", " ", m.group(1)))).strip() if m else ""
    m = re.search(r'data-qa="vacancy-description">(.*?)</div>\s*</div>', t, re.S)
    desc = re.sub(r"\s+", " ", h.unescape(re.sub("<[^>]+>", " ", m.group(1)))).strip() if m else ""
    return {"id": int(vid), "name": qa("vacancy-title"), "company": qa("vacancy-company-name"), "sal": qa("vacancy-salary"),
            "exp": qa("vacancy-experience"), "desc": desc[:2500]}


def main():
    vid = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--vid=")), None)
    if vid:  # проверка: оценить одну вакансию и заполнить отклик без отправки, что бы ни поставил Opus
        v = vacancy(vid)
        print("вакансия:", v["name"], "|", v["company"], "| описание", len(v["desc"]), "знаков")
        sc = score([v]).get(v["id"], {})
        print("Opus:", sc.get("score"), sc.get("why"), "| резюме:", sc.get("resume"))
        if not sc.get("letter"):
            sc = {**sc, "letter": "Тестовое письмо для проверки облачного отклика, не отправляется.", "resume": sc.get("resume") or RESUMES[1]}
        a = apply(v, sc)
        print("сухой отклик:", {k: a.get(k) for k in ("ok", "reason", "letter_chars")})
        return
    queue = curl("/queue")
    print("в очереди:", len(queue))
    if not queue:
        return
    scores = score(queue)
    st = curl("/cloudstat")
    cloud, mac = int(st.get("applied_today", 0)), int(st.get("mac_today", 0))
    # своих не больше CLOUD_PER_DAY, а вместе с маком не больше общего лимита на день
    left = min(CLOUD_PER_DAY - cloud, TOTAL_PER_DAY - cloud - mac)
    results = []
    queue.sort(key=lambda v: -((scores.get(v["id"]) or {}).get("score") or 0))  # сначала лучшие
    for v in queue:
        sc = scores.get(v["id"])
        if not sc:
            continue
        res = {"id": v["id"], "score": sc.get("score"), "why": sc.get("why"), "resume": sc.get("resume"), "letter": sc.get("letter")}
        if (sc.get("score") or 0) >= MIN_SCORE and sc.get("letter"):
            if left <= 0:
                res["apply_reason"] = "дневной лимит облачных откликов"
            elif sc.get("score") < 8 and left <= RESERVE_8:
                res["apply_reason"] = "последние слоты дня оставлены под 8+"
            else:
                a = apply(v, sc)
                print("отклик", v["id"], {k: a.get(k) for k in ("ok", "reason", "label", "letter_sent")})
                res["applied"] = bool(a.get("ok")) and not DRY
                res["apply_reason"] = str(a.get("reason") or "")[:150]
                left -= 1 if res["applied"] else 0
        print(v["id"], sc.get("score"), v["name"])
        results.append(res)
    if DRY:
        print("сухой прогон, вердикт не отправляю:", json.dumps(results, ensure_ascii=False)[:2000])
        return
    print("воркер:", curl("/verdict", results))


if __name__ == "__main__":
    main()
