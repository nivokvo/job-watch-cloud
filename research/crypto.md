# Крипто и web3: стоит ли строить сторож

Проверено 6 октября 2026 года: curl/WebFetch по площадкам, Telegram через t.me/s, веб-поиск. Ни на что не откликался и нигде не регистрировался.

## Вердикт

**Не строить.** Строить можно только если выполнены сразу три условия: (1) криптобанки РБ начали обслуживать физлиц; (2) Глеб оформил НПД или другую самозанятость и его вид деятельности позволяет получать токены от нерезидентов; (3) на площадках появились вакансии нашего типа. Сейчас не выполнено ни одно. Пересмотреть в январе 2027.

Почему:
1. **Нет потока.** За месяц на 8 площадках и в 12 Telegram-каналах нашлось 0 вакансий на 7+ по rubric.md и примерно 1 вакансия на 5. Начальный уровень в web3 сейчас означает стажировки разработчиков и трейдеров или модерацию живых чатов (её рубрика режет).
2. **Деньги нельзя законно получить.** На 06.10.2026 физлицо в РБ не может принимать USDT как оплату за работу: это нарушение Декрета №8, штраф 20-50 базовых величин и конфискация дохода. Законный путь через криптобанки (указ №19) действует с 18.07.2026 только на бумаге: два криптобанка одобрены Наблюдательным советом ПВТ 28.09.2026, но ещё не зарегистрированы в Нацбанке.
3. **Много скама.** Среди немногих объявлений «без опыта» заметная доля имеет признаки мошенничества (см. ниже). Новичку без опыта в крипте отбирать их вручную дорого.

Что можно сделать дёшево: перенести фильтр признаков скама (раздел 3) в основной сторож rabota.by. Крипто-схемы «заработка» попадаются и там.

## 1. Площадки

Наш тип: data entry, research, content ops, QA, community data, модерация без живых чатов, ончейн и airdrop ресёрч, тестирование. Без звонков и live-чатов.

| Площадка | Открывается | Формат для парсинга | Всего в неделю | Нашего типа в неделю | Ограничения по стране |
|---|---|---|---|---|---|
| cryptocurrencyjobs.co | да, без защиты | RSS `https://cryptocurrencyjobs.co/index.xml` (title, link, pubDate, description); фильтров в RSS нет (`/research/index.xml` отдаёт 404) | ~14 (56 за 08.09-05.10) | 0 (ближе всего: Sky Mavis «Freelance Travel Spend & Market Explorer», стажировка по контенту у Maple) | указываются в вакансии; в основном США/ЕС |
| cryptojobslist.com | сайт за Cloudflare (403 для curl), RSS работает | RSS `https://cryptojobslist.com/rss`: последние 100, **без pubDate**, есть `media:location` и полный HTML описания | десятки (точно не посчитать, дат нет) | 0 за месяц | много «US only», офисы Дубай/Сингапур/Гонконг |
| web3.career | да, сервер отдаёт по 15 строк на страницу | HTML: `tr[data-jobid]`, `h2` название, `h3` компания, `time[datetime]`, `.cell-salary`. API: `https://web3.career/api/v1?token=TOKEN&tag=...&remote=true&limit=100` (бесплатный токен по email, есть `.xml`) | entry-level ~10 (30 за 15.09-06.10) | 0. Рубрика `/moderator-jobs` — около 15 вакансий за 2 года, последняя 01.08.2026; `/data-entry-jobs` пуста | в ленте `/remote-jobs` много не-крипто (Zscaler, Zinnia) |
| remote3.co | да | RSS `https://www.remote3.co/api/rss` | ~0: 8 записей, последняя 11.09.2026 | 0 | площадка фактически мертва |
| RemoteOK, тег crypto | да | JSON `https://remoteok.com/api?tag=crypto` (первый элемент массива служебный) | ~2 (52 за 22.04-02.10) | 0; единственная «junior» вакансия за неделю со скам-признаками | разные |
| cryptojobs.com | WebFetch открывает, curl через прокси получает обрыв соединения | HTML `/jobs?keyword=...` | не посчитано | модерация: 1 вакансия за 5 месяцев ($800/мес), остальные 2-3-летней давности | разные |
| LaborX (крипто-фриланс, оплата в USDT через эскроу) | да | HTML `laborx.com/jobs/<категория>`, id в URL `-(\d+)`, даты ISO в странице | ~100 по росту id (104715 на 15.09 → 105010 на 06.10), публично видно ~12 | data-entry: 4 заказа с 2023 года. Много мусора: «аренда iOS/Apple-аккаунта», «нужен человек из США» | в правилах слово Belarus не нашёл; запрет на криптоплатежи в РБ действует в любом случае |
| JobStash, Dework, jobs.ethereum.org, beincrypto/jobs | JobStash отдаёт 4 МБ инженерных вакансий (часто не крипто); Dework — пустая SPA; ethereum.org — 502; beincrypto — 403 | — | — | 0 | — |

