"""Шанс, что после отклика позовут (собес, тестовое или живая переписка), по истории откликов Глеба.
Логистическая регрессия на чистом Python: признаки из полей вакансии, без LLM. Учится на маке (там исходы),
веса кладёт в ~/job-watch-cloud/model.json (только числа), облако читает тот же файл.
  python3 model.py train  — обучить и сохранить веса
  python3 model.py exam   — экзамен: перекрёстная проверка, модель против оценки Opus на тех же откликах"""
import json, math, os, re, sys, time, html, subprocess

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
         "junior": bool(re.search(JUNIOR, text)), "pay": math.log1p(pay) / 8 if pay else 0, "no_pay": not pay}
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


def fit(X, y, wt, lam=1.0, steps=3000, lr=0.3):
    """Градиентный спуск с L2: данных мало (~100 откликов, ~10 успехов), поэтому сильная регуляризация."""
    keys = sorted({k for x in X for k in x})
    w, b = {k: 0.0 for k in keys}, 0.0
    n = sum(wt)
    for _ in range(steps):
        gw, gb = {k: lam * w[k] for k in keys}, 0.0
        for x, t, c in zip(X, y, wt):
            e = c * (1 / (1 + math.exp(-(b + sum(w[k] * x.get(k, 0) for k in keys)))) - t) / n
            gb += e
            for k, xv in x.items():
                gw[k] += e * xv
        b -= lr * gb
        for k in keys:
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


def cv(X, y, wt, folds=4, seeds=2):
    """Качество на откликах, которых модель не видела (AUC: 0.5 = монетка, 1 = идеально)."""
    import random
    res = []
    for seed in range(seeds):
        idx = list(range(len(y)))
        random.Random(seed).shuffle(idx)
        pr = [0.0] * len(y)
        for k in range(folds):
            te = set(idx[k::folds])
            w = fit([X[i] for i in idx if i not in te], [y[i] for i in idx if i not in te], [wt[i] for i in idx if i not in te], steps=1500)
            for i in te:
                z = w["bias"] + sum(w["w"].get(f, 0) * x for f, x in X[i].items())
                pr[i] = 1 / (1 + math.exp(-z))
        a = auc(pr, y)
        if a is not None:
            res.append(a)
    return round(sum(res) / len(res), 3) if res else None


def train():
    """Обучить на всех исходах, сдать экзамен и сохранить веса, статистику по типам и итог экзамена."""
    rows = dataset()
    X, y, wt = [feats(r[0]) for r in rows], [r[1] for r in rows], [r[2] for r in rows]
    w = fit(X, y, wt)
    arms = {}
    for r in rows:
        a = arms.setdefault(arm(r[0]), [0, 0])
        a[0] += 1
        a[1] += r[1]
    w.update(n=len(rows), pos=sum(y), base=round(sum(y) / max(1, len(y)), 3), auc=cv(X, y, wt), arms=arms,
             at=time.strftime("%Y-%m-%d %H:%M"))
    json.dump(w, open(WEIGHTS, "w"), ensure_ascii=False, indent=1)
    return w


def exam():
    rows = dataset()
    X, y, wt = [feats(r[0]) for r in rows], [r[1] for r in rows], [r[2] for r in rows]
    opus = [r[3].get("score") if r[3].get("score") is not None else 5 for r in rows]
    return {"n": len(rows), "pos": sum(y), "auc_model": cv(X, y, wt, seeds=5), "auc_opus": auc(opus, y)}


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "exam"
    print(json.dumps(train() if cmd == "train" else exam(), ensure_ascii=False, indent=1))
