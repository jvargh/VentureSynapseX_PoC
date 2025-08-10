# VentureSynapseX — PoC (Semantic Kernel, Python)

A minimal multi-agent proof of concept for an AI-first corporate VC workflow using **Semantic Kernel**.

## What it does
- **DiscoveryAgent** → synthesizes inputs (Dynamics JSON, deck notes, research) into a crisp snapshot.
- **ScoringAgent** → returns strict JSON scores + **GO / LEARN_MORE / NO_GO**.
- **MemoAgent** → emits an M12-style TL;DR + compact Go/No-Go slide text.

Outputs are printed to the console for quick copy/paste into your IC memo or Go/No-Go slide.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Set API credentials (choose **OpenAI** *or* **Azure OpenAI**):

**OpenAI**
```bash
export OPENAI_API_KEY=sk-...
export VXC_MODEL=gpt-4o-mini   # or gpt-4o, o4-mini, etc.
```

**Azure OpenAI**
```bash
export AZURE_OPENAI_API_KEY=...
export AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com/
export AZURE_OPENAI_DEPLOYMENT=<deployment>
export VXC_PROVIDER=azure
```

### Run
```bash
python venturesynapsex_poc.py
```

### Inputs
Edit files in `inputs/`:
- `dynamics.json` — sample Dynamics CRM-style fields.
- `pitch_deck.txt` — raw text from the deck.
- `research_notes.txt` — analyst notes / third-party research.

## Customize
- Replace prompts in the file to match your voice.
- Persist outputs, or write `MemoAgent` to PowerPoint via `python-pptx`.
- Add a retrieval layer (SK Memory) and guardrails (policy/PII checks).

## Troubleshooting
- `KeyError: OPENAI_API_KEY` → set environment variables as above.
- If your SK version changes API slightly, upgrade/downgrade to the pinned versions in `requirements.txt`.

## License
Internal demo code for hackathon use. No warranties.
