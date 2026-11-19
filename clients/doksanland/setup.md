# Doksanland · setup checklist

What is connected, and what Bertuğ still has to do. No password or token ever goes in this repo or the chat.

- [x] Instagram @doksanland claimed
- [x] Switched to a Business account (category Media/news company)
- [x] Facebook Page "Doksanland" created and linked to @doksanland
- [ ] Contact options on Instagram: no personal phone or email shown publicly
- [x] GitHub repo bozguven/doksanland (public: Instagram fetches images from the publish-media branch)
- [x] Meta developer app (Development mode), use case "Manage messaging & content on Instagram"
- [x] Page access token (long-lived) → GitHub → Settings → Secrets and variables → Actions → secret `META_PAGE_TOKEN`
- [x] GitHub variable `PUBLISH_ENABLED` = `false` while testing, `true` to go live (the kill switch)
- [x] First workflow run with command `check` shows "Page Doksanland · Instagram @doksanland" (OK on 19 Nov; API quota 100 posts / 24 h)
- [ ] cron-job.org job every 5 min → workflow_dispatch of publish.yml (fine-grained token: this repo only, Actions read+write)
- [ ] Profile: name, bio, picture (Doksanland will propose them)
- [ ] Launch day picked → shift campaign.json dates (Day 1 is a placeholder: 2026-11-23)
