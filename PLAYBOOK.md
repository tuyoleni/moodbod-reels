# Moodbod reels: what we learned (from the shared session)

Brand: moodbod.agency, Windhoek. Websites, custom software, AI automation for small businesses in Namibia and beyond. Audience: small business owners in Namibia.

## Format that works
- Reel 35-46s, 1080x1920. One idea. Hook -> stake (one real number) -> body (frame changes every beat) -> payoff -> last line echoes a hook word so the replay loops.
- Write 3 hooks from different formulas, score them (hookscore.py), pick the best, time it (beats.py). Aim for hook under 3s, no beat over 4s.
- Turn the reel into a GAME or visible payoff, not advice. "Spot the mistake" and the 97-dot Google grid were the 10/10s. Advice reels get scrolled past; lame/boring feedback came on "stop closing at 5" and the 41-blues stick figures.
- Ask a question at the end ("Which one would you call?", "What are you still guessing on?"). NO "drop it in the comments" and NO on-screen CTA. The CTA lives in the caption only.
- Only true numbers, searched first (StatCounter, DataReportal, Google, named case studies). Never invent. List sources under the caption.

## Visual rules
- Real-looking screens: build real HTML pages (e.g. Ndapewa's Kitchen site) and screenshot them in clean modern phone/laptop frames. Real Pexels photos (free commercial). No stick figures, no grey-bar fake sites, no tiny diagrams.
- Elements big, filling the safe area, one clear focal point. No text under ~22px at 720 wide.
- The dot-grid effect: each dot blips with rising pitch, soft low note when it stops. Keep it.
- Never crop the phone when "focusing"; use a magnifier bubble or keep the phone whole. (Camera zoom version was preferred in one case; ask if unsure.)
- No wordmark at the top. No carousel dashes. No floating background shapes (looked dirty). Plain single background colour per reel.
- Colours: one colour per reel from the Moodbod grid: lime (strongest), lavender, sky blue, peach, off-white, plus dark tile with lime. Black regular-weight text, key word on a coloured highlight, white cards with thin black outlines. Reel 1 colour only.
- Safe area (measured from a posted reel, 1080x1920): nothing in top 250px, bottom 420px, 65px left, 140px right (button column from halfway down); IG crops ~31px/side at 720w on tall phones. Always send frames first, render after "go".

## Audio rules
- Voice: Ava (free neural voice, natural pace, energetic opening). Do NOT speed up (18% faster was rejected). The script is what makes it natural: write like talking to an owner, contractions, short lines.
- Music: no ticking background. Mellow ~96bpm groove (warm keys, soft bass, light kick), well under the voice, ducked while she speaks. Pops/clicks/dings OK. No whooshes.
- Optionally ship a voice-only version so they can add trending audio in Instagram.

## Captions
- Not a copy of the video. Line 1 adds a hook. Body carries search words (website design Windhoek). Single CTA at the end as a DM keyword (DM us CHECK / REPLY / SPEED / PHOTOS / TEST) and only if they can fulfil it.
- Max 5 hashtags, ALL LOWERCASE (#moodbod #websitedesign #smallbusinessnamibia #windhoek #namibia).
- Sources listed after.

## Topics already done (don't repeat)
Hidden full-time job (admin), same WhatsApp questions, should you have an app, customers Google you first (97%), stop checking on a laptop (mobile 50.67%), stop closing at 5, spot the mistake, 20 questions a day, half your visitors leave (53% / 3s), Airbnb camera, 41 shades of blue, Instagram/Burbn. Story-with-characters (Sheep, Mara the goat, Lio, Baba, Kovu, Zuri) was an experiment, dropped: "back to normal moodboard content".

## Ideas not yet made
Spot the mistake #2 (salon, car wash, guesthouse, school); Google Business Profile before/after; QR code/WhatsApp catalogue story; "your logo on a phone" test; real Moodbod client case (needs real client facts from the user).

## Tools
- ig-reel skill (hookscore.py, beats.py, hooks.json), ig-caption (caption.py), ig-human (humanize.py): github.com/Jakeschincariol/instagram-agent-skill
- Voice here: Kokoro ONNX (Edge TTS is blocked in this workspace); af_heart / af_bella / af_nicole closest to Ava.

## Format that did best on the feed (user-confirmed): "study story"
Caption shape: surprising true outcome as line 1 ("A grocery store put out more jam, and sold less of it.") -> who ran it + the numbers -> one plain-language lesson -> tie to the customer's website/business -> question + "DM us the word X". Examples: cafeteria screens (WALL), 24 vs 6 jams (JAM), restaurant = software analogy (MENU).
Animations must be well defined, relatable, hook-full. Reuse: real study, real numbers, named source, one keyword.

## New rules (user, 21 Nov)
1. Anchor every reel in a REAL, widely recalled event (average person remembers it), with a verified number and source. Candidates verified: Facebook/Instagram/WhatsApp outage 4 Oct 2021 (~6h; Zuckerberg lost >$6B; small businesses lost sales); Healthcare.gov launch 2013 (6 sign-ups on day 1, 248 by day 2; SNL joke); Spool's $300M button (+45% purchases).
2. Every visual must be real: real device proportions and real photos/screenshots inside UI. No invented-looking grey placeholders. Stock photos must be actually fetched (Pexels/Unsplash blocked from the workspace shell: need browser download or user-supplied images).
3. ig-viral skill: rank by outlier multiple (views / account's own median). Needs captured reels via a signed-in browser; never scrape.
