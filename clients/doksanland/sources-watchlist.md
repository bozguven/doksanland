# Source watchlist

Every URL below was **opened and read on 2026-11-20**. Nothing here is guessed. A feed is a *lead*,
never an asset: not one of these yields `owned` material, so each item either gets recreated in
Doksanland's own typography (`owned`) or goes out `curated` with `credit` + the original link.

## Rules this list changes in the workflow

1. **The off-limits filter runs before the LLM, not after.** One pull of Google Trends TR served
   politics, a minister, the economy and football inside ten items.
2. **Dedupe across sources, not just inside one.** On 20 Nov, GTA 6 dominated Onedio Gaming
   (17 of 17 items), Kotaku, Dexerto and ListeList at the same time. Without cross-source dedupe the
   desk proposes the same post three times.
3. **Alert on an empty pull.** Webtekno is served through Google FeedBurner and Google Trends is an
   undocumented Google endpoint — either can vanish without notice. Better a warning than a desk
   quietly drafting from whatever is left.
4. **Cap the body size.** Flashbak ~377 KB, Atlas Obscura ~281 KB, Webtekno ~245 KB, Onedio Magazin
   ~177 KB per pull.

## Wired into the Gündem desk now

| Source | Feed | Why this one |
| --- | --- | --- |
| Google Trends TR | `https://trends.google.com/trending/rss?geo=TR` | The hourly heartbeat. **Highest-risk feed we own** |
| Onedio · Goygoy | `https://onedio.com/Publisher/publisher-goygoy.rss` | The single best Gündem source: viral tweets, internet moments |
| ListeList | `https://listelist.com/feed/` | Listicles — the shape our carousels already have |
| Webtekno | `http://feeds.feedburner.com/webteknocom` | Tech and internet culture, fastest to publish |
| Know Your Meme | `https://knowyourmeme.com/newsfeed.rss` | Explains the trend *and* its origin — the Bülteni shape exactly. Only 5 items, so nothing is wasted |

The old `publisher-gundem.rss` path was dropped: it never returned items. Onedio's working feeds all
live at `https://onedio.com/Publisher/publisher-<kategori>.rss`.

## Ready for the other desks

**Ekran** — `https://kayiprihtim.com/feed/` (best fit: film, series, sci-fi, warm by nature) ·
`https://www.beyazperde.com/rss/haberler.xml` · `https://onedio.com/Publisher/publisher-tv.rss`
(dizi finals, reyting) · `https://oyungezer.com.tr/rss` (note `/rss`, not `/feed`) ·
`https://www.nintendolife.com/feeds/latest` (retro lists are perfect nostalgia hooks) ·
`https://www.retrododo.com/feed/` · `https://kotaku.com/rss`

**Nostalji** — `https://flashbak.com/feed/` is the one that matters: found photos, 90s/00s archives,
design manuals. **All of its images are third-party**, so it feeds our facts, never our frames.

**Teneffüs / Yaşam** — `https://www.openculture.com/feed` · `https://laughingsquid.com/feed/` ·
`https://www.thisiscolossal.com/feed/` · `https://mymodernmet.com/feed` ·
`https://www.goodnewsnetwork.org/feed/` · `https://www.positive.news/feed/` ·
`https://onedio.com/Publisher/publisher-genel+kultur.rss` · `https://bigumigu.com/feed/`
(design and animation — but much of it is ad campaigns: idea only, never reproduce brand creative)

**Format inspiration only** — `https://onedio.com/Publisher/publisher-test.rss` (75 quiz items).
Never copy their text; the shape is the lesson.

## Handle with care

- **Onedio Magazin** `publisher-magazin.rss` — high risk of mocking people. One of today's items was
  someone exposing another person on Instagram. If used at all, block `ifşa, kavga, aldat, boşan, ağladı`.
- **Dexerto** `https://www.dexerto.com/feed/` — streamer drama is its business. Block
  `drama, feud, slams, clapback, banned, exposed`.
- **Boing Boing** `https://boingboing.net/feed` — today's lead item was a Nazi-leader story. Manual read only.
- **Atlas Obscura** `https://www.atlasobscura.com/feeds/latest` — many entries are shrines and churches.
- **ScreenRant** `https://screenrant.com/feed/` — very heavy clickbait; useful only as a signal that a
  title is being talked about.

## Dead, do not add

`multiplayer.com.tr/feed` (one item, titled "deneme", Feb 2024) · `filmloverss.com/feed` (zero items) ·
`oyungezer.substack.com/feed` (dormant since Jan 2025) · `knowyourmeme.com/memes/popular.rss`
(stale since 2019 — Slender Man, Lenny Face) · `tamindir.com/rss` (HTML, not a feed) ·
`guinnessworldrecords.com/news/rss` (404) · `onedio.com/rss` and `donanimhaber.com/rss` (directory pages).

**The old Google Trends endpoint `trends.google.com/trends/trendingsearches/daily/rss?geo=TR` is dead.**
The live one is `/trending/rss?geo=TR`.

## Ekşi Sözlük: no feed exists

`/basliklar/gundem`, `/debe`, `/basliklar/populer` and `/stats/debemobile` all returned client errors;
the home page loaded but carries no RSS or Atom reference anywhere. A search for an official feed or
API found nothing. **Do not build an hourly workflow on Ekşi.** It stays a source Bertuğ reads himself —
and since entries are written by users, quoting one is curated content that needs his explicit yes.

## `[DOĞRULANACAK]` — verify from the Mac, not from here

The container's proxy refused every one of these, which says nothing about the feed itself:
`https://www.reddit.com/r/MadeMeSmile/top/.rss?t=day` (and `r/aww`, `r/nostalgia`, `r/BeAmazed` —
the biggest loss on this list) · `https://www.polygon.com/rss/index.xml` ·
`https://www.theverge.com/rss/index.xml` · `https://www.eurogamer.net/feed` ·
`https://mashable.com/feeds/rss/all` · `https://onedio.com/Publisher/publisher-dizi+%26+film.rss`
(real URL from Onedio's own directory, but two attempts both returned server errors).

Re-test each from the machine that will actually run n8n before adding it.
