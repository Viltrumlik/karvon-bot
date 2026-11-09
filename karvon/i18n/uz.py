"""O'zbekcha (lotin yozuvi) matnlar. Kalitlar en.py va ru.py bilan bir xil bo'lishi shart."""

STRINGS: dict[str, str] = {
    # ------------------------------------------------------------------ meta / units
    "lang.name": "O'zbekcha",
    "lang.prompt": "🌐 Tilni tanlang:",
    "lang.saved": "✅ Til: o'zbekcha.",
    "unit.days": "kun",
    "num.sep": " ",
    "stale": "⏳ Bu tugma eskirgan. Mana joriy ekran.",
    "use_buttons": "👇 Iltimos, pastdagi tugmalardan foydalaning.",
    "busy": "⏳ Bir daqiqa…",
    # ------------------------------------------------------------------ commands
    "cmd.start": "Bosh menyu",
    "cmd.lang": "Tilni o'zgartirish",
    "cmd.status": "Karvon holati",
    "cmd.restart": "Yangi karvon boshlash",
    "cmd.help": "Qanday o'ynaladi",
    "cmd.top": "Reyting",
    # ------------------------------------------------------------------ cities
    "city.sam": "Samarqand",
    "city.sam.in": "Samarqandda",
    "city.sam.to": "Samarqandga",
    "city.sam.from": "Samarqanddan",
    "city.sam.desc": "Registon gumbazlari moviy jilo sochadi, Siyob bo'yida qog'oz juvozlari g'ichirlaydi. Sudxo'r Yusuf Sarrofning daftari ham shu yerda.",
    "city.buk": "Buxoro",
    "city.buk.in": "Buxoroda",
    "city.buk.to": "Buxoroga",
    "city.buk.from": "Buxorodan",
    "city.buk.desc": "Har bir hovlida gilam dastgohlari taqillaydi, savdogarlar uyushmasining ko'zi esa bozordagi har bir bitimda.",
    "city.khi": "Xiva",
    "city.khi.in": "Xivada",
    "city.khi.to": "Xivaga",
    "city.khi.from": "Xivadan",
    "city.khi.desc": "Qizilqum chetidagi loy devorlar. Mo'ynafurushlar, arzon tuyalar va non hamda tutun hidi anqib turgan Nilufarning karvonsaroyi.",
    "city.mer": "Marv",
    "city.mer.in": "Marvda",
    "city.mer.to": "Marvga",
    "city.mer.from": "Marvdan",
    "city.mer.desc": "Paxtazorlar ufqqacha cho'zilgan. Marvning qadimiy darvozalari oldida uch yo'l tutashadi.",
    "city.tas": "Toshkent",
    "city.tas.in": "Toshkentda",
    "city.tas.to": "Toshkentga",
    "city.tas.from": "Toshkentdan",
    "city.tas.desc": "Temirchilar kechayu kunduz bolg'a uradi. Bu yerdan uzun tog' yo'li sharqqa, Qashqarga ko'tariladi.",
    "city.kas": "Qashqar",
    "city.kas.in": "Qashqarda",
    "city.kas.to": "Qashqarga",
    "city.kas.from": "Qashqardan",
    "city.kas.desc": "Sharq darvozasi. Tog'lar ortidan ipak, chinni va choy oqib keladi, bu yerda ular deyarli tekin.",
    "city.her": "Hirot",
    "city.her.in": "Hirotda",
    "city.her.to": "Hirotga",
    "city.her.from": "Hirotdan",
    "city.her.desc": "Hirotning soya-salqin bog'larida savdogarlar lojuvard va ziravorlarni mis tarozida tortadi.",
    # ------------------------------------------------------------------ goods
    "good.lapis": "lojuvard",
    "good.silk": "ipak",
    "good.porcelain": "chinni",
    "good.spices": "ziravorlar",
    "good.carpets": "gilamlar",
    "good.furs": "mo'ynalar",
    "good.tea": "choy",
    "good.iron": "temir asboblar",
    "good.paper": "qog'oz",
    "good.cotton": "bo'z",
    # ------------------------------------------------------------------ terrain / difficulty
    "terrain.steppe": "dasht",
    "terrain.desert": "cho'l",
    "terrain.mountain": "tog'lar",
    "diff.normal": "Oddiy",
    "diff.hard": "Qiyin",
    "diff.legendary": "Afsonaviy",
    "diff.title": "⚙️ <b>Qiyinlik darajasini tanlang</b>",
    "diff.text": (
        "🙂 <b>Oddiy</b>: qarz 2 500, boshida 500 tanga, yo'llar yumshoqroq.\n"
        "😐 <b>Qiyin</b>: qarz 3 000, 400 tanga. O'yin aynan shunday o'ylangan.\n"
        "💀 <b>Afsonaviy</b>: qarz 3 800, 350 tanga, shafqatsiz yo'llar va kuchli qaroqchilar."
    ),
    # ------------------------------------------------------------------ main menu
    "menu.text": (
        "🐪 <b>Karvonboshi</b>\n\n"
        "Movarounnahr, 1409-yil. Samarqandning eng mashhur karvonboshisi Hamid amakingiz «qum bo'ronida» "
        "halok bo'ldi. U sizga to'rtta tuya, keksa yo'lboshchisi Ravshan otani va sudxo'r Yusuf Sarrofga "
        "katta qarz qoldirdi.\n\n"
        "Ipak yo'lida savdo qiling, yo'llarda omon qoling va qarzni 100-kungacha uzing."
    ),
    "menu.active": "🐫 Karvoningiz kutmoqda: {day}-kun.",
    "btn.continue": "▶️ Davom etish",
    "btn.new_game": "🆕 Yangi o'yin",
    "btn.how_to": "📖 Qanday o'ynaladi",
    "btn.top": "🏆 Reyting",
    "btn.language": "🌐 Til",
    "btn.tips_on": "🧓 Maslahatlar: yoniq",
    "btn.tips_off": "🧓 Maslahatlar: o'chiq",
    "btn.menu": "☰ Menyu",
    "btn.back": "⬅️ Orqaga",
    "btn.continue_ev": "➡️ Davom etish",
    "btn.cancel": "✖️ Bekor qilish",
    "restart.text": "🔄 Yangi karvon boshlaysizmi? Hozirgi safar butunlay yo'qoladi.",
    "btn.restart_yes": "🔄 Ha, qaytadan",
    # ------------------------------------------------------------------ hub
    "hub.title": "🏙 <b>{city}</b>",
    "btn.market": "🏪 Bozor",
    "btn.stable": "🐫 Tuyaxona",
    "btn.guards": "🛡 Soqchilar",
    "btn.provisions": "🍞 Oziq-ovqat",
    "btn.inn": "🏨 Karvonsaroy",
    "btn.teahouse": "🫖 Choyxona",
    "btn.lender": "💰 Sudxo'r",
    "btn.council": "⚖️ Uyushma kengashi",
    "btn.deliver": "📦 Topshirish: {good} ×{n}",
    "btn.travel": "🗺 Safar",
    "btn.status": "📜 Holat",
    "btn.ledger": "📒 Daftar",
    "btn.retire": "🏁 Nafaqaga chiqish",
    # ------------------------------------------------------------------ market
    "mk.title": "🏪 <b>{city} bozori</b>",
    "mk.cols": "<i>olish / sotish · 🎒 sizda</i>",
    "mk.hint": "Savdo qilish uchun mol nomini bosing.",
    "gd.prices": "Olish: <b>{buy}</b> · Sotish: <b>{sell}</b>",
    "gd.have": "🎒 Yukingizda: {n} (o'rtacha tannarx {avg})",
    "gd.none": "🎒 Sizda bu mol yo'q.",
    "gd.space": "📦 Bo'sh joy: {space} · 💰 {money}",
    "gd.elsewhere": "📒 Boshqa shaharlarda sotish narxi:",
    "gd.elsewhere_row": "• {city}: {price} ({age})",
    "gd.unknown": "📒 Bu mol haqida boshqa shaharlardan hali xabar yo'q.",
    "btn.buy": "{n} ta olish",
    "btn.buy_max": "Maksimal ({n})",
    "btn.sell": "{n} ta sotish",
    "btn.sell_all": "Hammasini ({n})",
    "age.today": "bugun",
    "age.ago": "{days} oldin",
    # ------------------------------------------------------------------ stable / guards / provisions
    "st.title": "🐫 <b>Tuyaxona</b>",
    "st.text": (
        "Tuyalar: <b>{camels}</b>/{max}. Har biri {slots} toy yuk va {prov} ulush oziq ko'taradi, "
        "o'zi kuniga bir ulush yeydi.\n"
        "Bu yerda narxi: <b>{price}</b> · sizning tuyangizni olish narxi: {sell}."
    ),
    "st.deal": "🎪 Bozor kuni: bugun kechgacha tuyalar arzon!",
    "btn.camel_buy": "🐫 Bitta olish ({price})",
    "btn.camel_sell": "💱 Bitta sotish (+{price})",
    "gu.title": "🛡 <b>Soqchilar</b>",
    "gu.text": (
        "Soqchilar: <b>{n}</b>/{max}. Yollash {signup} tanga, har biriga kuniga {wage} maosh.\n"
        "Har bir soqchi odamdek ovqat yeydi va kuchingizga 10 qo'shadi.\n"
        "⚔️ Hozirgi kuchingiz ≈ {strength}."
    ),
    "btn.hire": "➕ {n} ta yollash ({money})",
    "btn.dismiss": "➖ Bittasini bo'shatish",
    "pr.title": "🍞 <b>Oziq-ovqat</b>",
    "pr.text": (
        "Qoplarda: <b>{prov}</b>/{cap}. Bu yerda bir ulushi {price} tanga.\n"
        "Karvoningiz kuniga {eat} ulush yeydi (cho'lda ikki barobar)."
    ),
    "btn.prov": "+{n} ({money})",
    "btn.prov_max": "To'ldirish (+{n})",
    # ------------------------------------------------------------------ inn / teahouse
    "inn.title": "🏨 <b>Karvonsaroy</b>",
    "inn.text": "Bir kunlik dam ruhni ko'taradi (+{morale}). Narxi: {cost}.\nHozirgi ruh: {cur}/100.",
    "inn.nilufar": "Nilufar pulingizni olmaydi: «Do'stlar bu yerda tekin tunaydi.»",
    "btn.rest": "🛏 Bir kun dam olish ({cost})",
    "btn.wait": "⏳ Bir kun kutish",
    "tea.title": "🫖 <b>Choyxona</b>",
    "tea.text": "Savdogarlar ko'k choy va turshak ustida gurung qiladi. Yaxshi mish-mish {cost} tanga turadi.",
    "tea.nilufar": "Nilufar choyni o'zi quyib beradi va mehmonlari og'zidan chiqib ketgan gaplarni tekinga aytib beradi.",
    "btn.rumor": "👂 Mish-mish olish ({cost})",
    "rumor.high": "{city_in} {good} kam: donasiga {price} atrofida to'lashyapti",
    "rumor.low": "{city_in} {good} serob: donasi {price} atrofida",
    # ------------------------------------------------------------------ moneylender / council
    "ln.title": "💰 <b>Sudxo'r Yusuf Sarrof</b>",
    "ln.text": (
        "Qarz: <b>{debt}</b>{loan}\n"
        "Keyingi foiz: {next}-kun (qarzga +3%).\n"
        "Muddat: <b>{deadline}-kun</b>. Qo'lingizdagi pul: {money}."
    ),
    "ln.loan": " (shundan qo'shimcha qarz: {loan})",
    "ln.offer": "Yusuf bir marta {amount} tanga qarz berishi mumkin, har 10 kunga 5% foiz bilan.",
    "ln.paid": "Yusufning shartnomasi yirtildi. Hech kimdan qarzingiz yo'q.",
    "btn.pay": "{n} to'lash",
    "btn.pay_all": "Hammasini to'lash ({n})",
    "btn.borrow": "💸 {n} qarz olish",
    "co.title": "⚖️ <b>Uyushma kengashi</b>",
    "co.text": (
        "Samarqand savdogarlar uyushmasining oqsoqollari oynavand zalda yig'ilgan. "
        "Qo'lingizda Hamid amakining maktubi va Buxoro uyushmasi tamg'asi bosilgan Qora Shamol muhri bor."
    ),
    "btn.expose": "📜 Dalillarni ko'rsatish",
    # ------------------------------------------------------------------ travel / road
    "tr.title": "🗺 <b>{city_from} ketadigan yo'llar</b>",
    "tr.hint": "⚔ xavf (1 dan 3 gacha) · 🌾 dasht · 🏜 cho'l (ovqat ×2) · ⛰ tog'lar",
    "tr.btn": "{city} · {n} kun {terrain} {danger}",
    "tc.title": "🧭 <b>{src} → {dst}</b>",
    "tc.text": (
        "⏳ Yo'l: {days} · {terrain} · xavf {danger}\n"
        "🍞 Ovqat: ≈{need} kerak, sizda {prov}\n"
        "🛡 Maosh: ≈{wages}\n"
        "📅 Yetib borish: {arrive}-kun"
    ),
    "tc.warn_food": "⚠️ Oziq-ovqat yetmaydi! Yo'lda uch kun och qolsangiz, qumlar sizni yutadi.",
    "tc.warn_cap": "⚠️ Tuyalar bu yo'l uchun yetarli ovqat ko'tara olmaydi. Tuya oling yoki soqchilarni bo'shating.",
    "tc.warn_wages": "⚠️ Butun yo'l uchun maoshga pulingiz yetmaydi. Maosh olmagan soqchilar g'azablanadi.",
    "tc.warn_deadline": "⚠️ {deadline}-kungacha Samarqandga qaytib ulgurmaysiz!",
    "btn.depart": "✅ Yo'lga chiqish",
    "rd.title": "🐪 <b>{src} → {dst}</b>",
    "rd.flavor.steppe": "Cheksiz dasht. Tuya qo'ng'iroqlari xayollaringizga hamohang jaranglaydi.",
    "rd.flavor.desert": "Ufqqacha barxanlar. Quyosh qumni toblaydi, meshlarda suv chayqaladi.",
    "rd.flavor.mountain": "So'qmoq qorli cho'qqilar orasidan buralib o'tadi. Havo siyrak va sovuq.",
    "rd.progress": "{bar} {total} kundan {done}-kun",
    "rd.food": "🍞 Ovqat ≈{days}ga yetadi.",
    "btn.next_day": "▶️ Keyingi kun",
    "btn.ride_on": "⏩ Yo'lda davom",
    # ------------------------------------------------------------------ status / ledger
    "stt.title": "📜 <b>Karvon holati</b>",
    "stt.day": "📅 {day}-kun. Muddatgacha {left} kun qoldi.",
    "stt.day_paid": "📅 {day}-kun. {final}-kungacha erkin savdo.",
    "stt.money": "💰 Tanga: {money}",
    "stt.debt": "💳 Qarz: {debt} (keyingi foiz {next}-kuni)",
    "stt.debt_paid": "💳 Qarz: {day}-kuni uzilgan ✅",
    "stt.camels": "🐫 Tuyalar: {camels} · 📦 yuk {cargo}/{cap}",
    "stt.prov": "🍞 Oziq-ovqat: {prov}/{cap} (dashtda ≈{days}ga yetadi)",
    "stt.guards": "🛡 Soqchilar: {guards} · ⚔️ kuch ≈{strength}",
    "stt.morale": "😊 Ruh: {morale}/100",
    "stt.rep": "⭐ Obro': {rep}/100",
    "stt.nw": "📈 Umumiy boylik: {nw}",
    "stt.diff": "⚙️ Qiyinlik: {diff}",
    "stt.cargo": "🎒 <b>Yuk:</b>",
    "stt.cargo_empty": "🎒 Yuk qoplari bo'sh.",
    "stt.contract": "📦 Shartnoma: {good} ×{n} → {city}, {until}-kungacha (mukofot {reward})",
    "stt.clues": "🗝 <b>Sir-asror:</b>",
    "stt.flag.letter": "✉️ Hamid amakining maktubi",
    "stt.flag.token": "🪬 Qora Shamolning muhri",
    "stt.flag.exposed": "⚖️ Qorabek fosh etildi",
    "stt.flag.hostile": "😠 Qorabek sizga dushman",
    "stt.flag.nilufar": "🤝 Nilufar sizning do'stingiz",
    "lg.title": "📒 <b>Narxlar daftari</b>",
    "lg.pick": "So'nggi ma'lum narxlarni (olish / sotish) ko'rish uchun shaharni tanlang.",
    "lg.city": "📒 <b>{city}</b> · {age}",
    "lg.none": "{city_from} hali xabar yo'q.",
    # ------------------------------------------------------------------ help / top / ending
    "help.text": (
        "📖 <b>Qanday o'ynaladi</b>\n\n"
        "🎯 <b>Maqsad:</b> 100-kun oxirigacha Samarqandda Yusuf Sarrofga butun qarzni to'lash. "
        "Qarz 10, 20 … 90-kunlarda 3 foizga oshadi.\n\n"
        "🏪 <b>Savdo:</b> har bir shahar ba'zi mollarni arzon ishlab chiqaradi, uzoqdan kelgan mol uchun esa "
        "qimmat to'laydi. Har bir xarid narxni ko'taradi, har bir sotuv tushiradi, shuning uchun pulni bir necha "
        "molga bo'ling. Vaqt o'tib narxlar o'z holiga qaytadi; bayramlar, bozor to'lib ketishi va mish-mishlar "
        "ham ularni o'zgartiradi.\n\n"
        "🐫 <b>Karvon:</b> bir tuya 10 toy yuk va 25 ulush oziq ko'taradi. Yo'ldagi har kuni har bir odam va "
        "har bir tuya bir ulush yeydi, cho'lda ikki barobar. Uch kun ovqatsiz qolsangiz, karvon halok bo'ladi.\n\n"
        "🛡 <b>Soqchilar</b> kuniga 4 tanga oladi va qaroqchilarga qarshi kuchingizni oshiradi. "
        "😊 <b>Ruh</b> yo'lda pasayadi, uni karvonsaroyda tiklang. Nolga tushsa, odamlar isyon ko'taradi. "
        "⭐ <b>Obro'</b> narxlarni yaxshilaydi va ko'p eshiklarni ochadi.\n\n"
        "⚡ <b>Hodisalar</b> karvonni to'xtatib, tanlov qilishga majbur etadi. Xavf ⚔ qancha baland bo'lsa, "
        "ular shuncha ko'p.\n\n"
        "🗝 Amakingizning o'limi ortida sir yashiringan. Sizni sakkizta yakun kutmoqda, ba'zilari yashirin.\n\n"
        "Buyruqlar: /start /status /lang /restart /top /help"
    ),
    "top.title": "🏆 <b>Eng yaxshi karvonlar</b>",
    "top.row": "{rank}. {emoji} <b>{name}</b> — {score}\n      {ending} · {diff} · {day}-kun",
    "top.empty": "Hali tugallangan safarlar yo'q. Birinchi bo'ling!",
    "end.head": "🏁 <b>{title}</b>",
    "end.stats": "📊 Ochko: <b>{score}</b>\n📅 {day}-kun · {diff}\n📈 Umumiy boylik: {nw}",
    "end.E1.title": "Ipak yo'li afsonasi",
    "end.E1.text": (
        "Samarqand sizni unutmaydi. Qorabekning xiyonati fosh bo'lib, Yusufning shartnomasi parcha-parcha "
        "qilingach, tuyalaringiz Qashqardan Hirotgacha bo'lgan har bir yo'lning tayanchiga aylandi. "
        "Karvonsaroy egalari siz uchun eng yaxshi xonani asraydi, qaroqchilar esa bayrog'ingizni ko'rib, "
        "ko'zini yerga tikadi. Endi otga minolmaydigan darajada keksaygan Ravshan ota favvora yonida o'tirib, "
        "bolalarga och odamlar va o'lgan odamning qarzi bilan Qizilqumni qanday kesib o'tganingizni hikoya "
        "qiladi. Hamid amakining nomi yana hurmat bilan tilga olinadi, uning ortidan esa sizning nomingiz. "
        "Ipak yo'lining yangi afsonasi bor va uning daftarini siz yozasiz."
    ),
    "end.E2.title": "Halol savdogar",
    "end.E2.text": (
        "Barcha qarzingizni tiyinigacha to'ladingiz va buni toza qo'l bilan qildingiz. Karvoningiz Samarqanddagi "
        "eng kattasi emas, ammo savdogarlar sizning so'zingizga muhrlangan shartnomadan ham ko'proq ishonadi. "
        "Hech qachon jilmaymaydigan Yusuf Sarrof bozorda sizga bosh irg'ab qo'yadi. Siyob bo'yidan uy olasiz, "
        "yosh tuyakashlarni yollab, ularga Ravshan otadan o'rganganlaringizni o'rgatasiz: oltindan oldin suvni "
        "sana, ertaga kerak bo'ladigan tuyani hech qachon sotma. Buxoro uyushmasi atrofida qanday pichir-pichirlar "
        "yurmasin, ular endi nomingizga dog' tushirolmaydi. Halol mehnat bilan, yo'lma-yo'l topilgan yaxshi hayot."
    ),
    "end.E3.title": "Ozod, ammo kambag'al",
    "end.E3.text": (
        "Yusuf shartnomani yirtgan kuni qo'lingizda bir qozon palovga zo'rg'a yetadigan pul qolgan edi. "
        "Tuyalar qari, qoplar yupqa, yo'llar esa hamon qo'rqitadi. Lekin qarz yo'q, endi Samarqandda hech kim "
        "sizni qul deb atay olmaydi. Ravshan ota kulib aytadi: qarzdor xondan ozod gado tinchroq uxlaydi. "
        "Balki kelasi bahorda Qashqarga olib boradigan uzoq yo'lni yana sinab ko'rarsiz. Balki o'rniga kichkina "
        "do'kon ocharsiz. Hozircha olib yurgan yagona xazinangiz ozodlik, uning esa hech qanday og'irligi yo'q."
    ),
    "end.E4.title": "Qorabekning mirzasi",
    "end.E4.text": (
        "Qorabek iliq jilmayib bir ming besh yuz tangani sanab berdi, Yusuf bilan o'zi hisob-kitob qildi va "
        "siyoh qurimasdanoq tuyalaringizni olib ketdi. Endi siz Buxoro uyushmasi zalining sovuq burchagida, "
        "chiroq yorug'ida o'zgalarning shartnomalarini ko'chirib o'tirasiz. Ba'zan keyinchalik cho'lda izsiz "
        "yo'qolgan karvonlarning nomlarini yozasiz va nima uchunligini so'ramaslikni o'rganasiz. Ravshan ota "
        "yangi xo'jayinga xizmat qilishdan bosh tortib, qishlog'iga qaytib ketdi. Amakingizning bayrog'i "
        "Qorabekning zalida ov o'ljasidek osig'liq turibdi. Siz xavfsizsiz, qorningiz to'q, maoshingiz o'z "
        "vaqtida beriladi. Faqat endi ozod emassiz."
    ),
    "end.E5.title": "Qarz quli",
    "end.E5.text": (
        "Yuzinchi kundan keyingi tongda Yusuf Sarrofning odamlari shahar darvozasida kutib turgan edi. Ular "
        "tuyalarni, yukni va amakingizning uyini olib ketishdi, daftarda esa hamon qarz ko'rinib turardi. Endi "
        "siz qarzni Yusufning omborlarida ishlab uzasiz: tongdan shomgacha o'zgalarning toylarini tashiysiz. "
        "Ochiq darvozadan qo'ng'iroqlarini jaranglatib Buxoro va Qashqarga ketayotgan karvonlarni kuzatasiz. "
        "Ravshan ota juma kunlari sizga non olib keladi va yo'llar haqida og'iz ochmaydi. Ba'zi qarzlar tanga "
        "bilan uziladi. Sizniki yillar bilan uziladi."
    ),
    "end.E6.title": "Qumlarda yo'qolgan",
    "end.E6.text": (
        "Avval shamol izni o'chirdi, keyin suv tugadi, so'ng tuyalar cho'kib, qaytib turmadi. Ravshan ota duo "
        "o'qidi, keyin jim bo'lib qoldi. Oylar o'tib, Xivadan kelgan bir karvon barxanga yarim ko'milgan, oqarib "
        "ketgan jabduqlar va singan sandiqni topdi. Ichida amakingizning eski bayrog'i yotardi: rangi o'chgan, "
        "ammo butun. Samarqandda Yusuf Sarrof hisobingizni bir chiziq siyoh bilan yopdi. Cho'lning o'z daftari "
        "bor va u suvni sanashdagi xatoni kechirmaydi."
    ),
    "end.E7.title": "Isyon",
    "end.E7.text": (
        "Hammasi gulxan yonidagi pichir-pichirdan boshlanib, tong chog'i pichoqlar bilan tugadi. Och va maosh "
        "olmagan tuyakashlaringiz sizni egar ustuniga bog'lab, tuyalarni o'zaro bo'lishib olishdi. Ravshan ota "
        "yolvorib jon-jahdi bilan sizni so'radi, faqat shu tufayli hali tiriksiz. Samarqandga yalangoyoq, "
        "egningizdagi kiyimdan boshqa hech narsasiz qaytdingiz. Yo'l bo'yi har bir quduq sizga xatoyingizni eslatib turdi. Bozorda hamon karvon faqat tuya va toylardan "
        "emas, odamlardan iborat ekanini unutgan karvonboshi haqida hikoya qilishadi."
    ),
    "end.E8.title": "Qora Shamolning sherigi",
    "end.E8.text": (
        "Qilichingizni tushirib, Qora Shamolning qo'lini siqdingiz. Bir mavsum ichida birorta karvon ikkalangizga "
        "boj to'lamay Qizilqumni kesib o'tolmay qoldi. Qorabekning oltini sizning xurjunlaringizga oqib keldi, "
        "so'ng oysiz bir tunda Qora Shamol bilan birga uning xazinasini ham bo'shatdingiz. Yusuf Sarrofning "
        "qarzi hech qachon uzilmadi, mirzalari nomingizni qizil siyoh bilan yozib qo'yishdi, xolos. Ravshan ota "
        "indamay sizni tashlab ketdi. Endi siz boy, qo'rqinchli va quvg'indasiz, yostig'ingiz ostida xanjar "
        "bilan uxlaysiz. Dasht nomingizni pichirlaydi, ammo hech qachon mehr bilan emas."
    ),
    # ------------------------------------------------------------------ Ravshan's tips
    "tip.prefix": "🧓 <b>Ravshan ota:</b>",
    "tip.welcome": (
        "Amaking bizga to'rtta tuya, bir chol va {debt} tanga qarz qoldirdi. Qarz har o'n kunda o'sadi, "
        "100-kuni esa Yusuf hamma narsani olib qo'yadi. Mol qayerda yasalsa, o'sha yerdan ol, qayerda unga zor "
        "bo'lishsa, o'sha yerda sot. Bu yerda qog'oz arzon; Buxoro bilan Toshkent besh kunlik yo'l."
    ),
    "tip.market": (
        "Har bir xarid narxni ko'taradi, har bir sotuv tushiradi; qimmat mollar ayniqsa tez sakraydi. "
        "Qoplarni bitta mol bilan to'ldirgandan ko'ra, pulni bir necha molga bo'l."
    ),
    "tip.travel": (
        "Kunlarga va xavfga qara. Cho'l 🏜 ikki barobar suv ichadi. "
        "Yetarli ovqatsiz yo'lga chiqma: uch kun och qolsak, qumlar bizni yutadi."
    ),
    "tip.road": "▶️ bir kun yuradi, ⏩ biror narsa bo'lgunicha yo'lda davom etadi. Har kuni ovqat va soqchilar maoshi ketadi.",
    "tip.event": "Yo'l kutilmagan hodisalarni yaxshi ko'radi. Tanlashdan oldin o'yla, ba'zi yo'qotishlarni qaytarib bo'lmaydi.",
    "tip.desert": "Cho'l, bolam. Suv ham, non ham ikki hissa. Quduqdan ketishdan oldin ikki marta sana.",
    "tip.mountain": "Tog'lar sovuq va bo'riga to'la. Bu yerda soqchi va issiq mol oltin bilan barobar.",
    "tip.city.buk": "Buxoro. Gilam arzon, bozorni esa Qorabekning uyushmasi boshqaradi. U juda shirin jilmayadi, ehtiyot bo'l.",
    "tip.city.khi": "Xivada mo'yna va eng arzon tuyalar sotiladi. Karvonsaroyni Nilufar tutadi, u hamma gapdan xabardor.",
    "tip.city.mer": "Marv: paxta va uch yo'l chorrahasi. Hirot janubda, xavfli tog'lar ortida, bir haftalik yo'l.",
    "tip.city.tas": "Toshkentda temir asboblar yasaladi. Qashqar sharqda, tog'lar oshib o'n bir kunlik yo'l.",
    "tip.city.kas": "Qashqar! Ipak, chinni va choy bu yerda arzon. Samarqandda ular ikki-uch barobar qimmat.",
    "tip.city.her": "Hirotda lojuvard va ziravorlar sotiladi. Qimmat mollar, ammo shimolda ular katta boylik keltiradi.",
    "tip.lender": "Yusuf sovuqqon, ammo halol. Qo'ling yetganda qarzning bir qismini uzib tur: foiz faqat qolganiga o'sadi.",
    "tip.guards": "Har bir soqchi kuchimizga 10 qo'shadi, lekin kuniga 4 tanga so'raydi. Qaroqchilar bizni yukimizga qarab baholaydi.",
    "tip.stable": "Tuya 10 toy yuk va 25 ulush oziq ko'taradi, lekin o'zi ham har kuni yeydi. Eng arzon tuya Xivada.",
    "tip.low_morale": "Odamlar charchagan, jahli chiqqan. Bizga qarshi chiqishlaridan oldin ularga karvonsaroyda bir kun dam ber.",
    "tip.debt_paid": "Qarz uzildi! Endi o'zimiz uchun savdo qilamiz. Xohlagan paytingda nafaqaga chiq yoki kattaroq marraga intil.",
    "tip.ledger": "Daftar biz ko'rgan narxlarni eslab qoladi. Eski xabar aldaydi, sanasiga qara.",
    "tip.teahouse": "Mish-mish arzon, ammo naf'i katta. Ba'zan biror shahar bir molga zor bo'ladi va buni faqat choyxona biladi.",
    # ------------------------------------------------------------------ action results
    "ok.bought": "✅ Sotib olindi: {good} ×{n}, {money} tanga.",
    "ok.sold": "✅ Sotildi: {good} ×{n}, {money} tanga (foyda {profit}).",
    "ok.camels_bought": "🐫 Karvonga yangi tuya qo'shildi ({money}).",
    "ok.camels_sold": "💱 Tuya sotildi: +{money} tanga.",
    "ok.guards_hired": "🛡 Soqchi yollandi: +{n} ({money}).",
    "ok.guards_dismissed": "🛡 Bo'shatilgan soqchilar: {n}.",
    "ok.provisions": "🍞 Oziq olindi: +{n} ulush, {money} tanga.",
    "ok.rested": "🛏 Bir kunlik dam. Odamlarning kayfiyati ko'tarildi.",
    "ok.waited": "⏳ Bir kun o'tdi.",
    "ok.rumor_high": "👂 Mish-mish: «{rumor}».",
    "ok.rumor_low": "👂 Mish-mish: «{rumor}».",
    "ok.departed": "🐪 Karvon {city_to} yo'l oldi.",
    "ok.day": "▶️ Yo'lda yana bir kun.",
    "ok.rode": "⏩ Yo'lda {days} o'tdi.",
    "ok.paid": "💰 To'landi: {money}. Qolgan qarz: {debt}.",
    "ok.debt_cleared": "🎉 Yusuf Sarrof shartnomani yirtib tashladi. Siz ozodsiz!",
    "ok.borrowed": "💸 Yusuf sizga {money} tanga qarz berdi, har 10 kunga 5% foiz bilan.",
    "ok.council": (
        "⚖️ Zal jimjit bo'lib qoldi. Qorabek unvonidan mahrum etildi, uning chavandozlari yo'llardan qochdi. "
        "Uyushma sizni {money} tanga bilan taqdirladi, nomingiz esa hammaning tilida."
    ),
    "ok.delivered": "📦 To'y egalari molni xursand bo'lib qabul qildi. Mukofot: {money}.",
    "ok.retired": "🏁 Siz yo'llardan nafaqaga chiqdingiz.",
    # ------------------------------------------------------------------ errors
    "err.ended": "Safar tugagan. Menyudan yangisini boshlang.",
    "err.pending": "Avval hodisa bo'yicha qaror qiling.",
    "err.not_in_city": "Siz shaharda emassiz.",
    "err.not_on_road": "Siz yo'lda emassiz.",
    "err.bad_input": "Bunday qilib bo'lmaydi.",
    "err.no_space": "Yuk uchun bo'sh joy yo'q. Tuya oling yoki biror narsa soting.",
    "err.no_money": "Pul yetmaydi.",
    "err.no_goods": "Sizda bu yo'q.",
    "err.max_camels": "Bitta karvonboshi {n} tadan ortiq tuyani eplay olmaydi.",
    "err.last_camel": "Oxirgi tuyangizni sota olmaysiz.",
    "err.cargo_wont_fit": "Qolgan tuyalarga yuk sig'maydi.",
    "err.max_guards": "{n} tadan ortiq soqchi bo'lmaydi.",
    "err.no_guards": "Bo'shatadigan soqchingiz yo'q.",
    "err.prov_full": "Oziq-ovqat qoplari to'la.",
    "err.no_road": "U yerga yo'l yo'q.",
    "err.no_event": "Hozir hech narsa sodir bo'lmayapti.",
    "err.bad_choice": "Bu tanlov mavjud emas.",
    "err.not_here": "Bu yerda buni qilib bo'lmaydi.",
    "err.no_debt": "Sizning qarzingiz yo'q.",
    "err.no_loan": "Yusuf boshqa qarz bermaydi.",
    "err.cannot_deliver": "Shartnomani bu yerda bajara olmaysiz.",
    "err.debt_first": "Avval qarzni uzing.",
    # ------------------------------------------------------------------ notes
    "note.interest": "📈 Foiz qo'shildi: +{money}. Endi qarz {debt}.",
    "note.wages_unpaid": "😠 Maoshga pul yo'q! Soqchilar norozi.",
    "note.guard_left": "🚪 Maosh olmagan soqchi karvonni tashlab ketdi.",
    "note.starving": "🍞 Ovqat yo'q! Odamlar och. Halokatgacha qolgan kunlar: {n}.",
    "note.arrived": "🏁 {city_to} yetib keldingiz.",
    "note.contract_here": "📦 To'y egalari shu yerda {good} ×{n} kutmoqda.",
    "note.contract_failed": "❌ To'y shartnomasining muddati o'tdi. Obro'ingizga putur yetdi.",
    "note.cargo_dropped": "📦 Tuya yetmadi: {n} toy yuk tashlab ketildi.",
    "note.debt_cleared": "🎉 Qarz uzildi! 150-kungacha erkin savdo qiling yoki xohlagan paytda nafaqaga chiqing.",
    "note.deadline_near": "⏳ Yusufning muddatigacha atigi {n} kun qoldi!",
    "note.ending": "🏁 Safar nihoyasiga yetdi.",
    # ------------------------------------------------------------------ event extras
    "ev.strength": "⚔️ Sizning kuchingiz ≈{ours} · ularniki ≈{theirs}",
    "ev.warned": "🤝 Nilufar pistirma haqida ogohlantirgan edi: kuchingizga +{bonus}.",
    # ------------------------------------------------------------------ road events
    "ev.sandstorm.title": "Qum bo'roni",
    "ev.sandstorm.text": "Ufqda qo'ng'ir devor ko'tarilmoqda. Ravshan ota havoni hidlaydi: «Bir soatga qolmay ustimizga yetib keladi.»",
    "ev.sandstorm.c.shelter": "⛺ Qo'nib, kutish (+1 kun)",
    "ev.sandstorm.c.push": "🐪 Bo'rondan yorib o'tish",
    "ev.sandstorm.r.shelter": "Cho'kkan tuyalar panasida yotasiz, qum tepangizdan vishillab o'tadi. Tongga bo'ron tinadi, u bilan birga bir kun ham ketadi.",
    "ev.sandstorm.r.push": "Ko'r-ko'rona olg'a intilasiz. Qoplar yirtilib, qum oziq-ovqatning bir qismini yutib yuboradi.",
    "ev.sandstorm.r.push_camel": "Ko'r-ko'rona olg'a intilasiz. Chang bosilganda bitta tuya yo'q; barxanlar uning izini allaqachon ko'mib bo'lgan.",
    "ev.bandits.title": "Qaroqchilar!",
    "ev.bandits.text": "Qo'llarida kamon tutgan {n} chog'li chavandoz yo'lni to'sib chiqdi. Sardorlari tirjayadi: «Yo yuking, yo joning, savdogar.»",
    "ev.bandits.c.fight": "⚔️ Jang qilish",
    "ev.bandits.c.pay": "💰 Yukning beshdan birini berish",
    "ev.bandits.c.flee": "🏃 Qochish",
    "ev.bandits.r.fight_win": "Soqchilaringiz hujumni qaytardi! Qaroqchilar tarqalib, {loot} tanga tashlab ketdi. Jasoratingiz haqidagi gap yo'llarga tarqaladi.",
    "ev.bandits.r.fight_lose": "Jang yomon tugadi. Bosqinchilar qoplaringizni yorib, o'ljani olib ketdi.",
    "ev.bandits.r.pay": "Yukning beshdan birini topshirasiz. Sardor masxaraomuz ta'zim qilib, yo'l beradi.",
    "ev.bandits.r.pay_money": "Qoplaringiz bo'sh, shuning uchun o'rniga tanga olishdi.",
    "ev.bandits.r.flee_ok": "Tuyalarni qamchilab yugurtirasiz va chavandozlarni jarliklar orasida adashtirib qo'yasiz.",
    "ev.bandits.r.flee_fail": "Ular eng sekin tuyalarga yetib olishdi. Qutulib qoldingiz, lekin hamma narsa bilan emas.",
    "ev.sick_camel.title": "Kasal tuya",
    "ev.sick_camel.text": "Tuyalardan biri o'rnidan turmayapti. Ko'zlari xira, o'zi dir-dir titraydi.",
    "ev.sick_camel.c.treat": "💊 Davolash (−8 oziq)",
    "ev.sick_camel.c.leave": "🚶 Qoldirib ketish",
    "ev.sick_camel.c.slaughter": "🔪 Go'shtga so'yish",
    "ev.sick_camel.r.treat_ok": "Ravshan ota tuya sutida giyoh qaynatadi. Tushga yaqin hayvon yana oyoqqa turadi.",
    "ev.sick_camel.r.treat_fail": "Hamma chorani ko'rdingiz, ammo tuya kechasi o'ldi.",
    "ev.sick_camel.r.leave": "Yukini olib, yo'lda davom etasiz. Uzoq vaqt orqangizdan uning bo'kirigi eshitilib turadi.",
    "ev.sick_camel.r.slaughter": "Og'ir ish, lekin odamlar bir necha kun go'sht yeydi.",
    "ev.oasis.title": "Voha",
    "ev.oasis.text": "Xurmo daraxtlari va tiniq buloq! Tuyalar o'zlari o'sha tomonga tortadi.",
    "ev.oasis.c.rest": "🌴 Bir kun shu yerda dam olish (+1 kun)",
    "ev.oasis.c.water": "💧 Meshlarni to'ldirib, yo'lda davom etish",
    "ev.oasis.r.rest": "Bir kun soya, xurmo va salqin suv. Odamlar yana qo'shiq aytmoqda.",
    "ev.oasis.r.water": "Suv sig'adigan hamma narsani to'ldirib, yo'lda davom etasiz.",
    "ev.traveler.title": "Adashgan yo'lovchi",
    "ev.traveler.text": "Sarob ichidan yirtiq kiyimli bir odam gandiraklab chiqib keladi, chanqoqdan lablari yorilgan. U o'z karvonidan adashib qolgan.",
    "ev.traveler.c.share": "🍞 Ovqat berish (−5 oziq)",
    "ev.traveler.c.escort": "🐪 O'zi bilan olish (−10 oziq, +1 kun)",
    "ev.traveler.c.pass": "🚶 Yonidan o'tib ketish",
    "ev.traveler.r.share": "U sizni va bolalaringizning bolalarini duo qiladi. Bu yo'llarda yaxshilik unutilmaydi.",
    "ev.traveler.r.escort": "Uni qarindoshlari kutib turgan quduqqa yetkazasiz. Ular nomingizni eslab qolishga va'da berishadi.",
    "ev.traveler.r.escort_paid": "Qarindoshlari savdogar bo'lib chiqdi. Ular qo'lingizga {money} tanga tutqazishadi.",
    "ev.traveler.r.pass": "Odamlar uning sarobda g'oyib bo'lishini kuzatib turadi. Uzoq vaqt hech kim churq etmaydi.",
    "ev.toll.title": "Boj posti",
    "ev.toll.text": "Mahalliy bek yo'lga zanjir tortib qo'ygan. Uning odamlari o'tish uchun {fee} tanga talab qilmoqda.",
    "ev.toll.c.pay": "💰 {fee} to'lash",
    "ev.toll.c.detour": "↩️ Aylanib o'tish (+2 kun)",
    "ev.toll.c.talk": "🗣 Gap bilan o'tib ketish",
    "ev.toll.r.pay": "Zanjir tushadi. Bekning mirzasi ismingizni yog'li daftarga yozib qo'yadi.",
    "ev.toll.r.detour": "Tepaliklarga burilasiz. Aylanma yo'l ikki kunga tushadi, lekin bir tanga ham emas.",
    "ev.toll.r.talk_ok": "Bek siz haqingizda eshitgan ekan. «Halol savdogarga yo'l tekin», deydi va o'tishga ishora qiladi.",
    "ev.toll.r.talk_fail": "Shirin so'zlaringiz uni kuldiradi, lekin narx o'sha-o'sha: {fee} tanga.",
    "ev.wolves.title": "Bo'rilar to'dasi",
    "ev.wolves.text": "Qoyalar orasida uvillash aks-sado beradi. G'ira-shirada o'nlab juft sariq ko'zni sanaysiz.",
    "ev.wolves.c.fight": "⚔️ Soqchilar bilan haydash",
    "ev.wolves.c.fire": "🔥 Tun bo'yi gulxan yoqish (−6 oziq)",
    "ev.wolves.c.run": "🏃 Dovondan shoshilib o'tish",
    "ev.wolves.r.fight_win": "Nayzalar va mash'alalar to'dani quvib soladi. Odamlar shodlikdan qiyqiradi.",
    "ev.wolves.r.fight_lose": "Bo'rilar safni yorib o'tib, bir tuyani zulmatga sudrab ketadi.",
    "ev.wolves.r.fire": "Tong otguncha tezak va ortiqcha qoplarni yoqasiz. Hech kim uxlamaydi, lekin hech kim o'lmaydi.",
    "ev.wolves.r.run_ok": "Karvonni dovondan yugurtirib o'tkazasiz. Uvillash ortda so'nib boradi.",
    "ev.wolves.r.run_loss": "Shoshqaloqlikda bir tuya ortda qoladi. Bo'rilar aynan shuni kutayotgan edi.",
    "ev.merchant.title": "Yo'l savdogari",
    "ev.merchant.text": "Eshaklariga og'ir yuk ortgan yolg'iz savdogar taklif qilmoqda: {good} ×{qty}, donasi {price} tangadan.",
    "ev.merchant.c.buy": "🤝 Sotib olish",
    "ev.merchant.c.haggle": "🗣 Savdolashish",
    "ev.merchant.c.decline": "🙅 Rad etish",
    "ev.merchant.r.buy": "Xarid qildingiz: {good} ×{n}, jami {money} tanga.",
    "ev.merchant.r.haggle_ok": "Uzoq tortishuvdan keyin u ko'nadi: {good} ×{n}, jami {money} tanga.",
    "ev.merchant.r.haggle_fail": "Taklifingizdan ranjigan savdogar tugunlarini bog'lab, jo'nab qoladi.",
    "ev.merchant.r.decline": "Xushmuomalalik bilan xayrlashasiz. Kim biladi, balki yo'l sizni yana uchrashtirar.",
    "ev.quarrel.title": "Qarorgohda janjal",
    "ev.quarrel.text": "Ikki tuyakash suv ulushi ustida baqirishmoqda. Qolganlar allaqachon ikki tomonga bo'linib olgan.",
    "ev.quarrel.c.bonus": "💰 Hammaga mukofot berish",
    "ev.quarrel.c.judge": "⚖️ Nizoni o'zingiz hal qilish",
    "ev.quarrel.c.ignore": "🙈 O'zlari hal qilsin",
    "ev.quarrel.r.bonus": "{money} tanga va bir-ikki iliq so'z mo''jiza yaratadi. Odamlar tinchlanadi.",
    "ev.quarrel.r.judge_ok": "Hukmingiz adolatli, hamma uni qabul qiladi. Hatto yutqazgan ham bosh irg'aydi.",
    "ev.quarrel.r.judge_fail": "Hukmingiz hech kimga yoqmaydi. Qarorgoh bir necha kun qovoq solib yuradi.",
    "ev.quarrel.r.ignore": "Janjal cho'g'dek tutab, butun qarorgohga yoyiladi. Kayfiyat tushadi.",
    "ev.dervish.title": "Sayyoh darvesh",
    "ev.dervish.text": "Yo'l chetida yamoq to'n kiygan darvesh o'tiribdi. «Men hamma joyda bo'lganman, — deydi u, — va hammasini ko'raman.»",
    "ev.dervish.c.alms": "🪙 Sadaqa berish (5 tanga)",
    "ev.dervish.c.listen": "👂 Shunchaki tinglash",
    "ev.dervish.c.pass": "🚶 Yo'lda davom etish",
    "ev.dervish.r.alms": "U sizni duo qilib, pichirlaydi: «{rumor}.»",
    "ev.dervish.r.listen_ok": "Topishmoqlar orasida og'zidan gap chiqib ketadi: «{rumor}.»",
    "ev.dervish.r.listen_vague": "U yulduzlar, qum va boylikning bevafoligi haqida gapiradi. Foydali hech narsa yo'q.",
    "ev.dervish.r.pass": "U ortingizdan kuladi, go'yo siz bilmagan narsani biladigandek.",
    "ev.flood.title": "Sel",
    "ev.flood.text": "Tog'larda momaqaldiroq gumburlaydi. Bir necha daqiqadan so'ng siz kesib o'tayotgan quruq soyga loyqa sel bostirib keladi!",
    "ev.flood.c.save_cargo": "📦 Yukni qutqarish",
    "ev.flood.c.save_camels": "🐫 Tuyalarni qutqarish",
    "ev.flood.r.cargo_ok": "Toylarni o'z vaqtida baland joyga sudrab chiqasiz. Hamma ivib ketgan, lekin tirik.",
    "ev.flood.r.cargo_camel": "Toylar qutqarildi, ammo suv bir tuyani yiqitib, oqizib ketdi.",
    "ev.flood.r.camels": "Yuklarni kesib tashlab, tuyalarni olib chiqasiz. Sel yukning bir qismini yutib yuboradi.",
    "ev.saddle.title": "Singan egar",
    "ev.saddle.text": "Egar ayili uzilib, butun bir yuk changga sirg'alib tushadi.",
    "ev.saddle.c.rope": "🪢 Oziq qoplari bilan bog'lash (−8 oziq)",
    "ev.saddle.c.fix": "🔧 Puxta tuzatish (+1 kun)",
    "ev.saddle.c.drop": "🗑 Yukning bir qismini qoldirish",
    "ev.saddle.r.rope": "Bir necha oziq qopini bo'shatib, arqon qilib eshasiz. Chidaydi.",
    "ev.saddle.r.fix": "Ravshan ota gulxan yonida charmni tikadi. Bir kun ketdi, lekin egar yangidek.",
    "ev.saddle.r.drop": "Yo'l chetida {good} ×{n} qoldirasiz. Qaysidir omadli yo'lovchi xursand bo'ladi.",
    "ev.cold.title": "Qahraton sovuq",
    "ev.cold.text": "Cho'qqilardan muzdek shamol esadi. Tuyalarning juniga qirov qo'nadi, eng zaifi titramoqda.",
    "ev.cold.c.camp": "⛺ Qo'nib, kutib turish (+1 kun)",
    "ev.cold.c.push": "🐪 Yo'lda davom etish",
    "ev.cold.c.burn": "🧣 Tuyalarni mo'yna va matoga o'rash",
    "ev.cold.r.camp": "Shamol tingunicha chuqurlikda bir-biringizga qisilib o'tirasiz.",
    "ev.cold.r.push_ok": "Tishlaringiz takillab, dovondan o'tasiz. Hamma omon.",
    "ev.cold.r.push_loss": "Dovon tepasida bir tuya qorga cho'kadi va boshqa turmaydi.",
    "ev.cold.r.burn": "Tuyalarni o'z molingizga o'raysiz. Bir necha toy buzildi, lekin hamma isindi.",
    "ev.abandoned.title": "Tashlab ketilgan yuk",
    "ev.abandoned.text": "Yo'l chetida o'lik tuya va bir necha toy yotibdi: {good}, taxminan {qty} dona. Egasi ko'rinmaydi.",
    "ev.abandoned.c.take": "🎒 Molni olish",
    "ev.abandoned.c.bury": "🙏 Suyaklarni ko'mib, duo qilish",
    "ev.abandoned.c.leave": "🚶 Hammasini qoldirish",
    "ev.abandoned.r.take": "Ortib olasiz: {good} ×{n}. Ravshan ota nimadir yomon alomat haqida g'o'ldiraydi.",
    "ev.abandoned.r.take_seen": "Ortib olasiz: {good} ×{n}, lekin cho'ponlar ko'rib qoldi. Tez orada bozorlarda sizni o'likni talagan deb gapirishadi.",
    "ev.abandoned.r.bury": "Marhumning haqini ado etasiz. Buni eshitgan yo'lovchilar sizni hurmat qiladi.",
    "ev.abandoned.r.leave": "Yonidan o'tib ketasiz. Yo'lning ham egasi bor, garchi ko'zga ko'rinmasa ham.",
    "ev.deserter.title": "Qochoq",
    "ev.deserter.text": "Kechasi soqchilaringizdan biri narsalarini yig'ishtiradi. «Maosh oz, yo'l uzoq», deb to'ng'illaydi u.",
    "ev.deserter.c.pay": "💰 Ustama to'lash (20)",
    "ev.deserter.c.let_go": "👋 Ketishiga ruxsat berish",
    "ev.deserter.c.chase": "🏇 Quvib yetish",
    "ev.deserter.r.pay": "Yigirma tanga uning fikrini o'zgartiradi. Hozircha.",
    "ev.deserter.r.let_go": "U tunga singib ketadi. Bitta nayza kamaydi.",
    "ev.deserter.r.chase_ok": "Tongda uni tutib olasiz. Hammaning oldida uyalib, sodiq xizmat qilishga qasam ichadi.",
    "ev.deserter.r.chase_fail": "U qochib qutuladi va bir hamyon tangani ham olib ketadi.",
    "ev.pilgrims.title": "Ziyoratchilar",
    "ev.pilgrims.text": "Muqaddas qadamjoga ketayotgan bir guruh ziyoratchi sizning panohingizda yo'l yurishni so'ramoqda.",
    "ev.pilgrims.c.escort": "🤝 Birga olish (−6 oziq)",
    "ev.pilgrims.c.decline": "🙅 Rad etish",
    "ev.pilgrims.r.escort": "Ziyoratchilar har bekatda siz uchun duo qiladi va {money} tanga nazr qoldiradi.",
    "ev.pilgrims.r.decline": "Ular yolg'iz yo'lga tushadi. Keyingi shaharda odamlar ularni rad etganingizni eshitadi.",
    "ev.dry_well.title": "Qurigan quduq",
    "ev.dry_well.text": "Ravshan otaning xaritasidagi quduq qurib qolibdi. Yaqin atrofdagi ko'chmanchilar suvni {cost} tangaga taklif qilmoqda.",
    "ev.dry_well.c.dig": "⛏ Chuqurroq qazish (+1 kun)",
    "ev.dry_well.c.buy": "💰 Suv sotib olish ({cost})",
    "ev.dry_well.c.ration": "🥤 Ulushni qisqartirish",
    "ev.dry_well.r.dig": "Bir kunlik qazishdan so'ng quduqqa sovuq loyqa suv yig'iladi.",
    "ev.dry_well.r.buy": "Ko'chmanchilar meshlaringizni to'ldiradi. Qimmat suv ham baribir suv.",
    "ev.dry_well.r.ration": "Yarim ulush. Odamlar har qadamda to'ng'illaydi.",
    "ev.black_wind.title": "Qora Shamol",
    "ev.black_wind.text": (
        "Har bir barxanda qora bayroqlar. O'nlab chavandoz karvonni o'rab oladi, yuzini qora ro'mol bilan "
        "to'sgan bir kishi oldinga chiqadi. «Men Qora Shamolman. Buxoroda kimdir boshing uchun yaxshi haq "
        "to'laydi, savdogar.»"
    ),
    "ev.black_wind.c.fight": "⚔️ Oxirigacha jang qilish",
    "ev.black_wind.c.tribute": "💰 O'lpon to'lash (yukning 40%)",
    "ev.black_wind.c.flee": "🏜 Barxanlarga qochish",
    "ev.black_wind.c.join": "🤝 «Keling, ish haqida gaplashaylik…»",
    "ev.black_wind.r.fight_win": (
        "Jang quyosh botguncha davom etadi. Qora Shamol otdan qulaganda, odamlari tumtaraqay qochadi. Uning "
        "barmog'idan Buxoro uyushmasi tamg'asi bosilgan muhr topasiz, xurjunidan esa {loot} tanga."
    ),
    "ev.black_wind.r.fight_lose": "Qora Shamolning chavandozlari safingizni yorib o'tadi. Tirik qoldingiz, ammo dahshatli bahoda.",
    "ev.black_wind.r.tribute": "Qora Shamolning odamlari o'z ulushini oladi. «Qorabekka salom ayt», deb kuladi sardorlari.",
    "ev.black_wind.r.flee_ok": "Karvonni otlar yurolmaydigan chuqur barxanlarga boshlaysiz. Bir muddat adashasiz, lekin qutulib ketasiz.",
    "ev.black_wind.r.flee_fail": "Barxanlar tuzoqqa aylanadi. Chavandozlar karvonning dumini kesib oladi.",
    "ev.black_wind.r.join": "Qora Shamol ro'molini tushirib jilmayadi. «Til topishishimizni bilardim.»",
    # ------------------------------------------------------------------ city events
    "ev.festival.title": "Bayram",
    "ev.festival.text": "Nog'ora va surnay sadolari! Shahar bayram qilmoqda. Savdogarlarning aytishicha, bir necha kun {good} va {good2} qimmatga o'tadi.",
    "ev.festival.c.feast": "🎉 Odamlarni mehmon qilish ({cost})",
    "ev.festival.c.trade": "🏪 Ish bilan band bo'lish",
    "ev.festival.r.feast": "Yarim tungacha palov, musiqa va o'yin-kulgi. Odamlar buni unutmaydi.",
    "ev.festival.r.trade": "Boshqalar raqsga tushayotganda, siz narxlarni o'rganasiz.",
    "ev.plague.title": "Vabo",
    "ev.plague.text": "Kambag'al mahallalarda isitma tarqalib, shahar darvozalarini yopmoqda. Narxlar osmonga chiqdi, tuyakashlaringiz qo'rqib turibdi.",
    "ev.plague.c.endure": "😷 Sabr qilib, ishda davom etish",
    "ev.plague.c.medicine": "💊 Dori sotib olish (25)",
    "ev.plague.c.help": "🍞 Bemorlarni ovqatlantirish (−10 oziq)",
    "ev.plague.r.endure": "Tez-tez savdo qilasiz, lekin qo'rquv odamlarni ichdan yemiradi.",
    "ev.plague.r.medicine": "Achchiq giyoh damlamalari va isiriq tutuni odamlarni sog'lom va xotirjam saqlaydi.",
    "ev.plague.r.help_ok": "Shahar kambag'allarini boqqan savdogarni unutmaydi.",
    "ev.plague.r.help_sick": "Shahar sizni olqishlaydi, ammo ikki tuyakashingiz ham yo'tala boshladi.",
    "ev.guild_tax.title": "Uyushma yig'imi",
    "ev.guild_tax.text": "Qorabekning mirzalari darvozani to'sib olgan. «Uyushma do'stligini rad etgan savdogarlar uchun maxsus yig'im: {tax} tanga.»",
    "ev.guild_tax.c.pay": "💰 {tax} to'lash",
    "ev.guild_tax.c.refuse": "✋ Rad etish",
    "ev.guild_tax.c.bribe": "🤫 Mirzaga pora berish ({bribe})",
    "ev.guild_tax.r.pay": "Mirza tangalaringizni ikki marta sanab, sovuq jilmayadi.",
    "ev.guild_tax.r.refuse": "Siz ketasiz. Ortingizdan mirzalar daftarlariga nimadir yozib qo'yadi.",
    "ev.guild_tax.r.refuse_seized": "Uyushma soqchilari yukingizning bir qismini «tekshirish uchun» musodara qiladi. Uni boshqa ko'rmaysiz.",
    "ev.guild_tax.r.bribe": "Mirza tangalarni cho'ntagiga solib, birdan osmonni tomosha qilishga tushadi.",
    "ev.guild_tax.r.bribe_caught": "Mirza pulni oladi-yu, baribir sizni chaqib beradi. Butun bozor bu haqda eshitadi.",
    "ev.glut.title": "Bozor to'lib ketdi",
    "ev.glut.text": "Karvonlar bozorni to'ldirib yubordi: {good} narxi tushib ketdi. Ulgurji savdogar sizga donasi {price} tangadan bir partiya taklif qilmoqda.",
    "ev.glut.c.buy_lot": "🛒 Partiyani olish (10 tagacha)",
    "ev.glut.c.note": "📝 Narxlarni yozib qo'yish",
    "ev.glut.r.buy_lot": "Xarid qildingiz: {good} ×{n}, jami {money} tanga.",
    "ev.glut.r.note": "Yozib qo'yasiz: bu yerda {good} bir muddat arzon bo'ladi.",
    "ev.wedding.title": "To'y buyurtmasi",
    "ev.wedding.text": "Badavlat bir oila to'yga tayyorlanmoqda. Ularga {until}-kungacha {city_to} yetkazib beriladigan {good} ×{qty} kerak. Mukofot: {reward} tanga.",
    "ev.wedding.c.accept": "✍️ Shartnomani qabul qilish",
    "ev.wedding.c.decline": "🙅 Rad etish",
    "ev.wedding.r.accept": "Qo'l berib ko'rishasiz. Shartnoma daftaringizga yozildi (📜 Holat).",
    "ev.wedding.r.decline": "Oila oqsoqoli xo'rsinib, boshqa karvonboshi qidirgani ketadi.",
    "ev.camel_fair.title": "Tuya bozori",
    "ev.camel_fair.text": "Ko'chmanchilar bozorga poda haydab kelishdi. Bugun bir tuya atigi {price} tanga.",
    "ev.camel_fair.c.buy_one": "🐫 Bitta olish ({price})",
    "ev.camel_fair.c.look": "👀 Shunchaki tomosha",
    "ev.camel_fair.r.buy_one": "Karvoningizga baquvvat yosh tuya qo'shildi.",
    "ev.camel_fair.r.look": "Podani tomosha qilasiz. Arzon narx kechgacha saqlanadi (🐫 Tuyaxona).",
    "ev.nilufar.title": "Nilufarning karvonsaroyi",
    "ev.nilufar.text": (
        "Xiva karvonsaroyining bekasi Nilufar sizni ko'zlarida yosh bilan kutib oladi. Qorabekning odamlari "
        "«himoya» uchun 60 tanga talab qilmoqda, aks holda ertaga otxonalariga o't qo'yishadi."
    ),
    "ev.nilufar.c.pay": "💰 Uning o'rniga to'lash (60)",
    "ev.nilufar.c.refuse": "🙅 Bu mening ishim emas",
    "ev.nilufar.r.pay": "«Buni unutmayman, — deydi Nilufar. — Uyimda sizga doim joy ham, rost gap ham topiladi.»",
    "ev.nilufar.r.refuse": "Nilufar indamay bosh irg'aydi. Ertasi tongda otxonalari ustida tutun ko'tariladi.",
    "ev.grateful.title": "Eski tanish",
    "ev.grateful.text": "Bozorda boy to'n kiygan bir savdogar sizni to'xtatadi: bu siz bir paytlar yo'lda yordam bergan yo'lovchi! U yaxshilikni qaytarmoqchi.",
    "ev.grateful.c.gift": "💰 Sovg'ani qabul qilish",
    "ev.grateful.c.news": "👂 Undan yangilik so'rash",
    "ev.grateful.r.gift": "U qo'lingizga {money} tanga tutqazib, oq yo'l tilaydi.",
    "ev.grateful.r.news": "U ikki sirni aytadi: tez orada {city_in} {good}, {city2_in} esa {good2} qimmatlashadi.",
    "ev.qorabek.title": "Qorabekning taklifi",
    "ev.qorabek.text": (
        "Buxoro savdogarlar uyushmasining boshlig'i Qorabek sizni uyiga taklif qiladi. Sharbat ustida xo'rsinadi: "
        "«Amakingiz buyuk inson edi, lekin yo'llar shafqatsiz. Karvon uchun sizga {money} tanga beraman, Yusuf "
        "bilan o'zim hisob-kitob qilaman. Menga xizmat qilasiz: issiq, to'q va xavfsiz.»"
    ),
    "ev.qorabek.c.accept": "🤝 Taklifni qabul qilish",
    "ev.qorabek.c.refuse": "✋ Rad etish",
    "ev.qorabek.r.accept": "Qorabek sizni o'z o'g'lidek quchoqlaydi. Mirzasi allaqachon hujjatni yozmoqda.",
    "ev.qorabek.r.refuse": "Qorabekning tabassumi o'zgarmaydi, ammo ko'zlari sovuqlashadi. «Cho'l yo'llari xavfli, do'stim. Ehtiyot bo'ling.»",
    "ev.letter.title": "Amakining maktubi",
    "ev.letter.text": (
        "Amakingizning eski uyidan bir xizmatkor muhrlangan maktub olib keladi. Hamidning qo'li bilan yozilgan: "
        "«Agar qaytmasam, bilib qo'y: Qorabek uyushmaga bo'ysunmagan karvonlarni talash uchun Qora Shamolga pul "
        "to'laydi. Menga dalil kerak: Qora Shamolning muhri.»"
    ),
    "ev.letter.c.keep": "✉️ Maktubni saqlash",
    "ev.letter.c.burn": "🔥 Yoqish: o'tgan ishga salovat",
    "ev.letter.r.keep": "Maktubni belbog'ingizga yashirasiz. Agar muhrni qo'lga kiritsangiz, Samarqanddagi uyushma kengashi ikkalasini ham ko'rishi kerak.",
    "ev.letter.r.burn": "Kul shamolda sochilib ketadi. Odamlar sizning xotirjamroq bo'lib qolganingizni sezadi.",
}
