"""Langfuse tracing via OpenInference (OpenTelemetry). Safe no-op if keys/packages are missing."""
import logging
import os

log = logging.getLogger("observability")
_initialized = False


def init_tracing() -> bool:
    global _initialized
    if _initialized:
        return True
    if not (os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY")):
        log.warning("Langfuse keys not set; tracing disabled.")
        return False
    try:
        from langfuse import get_client
        from openinference.instrumentation.crewai import CrewAIInstrumentor

        if not get_client().auth_check():
            log.warning("Langfuse auth check failed; tracing disabled.")
            return False
        CrewAIInstrumentor().instrument(skip_dep_check=True)
        try:  # also capture raw LLM calls (tokens/cost) made through LiteLLM (Hugging Face)
            from openinference.instrumentation.litellm import LiteLLMInstrumentor

            LiteLLMInstrumentor().instrument()
        except ImportError:
            pass
        _initialized = True
        return True
    except Exception as e:  # noqa: BLE001
        log.warning("Tracing init failed: %s", e)
        return False


def flush() -> None:
    if not _initialized:
        return
    try:
        from langfuse import get_client

        get_client().flush()
    except Exception:  # noqa: BLE001
        pass
