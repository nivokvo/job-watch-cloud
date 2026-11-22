#!/usr/bin/env bash
# Claude в облаке ходит через тот же сервер, что и на маке. Поднимает xray-клиент (конфиг из секрета XRAY_CLIENT_JSON),
# проверяет, что API Anthropic видит нужную страну, и отдаёт прокси через CLAUDE_HTTPS_PROXY (его берёт replier.claude).
# Не вышло — падает: напрямую Claude не зовём. В лог не пишет ни адресов, ни ключей: репо и логи публичные.
set -euo pipefail
V=v26.11.9
SHA=b651f7e1d9966ee2c1b1ee1bf8b52c72771824d3065dce96bbc8bcc19ed95f82
D="$RUNNER_TEMP/xray"
mkdir -p "$D"
[ -n "${XRAY_CLIENT_JSON:-}" ] || { echo "нет секрета XRAY_CLIENT_JSON"; exit 1; }
curl -fsSL -o "$D/x.zip" "https://github.com/XTLS/Xray-core/releases/download/$V/Xray-linux-64.zip"
echo "$SHA  $D/x.zip" | sha256sum -c --quiet -
unzip -q -o "$D/x.zip" xray -d "$D"
(umask 077; printf '%s' "$XRAY_CLIENT_JSON" > "$D/c.json")
nohup "$D/xray" run -c "$D/c.json" >/dev/null 2>&1 &
for _ in $(seq 40); do (echo > /dev/tcp/127.0.0.1/12334) 2>/dev/null && break; sleep 0.25; done
rm -f "$D/c.json"
loc=$(curl -s -m 20 -x http://127.0.0.1:12334 https://api.anthropic.com/cdn-cgi/trace | sed -n 's/^loc=//p')
[ "$loc" = "DE" ] || { echo "Claude не через сервер (loc=${loc:-нет ответа}), Claude не запускаю"; exit 1; }
echo "CLAUDE_HTTPS_PROXY=http://127.0.0.1:12334" >> "$GITHUB_ENV"
echo "Claude через сервер: loc=DE"
