"""Шанс, что после отклика позовут (собес, тестовое или живая переписка), по истории откликов Глеба.
Логистическая регрессия на чистом Python: признаки из полей вакансии, без LLM. Учится на маке (там исходы),
веса кладёт в ~/job-watch-cloud/model.json (только числа), облако читает тот же файл.
  python3 model.py  — обучить, сохранить веса и показать экзамены:
    auc       главный: прогноз записан при отклике, итог пришёл позже (нужно 20 таких откликов)
    auc_cv    перекрёстная проверка на истории; auc_prior — одни стартовые веса; auc_opus — оценка Opus"""
import json, math, os, re, time, html, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
WEIGHTS = os.path.expanduser("~/job-watch-cloud/model.json")  # мак и облако: корень облачного репо
if not os.path.isdir(os.path.dirname(WEIGHTS)):
    WEIGHTS = os.path.join(os.path.dirname(HERE), "model.json")
BY_RE = r"Минск|Беларус|Брест|Гомель|Гродно|Витебск|Могил|Бобруйск|Барановичи|Борисов|Пинск|Орша|Мозырь|Солигорск|Лида|Молодечно|Полоцк|Жодино|Слуцк|Речица"
ROLES = {"dev": r"engineer|developer|разработчик|программист|fullstack|backend|frontend|\bqa\b|devops|инженер",
         "content": r"контент|копирайт|рерайт|редактор|seo|писател|youtube|ютуб",
         "data": r"данн|оператор|ввод|модерат|верифик|разметк|асессор|каталог",
         "market": r"маркетплейс|wildberries|ozon|озон|авито|e-commerce",
         "analyst": r"аналитик|analyst"}
RULE = r"мониторинг|сверк|проверк|аудит|контрол|отч[её]т"
JUNIOR = r"стаж[её]р|junior|джун|начинающ|ученик|без опыта|intern|студент"
RATE = {"BYR": 1, "BYN": 1, "RUR": 1 / 29, "USD": 3.2, "EUR": 3.5}
# Стартовые веса заданы руками 11.11 (вклад в логит шанса): студент без стажа, рынок hh. На ~50 исходах обучение
# с нуля ничего не находит, поэтому модель стартует отсюда и отходит от этих чисел, только когда данные настаивают.
PRIOR_BIAS = -1.4  # шанс около 20% у «средней» вакансии
PRIOR = {"exp_1_3": -0.4, "exp_3plus": -1.5, "junior": 0.6, "role_dev": -0.8, "role_data": 0.4, "role_content": 0.2,
         "role_market": 0.1, "role_analyst": 0.0, "rule": 0.2, "by": 0.2, "remote": 0.2, "flex": 0.0,
         "pay_high": -0.5, "no_pay": 0.0, "crowd": -0.4, "few": 0.2}
SIGMA = 0.2  # насколько мы не уверены в стартовых весах. 11.11 на 51 исходе: 0.2 даёт AUC 0.65 на невиданных, 0.7 уже 0.43
# (обучение на таких данных ловит шум). Штраф 1/(SIGMA²·n) слабеет сам, когда исходов становится больше


def feats(v):
    """v: вакансия в виде core.norm() (name, exp, formats, area, sal, hours, desc)."""
    name = (v.get("name") or "").lower()
    text = name + " " + (v.get("desc") or "")[:600].lower()
    exp = v.get("exp") or "noExperience"
    hours = " ".join(v.get("hours") or [])
    m = re.match(r"(\d+)\D*(\d*)\s*(\w+)?", (v.get("sal") or "").replace(" ", "").replace(" ", ""))
    pay = float(m.group(1)) * RATE.get((m.group(3) or "BYN").upper(), 1) if m else 0
    f = {"exp_1_3": exp == "between1And3", "exp_3plus": exp in ("between3And6", "moreThan6"),
         "by": bool(re.search(BY_RE, v.get("area") or "")), "remote": "REMOTE" in (v.get("formats") or []),
         "flex": bool(re.search(r"FLEXIBLE|HOURS_[2-6]\b", hours)), "rule": bool(re.search(RULE, text)),
         "junior": bool(re.search(JUNIOR, text)), "pay_high": pay >= 2500, "no_pay": not pay,
         "crowd": (v.get("resp") or 0) >= 100, "few": v.get("resp") is not None and v["resp"] < 20}
    f.update({"role_" + k: bool(re.search(r, name)) for k, r in ROLES.items()})
    return {k: float(x) for k, x in f.items()}


