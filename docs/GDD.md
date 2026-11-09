# Karvonboshi / Караванщик / Caravan Master — Game Design Document

## 1. Pitch
A text-only **Silk Road trading roguelite** played entirely inside a Telegram chat with inline buttons.
You inherit a debt-ridden caravan and have 100 days to repay a ruthless moneylender by buying low,
selling high and surviving the roads between seven cities.

| | |
|---|---|
| Genre | Trading / management roguelite with narrative events (tycoon + survival decisions) |
| Platform | Telegram bot (NOT a WebApp). One "screen" message edited in place with inline keyboards |
| Tech | Python 3.12, aiogram 3.x, stdlib `sqlite3`, pytest |
| Audience | 14+, Central-Asian Telegram users, fans of trading sims; short sessions (5–15 min), one run ≈ 40–70 min |
| Languages | Uzbek (Latin), Russian, English — chosen on first `/start`, switchable with `/lang` |
| Difficulty | Hard by default ("Qiyin"); also "Oddiy/Normal" and "Afsonaviy/Legendary" |

## 2. Story
**Setting:** Transoxiana, 1409 (history-flavoured, fictional characters, no politics).

**Premise:** Your uncle Hamid, the most famous caravan master of Samarkand, died "in a sandstorm".
He left you 4 camels, his old guide **Ravshan-ota**, and a debt of **3,000 tanga** to the moneylender
**Yusuf Sarrof**. The debt grows **+3% every 10 days** and must be cleared by **day 100**, or Yusuf seizes everything.

**Characters**
- **Ravshan-ota** — loyal old guide; narrator of tips; his comments are the tutorial voice.
- **Yusuf Sarrof** — Samarkand moneylender; cold but fair; lets you borrow more at worse interest.
- **Qorabek** — head of the Bukhara merchant guild; smiles, offers to "help"; secretly wants the routes.
- **Qora Shamol (Black Wind)** — bandit chief who roams the desert roads; secretly paid by Qorabek.
- **Nilufar** — Khiva caravanserai keeper; sells rumors; can become an ally.

**Story beats** (triggered by day / place / flags):
1. *Day 1, Samarkand:* Ravshan introduces the debt, the market and the map (tutorial).
2. *First visit to Bukhara or day ≥ 15:* Qorabek offers to buy the caravan for 1,500 tanga.
   Accept → ending **"Qorabek's Clerk"**. Refuse → he becomes hostile (more bandits on danger ≥ 2 roads,
   Bukhara buys/sells 10% worse for you, the guild levy city event).
3. *Day ≥ 30 and reputation ≥ 40, any city:* a servant brings uncle's sealed letter — Hamid suspected
   Qorabek of paying Black Wind. Keep it → flag `letter`; burn it → +8 morale, the exposure path closes.
