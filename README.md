# job-watch-cloud

I'm a second-year math student in Minsk, and an agent looks for remote work for me. Its main part is a Python daemon on my MacBook. This repo is the half that runs on GitHub Actions while the laptop is asleep, plus the rules and data both halves share.

Live numbers from its logs: https://nivokvo.github.io/job-agent/

## How it works

A Cloudflare Worker checks rabota.by for new postings while the Mac is offline, and a cheap model (Gemini) filters out the obvious misses. When something scores 5 or more, the Worker starts `cloud-apply.yml`. `cloud_apply/run.py` then asks Claude Opus to score the posting against `rubric.md` and write a cover letter, and `cloud_apply/apply.py` applies through a headless browser. It applies at most 7 times a day from here, waits a few minutes between applications, and never sends one without a letter: before clicking submit it checks that the letter text is actually in the form.

`cloud-chats.yml` runs every 20 minutes and handles replies from employers. `cloud_apply/replier.py` reads the whole chat, and Opus drafts an answer using only facts from `me.md` and `resume.md`. A second Opus call checks the draft for invented facts and new promises. The bot sends the reply itself only if that check passes, the reply is short, and it has written fewer than 3 messages in that chat. Everything else becomes a Telegram card with buttons, and I decide. Once an employer invites me to an interview, sends a test task or an offer, the bot stops writing in that chat and leaves it to me.

It does not solve captchas. When rabota.by shows one, applications pause and I finish them by hand.

## Files

- `rubric.md`: the only copy of the scoring rules and the letter rules.
- `resume.md`, `me.md`: what the bot is allowed to say about me.
- `cloud_apply/pick.py`: decides whether to apply. Opus 7+ always, plus up to 3 postings a day that scored 5 or 6, picked by the model below so it keeps learning.
- `cloud_apply/model.py`, `model.json`: a small logistic regression that predicts invitations. It starts from hand-set weights because there are only 7 positive outcomes so far. Opus's own 0 to 10 fit score ranked invitations worse than a coin flip (AUC 0.41).
- `cloud_apply/test_replier.py`: tests for the auto-reply safeguards. Run with `python3 cloud_apply/test_replier.py`.

Keys and the browser session live in GitHub Secrets. Logs here are public, so the scripts print only ids and numbers.

## Contact

If you hire juniors for ML, LLM or agent work remotely: nivokvo@icloud.com, Telegram @nivokvo.
