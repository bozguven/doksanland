---
description: Daily Doksanland newsroom run - fill the next days' slots, render, check, put everything on the review board for Bertuğ.
---

Run the Doksanland newsroom for $ARGUMENTS (default: the next 2 days that still have `planned` slots).

1. Read `clients/doksanland/brief.md`, `.claude/skills/voice-tr/SKILL.md` and `clients/doksanland/campaign.json`.
2. Act as `genel-yayin-yonetmeni`: for each `planned` slot in range, ask the desk in its `desk` field for 3
   candidates (use the matching subagent; desks can run in parallel), pick one, write `caption_tr`,
   `title`, `credit`, `needs`, set status `draft`.
3. Images → `tasarim` (visuals.json + `node render.mjs doksanland <ids>`, look at every PNG).
   Reels → `video` (recipe + render + contact sheet check).
4. Every finished item → `haklar-guvenlik`. PASS → status `ready`. FAIL → stays `draft`, reasons in `needs`.
5. `node tools/campaign.mjs board`, publish/refresh the review board artifact, and reply to Bertuğ with one
   line per item: id · day/time · desk · hook · status · what (if anything) he must decide.
6. Never approve anything yourself. After Bertuğ's yes in the conversation:
   `node tools/campaign.mjs approve <ids>` → `bash tools/publish/upload-media.sh` → commit and push.