def p(v, w=None):
    w = w or load()
    if not w:
        return None
    z = w["bias"] + sum(w["w"].get(k, 0) * x for k, x in feats(v).items())
    return 1 / (1 + math.exp(-z))


def load():
    try:
        return json.load(open(WEIGHTS))
    except (OSError, ValueError):
        return None


def fit(X, y, wt, steps=2000, lr=0.5):
    """Логрегрессия со штрафом за уход от стартовых весов PRIOR (байесовская оценка MAP)."""
    w, b = dict(PRIOR), PRIOR_BIAS
    n = sum(wt)
    lam = 1 / (SIGMA ** 2 * n)
    for _ in range(steps):
        gw, gb = {k: lam * (w[k] - PRIOR[k]) for k in w}, lam * (b - PRIOR_BIAS)
        for x, t, c in zip(X, y, wt):
            e = c * (1 / (1 + math.exp(-(b + sum(w[k] * x.get(k, 0) for k in w)))) - t) / n
            gb += e
            for k, xv in x.items():
                gw[k] += e * xv
        b -= lr * gb
        for k in w:
            w[k] -= lr * gw[k]
    return {"bias": b, "w": w}


# ---------- данные (только мак: исходы лежат там) ----------

def vac_page(vid):
    h = subprocess.run(["curl", "-s", "-L", "-m", "30", "-A", "Mozilla/5.0", f"https://rabota.by/vacancy/{vid}"],
                       capture_output=True, timeout=60).stdout.decode("utf-8", "replace")
    m = re.search(r'id="HH-Lux-InitialState"[^>]*>(.*?)</template>', h, re.S)
    try:
        x = json.loads(html.unescape(m.group(1)), strict=False)["vacancyView"]["vacancyFull"]["vacancy"]
    except (AttributeError, KeyError, ValueError):
        return None
    c = x.get("compensation") or {}
    return dict(name=x.get("name"), exp=x.get("workExperience"), formats=x.get("workFormats") or [], hours=x.get("workingHours") or [],
                area=(x.get("area") or {}).get("name"), sal=f"{c.get('from') or c.get('to') or ''} {c.get('currencyCode', '')}".strip(),
                desc=re.sub(r"\s+", " ", html.unescape(re.sub("<[^>]+>", " ", x.get("description") or "")))[:1500])


def dataset(fetch_new=10):
    """Отклики с исходом. Успех: собес/приглашение или работодатель ведёт переписку (3+ сообщения, не отказ).
    Неудача: отказ (вес 1) или молчание 7+ дней (вес 0.5). Свежие без ответа и «позвали по резюме» не берём."""
    cache_f = os.path.join(HERE, "vac_cache.json")
    cache = json.load(open(cache_f)) if os.path.exists(cache_f) else {}
    applied = {a["id"]: a for a in map(json.loads, open(os.path.join(HERE, "applied.jsonl"))) if a.get("ok")}
    neg = {t["vacancy"]: t for t in json.load(open(os.path.join(HERE, "negotiations.json"))).values()}
    changed = False
    for vid in [i for i in applied if str(i) not in cache and not applied[i].get("v")][:fetch_new]:
        cache[str(vid)] = vac_page(vid)
        changed = True
        time.sleep(1)
    if changed:
        json.dump(cache, open(cache_f, "w"), ensure_ascii=False)
    rows = []
    now = time.time()
    for vid, a in applied.items():
        t = neg.get(vid)
        v = a.get("v") or cache.get(str(vid))
        if not t or not v:
            continue
        v = {**v, "resp": a.get("resp")}
        good = t["state"] == "INTERVIEW" or (t["state"] != "DISCARD" and (t.get("msgs") or 0) >= 3)
        age = (now - time.mktime(time.strptime(t["created"][:16], "%Y-%m-%dT%H:%M"))) / 86400 if t.get("created") else 99
        if good:
            rows.append((v, 1, 1.0, a))
        elif t["state"] == "DISCARD":
            rows.append((v, 0, 1.0, a))
        elif age >= 7:
            rows.append((v, 0, 0.5, a))
    return rows


