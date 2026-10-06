# Западные платформы и ИИ-разметка из Беларуси (проверка на 06.10.2026)

## Коротко

- **Сторож под западные платформы не строить.** Для гражданина РБ, живущего в Беларуси, в октябре 2026 почти всё закрыто. Где-то страну запрещают прямо (санкции и комплаенс), а где регистрация открыта, деньги некуда вывести: с 11.09.2026 закрыт Payoneer, Wise закрыт с 2022 года, PayPal в РБ работает только на отправку, Skrill и Neteller закрыты с марта 2026, Paysera и Remote.com Беларусь не поддерживают (Deel, по вторичным данным, тоже), Stripe Беларусь не обслуживает.
- **Крупные ИИ-платформы закрыты прямо:** Outlier/Scale, Mercor, Toloka/Mindrift и Prolific (белый список), у DataAnnotation/Surge только 6 англоязычных стран. Русскоязычные проекты Appen, Welo и TELUS набирают людей, живущих в Польше, Грузии, Казахстане или США, но не в РБ.
- **Единственная западная зацепка в ИИ-разметке:** Welo Data (Welocalize), сеть «AI Trainers Network – Belarusian» с требованием «Based in: Belarus», но нужен беларусский язык на уровне носителя, а способ выплаты не проверен.
- **ИИ-разметка на русском реально есть у Яндекса** (AI-тренеры: трудовой договор, ГПХ или самозанятость РФ). Это российский путь (задание 5), и берут ли граждан РБ из Минска, не проверено.
- **Крипта** не законный обход: по Декрету №8 получать токены как оплату за работу физлицу в РБ не разрешено (перечень операций закрытый). Кроме того, с 24.05.2026 действует запрет ЕС на транзакции с белорусскими криптоплатформами, а с 23.08.2026 Binance блокирует переводы с WhiteBird.
- **Что физически работает для денег из-за границы:** SWIFT в EUR на счёт в несанкционном белорусском банке (Приорбанк берёт 3%, но не меньше 120 BYN; в USD не меньше 200 BYN, поэтому мелкие суммы съедаются комиссией), Paysend (карта-карта от частного лица, площадки так не платят) и платёжный агент Plane, если его подключит заказчик (Беларусь поддерживается с проверками). Налог: НПД 10% с дохода от иностранных заказчиков, с 01.07.2026 минимум 45 BYN в месяц.
- **Реальный заработок с запада при 1-2 часах в день:** около 0. Время лучше тратить на СНГ-потоки (задание 5) и биржи из задания 4.

Обход через проживание в другой стране не рассматривается, как требует задание.

## 1. Что реально работает из Беларуси

Обозначения: ✅ доступно, ⚠️ только через ..., ❌ нет. В колонке «Причина»: **С** — санкции или комплаенс (страна запрещена прямо), **П** — платёжка (регистрация не запрещена, но вывести некуда), **—** — не подходит по другим причинам.

### 1.1 ИИ-разметка и обучение моделей