### Telegram

Англоязычные:
- **@cryptojobslist** (61,9K): ~111 постов за 30 дней, половина из них советы и повторы. За месяц нашего типа 0. Были Fiber Community Ambassador (амбассадорство), Turkish Social Media (нужен часовой пояс Турции), CLOWN Token Telegram CM ($15-30/час, живой чат).
- **@web3hiring** (61K): 3-4 дайджеста в день по ~5 названий, почти всё senior.

Русскоязычные. Это одна сеть, вакансии дублируются по 3-6 раз (подпись «Другие наши сообщества: Blockchain Hunter, Career Crypto, Крипто Head Hunter, Crypto Jobs, WEB 3.0 JOB, Crypto Job»):
- **@workingincrypto** (28,1K), **@careers_crypto** (26K), **@cryptoheadhunter** (20,5K), **@job_web3** (10,9K), **@opento_crypto** (8,9K), **@web30job** (7K), **@cryptovakansii** (5,3K), **@rabotaweb3** (2,5K), **@cryptojobsh** (1,8K).
- Всего около 105 уникальных вакансий за 30 дней (≈25 в неделю). Преобладают продажи и BD, маркетинг, разработчики, чат-операторы (одна и та же Genesis ходит по всем каналам), трейдинг.
- Парсинг: `https://t.me/s/<канал>`, посты в `.tgme_widget_message_text`, дата в `time[datetime]`, листание через `?before=<id>`. Защиты нет.

Самое близкое к нашему типу за месяц (оценка по rubric.md):

| Вакансия | Где | Оценка | Почему |
|---|---|---|---|
| Payments Crypto Marketing Research Analyst | t.me/workingincrypto/3141 | 5 | Ядро наше: собрать магазины с криптопроцессингом и внести тарифы и монеты в таблицу. Но есть переговоры в мессенджерах, «стабильный онлайн» по МСК, ТК РФ |
| Антифрод-оператор | t.me/cryptoheadhunter/6140 | 4 | Мониторинг транзакций и таблицы, но нужен опыт в антифроде и чарджбэках |
| Manual QA, Bitfarms | t.me/cryptojobsh/104 | 4 | «Любое GEO», до 2500 USDT, но нужен опыт QA, а оплата в крипте для РБ незаконна |
| Researcher / идейник под токен-запуски | t.me/workingincrypto/3146 | 3 | Креатив, мемкоины, график «за рынком», оплата в USDT |
| AML-аналитик (KYT) | t.me/web30job/1099 | 2 | От 2 лет опыта в Chainalysis/TRM |
| CLOWN Token Telegram Community Manager | cryptojobslist | 2 | Живой чат |
| Junior Crypto Arbitrage (AUREX), Empire Assets, Omega Enterprises | t.me/rabotaweb3/2527, RemoteOK | 0 | Признаки скама, см. ниже |

## 2. Реально ли новичку

