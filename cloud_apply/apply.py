"""Отклик на вакансию rabota.by через настоящий браузер с сохранённым входом.

login                              открыть окно, ты входишь в rabota.by сам, вход сохраняется в browser-profile/
check                              проверить, что вход ещё жив
apply VACANCY_ID "РЕЗЮМЕ" LETTER   откликнуться выбранным резюме (часть названия) с письмом из файла LETTER
probe VACANCY_ID                   открыть окно отклика и ничего не отправлять (отладка)
responses                          состояние всех откликов (приглашения, отказы, новые сообщения)
raise                              поднять в поиске все резюме, у которых кнопка уже доступна
Печатает одну строку JSON с результатом.
"""
import json, os, sys, time
from patchright.sync_api import sync_playwright

DIR = os.path.dirname(os.path.abspath(__file__))
PROFILE = os.path.join(DIR, "browser-profile")
BASE = "https://rabota.by"


def launch(pw, visible):
    # в облаке (GitHub Actions) вход берётся из файла сессии, выгруженного с мака
    state = os.environ.get("RABOTA_STATE_FILE")
    if state:
        browser = pw.chromium.launch(headless=True, args=["--lang=ru-RU"])
        ctx = browser.new_context(storage_state=state, locale="ru-RU", timezone_id="Europe/Minsk",
                                  viewport={"width": 1280, "height": 900})
        ctx.close_browser = browser.close
        return ctx
    # visible only for login; otherwise headless so no window ever steals focus
    if not visible:
        return pw.chromium.launch_persistent_context(PROFILE, headless=True, channel="chromium", locale="ru-RU",
                                                     timezone_id="Europe/Minsk", viewport={"width": 1280, "height": 900},
                                                     args=["--lang=ru-RU"])
    return pw.chromium.launch_persistent_context(PROFILE, headless=False, channel="chromium", no_viewport=True,
                                                 locale="ru-RU", timezone_id="Europe/Minsk",
                                                 args=["--lang=ru-RU", "--window-size=1280,900"])


def logged_in(ctx):
    r = ctx.request.get(f"{BASE}/applicant/resumes", max_redirects=5)
    return r.ok and "account/login" not in r.url and "Мои резюме" in r.text()


def out(**kw):
    print(json.dumps(kw, ensure_ascii=False), flush=True)


def login():
    with sync_playwright() as pw:
        ctx = launch(pw, True)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(f"{BASE}/account/login")
        for _ in range(200):  # до 10 минут ждём, пока войдёшь
            time.sleep(3)
            try:
                if logged_in(ctx):
                    out(ok=True, msg="вход сохранён")
                    break
            except Exception:
                pass
        else:
            out(ok=False, msg="не дождался входа")
        ctx.close()


def check():
    with sync_playwright() as pw:
        ctx = launch(pw, False)
        out(ok=logged_in(ctx))
        ctx.close()


def open_popup(page, vid):
    page.goto(f"{BASE}/vacancy/{vid}", wait_until="domcontentloaded")
    page.wait_for_timeout(1500)
    body = page.inner_text("body")
    if "Вы откликнулись" in body:
        return "already"
    btn = page.locator('[data-qa="vacancy-response-link-top"]').first
    if not btn.count():
        return "no_button"
    btn.click()
    page.wait_for_timeout(2500)
    # вакансия в другой стране (РФ): сторож берёт оттуда только удалёнку, так что подтверждаем
    confirm = page.locator('[data-qa="relocation-warning-confirm"]')
    if confirm.count() and confirm.first.is_visible():
        confirm.first.click()
        page.wait_for_timeout(2500)
    if "/applicant/vacancy_response" in page.url:  # отдельная страница: тест или вопросы работодателя
        return "questions"
    return "popup"


def choose_resume(page, title):
    titles = page.locator('[data-qa="resume-title"]')
    if titles.first.inner_text().strip() == title:
        return True
    titles.first.click()
    page.wait_for_timeout(1500)
    for i in range(1, titles.count()):
        t = titles.nth(i)
        if t.is_visible() and t.inner_text().strip() == title:
            t.click()
            page.wait_for_timeout(1500)
            break
    return page.locator('[data-qa="resume-title"]').first.inner_text().strip() == title


