# 🛡️ Scam Shield

Check a suspicious voice note before you trust it. Built for the **CMRIT × DetectifAI Hackathon** (Track 01: Scam Shield) using DetectifAI's **Aletheia** deepfake detection API.

## The problem

Scammers can clone a family member's voice from a few seconds of audio and send urgent voice notes asking for money or OTPs. Most people cannot tell a cloned voice from a real one, and they have no simple way to check before they act.

## What it does

1. The user uploads a voice note (4 to 120 seconds).
2. Scam Shield sends it to Aletheia (`/v1/deepfake/detect`).
3. The app shows the verdict, the score and the decision threshold, a reminder that the result is evidence and not proof, and clear next steps.

## Features

- Upload wav, mp3, ogg, m4a or opus clips
- Colour-coded result: green (genuine), red (synthetic), yellow (could not process)
- Friendly message for clips outside 4 to 120 seconds
- Next steps: call back on a saved number, ask a question only they would know, do not send money or OTPs until confirmed
- Tips for spotting voice scams

## Results

We tested four clips (threshold 0.62, higher score = more likely AI).

| Clip | Length | Result | Score |
|------|--------|--------|-------|
| Real voice (own recording) | 11 s | Genuine | 0.28 |
| AI voice (TTSMaker text-to-speech) | 8 s | Synthetic | 1.00 |
| AI voice played through a speaker, recorded on a phone, sent via WhatsApp | 13 s | Genuine (missed) | 0.33 |
| Very short clip | 2 s | Not processed (under 4 s) | n/a |

**What worked:** the real voice passed, and a clean AI voice was caught with a score of 1.00.

**What did not work:** an AI voice that was re-recorded through a speaker and WhatsApp was not flagged. Re-recording and compression probably hid the AI traces.

## Limitations

- A score is **evidence, not proof**. It should not be the only basis for a decision.
- A "genuine" result does not guarantee the voice is real. Always verify by calling back.
- Background noise, compression and re-recording can change the result.
- We tested a small number of clips, not a large benchmark.

## Tech stack

- Python
- Streamlit
- DetectifAI Aletheia API

## Setup

1. Create an API key at [platform.detectif.ai](https://platform.detectif.ai).
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set your API key (Windows PowerShell):
   ```
   $env:DETECTIF_API_KEY="your_key"
   ```
4. Run the app:
   ```
   python -m streamlit run app.py
   ```

Never commit your API key to GitHub.

## Ethics

All test voices were our own or AI voices from a text-to-speech tool. We only record or clone voices with the owner's permission.

## Team

- Rakshita
- Bhagyashree Chigari
- Pooja M B

CMRIT, [CSE,AIDS ,2nd year]

## Future work

- Telegram or WhatsApp bot for forwarding voice notes
- Replies in Hindi and Kannada
- Risk levels with different advice for low, medium and high scores
