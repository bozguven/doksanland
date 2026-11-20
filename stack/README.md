# Doksanland newsroom stack

The departments as software: each desk is a scheduled n8n workflow that runs on its own,
drafts a post, renders it in the house style, and asks Bertuğ on Telegram before anything goes out.

```
stack/
  docker-compose.yml     n8n + render service
  render-service/        the house template behind an HTTP API
  workflows/             one importable n8n workflow per department
  shared/                images the desks produce
```

## Start it

```bash
cd stack
docker compose up -d
```

- n8n: http://localhost:5678
- render service: http://localhost:4000/health (n8n reaches it at `http://render:4000`)

## What each desk looks like

Every department follows the same six steps. `DOK-10 Gündem desk` is the worked example:

1. **Schedule** — the desk wakes on its own (Gündem hourly, the slower desks daily).
2. **Sources** — RSS and searches (see `clients/doksanland/sources.md`).
3. **Gate and pick** — throws out anything off-limits, drops what we've already covered,
   and hands the desk a shortlist.
4. **Draft** — Claude writes the post against the brief and the Turkish voice rules,
   or refuses the lot.
5. **Render** — the visual spec goes to the render service, which returns a finished PNG.
6. **Approve** — the image and caption land on your Telegram with **Approve / Reject**.
   Reject and it dies there.

Nothing publishes without that tap. The schedule, the sources and the wording are all
visible and editable on the n8n canvas, and every run is kept in the execution list.

## The safety gate has two stages, on purpose

A Türkiye trend feed is mostly politics and football. Stage one is a blunt keyword
blocklist (121 terms, every Süper Lig club included). Stage two is the desk's own judgement.

**Stage one cannot catch proper names.** Checked against a real Google Trends Türkiye feed,
`fenerbahçe transfer son dakika`, `mavi vatan` and `çaykur rizespor` were blocked, but
`ömer bolat` (a government minister) and `željko obradović` (a basketball coach) passed.
That is why the desk's instructions carry a hard identity rule: if the topic is a person,
the desk must be able to say who they are *and* they must be an entertainment or culture
figure. Anything it cannot place is refused. Keep that rule if you edit the prompt.

## What you need to supply

| Thing | Where it goes | Note |
| --- | --- | --- |
| Anthropic API key | n8n → Credentials → Header Auth, header `x-api-key` | Used by the drafting step |
| Telegram bot token | n8n → Credentials → Telegram | Create a bot with @BotFather |
| Your Telegram chat id | n8n → Settings → Variables → `DOKSANLAND_TELEGRAM_CHAT_ID` | Message @userinfobot to get it |

No key is stored in this repo.

## Publishing, and the one catch

Instagram's API fetches images from a **public URL**, so a file on your Mac cannot be posted
directly. The repo already solves this: approved media is pushed to the orphan `publish-media`
branch and posted from its `raw.githubusercontent.com` address. `DOK-30 Publisher` wires the
approved queue to that path. Until it is connected, approved posts stop at "queued" — which is
the safe failure.