4. *Day 45–65 on a danger ≥ 2 road:* **Black Wind ambush** (unique event; 30% per road day, 60% from day 58). Choices: fight (guards vs his band),
   pay tribute (40% of cargo), flee into the dunes (risk camels). Winning the fight gives flag `token`
   (Black Wind's signet). If reputation < 20 he offers you to **join him** → secret ending **"Black Wind's Partner"**.
5. *Samarkand with `letter` + `token`:* option to bring the evidence to the Guild Council → Qorabek exposed,
   reputation +30, the guild pays a 300 tanga reward, prices at Bukhara normalise, bandit danger −1 everywhere
   (minimum 1). Flag `exposed`.
6. *Debt paid:* Yusuf tears up the contract. Free-trade continues until day 150 or until you press **Retire**.

**Endings (8)**
| # | Ending | Condition |
|---|---|---|
| E1 | **Legend of the Silk Road** (best) | debt paid, `exposed`, net worth ≥ 12,000 at retirement / day 150 |
| E2 | **Honest Trader** | debt paid, net worth ≥ 5,000 |
| E3 | **Free but Poor** | debt paid, net worth < 5,000 |
| E4 | **Qorabek's Clerk** | accepted Qorabek's buyout |
| E5 | **Debt Slave** | day 100 ends with debt > 0 (triggers when day 101 begins) |
| E6 | **Lost in the Sands** | no camels left, or provisions at 0 for 3 consecutive road days |
| E7 | **Mutiny** | morale reaches 0 |
| E8 | **Black Wind's Partner** (secret) | joined the bandits |

Each ending has its own epilogue text (60–120 words) and a score line; endings are recorded for `/top`.

## 3. World
**Cities (7):** Samarkand (home, moneylender, guild council), Bukhara, Khiva, Merv, Tashkent, Kashgar, Herat.

**Roads** (days, danger 1–3, terrain):
SAM–BUK 5d d1 steppe · SAM–TAS 5d d1 steppe · BUK–KHI 8d d2 desert · BUK–MER 6d d2 steppe ·
KHI–MER 7d d3 desert · MER–HER 7d d3 mountain · TAS–KAS 11d d2 mountain.
Desert doubles water/provision use; mountains add cold events; danger scales event and bandit chance.

**Goods (10)** — each takes 1 cargo slot. Producer city sells cheap (0.55× base); the price factor grows linearly
with road-days from the producer and reaches 2.0× at 12+ days (tuned from ~1.8× so the early game can grow).
Silk, Porcelain, Tea (Kashgar) · Spices, Lapis (Herat) · Paper (Samarkand) · Carpets (Bukhara) ·
Cotton cloth (Merv) · Furs (Khiva) · Iron tools (Tashkent).
Base prices roughly: lapis 90, silk 70, porcelain 60, spices 55, carpets 45, furs 40, tea 30, iron 25, paper 20, cotton 15.

**Market model:** each city/good has an equilibrium (mid) price. Buying one unit raises it, selling lowers it, by
0.8% for cheap bulk goods up to 2% for lapis (thin luxury markets), so dumping 40 units crashes the price.
The player buys at mid +4% and sells at mid −4%; reputation shifts both by up to ±5%. Every day prices drift 10%
back toward equilibrium plus a random walk (±6%), clamped to 0.3×–3× equilibrium. Rumors and city events create
temporary gluts/shortages (×0.55–0.7 / ×1.4–1.7 for 10–20 days); a silent world shock happens with 5% chance a day.

## 4. Resources
| Resource | Start (Hard) | Notes |
|---|---|---|
| Tanga | 400 | money |
| Camels | 4 | 10 cargo slots each; buy 110–130 (Khiva 80), resale 60; max 12; can die in events |
| Provisions | 40 | 1 per person (you, Ravshan-ota, each guard) + 1 per camel per road day; desert ×2; max 25 per camel; 1–3 tanga each (Khiva 3) |
| Guards | 0 | hire 30 signup + 4/day wage (paid every day that passes, also rest days); max 12; fight strength |
| Morale | 70 | 0–100; road drift −1 every other day (steppe), −1/day (mountains), −2/day (desert); unpaid wages −6, starving −10/day; +3 on arrival, +15 rest, +feast, +victories |
| Reputation | 30 | 0–100; moves buy and sell prices by up to ±5% each (10% range); unlocks story beats, talk-your-way-through tolls |
| Debt | 3,000 | +3% on days 10, 20 … 90 until paid; can borrow +1,000 once (Samarkand, before day 90) at +5%/10 days; the loan is repaid first |
| Day | 1 | deadline day 100; game hard-stops day 150 |

**Net worth** = tanga + cargo at current local sell prices + camels × 60 − debt.

## 5. Core loop
1. **In a city** (hub screen): 🏪 Market · 🐫 Camel stable · 🛡 Hire guards · 🍞 Provisions · 🏨 Caravanserai (rest 1 day: +15 morale, cost) ·
   🫖 Teahouse (rumor: price hint for another city, costs 5; free in Khiva once Nilufar is an ally) · 💰 Moneylender
   (Samarkand only) · ⚖️ Guild Council (Samarkand, with letter + signet) · 📦 Deliver contract · 🗺 Travel · 📜 Status ·
   📒 Ledger (last known prices per city) · 🏁 Retire (after the debt is paid).
2. **Market:** list of goods with buy/sell price and what you carry; tap a good → Buy 1/5/Max, Sell 1/5/All.
3. **Travel:** pick a neighbouring city → confirmation (days, danger, provisions needed, wages) → road screen.
4. **Road:** each "▶ Next day" advances a day (consume provisions, pay wages, morale drift). Event chance per day
   = (10% + 7% × danger, +4% on danger ≥ 2 roads while Qorabek is hostile) × difficulty factor (0.9 / 1.0 / 1.1).
   "⏩ Ride on" auto-advances until an event or arrival.
5. **Events** stop the ride and offer 2–3 buttons (Black Wind up to 4); outcomes are shown with resource deltas.
6. **Arrive** → story beats first, then a 30% chance of a city event → back to the hub.

## 6. Events (minimum 16 road + 5 city)
Road: Sandstorm (shelter +1 day vs push on: lose provisions/maybe a camel) · Bandits (scaled by cargo value:
fight / pay 20% cargo / flee) · Sick camel (treat with provisions / leave it) · Oasis (+provisions, +morale) ·
Lost traveler (share food −prov +rep; sometimes rewards later) · Toll post (pay vs 2-day detour) ·
Wolf pack (mountain) · Road merchant (one-off trade) · Crew quarrel (morale) · Dervish prophecy (free rumor) ·
Flash flood (lose cargo) · Broken saddle (lose cargo unless spare provisions used) · Cold snap (mountain, camel risk) ·
Abandoned cargo (take: +goods, −rep chance) · Deserter guard · Pilgrims (escort: +rep, donation) ·
Dry well (desert: dig +1 day / buy water / ration) · Black Wind (story, unique).
City: Festival (some goods ×1.5) · Plague (prices up, morale −) · Guild tax (−5% tanga at Bukhara if hostile) ·
Glut (one good ×0.6) · Wedding contract (deliver N units of a good to another city within D days for a bonus — simple quest) ·
Camel fair (camels −30% today). Story/city: Nilufar's plea (Khiva, pay 60 → ally: free rest and rumors, +15 strength
against Black Wind) · Grateful traveler (if you helped a lost traveler: gift or two rumors).

