# file: venturesynapsex_poc.py
import os, json, pathlib
from dataclasses import dataclass
from typing import Dict, Any

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatCompletion,
    AzureChatCompletion,
)
from semantic_kernel.prompt_template import PromptTemplateConfig
    # semantic-kernel >=0.9.x
from semantic_kernel.functions import KernelArguments
from semantic_kernel.agents.chat_agent import ChatAgent
from semantic_kernel.agents.agent_group_chat import AgentGroupChat
from semantic_kernel.agents.agent import Agent

def build_kernel() -> Kernel:
    """
    Build a Semantic Kernel instance with either OpenAI or Azure OpenAI
    based on environment variables.
    """
    provider = os.getenv("VXC_PROVIDER", "openai").lower()
    model = os.getenv("VXC_MODEL", "gpt-4o-mini")

    kernel = Kernel()

    if provider == "azure":
        endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
        deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]
        key = os.environ["AZURE_OPENAI_API_KEY"]
        service = AzureChatCompletion(
            service_id="chat",
            deployment_name=deployment,
            endpoint=endpoint,
            api_key=key,
        )
    else:
        # default: OpenAI
        key = os.environ["OPENAI_API_KEY"]
        service = OpenAIChatCompletion(
            service_id="chat",
            ai_model_id=model,
            api_key=key,
        )

    kernel.add_service(service)
    return kernel


def load_inputs(input_dir: str = "inputs") -> Dict[str, str]:
    """
    Load Dynamics-style JSON + free-form artifacts.
    """
    p = pathlib.Path(input_dir)
    p.mkdir(parents=True, exist_ok=True)

    def read_safe(path: pathlib.Path) -> str:
        return path.read_text(encoding="utf-8") if path.exists() else ""

    dynamics = {}
    dyn_path = p / "dynamics.json"
    if dyn_path.exists():
        dynamics = json.loads(dyn_path.read_text(encoding="utf-8"))

    return {
        "dynamics_json": json.dumps(dynamics, indent=2),
        "pitch_deck": read_safe(p / "pitch_deck.txt"),
        "research_notes": read_safe(p / "research_notes.txt"),
    }


DISCOVERY_SYS = """\
You are DiscoveryAgent for an AI-first venture fund (M12).
Task: Fuse all provided artifacts into a concise deal understanding.
Deliverables:
- Company snapshot (product, target customer, problem)
- Market size & momentum signals
- Competitive set (top 3)
- Key strengths/insights we might be missing in the market
Keep it bullet-y, <300 words, neutral tone.
"""

SCORING_SYS = """\
You are ScoringAgent for M12. Score this opportunity on 0-5 scale for each dimension:
- Strategic fit to M12 thesis (AI apps, Cloud Infra & Data, Deep Tech & Systems, Cybersecurity)
- Technical moat (defensibility, data advantage, roadmap)
- Go-to-market velocity (ICP clarity, ACV, cycle time, pipeline)
- Risk surface (model/regulatory/competitor/integration)
- Microsoft synergy (Azure usage, co-sell, product adjacencies)
- Unicorn likelihood (probability of $1B+ outcome in 7-10 years)

Return strict JSON with:
{
  "scores": {"fit": x, "moat": x, "gtm": x, "risk": x, "msft": x, "unicorn": x},
  "summary": "...",
  "go_no_go": "GO|LEARN_MORE|NO_GO",
  "rationale": "2-3 sentences"
}
"""

MEMO_SYS = """\
You are MemoAgent for M12. Produce:
1) A 5-sentence TL;DR aligned to M12 memo tone.
2) A compact Go/No-Go slide text using these sections:
   - Why excited (3 bullets)
   - Alignment to thesis (2 bullets)
   - Microsoft opportunity (2 bullets)
   - Known risks & mitigations (3 bullets)
   - Deal terms summary (valuation, raise, proposed check, FDO%)
Be crisp. Avoid hype. Use facts from inputs & upstream agents.
"""


from dataclasses import dataclass

@dataclass
class SimpleAgent(ChatAgent):
    name: str
    kernel: Kernel
    system_prompt: str

    def __post_init__(self):
        super().__init__(self.name, self.kernel)
        cfg = PromptTemplateConfig(template=self.system_prompt)
        self.prompt_template = cfg

    async def on_chat_turn(self, history, context) -> str:
        args = KernelArguments()
        result = await self._invoke_chat(history, self.prompt_template, args)
        return result


def make_discovery_agent(kernel: Kernel) -> Agent:
    return SimpleAgent(name="DiscoveryAgent", kernel=kernel, system_prompt=DISCOVERY_SYS)

def make_scoring_agent(kernel: Kernel) -> Agent:
    return SimpleAgent(name="ScoringAgent", kernel=kernel, system_prompt=SCORING_SYS)

def make_memo_agent(kernel: Kernel) -> Agent:
    return SimpleAgent(name="MemoAgent", kernel=kernel, system_prompt=MEMO_SYS)


ASYNC_HELP = """
Pipeline:
1) DiscoveryAgent returns a snapshot.
2) ScoringAgent returns JSON with scores and decision.
3) MemoAgent produces TL;DR + Go/No-Go slide text.
"""

async def run_pipeline():
    kernel = build_kernel()
    inputs = load_inputs()

    discovery = make_discovery_agent(kernel)
    scoring   = make_scoring_agent(kernel)
    memo      = make_memo_agent(kernel)

    group = AgentGroupChat(agents=[discovery, scoring, memo], kernel=kernel)

    seed = f"""Artifacts for evaluation (confidential):

[DYNAMICS CRM]
{inputs['dynamics_json']}

[PITCH DECK NOTES]
{inputs['pitch_deck']}

[RESEARCH NOTES]
{inputs['research_notes']}

Follow the pipeline strictly. Return only your role's deliverable each turn.
"""
    group.add_user_message(seed)

    discovery_out = await group.invoke(discovery)
    print("\\n=== DiscoveryAgent ===\\n", discovery_out.strip())

    scoring_prompt = f\"\"\"Use the artifacts and DiscoveryAgent output below:\\n\\n--- DISCOVERY\\n{discovery_out}\\n---\"\"\"
    group.add_user_message(scoring_prompt)
    scoring_out = await group.invoke(scoring)
    print("\\n=== ScoringAgent ===\\n", scoring_out.strip())

    memo_prompt = f\"\"\"Inputs for memo:\\n\\n--- DYNAMICS\\n{inputs['dynamics_json']}\\n\\n--- DISCOVERY\\n{discovery_out}\\n\\n--- SCORING(JSON)\\n{scoring_out}\\n---\"\"\"
    group.add_user_message(memo_prompt)
    memo_out = await group.invoke(memo)
    print("\\n=== MemoAgent ===\\n", memo_out.strip())

    print("\\n\\n##### VENTURESYNAPSE-X POC OUTPUT #####")
    print(memo_out.strip())
    print("\\nScores (for quick copy):")
    print(scoring_out.strip())


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_pipeline())
