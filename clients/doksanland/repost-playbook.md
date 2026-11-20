# Repost playbook

How the Repost desk finds content it may re-dress with credit. The method, not one-off picks.

**Status of every name in this file and in follow-list.md:** each handle is evidenced by a named
published source, but **no Instagram or X profile was opened** while compiling it (both block
automated access, and Reddit is blocked too). So `rights: unknown` is the honest status for all of
them. Bertuğ opens the bio before the first repost, every time.

## Where to look

**Ekşi Sözlük — idea mining, not reposting.** Entries are written by users, so Ekşi feeds the
owned-content desks. A line reused verbatim needs `Kaynak: ekşi sözlük / @nick` and a yes.
Topics worth standing watch (slugs verified via search; the site blocks bots, so browse by hand):

- `90 lar` · `90'ların özel olmasının nedeni` · `90'larda çocuk olmak`
- `doksanların güzel olmasının nedeni` · `1990-1995 arası doğan efsanevi nesil`
- `hatırladıkça gülümseten anılar` — the best fit for the brand promise
- `evde salonun sadece misafire açıldığı efsane dönem` · `babanın aldığı harika hediyeler`
- `90'lı yıllara özgü problemler` · `geceye bir 90'lar şarkısı bırak`

Daily string: `site:eksisozluk.com ("90'lar" OR "2000'ler" OR teneffüs OR "çocukluk") (hatırla OR gülümseten OR efsane)`

Two found and rejected, as a check that the filter works: a poverty-memories topic (economy is
off-limits) and one about teachers beating children (not joyful). Never carry a source topic's
wording into a hook — some of it is not our register.

**Reddit — machine-readable, works from Bertuğ's Mac.**
`https://www.reddit.com/r/<sub>/top/.rss?t=day` is the easiest n8n node. Set a real User-Agent.
Evidenced subs: r/Turkey, r/Turkiye, r/AskTurkey, r/TURKS. Mixed-humour subs will serve politics,
money talk and NSFW alongside the good stuff, so the keyword filter is not optional there.
A top Reddit post is usually **not** the poster's own work: use Reddit to spot a trend, then find
the real creator.

**X — logged-in browser only.** Append the exclusion block to every query:
`-siyaset -seçim -parti -zam -enflasyon -dolar -maaş -asgari -kriz -din -namaz -içki -bira -rakı`

- `lang:tr min_faves:2000 -filter:links -filter:replies (hatırlıyor OR hatırlayan OR "o zamanlar" OR nostalji)`
- `lang:tr min_faves:1000 -filter:replies ("teneffüs" OR ilkokul OR "90'lar" OR "2000'ler")`
- `lang:tr min_faves:3000 -filter:links ("ne ara" OR "biz büyüdük" OR "o yıllar")`

`-filter:links` matters: a link-free tweet is usually the author's own words.

**Instagram — the official route, and its catch.** We are a Business account with a Meta app, so
`ig_hashtag_search` → `top_media` / `recent_media` is available. Limits, from Meta's docs:
30 unique hashtags per 7 days; `recent_media` covers the last 24 hours only; 50 per page.

> **The catch that shapes this desk: the hashtag API cannot return `username`.** It gives a
> permalink but never the creator's handle, and our whole model is credit. So harvesting can be
> automatic, but **a human reads the handle off the opened permalink.** Never let a workflow guess
> a handle from a caption or an @ mention.

Fixed rotation, six a day (check each in-app before committing a slot):
`#doksanlar #90larnostalji #2000lernostalji #nostalji #çocukluk #teneffüs #eskiçizgifilmler #tazo #90larçocuğu #hatırlayanlar #mahalleoyunları #okulanıları`

**TikTok — manual only.** Tag pages load inconsistently; don't build a node on them.
Sweep by hand: `nostalji` (164.1M views), `90lar`, `2000ler`, `çocukluk`, `teneffüs`, `komik`.
TikTok's baked-in watermark is good for credit but Instagram demotes visibly reuploaded clips —
prefer re-dressing the *idea* in our template over reuploading.

**Turkish media as a tip-sheet.** onedio.com, listelist.com, Hürriyet Kelebek publish
"what went viral" listicles that name handles — a cheap scouting layer.

