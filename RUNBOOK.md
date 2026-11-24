# Moodbod reels: cloud autopilot runbook
You run unattended in the cloud, from a checkout of this repo (tuyoleni/moodbod-reels, the current working directory is the repo root). The user is away and their computer is off. Nobody answers questions: decide, say what you chose, finish. The user has authorised automatic posting to Instagram @moodbod.agency only, via the Composio instagram connection. They do NOT review reels before posting; they delete on Instagram anything they dislike. So quality gates are yours. Never post anywhere else, never reply to comments/DMs, never follow/unfollow.

## 1. Set up
1. `bash setup.sh` (installs offline voice, Playwright, Lucide icons, downloads models from GitHub). If google-chrome is missing, use Playwright's chromium and set the path in make_reel.py.
2. Read PLAYBOOK.md, config.json, last 10 lines of log.md, insights/latest.md (follow its recommendations).

## 2. Pick the story
- ONE real, widely remembered event/study that an average person recalls, linking to small business, websites, WhatsApp/online orders, UX or AI automation in Namibia. Not in log.md.
- Verify with at least two WebSearch calls (numbers, date, source). If only one source: "according to X". Never invent.
- Structure: true event first -> what happened (numbers) -> what it means for the viewer's business -> one question. CTA is a DM keyword in the caption only.
- Hook: 3 formulas, score with skill/skills/ig-reel/hookscore.py, pick best; beats.py for timing (32-42s, hook < 3s, no beat > 4s).

## 2b. FORMAT ROTATION (hard rule: reels must NOT look like each other)
Nine reels in a row used the same template (character scene, number card, character scene, character scene, question). That is banned. Every reel has a top-level `"format"` in its spec, recorded in log.md, and the midnight analysis compares formats.
Formats and the scene types each is built from (see make_reel.py; new scene types: kinetic, timeline, versus, thread, news, list, object, plus stat styles card/receipt/bars/big):
- `kinetic-type`: kinetic + stat + kinetic + versus/question. No characters at all.
- `newsroom`: news + timeline + versus + list.
- `phone-thread`: thread (real phone chat reenacting the event) + stat + versus + object.
- `icon-explainer`: object + list + stat + versus.
- `timeline-story`: timeline + news + object + kinetic.
- `character-scene`: stage scenes with flat characters (the old template). Use at most 1 reel in 4 and never twice in a row.
Rules: (1) pick the format by reading the last 4 `format` values in log.md and choosing one NOT in them (character-scene only if absent from the last 3); (2) a reel must use at least 4 different scene types and its scene order must differ from the previous reel's; (3) no more than 2 `stage` scenes per reel, and none outside the character-scene format; (4) vary the background colour, headline length and stat style from the previous reel; (5) invent a new scene variant or prop when none fits, rather than reusing a layout; (6) every 5th reel try something new on purpose (a new scene type in make_reel.py, or a new visual idea) and tag it `format: experiment-<name>` so the analysis can measure it.
The visuals must come from the story: icons (Lucide), a real-looking phone thread, a newspaper front page, a timeline of the actual dates, a before/after.

## 3. Design rules (learned the hard way)
- EVERY scene gets its own environment that belongs to the story. Research what the real place/situation looks like (WebSearch for references: reporting, photos described in captions) before drawing. The shop counter was only an art style; never reuse one setting across reels or scenes. Use the `prop` library in chars.py (board, carousel, bagpile, suitcase, window, desk, monitor, laptop, papers, clock, ringphone, note, bench, plant, mug, paper_float, ...) and add new props to chars.py when the story needs them.
- No background panel/wall/ground line behind scenes. Characters at realistic relative sizes (adults 1.12-1.16, kids ~0.75). Real phone/browser form factors. Icons from Lucide via icons.py, not hand-made.
- Bad outcome = `tone:"bad"` (red/pink); never green on a loss.
- Number scenes vary: stat `style` can be card (default), receipt, bars, big. Do not use the same style in consecutive reels.
- One pastel background per reel, different from the previous reel (lime, lavender, sky, peach, offwhite, dark).
- Safe column: x 88-575 and y 167-1000 at the 720x1280 design scale (Instagram crops ~9% off each side on tall phones and the right-side buttons sit at x>590, so keep a generous LEFT margin and never let text or art touch the edges; make_reel.py QA enforces it); nothing in top 250px / bottom 420px of the final frame. Speech bubbles must not overlap props or signs.
- Voice af_heart or af_bella, never sped up. No whoosh SFX; other SFX/VFX fine. Real photos only in UI scenes (photos/), never real public figures.
- `python3 make_reel.py specs/<file>.json --stills` until `QA: OK`, then LOOK at a contact sheet of all stills and fix anything flat, cramped, overlapping or empty. Render in background with nohup (~4 min) and poll. ffprobe: 1080x1920, audio present, 30-45s; view frames at several timestamps incl. the first second.
- Caption: line 1 adds a hook; body; final line question + "DM us the word X"; max 5 lowercase hashtags; Sources line.

## 4. Publish (all gates must pass, else keep as draft in drafts/ and log the failed gate)
1. QA OK + visual check + ffprobe OK. 2. Facts confirmed by two searches; caption has Sources. 3. Design rules above satisfied. 4. Fewer than 4 posts in log.md for today (Windhoek date) and INSTAGRAM_GET_IG_USER_CONTENT_PUBLISHING_LIMIT has quota.
Steps:
- Save mp4 to reels/<YYYY-MM-DD>-<slug>.mp4, caption .txt and spec to specs/. `git add`, commit, `git pull --rebase origin main`, `git push origin HEAD:main`.
- URL: https://raw.githubusercontent.com/tuyoleni/moodbod-reels/main/reels/<file>.mp4 (no query string). `curl -sI` must return 200 (retry a few times, up to 60s).
- COMPOSIO_SEARCH_TOOLS (instagram) then INSTAGRAM_POST_IG_USER_MEDIA {ig_user_id, video_url, media_type:"REELS", caption, share_to_feed:true, thumb_offset: 2000} (the cover must show the headline, not a blank frame).
- INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH {ig_user_id, creation_id, max_wait_seconds:300}; on 9007/500 wait 20s and retry same creation_id up to 3 times.
- INSTAGRAM_GET_IG_MEDIA for the permalink. Append to log.md: date | time | slug | event | colour | hook | DM word | permalink | media_id | format. Commit and push log.md.
On failure after retries: keep draft, log "FAILED: reason", never create a second post.
Final message: 3 lines (event, hook, permalink or why not posted).
