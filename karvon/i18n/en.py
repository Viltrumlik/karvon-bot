"""English strings. Keys must match uz.py and ru.py exactly (see tests/test_i18n.py)."""

STRINGS: dict[str, str] = {
    # ------------------------------------------------------------------ meta / units
    "lang.name": "English",
    "lang.prompt": "🌐 Choose your language:",
    "lang.saved": "✅ Language: English.",
    "unit.days": "day|days",
    "num.sep": ",",
    "stale": "⏳ That button is outdated. Here is the current screen.",
    "use_buttons": "👇 Please use the buttons below.",
    "busy": "⏳ One moment…",
    # ------------------------------------------------------------------ commands
    "cmd.start": "Main menu",
    "cmd.lang": "Change language",
    "cmd.status": "Caravan status",
    "cmd.restart": "Start a new caravan",
    "cmd.help": "How to play",
    "cmd.top": "Leaderboard",
    # ------------------------------------------------------------------ cities
    "city.sam": "Samarkand",
    "city.sam.in": "in Samarkand",
    "city.sam.to": "to Samarkand",
    "city.sam.from": "from Samarkand",
    "city.sam.desc": "The blue domes of the Registan glitter; paper mills creak along the Siab canal. Yusuf Sarrof keeps his ledger here.",
    "city.buk": "Bukhara",
    "city.buk.in": "in Bukhara",
    "city.buk.to": "to Bukhara",
    "city.buk.from": "from Bukhara",
    "city.buk.desc": "Carpet looms clatter in every courtyard, and the merchant guild's hall watches every bargain in the bazaar.",
    "city.khi": "Khiva",
    "city.khi.in": "in Khiva",
    "city.khi.to": "to Khiva",
    "city.khi.from": "from Khiva",
    "city.khi.desc": "Clay walls at the edge of the Kyzylkum. Fur traders, cheap camels and Nilufar's caravanserai, smelling of bread and smoke.",
    "city.mer": "Merv",
    "city.mer.in": "in Merv",
    "city.mer.to": "to Merv",
    "city.mer.from": "from Merv",
    "city.mer.desc": "Cotton fields stretch to the horizon. Three roads meet at Merv's ancient gates.",
    "city.tas": "Tashkent",
    "city.tas.in": "in Tashkent",
    "city.tas.to": "to Tashkent",
    "city.tas.from": "from Tashkent",
    "city.tas.desc": "Smiths hammer iron day and night; from here the long mountain road climbs east to Kashgar.",
    "city.kas": "Kashgar",
    "city.kas.in": "in Kashgar",
    "city.kas.to": "to Kashgar",
    "city.kas.from": "from Kashgar",
    "city.kas.desc": "The gate of the East. Silk, porcelain and tea pour in from beyond the mountains, and cost almost nothing here.",
    "city.her": "Herat",
    "city.her.in": "in Herat",
    "city.her.to": "to Herat",
    "city.her.from": "from Herat",
    "city.her.desc": "In Herat's shady gardens merchants weigh lapis lazuli and spices on brass scales.",
    # ------------------------------------------------------------------ goods
    "good.lapis": "lapis lazuli",
    "good.silk": "silk",
    "good.porcelain": "porcelain",
    "good.spices": "spices",
    "good.carpets": "carpets",
    "good.furs": "furs",
    "good.tea": "tea",
    "good.iron": "iron tools",
    "good.paper": "paper",
    "good.cotton": "cotton cloth",
    # ------------------------------------------------------------------ terrain / difficulty
    "terrain.steppe": "steppe",
    "terrain.desert": "desert",
    "terrain.mountain": "mountains",
    "diff.normal": "Normal",
    "diff.hard": "Hard",
    "diff.legendary": "Legendary",
    "diff.title": "⚙️ <b>Choose the difficulty</b>",
    "diff.text": (
        "🙂 <b>Normal</b>: debt 2,500, 500 tanga to start, gentler roads.\n"
        "😐 <b>Hard</b>: debt 3,000, 400 tanga. The game as intended.\n"
        "💀 <b>Legendary</b>: debt 3,800, 350 tanga, cruel roads and strong bandits."
    ),
    # ------------------------------------------------------------------ main menu
    "menu.text": (
        "🐪 <b>Caravan Master</b>\n\n"
        "Transoxiana, 1409. Your uncle Hamid, the most famous caravan master of Samarkand, died «in a sandstorm». "
        "He left you four camels, his old guide Ravshan-ota and a debt to the moneylender Yusuf Sarrof.\n\n"
        "Trade along the Silk Road, survive the roads, and pay the debt before day 100."
    ),
    "menu.active": "🐫 Your caravan is waiting: day {day}.",
    "btn.continue": "▶️ Continue",
    "btn.new_game": "🆕 New game",
    "btn.how_to": "📖 How to play",
    "btn.top": "🏆 Leaderboard",
    "btn.language": "🌐 Language",
    "btn.tips_on": "🧓 Tips: on",
    "btn.tips_off": "🧓 Tips: off",
    "btn.menu": "☰ Menu",
    "btn.back": "⬅️ Back",
    "btn.continue_ev": "➡️ Continue",
    "btn.cancel": "✖️ Cancel",
    "restart.text": "🔄 Start a new caravan? The current journey will be lost for good.",
    "btn.restart_yes": "🔄 Yes, start over",
    # ------------------------------------------------------------------ hub
    "hub.title": "🏙 <b>{city}</b>",
    "btn.market": "🏪 Market",
    "btn.stable": "🐫 Stable",
    "btn.guards": "🛡 Guards",
    "btn.provisions": "🍞 Provisions",
    "btn.inn": "🏨 Caravanserai",
    "btn.teahouse": "🫖 Teahouse",
    "btn.lender": "💰 Moneylender",
    "btn.council": "⚖️ Guild Council",
    "btn.deliver": "📦 Deliver {good} ×{n}",
    "btn.travel": "🗺 Travel",
    "btn.status": "📜 Status",
    "btn.ledger": "📒 Ledger",
    "btn.retire": "🏁 Retire",
    # ------------------------------------------------------------------ market
    "mk.title": "🏪 <b>Bazaar {city_in}</b>",
    "mk.cols": "<i>buy / sell · 🎒 yours</i>",
    "mk.hint": "Tap a good to trade it.",
    "gd.prices": "Buy: <b>{buy}</b> · Sell: <b>{sell}</b>",
    "gd.have": "🎒 In your packs: {n} (avg. cost {avg})",
    "gd.none": "🎒 You carry none.",
    "gd.space": "📦 Free space: {space} · 💰 {money}",
    "gd.elsewhere": "📒 Sell prices elsewhere:",
    "gd.elsewhere_row": "• {city}: {price} ({age})",
    "gd.unknown": "📒 No news from other cities about this good yet.",
    "btn.buy": "Buy {n}",
    "btn.buy_max": "Buy max ({n})",
    "btn.sell": "Sell {n}",
    "btn.sell_all": "Sell all ({n})",
    "age.today": "today",
    "age.ago": "{days} ago",
    # ------------------------------------------------------------------ stable / guards / provisions
    "st.title": "🐫 <b>Camel stable</b>",
    "st.text": (
        "Camels: <b>{camels}</b>/{max}. Each carries {slots} bales and {prov} rations, and eats one ration a day.\n"
        "Price here: <b>{price}</b> · we buy yours for {sell}."
    ),
    "st.deal": "🎪 Fair day: camels are cheap until tonight!",
    "btn.camel_buy": "🐫 Buy one ({price})",
    "btn.camel_sell": "💱 Sell one (+{price})",
    "gu.title": "🛡 <b>Guards</b>",
    "gu.text": (
        "Guards: <b>{n}</b>/{max}. Hiring costs {signup}, wages {wage} a day each.\n"
        "Each guard eats like a person and adds 10 to your strength.\n"
        "⚔️ Your strength now ≈ {strength}."
    ),
    "btn.hire": "➕ Hire {n} ({money})",
    "btn.dismiss": "➖ Dismiss one",
    "pr.title": "🍞 <b>Provisions</b>",
    "pr.text": (
        "In the sacks: <b>{prov}</b>/{cap}. Price here: {price} per ration.\n"
        "Your caravan eats {eat} a day (twice as much in the desert)."
    ),
    "btn.prov": "+{n} ({money})",
    "btn.prov_max": "Fill up (+{n})",
    # ------------------------------------------------------------------ inn / teahouse
    "inn.title": "🏨 <b>Caravanserai</b>",
    "inn.text": "A day of rest restores morale (+{morale}). Cost: {cost}.\nMorale now: {cur}/100.",
    "inn.nilufar": "Nilufar refuses your money: «Friends sleep here for free.»",
    "btn.rest": "🛏 Rest a day ({cost})",
    "btn.wait": "⏳ Wait a day",
    "tea.title": "🫖 <b>Teahouse</b>",
    "tea.text": "Merchants gossip over green tea and dried apricots. A good rumor costs {cost} tanga.",
    "tea.nilufar": "Nilufar pours the tea herself and shares what her guests let slip, for free.",
    "btn.rumor": "👂 Buy a rumor ({cost})",
    "rumor.high": "there is a hunger for {good} {city_in}: they pay about {price}",
    "rumor.low": "there is a glut of {good} {city_in}: about {price} apiece",
    # ------------------------------------------------------------------ moneylender / council
    "ln.title": "💰 <b>Yusuf Sarrof, moneylender</b>",
    "ln.text": (
        "Debt: <b>{debt}</b>{loan}\n"
        "Next interest: day {next} (+3% on the debt).\n"
        "Deadline: <b>day {deadline}</b>. Money in hand: {money}."
    ),
    "ln.loan": " (including the loan: {loan})",
    "ln.offer": "Yusuf can lend you {amount} once, at 5% per 10 days.",
    "ln.paid": "Yusuf's contract is torn. You owe nobody anything.",
    "btn.pay": "Pay {n}",
    "btn.pay_all": "Pay everything ({n})",
    "btn.borrow": "💸 Borrow {n}",
    "co.title": "⚖️ <b>Guild Council</b>",
    "co.text": (
        "The elders of the Samarkand guild gather in the hall of mirrors. "
        "You hold uncle Hamid's letter and Black Wind's signet with the mark of the Bukhara guild."
    ),
    "btn.expose": "📜 Present the evidence",
    # ------------------------------------------------------------------ travel / road
    "tr.title": "🗺 <b>Roads {city_from}</b>",
    "tr.hint": "⚔ danger (1 to 3) · 🌾 steppe · 🏜 desert (food ×2) · ⛰ mountains",
    "tr.btn": "{city} · {n}d {terrain} {danger}",
    "tc.title": "🧭 <b>{src} → {dst}</b>",
    "tc.text": (
        "⏳ Road: {days} · {terrain} · danger {danger}\n"
        "🍞 Food: need ≈{need}, you have {prov}\n"
        "🛡 Wages: ≈{wages}\n"
        "📅 Arrival: day {arrive}"
    ),
    "tc.warn_food": "⚠️ Not enough provisions! Three hungry days on the road, and the sands take you.",
    "tc.warn_cap": "⚠️ The camels can't carry enough food for this road. Buy camels or dismiss guards.",
    "tc.warn_wages": "⚠️ You can't pay the wages for the whole road. Unpaid guards grow angry.",
    "tc.warn_deadline": "⚠️ You won't make it back to Samarkand before day {deadline}!",
    "btn.depart": "✅ Set out",
    "rd.title": "🐪 <b>{src} → {dst}</b>",
    "rd.flavor.steppe": "Endless steppe. Camel bells keep time with your thoughts.",
    "rd.flavor.desert": "Dunes to the horizon. The sun hammers the sand; water sloshes in the skins.",
    "rd.flavor.mountain": "The path winds between snowy peaks. The air is thin and cold.",
    "rd.progress": "{bar} day {done} of {total}",
    "rd.food": "🍞 Food for ≈{days}.",
    "btn.next_day": "▶️ Next day",
    "btn.ride_on": "⏩ Ride on",
    # ------------------------------------------------------------------ status / ledger
    "stt.title": "📜 <b>Caravan status</b>",
    "stt.day": "📅 Day {day}. Days left until the deadline: {left}.",
    "stt.day_paid": "📅 Day {day}. Free trade until day {final}.",
    "stt.money": "💰 Tanga: {money}",
    "stt.debt": "💳 Debt: {debt} (next interest on day {next})",
    "stt.debt_paid": "💳 Debt: paid on day {day} ✅",
    "stt.camels": "🐫 Camels: {camels} · 📦 cargo {cargo}/{cap}",
    "stt.prov": "🍞 Provisions: {prov}/{cap} (≈{days} on the steppe)",
    "stt.guards": "🛡 Guards: {guards} · ⚔️ strength ≈{strength}",
    "stt.morale": "😊 Morale: {morale}/100",
    "stt.rep": "⭐ Reputation: {rep}/100",
    "stt.nw": "📈 Net worth: {nw}",
    "stt.diff": "⚙️ Difficulty: {diff}",
    "stt.cargo": "🎒 <b>Cargo:</b>",
    "stt.cargo_empty": "🎒 The packs are empty.",
    "stt.contract": "📦 Contract: {good} ×{n} {city_to} by day {until} (reward {reward})",
    "stt.clues": "🗝 <b>Story:</b>",
    "stt.flag.letter": "✉️ Uncle Hamid's letter",
    "stt.flag.token": "🪬 Black Wind's signet",
    "stt.flag.exposed": "⚖️ Qorabek has been exposed",
    "stt.flag.hostile": "😠 Qorabek is your enemy",
    "stt.flag.nilufar": "🤝 Nilufar is your friend",
    "lg.title": "📒 <b>Price ledger</b>",
    "lg.pick": "Pick a city to see the last prices you know (buy / sell).",
    "lg.city": "📒 <b>{city}</b> · {age}",
    "lg.none": "No news {city_from} yet.",
    # ------------------------------------------------------------------ help / top / ending
    "help.text": (
        "📖 <b>How to play</b>\n\n"
        "🎯 <b>Goal:</b> pay Yusuf Sarrof the whole debt in Samarkand by the end of day 100. "
        "The debt grows by 3% on days 10, 20 … 90.\n\n"
        "🏪 <b>Trade:</b> every city makes some goods cheaply and pays dearly for goods from afar. "
        "Each purchase raises the price and each sale lowers it, so spread your money over several goods. "
        "Prices drift back over time; festivals, gluts and rumors move them too.\n\n"
        "🐫 <b>Caravan:</b> a camel carries 10 bales and 25 rations. Every road day each person and each camel "
        "eats one ration, twice as much in the desert. Three days without food and the caravan is lost.\n\n"
        "🛡 <b>Guards</b> cost 4 tanga a day and make you stronger against bandits. "
        "😊 <b>Morale</b> falls on the road; rest at a caravanserai. At zero the crew mutinies. "
        "⭐ <b>Reputation</b> improves your prices and opens doors.\n\n"
        "⚡ <b>Events</b> stop the caravan and make you choose. Danger ⚔ makes them more frequent.\n\n"
        "🗝 There is a secret behind your uncle's death. Eight endings await, some of them hidden.\n\n"
        "Commands: /start /status /lang /restart /top /help"
    ),
    "top.title": "🏆 <b>Best caravans</b>",
    "top.row": "{rank}. {emoji} <b>{name}</b> — {score}\n      {ending} · {diff} · day {day}",
    "top.empty": "No finished journeys yet. Be the first!",
    "end.head": "🏁 <b>{title}</b>",
    "end.stats": "📊 Score: <b>{score}</b>\n📅 Day {day} · {diff}\n📈 Net worth: {nw}",
    "end.E1.title": "Legend of the Silk Road",
    "end.E1.text": (
        "Samarkand remembers. With Qorabek's treachery laid bare and Yusuf's contract torn to pieces, your camels "
        "became the backbone of every road from Kashgar to Herat. Caravanserai keepers save you their best rooms; "
        "bandits lower their eyes when your banner passes. Ravshan-ota, too old now to ride, sits by the fountain "
        "and tells the boys how you crossed the Kyzylkum with a hungry crew and a dead man's debt. Uncle Hamid's "
        "name is spoken with honour again, and yours is spoken right after it. The Silk Road has a new legend, "
        "and its ledger is written in your hand."
    ),
    "end.E2.title": "Honest Trader",
    "end.E2.text": (
        "You paid every coin you owed, and you did it with clean hands. Your caravan is not the largest in "
        "Samarkand, but merchants trust your word more than a sealed contract. Yusuf Sarrof, who never smiles, "
        "nods to you in the bazaar. You buy a house by the Siab canal, hire young drivers and teach them what "
        "Ravshan-ota taught you: count the water before the gold, and never sell a camel you will need tomorrow. "
        "Whatever whispers still drift around the Bukhara guild, they no longer touch your name. "
        "A good life, earned honestly, one road at a time."
    ),
    "end.E3.title": "Free but Poor",
    "end.E3.text": (
        "On the day Yusuf tore up the contract, you had barely enough left for a pot of plov. The camels are old, "
        "the packs are thin, and the roads still frighten you. But the debt is gone, and nobody in Samarkand can "
        "call you a slave. Ravshan-ota laughs and says that a free beggar sleeps better than an indebted khan. "
        "Perhaps next spring you will try the long road to Kashgar again. Perhaps you will open a small shop "
        "instead. For now freedom is the only treasure you carry, and it weighs nothing at all."
    ),
    "end.E4.title": "Qorabek's Clerk",
    "end.E4.text": (
        "Qorabek counted out fifteen hundred tanga with a warm smile, settled with Yusuf himself and took your "
        "camels before the ink was dry. Now you sit in a cold corner of the Bukhara guild hall, copying other "
        "men's contracts by lamplight. Sometimes you write down the names of caravans that later vanish in the "
        "desert, and you learn not to ask why. Ravshan-ota refused to serve the new master and went home to his "
        "village. Your uncle's banner hangs in Qorabek's hall like a hunting trophy. You are safe, fed and paid "
        "on time. You are no longer free."
    ),
    "end.E5.title": "Debt Slave",
    "end.E5.text": (
        "On the morning after the hundredth day, Yusuf Sarrof's men were waiting at the city gate. They took the "
        "camels, the cargo and your uncle's house, and still the ledger showed a debt. Now you work it off in "
        "Yusuf's warehouses, hauling other merchants' bales from dawn to dusk. Through the open gate you watch "
        "caravans leave for Bukhara and Kashgar, their bells ringing. Ravshan-ota brings you bread on Fridays and "
        "never mentions the roads. Some debts are paid in coin. Yours will be paid in years."
    ),
    "end.E6.title": "Lost in the Sands",
    "end.E6.text": (
        "The wind erased the trail first, then the water ran out, then the camels lay down and would not rise. "
        "Ravshan-ota prayed, and then fell silent. Months later a caravan from Khiva found bleached harnesses and "
        "a broken chest half buried in a dune. Inside lay your uncle's old banner, faded but whole. In Samarkand "
        "Yusuf Sarrof closed your account with a single line of ink. The desert keeps its own ledgers, and it "
        "does not forgive mistakes in counting water."
    ),
    "end.E7.title": "Mutiny",
    "end.E7.text": (
        "It began with whispers by the campfire and ended with knives at dawn. Your drivers, hungry and unpaid, "
        "tied you to a saddle post and divided the camels among themselves. Ravshan-ota begged for your life, "
        "and that is the only reason you still have one. You walked back to Samarkand barefoot, with nothing but "
        "the clothes on your back. In the bazaar they still tell the story of the caravan master who forgot that "
        "a caravan is made of people, not only of camels and bales."
    ),
    "end.E8.title": "Black Wind's Partner",
    "end.E8.text": (
        "You lowered your sword and took Black Wind's hand. Within a season no caravan crossed the Kyzylkum "
        "without paying you both. Qorabek's gold flowed into your saddlebags, and then, one moonless night, you "
        "and Black Wind emptied his treasury too. Yusuf Sarrof's debt was never paid; his scribes simply wrote "
        "your name in red ink. Ravshan-ota left without a word. Now you are rich, feared and hunted, and you sleep "
        "with a dagger under your pillow. The steppe whispers your name, but never with love."
    ),
    # ------------------------------------------------------------------ Ravshan's tips
    "tip.prefix": "🧓 <b>Ravshan-ota:</b>",
    "tip.welcome": (
        "Your uncle left us four camels, an old man, and a debt of {debt} tanga. Every ten days it grows, "
        "and on day 100 Yusuf takes everything. Buy where a good is made, sell where people miss it. "
        "Paper is cheap here; Bukhara and Tashkent are five days away."
    ),
    "tip.market": (
        "Every purchase pushes the price up and every sale pulls it down; dear goods jump fastest. "
        "Spread the money over several goods rather than stuffing the packs with one."
    ),
    "tip.travel": (
        "Look at the days and the danger. The desert 🏜 drinks twice the water. "
        "Never set out without enough food: three hungry days and the sands take us."
    ),
    "tip.road": "▶️ moves us one day, ⏩ rides on until something happens. Every day costs food and the guards' pay.",
    "tip.event": "The road loves surprises. Think before you choose; some losses cannot be undone.",
    "tip.desert": "Desert, my child. Double water, double bread. Count twice before you leave the well.",
    "tip.mountain": "The mountains are cold and full of wolves. Guards and warm goods are worth their weight here.",
    "tip.city.buk": "Bukhara. Carpets are cheap, and Qorabek's guild rules the bazaar. He smiles too sweetly, that one.",
    "tip.city.khi": "Khiva sells furs and the cheapest camels. Nilufar keeps the caravanserai; she hears everything.",
    "tip.city.mer": "Merv: cotton, and three roads meet. Herat lies a week south through dangerous mountains.",
    "tip.city.tas": "Tashkent forges iron tools. Kashgar is eleven days east, over the mountains.",
    "tip.city.kas": "Kashgar! Silk, porcelain and tea are cheap here. In Samarkand they are worth two or three times as much.",
    "tip.city.her": "Herat sells lapis and spices. Costly goods, but in the north they fetch a fortune.",
    "tip.lender": "Yusuf is cold but honest. Pay part of the debt whenever you can: interest only grows on what is left.",
    "tip.guards": "Each guard adds 10 to our strength but wants 4 tanga a day. Bandits judge us by the cargo we carry.",
    "tip.stable": "A camel carries 10 bales and 25 rations, but eats every day. Khiva sells them cheapest.",
    "tip.low_morale": "The men are tired and angry. Give them a day at a caravanserai before they turn on us.",
    "tip.debt_paid": "The debt is gone! Now we trade for ourselves. Retire whenever you wish, or reach for more.",
    "tip.ledger": "The ledger remembers the prices we have seen. Old news lies, so mind the age.",
    "tip.teahouse": "Rumors cost little and can be worth a lot. Sometimes a city hungers for a good, and only the teahouse knows.",
    # ------------------------------------------------------------------ action results
    "ok.bought": "✅ Bought {good} ×{n} for {money}.",
    "ok.sold": "✅ Sold {good} ×{n} for {money} (profit {profit}).",
    "ok.camels_bought": "🐫 A new camel joins the caravan ({money}).",
    "ok.camels_sold": "💱 You sold a camel for {money}.",
    "ok.guards_hired": "🛡 Guards hired: +{n} ({money}).",
    "ok.guards_dismissed": "🛡 Guards dismissed: {n}.",
    "ok.provisions": "🍞 Bought {n} rations for {money}.",
    "ok.rested": "🛏 A day of rest. The crew is in better spirits.",
    "ok.waited": "⏳ A day passes.",
    "ok.rumor_high": "👂 Rumor: «{rumor}».",
    "ok.rumor_low": "👂 Rumor: «{rumor}».",
    "ok.departed": "🐪 The caravan heads {city_to}.",
    "ok.day": "▶️ Another day on the road.",
    "ok.rode": "⏩ {days} on the road.",
    "ok.paid": "💰 Paid {money}. Debt left: {debt}.",
    "ok.debt_cleared": "🎉 Yusuf Sarrof tears up the contract. You are free!",
    "ok.borrowed": "💸 Yusuf lends you {money} at 5% per 10 days.",
    "ok.council": (
        "⚖️ The hall falls silent. Qorabek is stripped of his title and his riders flee the roads. "
        "The guild rewards you with {money} tanga, and your name is on every tongue."
    ),
    "ok.delivered": "📦 The wedding family receives the goods with joy. Reward: {money}.",
    "ok.retired": "🏁 You retire from the roads.",
    # ------------------------------------------------------------------ errors
    "err.ended": "The journey is over. Start a new one from the menu.",
    "err.pending": "First decide what to do about the event.",
    "err.not_in_city": "You are not in a city.",
    "err.not_on_road": "You are not on the road.",
    "err.bad_input": "That doesn't work.",
    "err.no_space": "No free cargo space. Buy camels or sell something.",
    "err.no_money": "Not enough money.",
    "err.no_goods": "You don't have that.",
    "err.max_camels": "One caravan master can't manage more than {n} camels.",
    "err.last_camel": "You can't sell your last camel.",
    "err.cargo_wont_fit": "The cargo won't fit on the remaining camels.",
    "err.max_guards": "No more than {n} guards.",
    "err.no_guards": "You have no guards to dismiss.",
    "err.prov_full": "The provision sacks are full.",
    "err.no_road": "There is no road there.",
    "err.no_event": "Nothing is happening right now.",
    "err.bad_choice": "That choice is not available.",
    "err.not_here": "That is not possible here.",
    "err.no_debt": "You owe nothing.",
    "err.no_loan": "Yusuf will not lend you any more.",
    "err.cannot_deliver": "You can't fulfil the contract here.",
    "err.debt_first": "Pay off the debt first.",
    # ------------------------------------------------------------------ notes
    "note.interest": "📈 Interest charged: +{money}. The debt is now {debt}.",
    "note.wages_unpaid": "😠 No money for wages! The guards are grumbling.",
    "note.guard_left": "🚪 An unpaid guard left the caravan.",
    "note.starving": "🍞 No food! The crew is starving. Days before disaster: {n}.",
    "note.arrived": "🏁 You have arrived {city_in}.",
    "note.contract_here": "📦 The wedding family is waiting here for {good} ×{n}.",
    "note.contract_failed": "❌ The wedding contract has expired. Your reputation suffers.",
    "note.cargo_dropped": "📦 Not enough camels: {n} bales were left behind.",
    "note.debt_cleared": "🎉 The debt is paid! Trade freely until day 150, or retire whenever you like.",
    "note.deadline_near": "⏳ Only {n} days left until Yusuf's deadline!",
    "note.ending": "🏁 The journey is over.",
    # ------------------------------------------------------------------ event extras
    "ev.strength": "⚔️ Your strength ≈{ours} · theirs ≈{theirs}",
    "ev.warned": "🤝 Nilufar warned you about the ambush: +{bonus} strength.",
    # ------------------------------------------------------------------ road events
    "ev.sandstorm.title": "Sandstorm",
    "ev.sandstorm.text": "A brown wall rises on the horizon. Ravshan-ota sniffs the air: «Within the hour it will be upon us.»",
    "ev.sandstorm.c.shelter": "⛺ Make camp and wait (+1 day)",
    "ev.sandstorm.c.push": "🐪 Push through the storm",
    "ev.sandstorm.r.shelter": "You lie behind the kneeling camels while the sand hisses overhead. By morning the storm is gone, and so is a day.",
    "ev.sandstorm.r.push": "You stagger on blindly. Sacks tear open, and the sand swallows part of your provisions.",
    "ev.sandstorm.r.push_camel": "You stagger on blindly. When the dust settles, a camel is missing; the dunes have already covered its tracks.",
    "ev.bandits.title": "Bandits!",
    "ev.bandits.text": "About {n} riders block the road, bows in hand. Their leader grins: «Your cargo or your blood, merchant.»",
    "ev.bandits.c.fight": "⚔️ Fight",
    "ev.bandits.c.pay": "💰 Pay a fifth of the cargo",
    "ev.bandits.c.flee": "🏃 Flee",
    "ev.bandits.r.fight_win": "Your guards break the attack! The bandits scatter and leave {loot} tanga behind. Word of your courage will travel.",
    "ev.bandits.r.fight_lose": "The fight goes badly. The raiders slash open your packs and ride off with the spoils.",
    "ev.bandits.r.pay": "You hand over a fifth of the cargo. The leader bows mockingly and lets you pass.",
    "ev.bandits.r.pay_money": "Your packs are empty, so they take coins instead.",
    "ev.bandits.r.flee_ok": "You whip the camels into a run and lose the riders among the ravines.",
    "ev.bandits.r.flee_fail": "They catch the slowest camels. You get away, but not with everything.",
    "ev.sick_camel.title": "A sick camel",
    "ev.sick_camel.text": "One of the camels refuses to stand. Its eyes are dull and it is shivering.",
    "ev.sick_camel.c.treat": "💊 Treat it (−8 provisions)",
    "ev.sick_camel.c.leave": "🚶 Leave it behind",
    "ev.sick_camel.c.slaughter": "🔪 Slaughter it for meat",
    "ev.sick_camel.r.treat_ok": "Ravshan-ota boils herbs in camel milk. By noon the animal is back on its feet.",
    "ev.sick_camel.r.treat_fail": "You tried everything, but the camel dies in the night.",
    "ev.sick_camel.r.leave": "You unload it and walk on. For a long while you hear it calling behind you.",
    "ev.sick_camel.r.slaughter": "A grim job, but the crew will eat meat for days.",
    "ev.oasis.title": "Oasis",
    "ev.oasis.text": "Palm trees and a spring of clear water! The camels pull towards it on their own.",
    "ev.oasis.c.rest": "🌴 Rest here a day (+1 day)",
    "ev.oasis.c.water": "💧 Fill the waterskins and move on",
    "ev.oasis.r.rest": "A day of shade, dates and cool water. The crew is singing again.",
    "ev.oasis.r.water": "You fill everything that holds water and press on.",
    "ev.traveler.title": "A lost traveler",
    "ev.traveler.text": "A man in torn clothes stumbles out of the haze, his lips cracked with thirst. He has lost his caravan.",
    "ev.traveler.c.share": "🍞 Share food (−5 provisions)",
    "ev.traveler.c.escort": "🐪 Take him along (−10 provisions, +1 day)",
    "ev.traveler.c.pass": "🚶 Ride past",
    "ev.traveler.r.share": "He blesses you and your children's children. Kindness is remembered on these roads.",
    "ev.traveler.r.escort": "You bring him to a well where his kinsmen are waiting. They promise to remember your name.",
    "ev.traveler.r.escort_paid": "His kinsmen turn out to be merchants. They press {money} tanga into your hand.",
    "ev.traveler.r.pass": "The crew watches him fade into the haze. Nobody speaks for a long time.",
    "ev.toll.title": "Toll post",
    "ev.toll.text": "A local beg has stretched a chain across the road. His men demand {fee} tanga for passage.",
    "ev.toll.c.pay": "💰 Pay {fee}",
    "ev.toll.c.detour": "↩️ Take a detour (+2 days)",
    "ev.toll.c.talk": "🗣 Talk your way through",
    "ev.toll.r.pay": "The chain drops. The beg's scribe writes your name in a greasy book.",
    "ev.toll.r.detour": "You turn into the hills. The detour costs two days, but not a single coin.",
    "ev.toll.r.talk_ok": "The beg has heard of you. «For an honest merchant the road is free,» he says, and waves you on.",
    "ev.toll.r.talk_fail": "Your fine words amuse him, but the price stays the same: {fee} tanga.",
    "ev.wolves.title": "Wolf pack",
    "ev.wolves.text": "Howls echo between the cliffs. In the dusk you count a dozen pairs of yellow eyes.",
    "ev.wolves.c.fight": "⚔️ Drive them off with the guards",
    "ev.wolves.c.fire": "🔥 Keep fires burning all night (−6 provisions)",
    "ev.wolves.c.run": "🏃 Hurry on through the pass",
    "ev.wolves.r.fight_win": "Spears and torches send the pack running. The crew cheers.",
    "ev.wolves.r.fight_lose": "The wolves break through the line and drag a camel into the dark.",
    "ev.wolves.r.fire": "You burn dung and spare sacks until dawn. Nobody sleeps, but nobody dies.",
    "ev.wolves.r.run_ok": "You drive the caravan through the pass at a run. The howling fades behind you.",
    "ev.wolves.r.run_loss": "In the rush a camel falls behind. That is exactly what the wolves were waiting for.",
    "ev.merchant.title": "Road merchant",
    "ev.merchant.text": "A lone trader with heavily laden donkeys offers: {good} ×{qty} at {price} tanga apiece.",
    "ev.merchant.c.buy": "🤝 Buy",
    "ev.merchant.c.haggle": "🗣 Haggle",
    "ev.merchant.c.decline": "🙅 Decline",
    "ev.merchant.r.buy": "You buy {good} ×{n} for {money} tanga.",
    "ev.merchant.r.haggle_ok": "After a long argument he gives in: {good} ×{n} for {money} tanga.",
    "ev.merchant.r.haggle_fail": "Offended by your offer, he ties up his bundles and rides off.",
    "ev.merchant.r.decline": "You part politely. Who knows, perhaps the road will bring you together again.",
    "ev.quarrel.title": "Quarrel in the camp",
    "ev.quarrel.text": "Two drivers are shouting over a share of water. The others are already taking sides.",
    "ev.quarrel.c.bonus": "💰 Pay everyone a bonus",
    "ev.quarrel.c.judge": "⚖️ Judge the dispute yourself",
    "ev.quarrel.c.ignore": "🙈 Let them sort it out",
    "ev.quarrel.r.bonus": "{money} tanga and a few kind words work wonders. The crew calms down.",
    "ev.quarrel.r.judge_ok": "Your ruling is fair and everyone accepts it. Even the loser nods.",
    "ev.quarrel.r.judge_fail": "Your verdict pleases nobody. The camp sulks for days.",
    "ev.quarrel.r.ignore": "The quarrel smoulders and spreads. Spirits sink.",
    "ev.dervish.title": "Wandering dervish",
    "ev.dervish.text": "A dervish in a patched cloak sits by the road. «I have been everywhere,» he says, «and I see everything.»",
    "ev.dervish.c.alms": "🪙 Give alms (5 tanga)",
    "ev.dervish.c.listen": "👂 Just listen",
    "ev.dervish.c.pass": "🚶 Ride on",
    "ev.dervish.r.alms": "He blesses you and whispers: «{rumor}.»",
    "ev.dervish.r.listen_ok": "Between riddles he lets slip: «{rumor}.»",
    "ev.dervish.r.listen_vague": "He talks of stars, sand and the vanity of riches. Nothing useful.",
    "ev.dervish.r.pass": "He laughs after you, as if he knows something you don't.",
    "ev.flood.title": "Flash flood",
    "ev.flood.text": "Thunder rolls in the hills. Minutes later a muddy torrent roars down the dry riverbed you are crossing!",
    "ev.flood.c.save_cargo": "📦 Save the cargo",
    "ev.flood.c.save_camels": "🐫 Save the camels",
    "ev.flood.r.cargo_ok": "You drag the bales to high ground just in time. Everyone is soaked, but alive.",
    "ev.flood.r.cargo_camel": "The bales are saved, but the water knocks a camel off its feet and carries it away.",
    "ev.flood.r.camels": "You cut the loads loose and lead the camels out. The torrent swallows part of the cargo.",
    "ev.saddle.title": "Broken saddle",
    "ev.saddle.text": "A saddle girth snaps and a whole load slides into the dust.",
    "ev.saddle.c.rope": "🪢 Tie it with food sacks (−8 provisions)",
    "ev.saddle.c.fix": "🔧 Repair it properly (+1 day)",
    "ev.saddle.c.drop": "🗑 Leave part of the load",
    "ev.saddle.r.rope": "You empty a few food sacks and twist them into rope. It holds.",
    "ev.saddle.r.fix": "Ravshan-ota stitches the leather by the fire. A day lost, but the saddle is as good as new.",
    "ev.saddle.r.drop": "You leave {good} ×{n} by the road. Some lucky traveller will be glad.",
    "ev.cold.title": "Cold snap",
    "ev.cold.text": "An icy wind sweeps down from the peaks. Frost forms on the camels' coats; the weakest one is trembling.",
    "ev.cold.c.camp": "⛺ Camp and wait it out (+1 day)",
    "ev.cold.c.push": "🐪 Keep going",
    "ev.cold.c.burn": "🧣 Wrap the camels in furs and cloth",
    "ev.cold.r.camp": "You huddle together in a hollow until the wind dies down.",
    "ev.cold.r.push_ok": "Teeth chattering, you cross the pass. Everyone made it.",
    "ev.cold.r.push_loss": "At the top of the pass a camel lies down in the snow and never gets up.",
    "ev.cold.r.burn": "You wrap the camels in your own goods. A few bales are ruined, but everyone is warm.",
    "ev.abandoned.title": "Abandoned cargo",
    "ev.abandoned.text": "By the road lie a dead camel and several bales: {good}, about {qty} of them. There is no owner in sight.",
    "ev.abandoned.c.take": "🎒 Take the goods",
    "ev.abandoned.c.bury": "🙏 Bury the bones and pray",
    "ev.abandoned.c.leave": "🚶 Leave everything",
    "ev.abandoned.r.take": "You load {good} ×{n}. Ravshan-ota mutters something about bad luck.",
    "ev.abandoned.r.take_seen": "You load {good} ×{n}, but shepherds saw you. Soon the bazaars will be calling you a grave robber.",
    "ev.abandoned.r.bury": "You give the dead their due. Travellers who hear of it will respect you.",
    "ev.abandoned.r.leave": "You ride past. The road has its owners, even when you cannot see them.",
    "ev.deserter.title": "A deserter",
    "ev.deserter.text": "At night one of your guards packs his things. «The pay is poor and the road is long,» he grumbles.",
    "ev.deserter.c.pay": "💰 Pay him extra (20)",
    "ev.deserter.c.let_go": "👋 Let him go",
    "ev.deserter.c.chase": "🏇 Chase him",
    "ev.deserter.r.pay": "Twenty tanga change his mind. For now.",
    "ev.deserter.r.let_go": "He rides off into the night. One spear fewer.",
    "ev.deserter.r.chase_ok": "You catch him at dawn. Shamed in front of everyone, he swears to serve faithfully.",
    "ev.deserter.r.chase_fail": "He escapes, and takes a purse of coins with him.",
    "ev.pilgrims.title": "Pilgrims",
    "ev.pilgrims.text": "A group of pilgrims on their way to a holy shrine asks to travel under your protection.",
    "ev.pilgrims.c.escort": "🤝 Take them along (−6 provisions)",
    "ev.pilgrims.c.decline": "🙅 Refuse",
    "ev.pilgrims.r.escort": "The pilgrims pray for you at every halt and leave a donation of {money} tanga.",
    "ev.pilgrims.r.decline": "They walk on alone. In the next town people will hear that you turned them away.",
    "ev.dry_well.title": "Dry well",
    "ev.dry_well.text": "The well on Ravshan-ota's map is dry. Nearby nomads offer water for {cost} tanga.",
    "ev.dry_well.c.dig": "⛏ Dig deeper (+1 day)",
    "ev.dry_well.c.buy": "💰 Buy water ({cost})",
    "ev.dry_well.c.ration": "🥤 Cut the rations",
    "ev.dry_well.r.dig": "After a day of digging, cold muddy water fills the shaft.",
    "ev.dry_well.r.buy": "The nomads fill your skins. Expensive water is still water.",
    "ev.dry_well.r.ration": "Half rations. The crew grumbles with every step.",
    "ev.black_wind.title": "Black Wind",
    "ev.black_wind.text": (
        "Black banners on every dune. Dozens of riders surround the caravan, and a man with a black scarf over his "
        "face rides forward. «I am Qora Shamol, the Black Wind. Someone in Bukhara pays well for your head, merchant.»"
    ),
    "ev.black_wind.c.fight": "⚔️ Fight to the end",
    "ev.black_wind.c.tribute": "💰 Pay tribute (40% of the cargo)",
    "ev.black_wind.c.flee": "🏜 Flee into the dunes",
    "ev.black_wind.c.join": "🤝 «Let's talk business…»",
    "ev.black_wind.r.fight_win": (
        "The battle lasts until sunset. When Black Wind falls from his horse, his men scatter. On his finger you "
        "find a signet bearing the mark of the Bukhara guild, and {loot} tanga in his saddlebags."
    ),
    "ev.black_wind.r.fight_lose": "Black Wind's riders cut through your line. You survive, but at a terrible price.",
    "ev.black_wind.r.tribute": "Black Wind's men take their share. «Give my regards to Qorabek,» their leader laughs.",
    "ev.black_wind.r.flee_ok": "You lead the caravan deep into the dunes where horses cannot follow. You lose your way for a while, but you escape.",
    "ev.black_wind.r.flee_fail": "The dunes become a trap. The riders cut off the tail of the caravan.",
    "ev.black_wind.r.join": "Black Wind lowers his scarf and smiles. «I knew we would understand each other.»",
    # ------------------------------------------------------------------ city events
    "ev.festival.title": "Festival",
    "ev.festival.text": "Drums and music! The city is celebrating. Merchants say {good} and {good2} will fetch a premium for a few days.",
    "ev.festival.c.feast": "🎉 Treat the crew ({cost})",
    "ev.festival.c.trade": "🏪 Stick to business",
    "ev.festival.r.feast": "Plov, music and dancing till midnight. The crew won't forget it.",
    "ev.festival.r.trade": "While others dance, you study the prices.",
    "ev.plague.title": "Plague",
    "ev.plague.text": "Fever in the poor quarters; the city is closing its gates. Prices are soaring, and your drivers are afraid.",
    "ev.plague.c.endure": "😷 Keep calm and carry on",
    "ev.plague.c.medicine": "💊 Buy medicines (25)",
    "ev.plague.c.help": "🍞 Feed the sick (−10 provisions)",
    "ev.plague.r.endure": "You trade quickly, but fear eats away at the crew.",
    "ev.plague.r.medicine": "Bitter herbal brews and incense keep the crew healthy and calm.",
    "ev.plague.r.help_ok": "The city will remember the merchant who fed its poor.",
    "ev.plague.r.help_sick": "The city praises you, but two of your drivers have started coughing too.",
    "ev.guild_tax.title": "Guild levy",
    "ev.guild_tax.text": "Qorabek's clerks block the gate. «A special levy for merchants who refuse the guild's friendship: {tax} tanga.»",
    "ev.guild_tax.c.pay": "💰 Pay {tax}",
    "ev.guild_tax.c.refuse": "✋ Refuse",
    "ev.guild_tax.c.bribe": "🤫 Bribe the clerk ({bribe})",
    "ev.guild_tax.r.pay": "The clerk counts your coins twice and smiles thinly.",
    "ev.guild_tax.r.refuse": "You walk away. Behind your back the clerks write something in their books.",
    "ev.guild_tax.r.refuse_seized": "Guild guards confiscate part of your cargo «for inspection». You will never see it again.",
    "ev.guild_tax.r.bribe": "The clerk pockets the coins and develops a sudden interest in the sky.",
    "ev.guild_tax.r.bribe_caught": "The clerk takes the money and reports you anyway. The whole bazaar hears about it.",
    "ev.glut.title": "Market glut",
    "ev.glut.text": "Caravans have flooded the bazaar: {good} has collapsed in price. A wholesaler offers you a lot at {price} apiece.",
    "ev.glut.c.buy_lot": "🛒 Buy the lot (up to 10)",
    "ev.glut.c.note": "📝 Just note the prices",
    "ev.glut.r.buy_lot": "You buy {good} ×{n} for {money} tanga.",
    "ev.glut.r.note": "You make a note: {good} will be cheap here for a while.",
    "ev.wedding.title": "Wedding contract",
    "ev.wedding.text": "A wealthy family is preparing a wedding. They need {good} ×{qty} delivered {city_to} by day {until}. Reward: {reward} tanga.",
    "ev.wedding.c.accept": "✍️ Accept the contract",
    "ev.wedding.c.decline": "🙅 Decline",
    "ev.wedding.r.accept": "You shake hands. The contract is written into your ledger (📜 Status).",
    "ev.wedding.r.decline": "The family's elder sighs and goes off to find another caravan master.",
    "ev.camel_fair.title": "Camel fair",
    "ev.camel_fair.text": "Nomads have driven a herd to market. Today a camel costs only {price} tanga.",
    "ev.camel_fair.c.buy_one": "🐫 Buy one ({price})",
    "ev.camel_fair.c.look": "👀 Just look",
    "ev.camel_fair.r.buy_one": "A strong young camel joins your caravan.",
    "ev.camel_fair.r.look": "You admire the herd. The fair price holds until tonight (🐫 Stable).",
    "ev.nilufar.title": "Nilufar's caravanserai",
    "ev.nilufar.text": (
        "Nilufar, keeper of the Khiva caravanserai, meets you with tears in her eyes. Qorabek's men demand "
        "60 tanga for «protection», or tomorrow they will burn her stables."
    ),
    "ev.nilufar.c.pay": "💰 Pay for her (60)",
    "ev.nilufar.c.refuse": "🙅 It's not my business",
    "ev.nilufar.r.pay": "«I will not forget this,» Nilufar says. «In my house you will always find a bed and the truth.»",
    "ev.nilufar.r.refuse": "Nilufar nods in silence. The next morning there is smoke above her stables.",
    "ev.grateful.title": "An old acquaintance",
    "ev.grateful.text": "A merchant in a rich robe stops you in the bazaar: it is the traveler you once helped on the road! He wants to repay you.",
    "ev.grateful.c.gift": "💰 Accept a gift",
    "ev.grateful.c.news": "👂 Ask him for news",
    "ev.grateful.r.gift": "He presses {money} tanga into your hands and wishes you a safe road.",
    "ev.grateful.r.news": "He shares two secrets: soon {good} will be dear {city_in}, and {good2} {city2_in}.",
    "ev.qorabek.title": "Qorabek's offer",
    "ev.qorabek.text": (
        "Qorabek, head of the Bukhara merchant guild, invites you to his house. Over sherbet he sighs: «Your uncle "
        "was a great man, but the roads are cruel. I will give you {money} tanga for the caravan and settle with "
        "Yusuf myself. You will work for me: warm, fed and safe.»"
    ),
    "ev.qorabek.c.accept": "🤝 Accept the offer",
    "ev.qorabek.c.refuse": "✋ Refuse",
    "ev.qorabek.r.accept": "Qorabek embraces you like a son. His scribe is already writing the deed.",
    "ev.qorabek.r.refuse": "Qorabek's smile does not change, but his eyes turn cold. «Desert roads are dangerous, my friend. Take care.»",
    "ev.letter.title": "Uncle's letter",
    "ev.letter.text": (
        "A servant from your uncle's old house brings a sealed letter in Hamid's hand: «If I do not return, know "
        "this: Qorabek pays Qora Shamol to rob the caravans that won't bow to the guild. I need proof: "
        "Black Wind's signet.»"
    ),
    "ev.letter.c.keep": "✉️ Keep the letter",
    "ev.letter.c.burn": "🔥 Burn it: the past is past",
    "ev.letter.r.keep": "You hide the letter in your belt. If you ever get the signet, the Guild Council in Samarkand must see both.",
    "ev.letter.r.burn": "The ashes scatter in the wind. The crew notices that you have grown calmer.",
}