| Платформа | Статус | Причина | Что именно | Источник (дата проверки) |
|---|---|---|---|---|
| Outlier (Scale AI) | ❌ | С | Белый список стран, Беларуси нет; VPN запрещён | [outlier.ai/legal/flexible-working-guidelines](https://outlier.ai/legal/flexible-working-guidelines) (06.10.2026) |
| Remotasks (Scale AI) | ❌ | С+П | Выплаты только через PayPal или AirTM, список стран не публикуется, проекты ушли в Outlier | [remotasks.com](https://www.remotasks.com/en) (06.10.2026) |
| DataAnnotation.tech (Surge) | ❌ | С+П | Только US, UK, CA, AU, NZ, IE; выплаты только через PayPal | [обзор aitrainer.work](https://aitrainer.work/guides/is-dataannotation-legit-review), [FAQ](https://dataannotation.tech/faq) |
| Mercor | ❌ | С | Беларусь прямо в списке «Unsupported countries» (там же Россия, Казахстан, Армения, Грузия) | [talent.docs.mercor.com/policies/supported-countries](https://talent.docs.mercor.com/policies/supported-countries) (06.10.2026) |
| Alignerr (Labelbox) | ❌ | П | Выплаты через Stripe Connect, PayPal или Deel, и ни один из них РБ не обслуживает | [обзор](https://www.aigigjobs.com/platforms/alignerr) |
| Toloka | ❌ | С | Беларусь в «Restricted Jurisdictions»: нельзя ни работать, ни выводить деньги на счёт в РБ | [toloka.ai/legal/eligibility…](https://toloka.ai/legal/eligibility-and-geographic-restrictions) (06.10.2026) |
| Mindrift (Toloka) | ❌ | С | Тот же список запрещённых стран | [mindrift.ai/legal/…](https://mindrift.ai/legal/eligibility-and-geographic-restrictions) (06.10.2026) |
| Appen / CrowdGen | ❌ | С+П | Русскоязычные проекты только для живущих в Грузии, Польше или США (Lever, 06.2026); выплаты через PayPal или Payoneer | [api.lever.co/v0/postings/appen](https://api.lever.co/v0/postings/appen?mode=json) (06.10.2026) |
| TELUS Digital AI Community (бывший Lionbridge AI) | ❌ | С | Вакансии для носителей беларусского ищут людей, **5 лет живущих в Польше**; сайт отдаёт 403 | [praca.pl](https://praca.pl/personalized-internet-assessor-belarusian-speaker_8563137.html), [ur.edu.pl](https://biurokarier.ur.edu.pl/job_offer,8477/oferta-230120258477.htm) (01.2025) |
| Clickworker | ❌ | П | Выплаты через PayPal, Payoneer, SEPA, AirTM, eWallet или ACH; если вывести нельзя, Clickworker сам просит не регистрироваться | [support-workplace.clickworker.com](https://support-workplace.clickworker.com/support/solutions/articles/80000671469) (обновлено 13.03.2026) |
| Prolific | ❌ | С / — | Белый список стран (OECD и др.), Беларуси нет; к тому же это опросы, по rubric максимум 2 балла | [participant-help.prolific.com](https://participant-help.prolific.com/en/article/628d72) (02.09.2026) |
| Invisible Technologies | ❌ (не проверено) | — | Почти все роли экспертные (медики, 3D+Python), $6-65 в час; выплаты для РБ не проверены | Himalayas API, вакансии 06.10.2026 |
| OneForma (Pactera) | ❌ | П | Payoneer, PayPal или Tipalti; первые два для РБ закрыты, Tipalti не проверен | [oneforma.com/help-center/…](https://www.oneforma.com/help-center/payment-issues-and-finance/what-payment-methods-are-available-for-you/) (06.10.2026) |
| **Welo Data (Welocalize)** | ⚠️ | — | «AI Trainers Network – Belarusian»: «Based in: Belarus», беларусский язык на уровне носителя и английский. Это пул талантов, а не открытая вакансия. Русскоязычная сеть Welo берёт только GE, KZ, LV, US, MD, KG, TM, UZ, TJ, без РБ. **Выплаты не проверены** | [jobs.lever.co/weloglobal/63cff927…](https://jobs.lever.co/weloglobal/63cff927-d6ac-4769-b594-00686ede8e40) (размещено 07.08.2025, активно 06.10.2026) |
| micro1, Productive Playhouse (русскоязычные AI rater) | ❌ (не проверено) | — | Вакансии «Russian AI Model Rater» и «Russian Bilingual Expert» на Himalayas размечены как Russian Federation; выплаты для РБ неизвестны | Himalayas API, 06.10.2026 |
| **Яндекс, AI-тренеры** (найдено самостоятельно) | ⚠️ | — | Русский язык, RLHF. Общий трек по трудовому договору, экспертный трек по ГПХ или как самозанятый РФ на платформе. Берут ли граждан РБ, живущих в Минске, **не проверено** | [ai-trainers.ya.ru](https://ai-trainers.ya.ru/), [how-we-hire](https://ai-trainers.ya.ru/how-we-hire) (06.10.2026) |

Про rubric: на всех платформах RLHF и оценки ответов ИИ правила **запрещают** генерировать ответы нейросетью и автоматизировать работу. Это ручной труд, поэтому даже доступная платформа даёт не больше 5-6 баллов, а конвейер с минимумом часов в день не больше 4.

### 1.2 Биржи и маркетплейсы

| Площадка | Статус | Причина | Что именно | Источник |
|---|---|---|---|---|
| Upwork | ❌ | С | Работа с РБ приостановлена с 01.05.2022 | [Upwork, 8-K 2022](https://www.sec.gov/Archives/edgar/data/1627475/000119312522067173/d323878d8k.htm) |
| Fiverr | ❌ | П | Регистрация из РБ проходит, но вывод только через PayPal, Payoneer или банковский перевод через Payoneer, а всё это для РБ закрыто | [обзор методов вывода](https://ruul.io/blog/fiverr-payments-guide); Payoneer см. п. 1.3 |
| Freelancer.com | ⚠️ не проверено | П | В правилах нет прямого запрета РБ, только общий пункт про санкции. Вывод: Express (списка с РБ нет), PayPal и Skrill закрыты, остаётся wire в USD от $500 с комиссией $25 | [freelancer.com/about/terms](https://www.freelancer.com/about/terms), [withdrawal-methods](https://www.freelancer.ca/support/payments/withdrawal-methods) |
| PeoplePerHour | ⚠️ не проверено | П | По UK AML не обслуживает только КНДР, Иран, Сирию, Кубу, Судан и Крым, Беларусь не упомянута. Вывод через PayPal, Payoneer или банк, для РБ не проверено | [peopleperhour.com/static/terms](https://www.peopleperhour.com/static/terms) (06.10.2026) |
| Contra | ⚠️ | П | Комиссии 0%, вывод через Stripe, PayPal, Payoneer или **USDC**. Из этого для РБ остаётся только USDC, а он юридически серый (см. п. 1.3) | [help.contra.com](https://help.contra.com/en/articles/9322938-payout-methods-for-freelancers-on-contra) |
| Guru | ❌ | П | Payoneer отключён с 05.10.2023, банковский вывод вне США только в 48 стран, РБ нет | [сводка по Guru](https://www.guru.com/blog/?p=18257) |
| Toptal | ❌ | — | Сеть сеньоров с жёстким отбором и комплаенс-проверкой, новичку не подходит; позиция по РБ не проверена (сайт отдаёт 403) | — |
| Malt | ❌ | С / — | Работает в FR, DE, ES, BE, NL, CH, UK, UAE и Северных странах; ИП-одиночек вне ~10 стран ЕС не берут | [help.malt.com](https://help.malt.com/kb/guide/en/i-am-a-freelancer-registered-abroad-for-which-countries-does-malt-authorize-registration-in-this-situation-1qLLe7BZH8/Steps/2511427) |
| Workana | ❌ | — | Латинская Америка, испанский и португальский; по РБ не проверено (сайт отдаёт 403) | — |
| TemplateMonster (найдено) | ❌ | С | Новых авторов из РФ и РБ не регистрируют, даже после переезда | [helpdesk.templatemonster.com](https://helpdesk.templatemonster.com/restrictions-russian-belarusian-authors/) |

### 1.3 Способы оплаты

| Способ | Статус для РБ | Причина | Что именно | Источник |
|---|---|---|---|---|
| Payoneer | ❌ с 11.09.2026 | С (банки-партнёры) | USD отключён с 11.2025, переводы в банки РБ прекращены с 01.09.2026, аккаунты закрыты 11.09.2026 | [dev.by 07.08.2026](https://devby.io/be/news/payoneer-tsalkam-adkluchae-bankauskiya-peravody-u-belarus), [citydog 08.2026](https://citydog.io/post/zaden-poayineer-close/), [Наша Ніва](https://nashaniva.com/ru/402967) |
| PayPal | ❌ | П | В РБ только «Send only»: принимать и выводить нельзя | [myfin wiki](https://myfin.by/wiki/term/paypal-v-belarusi), [paypal.com/by](https://www.paypal.com/by/home) |
| Wise | ❌ с 2022 | С | «We're not able to serve customers in Belarus» | [wise.com help](https://wise.com/help/articles/3bzQ5PYiMU80HHPMFi0XAo/restrictions-for-customers-based-in-belarus) |
| Deel | ❌ (по вторичным данным) | С | В выдаче поиска справка Deel указывает Беларусь среди стран, где Deel недоступен, но сама страница отдаёт 403, и первоисточник прочитать не удалось | [help.letsdeel.com «Where Is Deel Available?»](https://help.letsdeel.com/hc/en-gb/articles/4407737728273-Where-Is-Deel-Available) |
| Remote.com | ❌ | С | Беларусь в списке «Contractor Management NOT cover» | [support.remote.com](https://support.remote.com/hc/en-us/articles/22494726617229) |
| Skrill | ❌ с 09.03.2026 | С (ЕС и UK) | Аккаунты белорусов закрыты, реквизиты банков РБ для возврата не принимают | [Зеркало 10.03.2026](https://news.zerkalo.io/economics/122264.html) |
| Neteller | ❌ с 10.03.2026 | С | Тот же владелец (Paysafe), та же причина | [Зеркало 11.03.2026](https://news.zerkalo.io/economics/122355.html) |
| Paysera | ❌ | С | Карты Paysera не работают в РБ с 11.02.2026, белорусов не обслуживают | [dev.by](https://devby.io/news/v-belarusi-perestali-rabotat-kartochki-paysera) |
| Revolut | ❌ | С | Только для легальных резидентов ЕС, счета на визе D закрываются по 19-му пакету | [dev.by](https://devby.io/news/revolut-zakryvaet-scheta-belarusam-i-rossiyanam-s-rabochimi-vizami-d) |
| Stripe Connect | ❌ | С | Беларуси нет в списке стран Stripe. Отсюда закрыты Mercor, Alignerr, OpenTrain и др. | [stripe.com/global](https://stripe.com/global) |
| Veem | ❌ с 06.04.2022 | С | — | [help.veem.com](https://help.veem.com/hc/en-us/articles/5323322452499-countries-update-belarus) |
| **Plane** (payroll для подрядчиков) | ⚠️ | — | «Plane currently supports payments to Belarus» с дополнительной проверкой на санкции. Работает, только если заказчик сам платит через Plane | [help.plane.com](https://help.plane.com/en/articles/6020895-how-the-situation-in-ukraine-and-russia-affects-payments) (06.10.2026) |
| **SWIFT в белорусский банк** | ⚠️ | П (дорого) | Брать **несанкционный** банк (Приорбанк и т. п.). Приорбанк принимает EUR под 3% с минимумом 120 BYN, USD под 3% с минимумом 200 BYN (с 27.01.2025). Банк отправителя может отказать, из Канады переводы не проходят. По отзывам, SWIFT принимают также Технобанк и БНБ-Банк | [telegraf.news 22.01.2025](https://telegraf.news/ehkonomika/priorbank-rezko-podnyal-minimalnuju-komissiju-za-perevody-v-dollarah-i-evro-komu-pridjotsya-zaplatit-ot-200-rublej/), [myfin](https://myfin.by/article/banki/priorbank-zametno-uvelicit-minimalnuu-komissiu-za-polucenie-swift-perevodov-35048), [citydog 08.2026](https://citydog.io/post/zaden-poayineer-close/) |
| Paysend | ⚠️ | — | Перевод с карты частного лица на карту в РБ (лучше всего в USD на Приорбанк). Подходит для прямого заказчика-человека, площадки так не платят | [citydog 08.2026](https://citydog.io/post/zaden-poayineer-close/) |
| Крипта (USDT/USDC) | ⚠️ юридически серо | С + закон РБ | Декрет №8 даёт физлицу **закрытый** перечень операций (майнинг, хранение, обмен, покупка или продажа за деньги, дарение), а **оплата токенами за работы и услуги в РБ не допускается**. Продавать можно только через резидентов ПВТ (Указ №367), P2P и иностранные биржи запрещены. ЕС запретил транзакции с белорусскими криптоплатформами с 24.05.2026, Binance с 23.08.2026 блокирует переводы с WhiteBird. Подробности в задании 6 | [REVERA «Крипторегулирование в Беларуси-2025»](https://revera.legal/uploads//LEGAL/Cryptocurrency-Regulation-in-Belarus-2025-1.pdf), [Lexology, 20-й пакет](https://www.lexology.com/library/detail.aspx?g=39874ee0-874e-4094-8bab-49623b50de13), [cryptoadventure 14.08.2026](https://cryptoadventure.com/binance-to-restrict-htx-exmo-and-nine-other-platforms-from-august-23/) |

Налоги для законного пути: **НПД** (налог на профессиональный доход РБ), 10% с дохода от физлиц и иностранных организаций, 20% только с белорусских организаций и ИП сверх 60 000 BYN в год. С 01.07.2026 минимальный налог 45 BYN в месяц, даже без дохода. Валюту пересчитывают по курсу НБРБ на дату получения, а чек формируют в приложении. Нельзя иметь нанимателя и привлекать других людей ([bii.by 01.10.2026](https://bii.by/docs/628473), [apr.gov.by](https://apr.gov.by/news/nalogi-i-sbory/nalog-na-professionalnyy-dokhod-chto-izmenitsya-s-1-iyulya-2026-goda)). Входит ли «обработка данных» в перечень видов деятельности НПД, **не проверено**: проверить в перечне до регистрации.

### 1.4 Удалённые job boards

| Сайт | Открывается из РБ | Нанимают ли «anywhere» с РБ | Формат для сторожа | Источник |
|---|---|---|---|---|
| Himalayas | ✅ | Почти нет. За 14,5 часа вышло 3000 вакансий: без ограничения по стране 182 (6%), с явным упоминанием РБ 2 (обе в EMEA-списке из 149 стран, сеньорские). Нашего типа 76, из них «worldwide» 5, и все экспертные | JSON API `https://himalayas.app/jobs/api?limit=20&cursor=…`, поле `locationRestrictions` (пустое значит worldwide) | выгрузка 06.10.2026 |
| We Work Remotely | ✅ | Лента почти вся «Anywhere in the World», но это разработка, дизайн, продажи и поддержка; за 7 дней 72 вакансии, нашего типа 0 | RSS `https://weworkremotely.com/remote-jobs.rss`, поле `region` | выгрузка 06.10.2026 |
| RemoteOK | ✅ | Публичный API с задержкой: 99 вакансий за 2 месяца, нашего типа 3 (iMerit annotator/evaluator без страны) | `https://remoteok.com/api` | выгрузка 06.10.2026 |
| Remotive | ✅ | Публичный API отдаёт 18 вакансий за месяц, «Worldwide» 5, нашего типа 0 | `https://remotive.com/api/remote-jobs` | выгрузка 06.10.2026 |
| Working Nomads | ✅ | 56 за месяц, «Global» 6; TELUS QA Rater только для своих языков (ES, FR, DE), Peroptyx по странам без РБ | `https://www.workingnomads.com/api/exposed_jobs/` | выгрузка 06.10.2026 |
| LinkedIn Remote | ✅ (у одного провайдера, Unet.by, был блок) | Premium для РБ недоступен. Те же проблемы с оплатой | — | [dev.by](https://devby.io/news/linkedin-zablokiroval-premium-podpisku-dlya-belarusov), [NapoleonCat 09.2026](https://napoleoncat.com/stats/linkedin-users-in-belarus/) |

Через что платят «anywhere»-работодатели: почти всегда через Deel, Remote, Wise, Payoneer или Stripe, а всё это для РБ закрыто (п. 1.3). Санкционная оговорка в описаниях встречается редко (4 из 3000 на Himalayas, например Aptiv прямо исключает граждан РБ), отсекает обычно платёжка на этапе оффера. Работает только SWIFT в EUR или Plane, если заказчик согласен.

## 2. Топ-5 вариантов (по реалистичности)

Ни один из них не тянет на «вау» по rubric: ИИ-разметку запрещено автоматизировать, а западные биржи упираются в вывод денег. Список для полноты, а не как рекомендация строить сторож.

### 1) Яндекс AI-тренер (русский язык, RLHF): российский путь
- **Путь:** заявка на [ai-trainers.ya.ru](https://ai-trainers.ya.ru/) → тест на грамотность и логику → практическое задание (оценить ответ модели, написать эталон) → интервью. Формы работы: трудовой договор на общем треке, ГПХ или самозанятость на платформе на экспертном.
- **Деньги в РБ:** при ГПХ или самозанятости РФ (гражданин ЕАЭС может стать самозанятым по российскому ИНН, но нужен номер +7 и, по ряду источников, документ о пребывании в РФ ([nalog-nalog.ru](https://nalog-nalog.ru/samozanyatye/mozhet-li-belorus-stat-samozanyatym-v-rossii/), [harant.ru](https://harant.ru/questions/q-226682/))) деньги приходят на карту российского банка, дальше перевод в РБ. Берёт ли Яндекс граждан РБ, живущих в Минске, **не проверено**: это вопрос к jobs@yandex-team.ru и к заданию 5.
- **Rubric:** работа задачами без звонков, но ручная, автоматизировать нельзя. Общий трек требует 4-8 часов в день и быть в чатах с 11 до 18 МСК, это минус. Оценка 5-6, при трудовом договоре по ТК РФ ещё −2.
- **Сколько:** на общем треке 36-120 тыс. ₽ в месяц за 4-8 часов в день, то есть примерно 430-750 ₽ в час. При 1-2 часах в день (30-60 ч в месяц), если ставка экспертного трека сопоставима: **≈13-45 тыс. ₽ в месяц**. Это прикидка, ставки самозанятых не проверены. Источник по вилке: [hh.ru/vacancy/128446894](https://hh.ru/vacancy/128446894).

### 2) Welo Data, беларусскоязычная сеть
- **Путь:** форма на [jobs.lever.co/weloglobal/63cff927…](https://jobs.lever.co/weloglobal/63cff927-d6ac-4769-b594-00686ede8e40) → попадание в пул → письмо с конкретным проектом, где сразу указаны объём, сроки и оплата → тесты по проекту.
- **Условие:** беларусский на уровне носителя и английский. Если Глеб не пишет по-беларусски свободно, вариант отпадает.
- **Деньги:** **не проверено.** Обычно Welo платит через Payoneer или PayPal, оба для РБ закрыты. До работы спросить у TalentRequests@welocalize.com, есть ли выплата SWIFT в EUR на счёт в РБ.
- **Сколько:** проекты эпизодические, ставка не опубликована. Реалистично **$0-150 в месяц** при 1-2 часах в день (оценка, не проверено).

### 3) Прямой заказчик с job board + SWIFT в EUR + НПД
- **Путь:** отклик на «worldwide»-вакансию (Himalayas, WWR) → до оффера проверить, что заказчик может платить SWIFT в EUR на счёт в РБ (или через Plane) и не требует Deel или Wise → валютный счёт и карта в Приорбанке → регистрация НПД, чек на каждое поступление по курсу НБРБ.
- **Подводные камни:** комиссия Приорбанка минимум 120 BYN за входящий EUR-перевод, поэтому платить надо реже и крупнее (от €1000). Банк отправителя может отказать. Договор с нерезидентом регистрируется в банке, если сумма выше 2000 базовых величин ([buyhold.by](https://buyhold.by/zarubezhnyy-frilans-rynok/), не первоисточник).
- **Rubric:** такие вакансии почти всегда для мидлов и сеньоров, нашего типа за выборку 0.
- **Сколько:** для новичка **≈0** в ближайшие месяцы.

### 4) Freelancer.com или PeoplePerHour + банковский вывод
- **Путь:** регистрация (прямого запрета РБ в правилах нет) → верификация → заказы → вывод банковским переводом. **Не проверено**, примет ли верификация паспорт РБ и дойдёт ли wire в USD до белорусского банка. У Freelancer минимум $500 плюс $25 комиссии, а Приорбанк берёт ещё минимум 200 BYN за USD.
- **Сколько:** при первых заказах на $20-50 вывод нереален. **$0** до первых $500 на балансе.

### 5) Contra + USDC: не рекомендую
- Contra платит в USDC почти во все страны, но для резидента РБ получение токенов как оплаты за услуги не входит в разрешённые Декретом №8 операции, а белорусские криптоплатформы под запретом ЕС (с 24.05.2026) и Binance (WhiteBird с 23.08.2026). Это не законный путь из РБ, подробности в задании 6.

## 3. Что из этого полезно сторожу

- Строить отдельный сторож под Outlier, Mercor, Upwork, Fiverr и похожие **не нужно**: из РБ они либо закрыты, либо без вывода денег.
- Дёшево добавить один источник: **Lever API Welo Data** `https://api.lever.co/v0/postings/weloglobal?mode=json`, фильтр по `categories.allLocations` или тексту `Belarus|Minsk|Belarusian`. Сейчас там 1 запись из 513. Тот же фильтр подходит для `https://api.lever.co/v0/postings/appen?mode=json` (сейчас 0 из 45). Новые записи появляются редко, проверять хватит раз в сутки.
- Himalayas API годится только как фон: фильтр `locationRestrictions` пустой или содержит `Belarus` плюс ключевые слова нашего типа дали 0 подходящих за 14,5 часа.
- В rubric можно добавить правило: «Вакансии платформ ИИ-разметки, недоступных из РБ (Outlier, Mercor, DataAnnotation, Toloka/Mindrift, Prolific, Alignerr), = 0» и «выплата только через Payoneer, Wise, PayPal или Deel = максимум 2».

## Не проверено
- Выплаты Welo Data, Invisible, micro1 и Productive Playhouse для РБ; Tipalti для РБ.
- Проходит ли паспорт РБ верификацию на Freelancer.com и PPH и доходит ли их wire в USD.
- Берёт ли Яндекс (экспертный трек) граждан РБ, живущих в Минске, и как устроена выплата.
- Есть ли у SWIFT Технобанка и БНБ-Банка тарифы ниже Приорбанка на октябрь 2026.
- Входит ли «обработка данных или разметка» в перечень видов деятельности НПД.