Fight resolution: strength = guards×10 + camels×1 + morale/10 + d6; bandits = (10 + 5×danger + 0.25×day +
cargo base value/150) × difficulty × U(0.85–1.15), re-rolled ±10% at the fight; Black Wind = (58 + 0.6×(day−45) +
cargo/120) × difficulty. Both sides' approximate strengths are shown before you choose (hard but fair).
Win → loot/reputation/morale; lose → cargo and guard losses.

## 7. Progression & difficulty
- Early game: short safe runs SAM↔BUK↔TAS with cheap goods; the debt clock forces risk.
- Mid game: buy camels and guards, attempt Kashgar (silk) or Herat (lapis/spices) long routes for big margins.
- Late game: story confrontation, exposing Qorabek, scaling net worth for the best ending.
- Difficulty levels: Normal (debt 2,500, 500 tanga, harm ×0.8, bandits ×0.8, events ×0.9) / Hard (3,000, 400, ×1.0)
  / Legendary (3,800, 350, harm ×1.25, bandits ×1.25, events ×1.1).
- **Balance target** (verified by `scripts/balance.py`, a greedy bot over 300 seeds per difficulty): Hard win (debt paid)
  rate for the greedy bot 20–50%; doing nothing must always lose; Legendary noticeably harder than Hard; Normal easier.
- **Score** (leaderboard): net worth + ending bonus (E1 5,000 · E2 2,000 · E3 500 · E8 1,000) + 25 per day the debt was
  paid before day 100, × difficulty (0.75 / 1.0 / 1.5). E4 scores the 1,500 buyout; E5–E7 score ¼ of a positive net
  worth + 2 per day survived.

## 8. Telegram UX
- `/start` (language pick on first run, then main menu: New game / Continue / How to play / Top), `/lang`, `/status`,
  `/restart`, `/help`, `/top`.
- One persistent game message edited via `editMessageText` (a new one is sent if editing fails); callback data kept
  < 64 bytes as `<seq>|<action>` (e.g. `17|b:silk:5`). The per-render sequence number makes double taps and old
  buttons harmless; a per-user lock serialises updates.
- HTML formatting, emoji icons, compact status header on every screen (day, tanga, cargo x/y, provisions, morale, debt).
- Ravshan's tips appear on first visits (tutorial), can be disabled.
- Stale/old buttons must not crash: unknown or outdated callbacks re-render the current screen.

## 9. Tech & structure
- Pure engine (`karvon/engine/`) with no aiogram imports; seeded RNG stored in state for reproducibility.
- Bot layer (`karvon/bot/`) renders state → text + keyboards using i18n strings (`karvon/i18n/{uz,ru,en}.py`).
- Storage: SQLite (`players`: user_id, lang, state_json, msg_id, updated_at; `runs`: id, user_id, name, ending, score, day,
  difficulty, finished_at), ISO-8601 UTC timestamps.
- Testing: engine unit tests, i18n completeness test, and an **end-to-end polling test** that runs the real aiogram
  dispatcher against a local fake Telegram Bot API server (no real token needed).
