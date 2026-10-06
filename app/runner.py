"""Runs the 4-agent crew and adds the Verify -> Write retry loop,
which a plain sequential crew.jsonc cannot express."""
import re
from dataclasses import dataclass
from pathlib import Path

from crewai.project import load_crew

from app import observability

ROOT = Path(__file__).resolve().parent.parent
CREW_FILE = ROOT / "crew.jsonc"
VERDICT_RE = re.compile(r"VERDICT:\s*(PASS|FAIL)", re.IGNORECASE)


@dataclass
class ResearchResult:
    topic: str
    verdict: str          # PASS | FAIL | UNKNOWN
    attempts: int
    report: str           # full verifier output (verdict + notes + corrected report)


def _split_report(text: str) -> str:
    """Return only the corrected report (after the '---' separator) if present."""
    parts = re.split(r"\n-{3,}\n", text, maxsplit=1)
    return parts[1].strip() if len(parts) == 2 else text.strip()


def run_pipeline(topic: str, max_revisions: int = 2) -> ResearchResult:
    """Traced wrapper: one Langfuse trace per research job."""
    if not observability.init_tracing():
        return _run(topic, max_revisions)
    from langfuse import get_client

    lf = get_client()
    try:
        with lf.start_as_current_observation(
            as_type="span", name="research-job", input={"topic": topic}
        ) as span:
            res = _run(topic, max_revisions)
            span.update(output={"verdict": res.verdict, "attempts": res.attempts})
            return res
    finally:
        observability.flush()


def _run(topic: str, max_revisions: int) -> ResearchResult:
    feedback = "None"
    verdict, raw = "UNKNOWN", ""
    attempts = 0

    for attempts in range(1, max_revisions + 2):
        crew, defaults = load_crew(CREW_FILE)  # fresh crew per attempt
        result = crew.kickoff(inputs={**defaults, "topic": topic, "feedback": feedback})
        raw = result.raw
        m = VERDICT_RE.search(raw)
        verdict = m.group(1).upper() if m else "UNKNOWN"
        if verdict == "PASS":
            break
        # Feed the verifier's notes back to Search/Write on the next attempt.
        feedback = raw[:4000]

    return ResearchResult(topic, verdict, attempts, _split_report(raw))
