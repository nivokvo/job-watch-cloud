"""Откликаться или нет: одно правило для мака и облака.
Opus решает по score (7+). Модель добавляет до MODEL_PER_DAY своих откликов среди 5-6:
пока экзамен не сдан (качество ниже GATE), она исследует типы вакансий (сэмплинг Томпсона), после экзамена берёт по шансу."""
import random, re
import model

MIN_SCORE = 7
MODEL_MIN = 5
MODEL_PER_DAY = 3
GATE = 0.6  # AUC на откликах, которых модель не видела; 0.5 = монетка
PAY_FLOOR = 23000  # RUR в месяц (~800 BYN), по верхней границе; зарплата не указана = проходит
RATES = ((r"BYN|Br", 29), (r"USD|\$", 80), (r"EUR|€", 90), (r"KZT|₸", 0.15), (r"RUR|RUB|₽|руб", 1))
BAD = r"посредник|реферал|запрет"


def pays(sal):
    nums = [int(x) for x in re.findall(r"\d+", re.sub(r"[\s  ]", "", sal or ""))]
    rate = next((r for p, r in RATES if re.search(p, sal or "")), None)
    return not nums or not rate or max(nums) * rate >= PAY_FLOOR


def chance(v, w=None):
    """Шанс приглашения, только если модель сдала экзамен. Иначе None: показывать непроверенное незачем."""
    w = w or model.load()
    return model.p(v, w) if w and (w.get("auc") or 0) >= GATE else None


def worth(v, sc, model_today=0, w=None):
    """'opus', 'model' или None."""
    s = sc.get("score") or 0
    if not pays(v.get("sal")) or re.search(BAD, sc.get("why") or "", re.I):
        return None
    if s >= MIN_SCORE:
        return "opus"
    if s < MODEL_MIN or model_today >= MODEL_PER_DAY:
        return None
    w = w or model.load()
    if not w:
        return None
    p = chance(v, w)
    if p is not None:
        return "model" if p >= 1.3 * w["base"] else None
    # исследование: тип вакансии с неизвестным или хорошим итогом пробуем чаще
    n, k = (w.get("arms") or {}).get(model.arm(v), [0, 0])
    return "model" if random.betavariate(1 + k, 1 + n - k) > w["base"] else None


if __name__ == "__main__":  # самопроверка
    assert pays("") and pays("1500 BYN") and not pays("500 BYN") and pays("40000 RUR")
    w = {"base": 0.2, "auc": 0.3, "arms": {"dev": [50, 0]}, "bias": 0, "w": {}}
    assert worth({"sal": ""}, {"score": 8}, w=w) == "opus"
    assert worth({"sal": "400 BYN"}, {"score": 9}, w=w) is None
    assert worth({"sal": ""}, {"score": 6}, model_today=3, w=w) is None
    assert sum(worth({"name": "Python разработчик"}, {"score": 6}, w=w) == "model" for _ in range(200)) < 5
    print("ok")
