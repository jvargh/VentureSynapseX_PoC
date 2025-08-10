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

## Sample output
```python
$ python venturesynapsex_poc.py

=== DiscoveryAgent ===
• **Company Snapshot:** AI fraud detection platform for real-time payments, targeting Tier-1 banks, payment processors, and digital wallets. Uses graph neural networks and a streaming feature store to detect fraud within milliseconds.
• **Market Momentum:** Global instant payments adoption accelerating (FedNow, PSD2, UPI). Fraud losses projected to exceed $400B annually by 2027.
• **Competitive Set:** Sift, Featurespace, Sardine — none combine real-time graph inference with fully integrated streaming data pipelines.
• **Key Strengths:** Experienced 2nd-time founders (ex-PayPal, ex-Microsoft), proven technical depth, strong early pilots with banks.
• **Potential Blind Spots:** Regulatory changes could require model retraining; integration complexity may slow large bank adoption.

=== ScoringAgent ===
{
  "scores": {
    "fit": 5,
    "moat": 4,
    "gtm": 4,
    "risk": 3,
    "msft": 4,
    "unicorn": 4
  },
  "summary": "Strong alignment to M12's AI apps & cybersecurity thesis with technical differentiation via real-time graph models. Early customer traction validates product-market fit, though regulatory risk remains.",
  "go_no_go": "GO",
  "rationale": "The company’s solution addresses a fast-growing fraud problem with a defensible approach, experienced team, and clear Azure integration potential. Risks are manageable given current trajectory."
}

=== MemoAgent ===
**TL;DR:**  
This Series A opportunity targets the escalating problem of fraud in instant payment systems using advanced graph neural networks for real-time detection. The founding team has deep domain and technical expertise, with strong early pilots at major banks. The market is expanding rapidly with regulatory support for instant payments globally. Competitive differentiation is clear versus incumbents, and the solution is Azure-friendly for potential co-sell opportunities. Risks relate primarily to regulatory shifts and complex integrations, both of which are mitigated by current team experience.

**Go/No-Go Slide Text**  
- **Why Excited:**  
  • Market size & urgency driven by instant payments adoption  
  • Defensible technical moat via real-time graph neural networks  
  • Experienced, repeat-founder team with relevant exits  

- **Alignment to Thesis:**  
  • AI Applications & Cybersecurity focus  
  • Cloud-native architecture aligns with Azure services  

- **Microsoft Opportunity:**  
  • Azure compute & data services integration potential  
  • Co-sell opportunities with Microsoft financial services partners  

- **Known Risks & Mitigations:**  
  • Regulatory changes → active monitoring, adaptive ML pipeline  
  • Integration complexity → dedicated bank integration team  
  • Model drift → continuous retraining pipeline in place  

- **Deal Terms Summary:**  
  • $100M valuation, $8M M12 check in $20M Series A  
  • 13% FDO target

##### VENTURESYNAPSE-X POC OUTPUT #####
(Repeat of the MemoAgent’s TL;DR + Go/No-Go text)

Scores (for quick copy):
{"fit":5,"moat":4,"gtm":4,"risk":3,"msft":4,"unicorn":4}
```


## Troubleshooting
- `KeyError: OPENAI_API_KEY` → set environment variables as above.
- If your SK version changes API slightly, upgrade/downgrade to the pinned versions in `requirements.txt`.

## License
Internal demo code for hackathon use. No warranties.
