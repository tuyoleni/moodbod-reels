# Moodbod reels: midnight analysis (00:07 Windhoek, cloud)
Unattended, read-only on Instagram: never post, comment, DM or change the account. Work from the repo checkout.
1. Read log.md, config.json, PLAYBOOK.md, insights/*.md.
2. Via Composio (COMPOSIO_SEARCH_TOOLS first; instagram): INSTAGRAM_GET_USER_INFO, INSTAGRAM_GET_IG_USER_MEDIA (last ~40), then INSTAGRAM_GET_IG_MEDIA / INSTAGRAM_GET_IG_MEDIA_INSIGHTS per recent post: views, reach, likes, comments, saves, shares, watch time, follows.
3. Join with log.md (topic, hook formula, colour, slot, length, DM word, format (last column), stat style). Compare FORMATS first: median views/saves/shares per format and per scene type; name the best and worst format and recommend which format to use more next. Rank by views vs the account median. Find patterns (hook, topic family, colour, scene/environment, length, slot, CTA word). With <10 comparable posts say it is weak and vary one thing at a time.
4. Write insights/<YYYY-MM-DD>.md and overwrite insights/latest.md (<60 lines): top 3 / bottom 3 with numbers; do more / stop; 5 specific topic ideas (real, widely recalled, not in log.md); best slots; one experiment for tomorrow.
5. If data clearly disproves a PLAYBOOK rule, add a dated note (never delete rules).
6. `git add insights PLAYBOOK.md`, commit, `git pull --rebase origin main`, `git push origin HEAD:main`. Final message: 5 lines max.