def apply(vid, resume, letter, dry=False):
    with sync_playwright() as pw:
        ctx = launch(pw, False)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            if not logged_in(ctx):
                return out(ok=False, reason="not_logged_in")
            state = open_popup(page, vid)
            if state != "popup":
                return out(ok=False, reason=state)
            if page.locator('[data-qa="hidden-resume-warning"]').is_visible():
                return out(ok=False, reason="resume_hidden_for_employer")
            if resume and not choose_resume(page, resume):
                return out(ok=False, reason="resume_not_found")
            # когда письмо необязательное, поле прячется за кнопкой «Добавить сопроводительное»
            for qa in ("add-cover-letter", "vacancy-response-letter-toggle"):
                toggle = page.locator(f'[data-qa="{qa}"]')
                if toggle.count() and toggle.first.is_visible():
                    toggle.first.click()
                    page.wait_for_timeout(800)
                    break
            box = page.locator('[data-qa="vacancy-response-popup-form-letter-input"]')
            if not letter or not letter.strip():
                return out(ok=False, reason="no_letter_text")
            if not box.count() or not box.first.is_visible():
                return out(ok=False, reason="no_letter_field")
            box.first.click()
            box.first.fill(letter)
            # без письма не отправляем никогда: проверяем, что текст реально в поле
            if box.first.input_value().strip()[:50] != letter.strip()[:50]:
                return out(ok=False, reason="letter_not_filled")
            submit = page.locator('[data-qa="vacancy-response-submit-popup"]')
            if not submit.count():
                return out(ok=False, reason="no_submit")
            if dry:
                return out(ok=True, reason="dry_run", letter_chars=len(box.first.input_value()))
            with page.expect_response(lambda r: "/applicant/vacancy_response/popup" in r.url
                                      and r.request.method == "POST", timeout=20000) as resp:
                submit.first.click()
            data = resp.value.json()
            label = data.get("response_label") or ""
            out(ok=data.get("success") == "true", reason=str(data.get("error") or ""), label=label,
                letter_sent="without-letter" not in label)
        except Exception as e:
            out(ok=False, reason=f"error: {e}"[:300])
        finally:
            ctx.close()


def responses():
    """Состояние всех откликов: приглашения, отказы, новые сообщения."""
    import re, html as h
    with sync_playwright() as pw:
        ctx = launch(pw, False)
        try:
            if not logged_in(ctx):
                return out(ok=False, reason="not_logged_in")
            topics, names = [], {}
            for page_no in range(5):
                r = ctx.request.get(f"{BASE}/applicant/negotiations?page={page_no}")
                m = re.search(r'id="HH-Lux-InitialState"[^>]*>(.*?)</template>', r.text(), re.S)
                d = json.loads(h.unescape(m.group(1)), strict=False)
                for v in (d.get("vacanciesShort") or {}).get("vacanciesList", []):
                    names[v["vacancyId"]] = (v.get("name", ""), (v.get("company") or {}).get("visibleName", ""))
                topics += d["applicantNegotiations"]["topicList"]
                if page_no + 1 >= int(d["applicantNegotiations"].get("pageCount") or 1):
                    break
            out(ok=True, topics=[{"id": t["id"], "vacancy": t["vacancyId"], "name": names.get(t["vacancyId"], ("", ""))[0],
                                  "company": names.get(t["vacancyId"], ("", ""))[1], "state": t["lastState"],
                                  "new": t.get("hasNewMessages", False), "msgs": t.get("conversationMessagesCount", 0),
                                  "chat": t.get("chatId")} for t in topics])
        finally:
            ctx.close()


def raise_resumes():
    """Жмёт «Поднять в поиске» у всех резюме, где можно. Остальные показывают «Поднять в ЧЧ:ММ»."""
    import re
    with sync_playwright() as pw:
        ctx = launch(pw, False)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            if not logged_in(ctx):
                return out(ok=False, reason="not_logged_in")
            page.goto(f"{BASE}/applicant/resumes", wait_until="domcontentloaded")
            page.wait_for_timeout(8000)
            raised = 0
            btns = page.locator('[data-qa="resume-update-button"]')
            for i in range(btns.count()):
                b = btns.nth(i)
                if b.is_visible() and b.is_enabled() and "поднять в поиске" in b.inner_text().lower():
                    b.click()
                    page.wait_for_timeout(2500)
                    raised += 1
            page.reload(wait_until="domcontentloaded")
            page.wait_for_timeout(6000)
            nxt = sorted(set(re.findall(r"Поднять в\s(\d\d:\d\d)", page.inner_text("body"))))
            out(ok=True, raised=raised, next=nxt)
        finally:
            ctx.close()


def probe(vid):
    with sync_playwright() as pw:
        ctx = launch(pw, False)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        state = open_popup(page, vid)
        qas = page.eval_on_selector_all("[data-qa]", "els => [...new Set(els.filter(e => e.offsetParent).map(e => e.dataset.qa))]")
        out(state=state, url=page.url, qa=[q for q in qas if "response" in q or "resume" in q or "letter" in q])
        ctx.close()


if __name__ == "__main__":
    cmd = sys.argv[1:2]
    if cmd == ["login"]:
        login()
    elif cmd == ["check"]:
        check()
    elif cmd == ["apply"] and len(sys.argv) in (5, 6):
        apply(sys.argv[2], sys.argv[3], open(sys.argv[4]).read(), dry=sys.argv[5:] == ["--dry"])
    elif cmd == ["responses"]:
        responses()
    elif cmd == ["raise"]:
        raise_resumes()
    elif cmd == ["probe"] and len(sys.argv) == 3:
        probe(sys.argv[2])
    else:
        print(__doc__)
