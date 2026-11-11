# -*- coding: utf-8 -*-
"""Откликаться или нет: одно правило для мака и облака.
Opus решает по score (7+). Модель добавляет до MODEL_PER_DAY своих откликов среди 5-6:
чем выше её шанс приглашения, тем чаще берёт. Шанс показываем в Telegram только после экзамена на новых откликах (GATE)."""
import random, re
import model

MIN_SCORE = 7
MODEL_MIN = 5
MODEL_PER_DAY = 3
GATE = 0.6  # AUC главного экзамена (model.live): прогноз записан при отклике, итог пришёл позже; 0.5 = монетка
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
    p = model.p(v, w) if w else None
    if p is None:
        return None
    # чем выше шанс, тем чаще берём: при шансе в 1.5 раза выше среднего всегда, при среднем в 2 случаях из 3.
    # Слабые тоже иногда пробуем, иначе модель никогда не узнает, что ошибалась
    return "model" if random.random() < p / (1.5 * w["base"]) else None


if __name__ == "__main__":  # самопроверка
    assert pays("") and pays("1500 BYN") and not pays("500 BYN") and pays("40000 RUR")
    w = {"base": 0.2, "auc": None, "bias": model.PRIOR_BIAS, "w": dict(model.PRIOR)}
    assert worth({"sal": ""}, {"score": 8}, w=w) == "opus"
    assert worth({"sal": "400 BYN"}, {"score": 9}, w=w) is None
    assert worth({"sal": ""}, {"score": 6}, model_today=3, w=w) is None
    dev = {"name": "Senior Python разработчик", "exp": "between3And6", "resp": 300}
    easy = {"name": "Стажёр, модератор данных", "exp": "noExperience", "formats": ["REMOTE"], "resp": 5}
    take = lambda v: sum(worth(v, {"score": 6}, w=w) == "model" for _ in range(400))
    assert take(dev) < 60 < 340 < take(easy), (take(dev), take(easy))
    assert chance(easy, w) is None and chance(easy, {**w, "auc": 0.7}) > 0.3
    print("ok")