## Who not to repost

1. Caps and meme aggregators — crediting them credits a thief. Ten posts a day in six styles = aggregator.
2. Pages built on TV stills, dizi screenshots, film frames or ad clips. **This is the trap with
   Turkish nostalgia pages: the genre is TV stills.** Watch for ideas, never reuse the images.
3. Game-IP and character pages (Pokémon, Mario, cartoon characters).
4. Hidden-camera, prank and "social experiment" accounts — people filmed without real consent.
5. Accounts mixing in politics or religion, even at 10%. Their handle on our page invites their
   timeline into our comments.
6. Street-interview and daytime-TV clip farms.
7. Anything with alcohol in the handle, bio or frame — a bottle in the background is still a fail.
8. Then-vs-now price or salary content. **The commonest way a 90s post smuggles in a banned topic.**
9. Accounts showing real children's faces.
10. Fan edit accounts — commercial music plus celebrity footage, two rights problems at once.
11. Dormant accounts (>6 months silent) — nobody to ask, and a deleted post breaks our caption.

Red flags on a post: a bio saying `izinsiz paylaşım yasak` / `repost yasak` / `no repost` / `© `;
a watermark that is cropped, blurred or covered; the same clip appearing earlier under another
handle; comments asking "kaynak?"; embeds disabled.

## Verify before posting — one fail drops the candidate

1. **Record the evidence.** Source URL, handle verbatim, timestamp, screenshot of the post **and
   the bio**, check date in `needs`. No screenshot, no record that the bio was clean.
2. **Liveness + public + embeds allowed, in one call.** Instagram's oEmbed endpoint refuses posts
   from private, inactive or age-restricted accounts and from accounts that disabled embeds.
   Fails → drop. Embeds off is a stated preference; treat it as a soft no.
3. **Resolve the handle by hand** off the permalink (see the API catch above).
4. **Prove authorship.** Search the exact caption line in quotes; for a Reel, tap the audio to see
   who used it first. An earlier posting elsewhere → credit them or drop. *This step kills the most
   candidates, and it should.*
5. **Check for a permission block** — full bio, link-in-bio page, pinned post.
6. **Off-limits sweep on everything visible in the frame**, not just the subject: flags, party
   colours, religious figures, alcohol (including background bottles), prices, children's faces,
   TV bugs, brand packaging, game IP, commercial music.
7. **Watermark integrity** — present and uncropped, and our template must not sit on it. Our credit
   is *in addition*, never instead.
8. **Audio** — commercial music out. If the joke *is* the audio and they don't own it, drop it.
9. **Caption** passes the voice-tr self-check and ends `Kaynak: @handle`, with no `[DOĞRULANACAK]`.
10. **Freshness** — more than 48 h between the check and the post time, re-run step 2.
11. **Rights gate, then Bertuğ's explicit yes.** No standing approval for this desk, ever.
12. **Courtesy after publishing** — tag the creator and send them the link in Stories. It turns a
    credited repost into a relationship, and it is the cheapest insurance against a takedown.

Record every refusal in `do-not-repost.json`. It is the asset that compounds.

## Outreach (Bertuğ sends these, never an agent)

**The ask**
```
selam [isim] 👋

doksanland'dan yazıyoruz. 90'lar, 2000'ler ve küçük mutluluklar
paylaşan yeni bir sayfayız.

[paylaşımın konusu] paylaşımına bayıldık. izin verirsen onu kendi
tasarımımızla yeniden hazırlayıp sayfamızda paylaşmak istiyoruz.

nasıl olacağını baştan söyleyeyim:
· adın hem görselin üstünde, hem açıklamada: Kaynak: @[handle]
· filigranın hiç silinmez, kırpılmaz
· paylaşımda seni etiketleriz, story'de de linkini veririz
· "kaldır" dediğin an aynı gün kaldırırız

uygun mu? uygun değilse de hiç sorun yok, yine de kolay gelsin.
```

**After a no — always send it**
```
anladım, hiç sorun değil — haber verdiğin için teşekkürler.
sayfanı takip etmeye devam ediyoruz, kolay gelsin.
```
Then add the handle to `do-not-repost.json`.