Почти нет, и вакансий нашего формата в этой нише не видно:
- Начальный уровень без опыта в web3 сводится к модерации Discord и Telegram, комьюнити и поддержке. Это живые чаты и смены, рубрика ставит максимум 3.
- Research и аналитика требуют реальной истории в крипте: свой кошелёк с историей сделок, опыт запусков, ончейн-инструменты, «это не обучающая позиция» (t.me/workingincrypto/3136).
- Конкуренция: рекрутеры пишут, что на одну начальную позицию «сотни людей», а «100 откликов на крипто-бордах дают ноль ответов» ([cryptorecruit, 2026](https://www.cryptorecruit.com/news/how-to-break-into-web3-without-experience/)).
- Типичный вход для русскоязычных: амбассадорские программы с оплатой токенами проекта, потом модерация примерно от 500 USDT в месяц ([teletype-гайды 2024-2025](https://teletype.in/@nocashnocap/rabotavkripte)). Для Глеба это и живой чат, и незаконная оплата.

## 3. Мошенничество: схемы и фильтр

Схемы, актуальные в 2025-2026:
1. **Task scam («оптимизация заданий»).** Лайки, оценки товаров или отелей, «уровни VIP». Сначала платят $50-60 в USDT, потом просят «депозит», чтобы вывести деньги. В 2024 году ~20 тыс. жалоб в FTC против 5 тыс. в 2023 ([BleepingComputer/FTC](https://www.bleepingcomputer.com/news/security/ftc-warns-of-online-task-job-scams-hooking-victims-like-gambling/), [Bitdefender](https://www.bitdefender.com/en-au/blog/hotforsecurity/task-scams-fake-online-jobs)).
2. **Фейковое собеседование с вредоносным софтом.** Просят поставить «приложение для звонков» (GrassCall и ChainSeeker.io от группы Crazy Evil; Relay в сентябре 2026) или вставить команду в Терминал macOS. Софт крадёт кошельки, пароли и сессии Telegram ([Decrypt](https://decrypt.co/308027/crazy-evil-hackers-create-fake-web3-firm-drain-job-seekers-crypto-wallets), [CyberSecurityNews 15.09.2026](https://cybersecuritynews.com/fake-recruiter-web3-developers/)).
3. **Тестовое как репозиторий (Contagious Interview, КНДР).** Просят «склонировать и запустить» проект или `npm install`. Только во второй волне было около 200 вредоносных npm-пакетов ([SecurityAffairs](https://securityaffairs.com/185170/apt/contagious-interview-campaign-expands-with-197-npm-ppackages-spreading-new-ottercookie-malware.html), [Microsoft](https://www.microsoft.com/en-us/security/blog/?p=145718)).
4. **«Кошелёк для зарплаты» и сид-фраза.** Присылают сид-фразу от «рабочего» кошелька с USDT. Чтобы вывести, нужно докинуть газ, а газ уходит sweeper-боту. Обратный вариант: просят твою сид-фразу или приватный ключ «для начисления» ([ForkLog](https://forklog.com/news/glava-binance-predupredil-o-novom-skame-s-sid-frazami)).
5. **Drainer-ссылки.** «Подключи кошелёк и подпиши, чтобы получить оплату, пройти верификацию или claim». Подпись permit/approve/setApprovalForAll отдаёт токены.
6. **Трейдинг «с нуля с наставником».** Высокая зарплата без опыта, «реальные торговые операции», «до 20 часов в неделю». Дальше просят пополнить счёт на «платформе компании». Пример: Empire Assets и Omega Enterprises на RemoteOK — одинаковый шаблон текста, одинаковая зарплата $60-80k, ссылки вида `/work/remoteok`, у обоих доменов (empireground.com, omegadg.com) одна дата изменения в RDAP: 03.09.2026.
7. **Дропы и аренда аккаунтов.** «Нужен аккаунт Apple/iOS в аренду», «нужен человек из США/Канады», «оформи карту или KYC на себя». В РБ передача карт и доступа к счетам за вознаграждение подпадает под ст. 222 УК ([onliner](https://tech.onliner.by/2023/01/23/internet-banking-za-dengi)).
8. **Платное «обучение», «страховой взнос», покупка «рабочего аккаунта».**

Автофильтр для сторожа. Регистр не важен, проверять текст вакансии, ссылки и первое сообщение рекрутера.

Жёсткий отказ (оценка 0, в Telegram не слать):
```
депозит|пополн\w* (баланс|счёт|счет)|активаци\w* аккаунта|оплат\w* (обучени|курс|доступ)|страхов\w* взнос
deposit|top[- ]?up|activation fee|training fee|upgrade (your )?level|vip level|combo (task|order)
optimi[sz]ation tasks?|задани\w* по оптимизации|лайк\w* за деньги|оцен\w* (товар|отел)\w* за
seed[- ]?phrase|сид[- ]?фраз|мнемони|private key|приватн\w* ключ|recovery phrase
connect (your )?wallet|подключ\w* кошел|sign (the )?(message|transaction) to|claim (your )?(salary|reward|payment)
(download|install|скача\w*|установ\w*) .{0,40}(meeting|call|interview|звонк|собеседован)\w* (app|software|приложени)
npm (i|install)|git clone .{0,80}(run|запуст)|terminal|терминал.{0,40}(встав|paste)
аренд\w* (аккаунт|карт)|(rent|need) .{0,20}(apple|ios|upwork|account)|someone from (usa|us|canada)|оформ\w* карт\w* на себя
```

Мягкие флаги (минус 3, в карточке пометка «⚠ похоже на скам», Opus перепроверяет):
- нет опыта + зарплата от $1000/мес или от $50k/год + неполная занятость;
- трейдинг, арбитраж, «торговые операции» + «обучение с нуля» или «наставник»;
- контакт только личный @username, WhatsApp или Gmail, нет сайта или домена компании;
- домен ссылки отклика моложе 12 месяцев (RDAP `https://rdap.org/domain/<домен>`, событие `registration`) или не совпадает с доменом компании;
- тот же шаблон текста у разных «компаний» (совпадение шинглов больше 70%);
- известная компания (Binance, Bybit, OKX…), но отклик не через их career-домен;
- «оплата в токенах проекта» или «амбассадор» без фиксированной ставки.

## 4. Законность и схема вывода денег (РБ, октябрь 2026)

Что действует:
- **Декрет №8 (2017):** физлицо может владеть токенами, майнить, менять одни токены на другие и покупать или продавать их за деньги через резидентов ПВТ. Токены не средство платежа. Получать их как оплату за работу или услуги физлицу **нельзя**. МНС в 2026 году прямо писало: «физлица могут только владеть, майнить, хранить и менять токены» ([dev.by, 07.04.2026](https://devby.io/news/dohody-v-kripte)).
- **Ответственность:** КоАП ст. 13.3 ч. 3, штраф 20-50 БВ и конфискация до 100% дохода. Реальный случай: 5536 USDT от московской компании, проданные через P2P ([pnkbel.by](https://pnkbel.by/mns/zarplata_kripta/)). Налог на доход от незаконных операций 26% ([jurisprudent.by, 26.03.2026](https://jurisprudent.by/kriptovalyuta-v-belarusi/); [myconsult.by, 28.06.2026](https://myconsult.by/articles/crypto/crypto-belarus-2026/)).
- **Указ №367 (17.09.2024):** покупать и продавать токены за деньги находясь в РБ можно только через резидентов ПВТ. P2P запрещён, как и зарубежные биржи с выводом на белорусские счета ([jurisprudent.by](https://jurisprudent.by/kriptovalyuta-v-belarusi/)).
- **Банки:** в апреле 2025 были массовые блокировки P2P, Нацбанк вводит правило «один клиент — одна карта», антифрод блокирует подозрительные операции автоматически ([vc.ru](https://vc.ru/marketing/2294081-kupit-kriptu-v-2025-godu), [neg.by](https://neg.by/novosti/otkrytj/kriptorynok-pod-kontrolem-natsbank-vvodit-pravilo-odin-klient-odna-karta/)). Значит, если гнать USDT через P2P на карту, есть реальный риск блокировки карты.
- **Санкции ЕС:** с 24.02.2025 (Регламент 2025/392) провайдерам из ЕС запрещено открывать криптокошельки, счета и хранение гражданам и резидентам РБ ([EUR-Lex](https://eur-lex.europa.eu/eli/reg/2025/392/oj/eng)). Биржи с лицензией MiCA откажут; остаются только некастодиальные кошельки.
- **Налоги:** операции через резидентов ПВТ для физлица 0% без декларации; доход через зарубежные площадки 13% с декларацией до 31 марта ([myconsult.by](https://myconsult.by/articles/crypto/crypto-belarus-2026/)).

Новое с 2026 года, указ №19 от 16.01.2026 «О криптобанках»:
- С **18.07.2026** самозанятые (включая плательщиков НПД), ремесленники и агроэкотуризм могут **получать** токены от нерезидентов по внешнеэкономическим договорам, но **только на криптоаккаунт в белорусском криптобанке** ([ardenna.by](https://ardenna.by/law/samozanjatye-na-npd-smogut-ispolzovat-kriptovaljutu-v-kachestve-sredstva-rascheta-cherez-belorusskie-kriptobanki/)).
- Статус: 28.09.2026 Наблюдательный совет ПВТ одобрил первых двух резидентов в статусе криптобанка. Названия не раскрыты, нужна ещё регистрация в Нацбанке, срок начала работы с физлицами не объявлен ([bits.media, 29.09.2026](https://bits.media/v-belarusi-zaregistrirovany-pervye-kriptobanki/)). **На 06.10.2026 этим путём воспользоваться нельзя.**

Схема, когда криптобанки заработают (каждый шаг проверить заново):
1. Встать на учёт как плательщик НПД в приложении «Налоги»/«Профессии». Входит ли сбор и обработка данных для иностранного заказчика в перечень видов деятельности для НПД (постановление СовМина №457), **не проверено**.
2. Подписать с иностранным работодателем письменный внешнеэкономический договор оказания услуг.
3. Открыть криптоаккаунт в криптобанке и дать работодателю адрес только этого аккаунта.
4. Работодатель платит USDT. Продать за BYN внутри криптобанка и вывести на свою карту.
5. НПД 10% с суммы по курсу на дату получения ([ardenna.by](https://ardenna.by/nalog-na-prof-dohod/)). Применяется ли ставка 10% к иностранным организациям, **не проверено**.

Биржи-резиденты ПВТ, через которые законно продают токены, полученные законно (сведения агрегатора [profinvestment.com, 14.04.2026](https://profinvestment.com/withdraw-crypto-belarus-card/); сайты бирж — SPA, сам не проверил):
- **Bynex:** Visa, Mastercard, Белкарт, ЕРИП, «Оплати»; комиссия до 0,25%; USDT в сетях ERC-20, TRC-20, BEP-20.
- **Whitebird:** карты Альфа-Банка и Беларусбанка; спот до 0,3%, вывод до 1,5%; минимум около 35 BYN.
- **Free2Ex:** до 0,25%. **Dzengi.com** (бывший Currency.com) и **Tradex:** до 0,2%.
- На всех обязательна верификация. Источник USDT, полученных в качестве зарплаты, могут проверить («могут заставить отчитаться, откуда “жемчуг”», [dev.by](https://devby.io/news/dohody-v-kripte)). До появления криптобанков такой доход незаконен и при честном объяснении источника.

Итог по деньгам: сейчас законно получить USDT за работу нельзя. Обходы (P2P, зарубежная биржа, «друг продаст») нарушают указ №367 и грозят штрафом, конфискацией и блокировкой карты. Если иностранный работодатель интересен, законный вариант — оплата в фиате на белорусский счёт (это тема задания 7).

## Источники

- Площадки: проверены напрямую 06.10.2026 — cryptocurrencyjobs.co/index.xml, cryptojobslist.com/rss, web3.career (+ [документация API](https://docs.bondex.app/api-reference)), remote3.co/api/rss, remoteok.com/api?tag=crypto, laborx.com/jobs, [cryptojobs.com](https://cryptojobs.com/jobs?keyword=moderator), t.me/s/… для каналов, перечисленных выше.
- Право РБ: [myconsult.by](https://myconsult.by/articles/crypto/crypto-belarus-2026/), [jurisprudent.by](https://jurisprudent.by/kriptovalyuta-v-belarusi/), [yur-24.by](https://yur-24.by/articles/kripta-v-belarusi-2026-0-v-pvt-nalogi-i-kriptobanki/), [ardenna.by (указ №19)](https://ardenna.by/law/samozanjatye-na-npd-smogut-ispolzovat-kriptovaljutu-v-kachestve-sredstva-rascheta-cherez-belorusskie-kriptobanki/), [ardenna.by (НПД)](https://ardenna.by/nalog-na-prof-dohod/), [dev.by](https://devby.io/news/dohody-v-kripte), [pnkbel.by](https://pnkbel.by/mns/zarplata_kripta/), [bits.media](https://bits.media/v-belarusi-zaregistrirovany-pervye-kriptobanki/), [neg.by](https://neg.by/novosti/otkrytj/v-belarusi-gotovyatsya-zaregistrirovat-pervye-dva-kriptobanka/), [EUR-Lex 2025/392](https://eur-lex.europa.eu/eli/reg/2025/392/oj/eng), [revera.legal](https://www.revera.legal/?p=4022).
- Скам: [FTC через BleepingComputer](https://www.bleepingcomputer.com/news/security/ftc-warns-of-online-task-job-scams-hooking-victims-like-gambling/), [Malwarebytes](https://www.malwarebytes.com/blog/news/2025/03/i-spoke-to-a-task-scammer-heres-how-it-went), [Decrypt](https://decrypt.co/308027/crazy-evil-hackers-create-fake-web3-firm-drain-job-seekers-crypto-wallets), [CyberSecurityNews](https://cybersecuritynews.com/fake-recruiter-web3-developers/), [SecurityAffairs](https://securityaffairs.com/185170/apt/contagious-interview-campaign-expands-with-197-npm-ppackages-spreading-new-ottercookie-malware.html), [AMLBot](https://blog.amlbot.com/hacked-by-a-dream-job-a-case-study-on-web3-job-scams/), [ForkLog](https://forklog.com/news/glava-binance-predupredil-o-novom-skame-s-sid-frazami).