def auc(scores, y):
    pos = [s for s, t in zip(scores, y) if t]
    neg = [s for s, t in zip(scores, y) if not t]
    if not pos or not neg:
        return None
    return sum((a > b) + 0.5 * (a == b) for a in pos for b in neg) / (len(pos) * len(neg))


def arm(v):
    """Тип вакансии для исследования: что из этого реально зовёт."""
    name = (v.get("name") or "").lower()
    return next((k for k, r in ROLES.items() if re.search(r, name)), "other")


def cv(X, y, wt, folds=4, seeds=3):
    """AUC на откликах, которых модель не видела. Доли успехов в частях равные: иначе на малых данных AUC занижается сам собой."""
    import random
    res = []
    for seed in range(seeds):
        pos, neg = [i for i, t in enumerate(y) if t], [i for i, t in enumerate(y) if not t]
        random.Random(seed).shuffle(pos)
        random.Random(seed + 100).shuffle(neg)
        fold = {i: j % folds for j, i in enumerate(pos + neg)}
        pr = [0.0] * len(y)
        for k in range(folds):
            tr = [i for i in fold if fold[i] != k]
            w = fit([X[i] for i in tr], [y[i] for i in tr], [wt[i] for i in tr], steps=800)
            for i in fold:
                if fold[i] == k:
                    pr[i] = w["bias"] + sum(w["w"].get(f, 0) * x for f, x in X[i].items())
        a = auc(pr, y)
        if a is not None:
            res.append(a)
    return round(sum(res) / len(res), 3) if res else None


def live(rows, need=20):
    """Главный экзамен: прогноз записан в момент отклика (поле p), итог пришёл позже. Подогнать нельзя."""
    got = [(r[3]["p"], r[1]) for r in rows if r[3].get("p") is not None]
    a = auc([g[0] for g in got], [g[1] for g in got])
    ok = len(got) >= need and sum(g[1] for g in got) >= 3
    return (round(a, 3) if a is not None and ok else None), len(got)


def train():
    """Обучить на всех исходах и сохранить веса, статистику по типам и итоги экзаменов."""
    rows = dataset()
    X, y, wt = [feats(r[0]) for r in rows], [r[1] for r in rows], [r[2] for r in rows]
    w = fit(X, y, wt)
    arms = {}
    for r in rows:
        a = arms.setdefault(arm(r[0]), [0, 0])
        a[0] += 1
        a[1] += r[1]
    prior = [PRIOR_BIAS + sum(PRIOR[k] * x for k, x in f.items()) for f in X]
    w["auc"], w["auc_n"] = live(rows)
    w.update(n=len(rows), pos=sum(y), base=round(sum(y) / max(1, len(y)), 3), auc_cv=cv(X, y, wt), auc_prior=round(auc(prior, y) or 0, 3),
             auc_opus=round(auc([r[3].get("score") if r[3].get("score") is not None else 5 for r in rows], y) or 0, 3),
             arms=arms, at=time.strftime("%Y-%m-%d %H:%M"))
    json.dump(w, open(WEIGHTS, "w"), ensure_ascii=False, indent=1)
    return w


if __name__ == "__main__":
    w = train()
    print(json.dumps({k: w[k] for k in w if k != "arms"}, ensure_ascii=False, indent=1))
