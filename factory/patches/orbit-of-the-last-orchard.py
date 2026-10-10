# Claude full read-through patches (2026-10-10). (chapter or 0 for any, old, new); each old string must exist.
E1 = "*The Handbook of Small Truths, Entry 12: The machine does not sleep; it only listens for the leak.*\n\n"
E2 = "*The Handbook of Small Truths, Entry 4: A name is a latch that holds the door open.*\n\n"
E3 = "*The Handbook of Small Truths, Entry 4: A seed does not know it is a promise. It only knows it is hungry.*\n\n"
PATCHES = [
 # spelling (American) and dashes
 (0, "kilometres", "kilometers"), (0, "practised", "practiced"), (0, "centimetres", "centimeters"), (0, "litres", "liters"),
 (0, "metres", "meters"), (0, "graphite-fibre", "graphite-fiber"),
 (0, "You're stood on", "You're standing on"),
 (0, "we should not—\"", "we should not...\""),
 (0, "spectral response against the—\"", "spectral response against the...\""),
 # ch2 logic
 (2, "He had been told, she realized, to stay away from the Power Office. But he had stayed near it. He had been waiting for her.", "He had been waiting, she realized, for her to leave the Power Office."),
 # ch4 physics of Voss's speech
 (4, "If we lose that margin, we must throttle the reactor. If we throttle the reactor, we lose heat rejection. If we lose heat rejection, we cook ourselves.", "If we lose that margin, the radiators cannot shed the heat. Then we must throttle the reactor, and every pump and light on the ship goes with it. If we do not throttle it, we cook ourselves."),
 # ch7 continuity
 (7, "the way the light caught the silver in her own hair, a streak of rebellion in the dark curls", "the way the light caught the white of her close-cropped hair"),
 (7, "a long time ago. Before you were born. Before the orchard was even a thought.", "eleven years ago, when you were six."),
 (7, "\"I served on the Council’s technical subcommittee, a long time ago. Before you were born. Before the orchard was even a thought.\"", "\"I served on the Council’s technical subcommittee, eleven years ago, when you were six.\""),
 # ch8
 (8, "such a perfect, deflection answer", "such a perfect, deflecting answer"),
 (8, "the only living thing on the ship that bloomed in winter", "the only fruit trees on the ship"),
 # ch9 Daro description consistent with ch3
 (9, "He was a small man with a white beard and eyes that missed nothing", "He was a large, bald man with thick grey eyebrows and eyes that missed nothing"),
 # ch10 timeline wording
 (10, "It has been bad for eleven years,\" he said. \"The radiator loop.", "It has been bad for eleven years, and lately it is worse,\" he said. \"The radiator loop."),
 (10, "Enough to drop the rejection capacity by zero point four percent every month,", "Enough to drop the rejection capacity by zero point four percent every month now,"),
 # ch11
 (11, "It’s been going for years. Decades, maybe.", "It’s been going for eleven years at least."),
 # ch12
 (12, "They have been growing in the dark for two hundred years.", "They have been growing under lamps for two hundred years."),
 (12, "\"The last time I sent a kid out there,\" he said, his voice low and rough, \"he made a mistake. A small one. A fraction of a second too late.\"", "\"The last time I sent someone out there,\" he said, his voice low and rough, \"he made a mistake. A small one. A fraction of a second too late. He lost his left hand.\""),
 (12, "\"He survived,\" Voss added, after a pause. \"But he was not fast enough. And he was not right.\"", "\"He survived,\" Voss added, after a pause. \"But he never worked again.\""),
 # ch13
 (13, "\"We have thirty days,\" Kess said. \"And we have a plan. Let's go.\"", "\"We have three weeks,\" Kess said. \"And we have a plan. Let's go.\""),
 # ch14
 (14, "The barn smelled of rust and old grease", "The workshop smelled of rust and old grease"),
 (14, "like a astronaut", "like an astronaut"),
 (14, "cold concrete", "cold steel decking"),
 (14, "hair the color of iron filings", "sleek white hair"),
 (15, "the concrete walls cool", "the steel walls cool"),
 # ch17
 (17, "I am the best one in the fleet.", "I am the best one aboard."),
 # ch18
 (18, "Mr. Daro, the senior rigger,", "Mr. Daro, the retired welder,"),
 (18, "Keep the tenses tight", "Keep the tethers tight"),
 # ch19
 (19, "the dried apple cores clinking softly", "the wooden cores clinking softly"),
 # ch20 stray epigraphs (only page 1 of a chapter carries one)
 (20, E1, ""), (20, E2, ""),
 # ch21 zero-g
 (21, "He felt the spin of the ship, a gentle, constant pull tugging at his limbs, a reminder of the world that held them all together.", "He felt no pull at all, only the faint drag of the tether, and behind him the whole turning world that held them together."),
 # ch24
 (23, "not shown a soft expression in the three years Kess had known him", "not shown a soft expression in all the years Kess had known him"),
 (24, "A young engineer named Ferris Quill stood up. He had a shock of red hair and a tool-belt that looked older than the ship.\n\n\"I have been waiting for that proposal for ten years,\" he said, his voice rough. \"I have been trying to tell people about the coolant leaks. They looked at me as if I had grown a second head. This is the first time I feel like I am part of the ship, not just a part of the machine.\"",
     "Councilor Ferris Quill stood up, thin and white-haired, and for once he did not look skeptical.\n\n\"I objected to every number that girl brought me,\" he said, his voice dry. \"She made me check all of them. I withdraw the rest of my objections, and I second the motion.\""),
 # ch25
 (25, "Mr. Daro, the baker who rarely left his kitchen,", "Mr. Daro, the retired welder who rarely left his workshop,"),
 (25, "which clashed violently with his usual stained coveralls", "which clashed violently with his usual scorched leather apron"),
 (25, E3, ""),
 (25, "The eleven-thousand-ninety-fortieth apple", "The eleven-thousand-nine-hundred-fortieth apple"),
]
