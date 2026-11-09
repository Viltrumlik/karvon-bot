# Karvonboshi · Караванщик · Caravan Master

![Python: 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) ![aiogram: 3](https://img.shields.io/badge/aiogram-3-26A5E4?logo=telegram&logoColor=white) ![tests: 242](https://img.shields.io/badge/tests-242-2ea44f) ![languages: uz · ru · en](https://img.shields.io/badge/languages-uz%20%C2%B7%20ru%20%C2%B7%20en-orange) ![license: proprietary](https://img.shields.io/badge/license-proprietary-lightgrey)

A text-only **Silk Road trading roguelite** that you play entirely inside a Telegram chat, with inline buttons.
You inherit a debt-ridden caravan in 1409 Samarkand and have 100 days to repay a ruthless moneylender by buying
low, selling high and surviving the roads between seven cities. It is hard on purpose: prices react to every bale
you trade, the desert drinks your water, unpaid guards desert you, and a bandit chief is hunting your caravan.

- 🐪 **Trading sim with a living market**: 7 cities, 7 roads, 10 goods. Every trade moves the price, prices drift back over time, and gluts, shortages, festivals and rumors shake things up.
- 🧭 **Survival logistics**: camels (cargo and food capacity), provisions (doubled in the desert), guards with daily wages, morale, reputation.
- 💳 **A debt clock**: 3% interest every 10 days, one optional loan, the deadline on day 100.
- ⚡ **17 road events, 6 city events and 5 story encounters**, each with 2–4 choices and visible consequences.
- 🗝 **A story**: the Black Wind bandit, a guild master's secret, your uncle's letter. **8 endings** with epilogues, one of them secret.
- 🌐 **Three languages**: Uzbek (Latin), Russian and English, switchable at any time.
- 🎚 **Three difficulties** (Normal, Hard, Legendary), Ravshan-ota's tutorial tips, and a `/top` leaderboard.
- 📱 **Built for Telegram**: one message edited in place, a compact status header, and buttons that survive double taps and stale messages.

## What it looks like

The first city screen on Hard, captured from the console mode. The header shows the day, money, cargo,
food, morale and debt. In Telegram the buttons are inline buttons under a single message that the bot
edits in place.

> 📅 1/100 · 💰 400 · 📦 0/40 · 🍞 40 · 😊 70 · 💳 3,000
>
> 🧓 **Ravshan-ota:** Your uncle left us four camels, an old man, and a debt of 3,000 tanga. Every ten days it grows, and on day 100 Yusuf takes everything. Buy where a good is made, sell where people miss it. Paper is cheap here; Bukhara and Tashkent are five days away.
>
> 🏙 **Samarkand**
>
> The blue domes of the Registan glitter; paper mills creak along the Siab canal. Yusuf Sarrof keeps his ledger here.
>
> `🏪 Market` `🐫 Stable` `🛡 Guards` `🍞 Provisions` `🏨 Caravanserai` `🫖 Teahouse` `💰 Moneylender` `🗺 Travel` `📜 Status` `📒 Ledger` `☰ Menu`

## Qisqacha · Кратко

**🇺🇿 O'zbekcha.** Telegram chatining o'zida inline tugmalar bilan o'ynaladigan Ipak yo'li savdo o'yini. 1409-yil, Samarqand: amakingizdan qarzga botgan karvon meros qoldi. 100 kun ichida sudxo'r Yusuf Sarrofga qarzni qaytarishingiz kerak: molni arzon joyda oling, qimmat joyda soting, cho'l yo'llarida omon qoling. 7 shahar, 10 xil mol, 28 ta voqea, 8 ta yakun va uch qiyinlik darajasi. Til istalgan payt `/lang` buyrug'i bilan almashtiriladi.

**🇷🇺 Русский.** Торговый роглайт о Великом шёлковом пути, в который играют прямо в чате Telegram, кнопками. Самарканд, 1409 год: вам достался караван в долгах. За 100 дней нужно вернуть долг ростовщику Юсуфу: покупайте дёшево, продавайте дорого и переживите дороги пустыни. 7 городов, 10 товаров, 28 событий, 8 концовок и три уровня сложности. Язык меняется в любой момент командой `/lang`.

## Story teaser

> Transoxiana, 1409. Hamid, the most famous caravan master of Samarkand, died «in a sandstorm».
> He left you four camels, his old guide Ravshan-ota, and a debt of 3,000 tanga to the moneylender Yusuf Sarrof.
> Qorabek, the smiling head of the Bukhara guild, offers to take the caravan off your hands.
> Out in the Kyzylkum, the riders of Qora Shamol, the Black Wind, are waiting for someone.
> Was it really a sandstorm?

## How to play

1. `/start`, pick your language, then **New game** and a difficulty (**Hard** is the intended experience).
2. In a city, the hub offers: 🏪 Market, 🐫 Stable, 🛡 Guards, 🍞 Provisions, 🏨 Caravanserai (rest), 🫖 Teahouse
   (rumors), 💰 Moneylender (Samarkand), 🗺 Travel, 📜 Status, 📒 Ledger.
3. **Buy where a good is made and sell where it is missed.** Each purchase raises the price, so spread your money over
   several goods. The ledger remembers the prices you have seen.
4. **Travel** to a neighbouring city. The confirmation screen shows days, danger, food needed and wages.
   On the road, ▶️ moves one day and ⏩ rides on until something happens.
5. **Events** stop the caravan. Read the odds (bandit strength is shown) and choose.
6. Return to **Samarkand** and pay Yusuf before the end of day 100. After that, keep trading until day 150 or
   🏁 retire. How rich you are, and what you uncovered, decide your ending.

Commands: `/start` menu · `/status` caravan · `/lang` language · `/restart` new caravan · `/help` rules · `/top` leaderboard.

## Requirements

- Python **3.12**
- [aiogram](https://docs.aiogram.dev/) 3.x (installed from `requirements.txt`); storage uses the standard library `sqlite3`
- For the real bot, a token from [@BotFather](https://t.me/BotFather). Playing locally needs no token.

## Install and run

```bash
git clone https://github.com/Viltrumlik/karvon-bot.git && cd karvon-bot
python3.12 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt     # or requirements.txt for production only
```

### Run the real Telegram bot

1. In Telegram, talk to **@BotFather**, send `/newbot`, and copy the token.
2. Configure and start:

```bash
cp .env.example .env
# edit .env and set BOT_TOKEN=123456789:AA...
.venv/bin/python -m karvon
```

Environment variables (from the environment or `.env`):

| Variable | Default | Meaning |
|---|---|---|
| `BOT_TOKEN` | (required) | Bot token from @BotFather |
| `TELEGRAM_API_BASE` | Telegram cloud | Custom Bot API server base URL, e.g. `http://127.0.0.1:8081` |
| `DB_PATH` | `./karvon.db` | SQLite database file |

The bot uses long polling and registers its command menu in Uzbek, Russian and English on startup.

### Play locally without a token (console mode)

`scripts/console_play.py` starts a local fake Telegram Bot API server and the *real* bot polling it, then lets
you play in the terminal: each bot message is printed with numbered buttons. Type a number to press a button;
any other text is sent as a chat message (`/status`, `/lang`, …); `q` quits.

```bash
.venv/bin/python scripts/console_play.py              # language picker first
.venv/bin/python scripts/console_play.py --lang uz    # pretend your Telegram app is in Uzbek
```

Automated smoke test: press N random buttons (biased towards progress so roads, events and endings get exercised,
`--uniform` for pure random). Exits non-zero on any bot error, unanswered callback or Bot API error:

```bash
.venv/bin/python scripts/console_play.py --auto 300 --lang uz
```

## Tests

```bash
.venv/bin/pytest -q
```

- `tests/test_engine.py`, `tests/test_endings.py`: price movement, capacity, provisions and wages, interest schedule,
  fight bounds, every event choice, bad input, all 8 endings from prepared states, serialisation, determinism.
- `tests/test_i18n.py`: identical keys and placeholders across uz/ru/en, no empty strings, every engine key present.
- `tests/test_render.py`: every screen in all three languages renders without unfilled placeholders, with balanced
  HTML, text ≤ 4096 characters and callback data ≤ 64 bytes.
- `tests/test_e2e_polling.py`: the real aiogram `Dispatcher.start_polling` against `tests/fake_telegram.py`
  (a small aiohttp Bot API: getMe, getUpdates long-poll, sendMessage, editMessageText, answerCallbackQuery,
  setMyCommands, deleteMessage …). It plays /start → language → new game → market → buy → travel → days → event →
  arrival in Uzbek and English, and checks stale buttons, double taps, commands and the edit-failure fallback.
- `tests/test_storage.py`: SQLite sessions and leaderboard.

## Balance

`scripts/balance.py` runs a greedy trading bot and a do-nothing bot over many seeds per difficulty
(`--seeds 300` by default). The greedy bot knows each city's typical prices and its own ledger, plans cargo for the
best of the next two legs, buys provisions and a few guards, rests when needed and runs home to pay Yusuf.
It is a decent but not expert player: it never takes contracts, never uses rumors and avoids the story.

```bash
.venv/bin/python scripts/balance.py            # about 3 minutes
```

Final table (300 seeds per difficulty):

| Bot | Difficulty | Runs | Debt paid | Avg payoff day | Median final net worth | Endings |
|---|---|---|---|---|---|---|
| greedy | normal | 300 | 72.3% | 87.7 | 3,824 | E2:98 E3:110 E5:63 E6:19 E7:10 |
| do-nothing | normal | 300 | 0.0% | — | -2,526 | E5:300 |
| greedy | hard | 300 | 34.0% | 90.9 | -674 | E2:18 E3:82 E5:164 E6:28 E7:8 |
| do-nothing | hard | 300 | 0.0% | — | -3,279 | E5:300 |
| greedy | legendary | 300 | 10.3% | 94.1 | -2,081 | E2:2 E3:28 E5:231 E6:23 E7:16 |
| do-nothing | legendary | 300 | 0.0% | — | -4,373 | E5:300 |

Endings: E2 Honest Trader, E3 Free but Poor, E5 Debt Slave, E6 Lost in the Sands, E7 Mutiny.
The bots refuse Qorabek's offer and never chase the story, so E1 (Legend), E4 (Qorabek's Clerk) and E8 (Black Wind's
Partner) only appear in human play; the tests reach all eight endings.

## Project structure

```
karvon-bot/
├── karvon/
│   ├── __main__.py        # python -m karvon (reads BOT_TOKEN, TELEGRAM_API_BASE, DB_PATH)
│   ├── config.py          # env / .env loading
│   ├── storage.py         # sqlite3: players (sessions) and runs (leaderboard)
│   ├── engine/            # pure game logic, no aiogram import
│   │   ├── data.py        # cities, roads, goods, difficulties, tunable constants
│   │   ├── state.py       # GameState dataclass (JSON), Result objects
│   │   ├── rng.py         # splitmix64 RNG whose state lives in GameState
│   │   ├── market.py      # prices, impact, drift, rumors, ledger
│   │   ├── events.py      # 17 road + 6 city + 5 story events, fights, triggers
│   │   ├── actions.py     # buy, sell, travel_start, next_day, ride_on, resolve_event_choice, pay_debt, ...
│   │   ├── endings.py     # 8 endings, net worth, score
│   │   └── core.py        # shared helpers (snapshots, cargo, clamping)
│   ├── i18n/              # uz.py, ru.py, en.py (identical keys) + t(lang, key, **params)
│   └── bot/               # aiogram layer
│       ├── app.py         # Bot/Dispatcher factory, command registration, polling
│       ├── handlers.py    # commands, callbacks, per-user lock, edit-in-place
│       ├── render.py      # screens -> HTML text + buttons
│       ├── keyboards.py   # "<seq>|<action>" callback data (< 64 bytes)
│       └── session.py     # per-player UI session stored as JSON
├── scripts/
│   ├── balance.py         # greedy and do-nothing bots over many seeds
│   └── console_play.py    # play in the terminal / --auto smoke test (no token)
├── tests/                 # pytest suite, including fake_telegram.py
├── docs/GDD.md            # game design document (source of truth)
├── requirements.txt, requirements-dev.txt, .env.example, pytest.ini
└── LICENSE
```

## Design document

The full design (story, characters, world, economy, events, endings and tuned numbers) is in
[docs/GDD.md](docs/GDD.md).

## More games by Viltrumlik

- [Last Shore](https://github.com/Viltrumlik/last-shore): pixel-art survival city-builder on a drying sea (browser)
- [Night Express](https://github.com/Viltrumlik/night-express): text-adventure mystery on an overnight train (terminal)
- [Dispatch 112](https://github.com/Viltrumlik/dispatch-112): real-time emergency-dispatch sim (terminal)
- [Zero to Mars](https://github.com/Viltrumlik/zero-to-mars): 3D founder life-sim Telegram WebApp

## License

Copyright (c) 2026 Viltrumlik. All rights reserved. No permission is granted to use, copy, modify or distribute
this software without the author's written permission. See [LICENSE](LICENSE).
