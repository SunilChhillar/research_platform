# 🔬 Autonomous Research Platform — Agentic AI Research

> **An autonomous AI research platform powered by CrewAI that searches, summarizes, writes, verifies, and automatically retries when research quality is insufficient.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Agentic_AI-FF5A1F)](https://www.crewai.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Langfuse](https://img.shields.io/badge/Langfuse-Observability-000000)](https://langfuse.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-Data_Validation-E92063)](https://docs.pydantic.dev/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-499848)](https://www.uvicorn.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

---

# 🌟 About the Project

**Autonomous Research Platform** is an **Agentic AI research system** that transforms a research topic into a verified, structured report.

Instead of relying on a single LLM call, the platform uses a **multi-agent CrewAI workflow** where specialized agents collaborate to:

1. 🔎 Search for relevant information
2. 📝 Summarize research findings
3. ✍️ Write a structured report
4. 🔍 Verify factual claims against the research sources
5. 🔄 Retry the research workflow when verification fails
6. 📊 Trace the complete execution using Langfuse

The core workflow is:

```text
Research Topic
      │
      ▼
┌───────────────┐
│ 🔎 Researcher │
└───────┬───────┘
        │
        ▼
┌────────────────┐
│ 📝 Summarizer  │
└───────┬────────┘
        │
        ▼
┌───────────────┐
│ ✍️ Writer     │
└───────┬───────┘
        │
        ▼
┌────────────────┐
│ 🔍 Verifier    │
└───────┬────────┘
        │
        ▼
   Verification
      Decision
      │      │
   PASS     FAIL
      │      │
      ▼      ▼
   Final   🔄 Retry
   Report
```

### 🎯 Example

A user could submit:

> 💬 **"Research the impact of Agentic AI on enterprise software development."**

The platform can autonomously:

- Search the web for relevant sources
- Extract important information
- Summarize the findings
- Produce a coherent research report
- Check whether claims are actually supported
- Correct unsupported claims
- Retry the research workflow when necessary
- Return a verified final report

---

# 🎯 Key Highlights

- 🤖 **Multi-agent Agentic AI architecture**
- 🔎 **Autonomous web research**
- 📝 **Research summarization**
- ✍️ **LLM-powered report generation**
- 🔍 **Fact-checking verification agent**
- 🔄 **Verify → Retry feedback loop**
- 🎯 **Source-grounded research**
- 📊 **Langfuse observability**
- ⚡ **FastAPI REST API**
- 🚦 **API rate limiting**
- 🛑 **Concurrency backpressure**
- ⏱️ **LLM rate limiting**
- 🧵 **Concurrent research jobs**
- 🛡️ **Pydantic validation**
- 🧪 **Production-oriented architecture**
- 🐳 **Docker-ready deployment**
- 🔐 **Environment-based configuration**

---

# 🏗️ Architecture

The platform uses **CrewAI** to orchestrate specialized agents and tasks.

The overall architecture is:

```text
                         ┌──────────────────────┐
                         │        USER          │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   FastAPI Service    │
                         │                      │
                         │ Rate Limit           │
                         │ Backpressure         │
                         │ Job Management       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Research Job       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                     ┌──────────────────────────────┐
                     │       CrewAI Crew             │
                     └──────────────┬───────────────┘
                                    │
             ┌──────────────────────┼─────────────────────┐
             │                      │                     │
             ▼                      ▼                     ▼
      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
      │ 🔎 Researcher│      │ 📝 Summarizer │      │ ✍️ Writer    │
      └──────┬───────┘      └──────┬───────┘      └──────┬───────┘
             │                     │                     │
             └─────────────────────┼─────────────────────┘
                                   │
                                   ▼
                         ┌──────────────────────┐
                         │   🔍 Verifier Agent  │
                         │                      │
                         │ Check every claim    │
                         │ against sources      │
                         └──────────┬───────────┘
                                    │
                         ┌──────────┴──────────┐
                         │                     │
                       PASS                  FAIL
                         │                     │
                         ▼                     ▼
                ┌─────────────────┐     ┌───────────────┐
                │ ✅ Final Report │     │ 🔄 Retry      │
                └─────────────────┘     │ Research      │
                                        └───────┬───────┘
                                                │
                                                └──────────►
                                                   Researcher
```

---

# 🤖 Agent Responsibilities

The architecture deliberately separates **research, synthesis, writing, and verification**.

---

## 🔎 1. Researcher Agent

**Role:** The Researcher

The Researcher is responsible for finding relevant and trustworthy information about the requested topic.

### Responsibilities

- Search the web
- Identify relevant sources
- Gather source notes
- Extract important facts
- Identify supporting evidence
- Avoid unsupported assumptions
- Return research material to downstream agents

```text
Research Topic
      │
      ▼
┌─────────────────┐
│ Researcher Agent│
└────────┬────────┘
         │
         ▼
   Web Search
         │
         ▼
   Source Material
         │
         ▼
   Research Notes
```

### Boundary

The Researcher focuses on **information discovery**.

It does not produce the final report.

---

# 📝 2. Summarizer Agent

**Role:** The Synthesizer

The Summarizer transforms raw research results into structured research notes.

### Responsibilities

- Combine information from multiple sources
- Remove unnecessary information
- Identify important facts
- Group related findings
- Preserve source references
- Highlight conflicting information
- Produce concise research notes

```text
Raw Research
      │
      ▼
┌─────────────────┐
│ Summarizer Agent│
└────────┬────────┘
         │
         ▼
Structured Research
Notes
```

### Boundary

The Summarizer should not invent facts that are not present in the research material.

---

# ✍️ 3. Writer Agent

**Role:** The Author

The Writer transforms the summarized research into a readable final draft.

### Responsibilities

- Create a logical report structure
- Organize findings into sections
- Explain concepts clearly
- Preserve source attribution
- Produce professional prose
- Maintain consistency
- Avoid introducing unsupported claims

```text
Research Notes
      │
      ▼
┌───────────────┐
│ Writer Agent  │
└───────┬───────┘
        │
        ▼
  Draft Report
```

### Example Output

```text
# Research Report

## Introduction

...

## Key Findings

...

## Analysis

...

## Conclusion

...

## Sources

...
```

---

# 🔍 4. Verifier Agent

**Role:** The Fact Checker

The Verifier is responsible for determining whether the generated report is actually supported by the research sources.

This is one of the most important components of the platform.

### Responsibilities

- Inspect every cited claim
- Compare claims against source notes
- Validate source attribution
- Identify unsupported claims
- Identify incorrect statements
- Correct claims when possible
- Remove unsupported claims when necessary
- Produce a verification verdict

The agent follows the principle:

```text
Claim
  │
  ▼
Source Evidence
  │
  ▼
Supported?
 ┌───────┴───────┐
 │               │
 YES             NO
 │               │
 ▼               ▼
Accept       Correct / Remove
```

### Verification Result

The verifier can return a structured result such as:

```json
{
  "verdict": "FAIL",
  "issues": [
    {
      "claim": "Example unsupported claim",
      "reason": "The cited source does not support the statement"
    }
  ],
  "corrected_report": "..."
}
```

---

# 🔄 Verify → Retry Loop

The platform does not simply generate a report and return it.

Instead, it introduces a **verification feedback loop**.

```text
Research
   │
   ▼
Summarize
   │
   ▼
Write
   │
   ▼
Verify
   │
   ▼
┌───────────────────┐
│ Verification Pass?│
└─────────┬─────────┘
          │
     ┌────┴────┐
     │         │
    YES       NO
     │         │
     ▼         ▼
  Return     Retry
  Report     Research
               │
               ▼
            Summarize
               │
               ▼
             Write
               │
               ▼
             Verify
```

### Why the Retry Loop?

LLMs can generate plausible but unsupported statements.

The verification loop provides a mechanism to detect and recover from these situations.

### Bounded Retry

The retry process is intentionally bounded.

```text
MAX_RETRIES = 2
```

This prevents:

```text
Verification Failure
        │
        ▼
      Retry
        │
        ▼
Verification Failure
        │
        ▼
      Retry
        │
        ▼
Verification Failure
        │
        ▼
   STOP ❌
```

Instead, the system guarantees controlled execution.

---

# 🧩 Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| 🐍 Language | **Python 3.11+** | Core application |
| 🤖 Agent Framework | **CrewAI** | Multi-agent orchestration |
| 🔎 Search | **Serper** | Web search |
| 🧠 LLM | **Configurable LLM Provider** | Agent reasoning and generation |
| ⚡ API | **FastAPI** | REST API |
| 🌐 ASGI | **Uvicorn** | Application server |
| 📊 Observability | **Langfuse** | Tracing and monitoring |
| 🛡️ Validation | **Pydantic** | Structured data validation |
| 🚦 API Limiting | **SlowAPI** | Per-client rate limiting |
| 🔄 Concurrency | **Worker Pool** | Job backpressure |
| 🧪 Testing | **Pytest** | Automated tests |
| 📦 Configuration | **Environment Variables** | Runtime configuration |
| 🐳 Deployment | **Docker** | Containerized execution |

---

# 📁 Project Layout

```text
research_platform/
│
├── agents/
│   ├── researcher.jsonc
│   │   # Research agent configuration
│   │
│   ├── summarizer.jsonc
│   │   # Summarization agent configuration
│   │
│   ├── writer.jsonc
│   │   # Report writer configuration
│   │
│   └── verifier.jsonc
│       # Fact-checking verifier configuration
│
├── app/
│   ├── api.py
│   │   # FastAPI application
│   │
│   ├── config.py
│   │   # Environment configuration
│   │
│   ├── jobs.py
│   │   # Research job execution / worker management
│   │
│   └── ...
│       # API and service implementation
│
├── crew.jsonc
│   # CrewAI crew configuration
│
├── .env.example
│   # Environment variable template
│
├── tests/
│   └── ...
│       # Automated tests
│
├── pyproject.toml
│   # Generated CrewAI project configuration
│
└── README.md
```

> The generated `pyproject.toml` should remain intact. Additional dependencies such as FastAPI and Uvicorn can be added using `uv add`.

---

# 🔄 End-to-End Flow

```text
👤 User
 │
 │ Research Topic
 ▼
⚡ FastAPI
 │
 ├── Rate Limit Check
 │
 ├── Concurrency Check
 │
 └── Job Creation
 │
 ▼
🤖 CrewAI Crew
 │
 ▼
🔎 Researcher
 │
 ├── Search Web
 │
 └── Gather Sources
 │
 ▼
📝 Summarizer
 │
 └── Create Research Notes
 │
 ▼
✍️ Writer
 │
 └── Generate Draft
 │
 ▼
🔍 Verifier
 │
 ├── Validate Claims
 │
 ├── Check Sources
 │
 └── Correct Unsupported Claims
 │
 ▼
🔀 Verification Decision
 │
 ├── PASS ───────────────► ✅ Final Report
 │
 └── FAIL
        │
        ▼
   🔄 Retry Research
        │
        └──────────────► Researcher
```

---

# 🚀 Getting Started

## 1️⃣ Create the CrewAI Project

```bash
crewai create crew research_platform
cd research_platform
```

---

## 2️⃣ Copy the Project Files

Copy the following files from this project into the generated CrewAI project:

```text
agents/*.jsonc
crew.jsonc
app/
.env.example
```

### Important

Do **not** overwrite the generated:

```text
pyproject.toml
```

The CrewAI CLI-generated project configuration should remain intact.

---

# 🔑 Configure the LLM

Open every file under:

```text
agents/
```

Replace:

```json
"provider/model-id"
```

with the model you want to use.

For example:

```json
"openai/gpt-4o"
```

You can configure different models for different agents if required.

---

# 🔐 Environment Configuration

Create your environment file:

```bash
cp .env.example .env
```

Then configure the required API keys.

Example:

```env
SERPER_API_KEY=your_serper_api_key

OPENAI_API_KEY=your_openai_api_key
```

If you are using another LLM provider, configure the appropriate provider credentials.

---

# 📦 Install Dependencies

Using `uv`:

```bash
uv add fastapi "uvicorn[standard]"
```

Or using `pip`:

```bash
pip install fastapi uvicorn
```

---

# ▶️ Running the Application

There are two execution modes.

## 🖥️ CLI Mode

Run a single CrewAI execution:

```bash
crewai run
```

The CLI execution performs the research workflow as configured by the CrewAI crew.

> The CLI mode is intended for direct execution and does not provide the FastAPI retry-loop service.

---

# 🌐 API Mode

Start the FastAPI service:

```bash
uvicorn app.api:app --port 8000
```

The service will be available at:

```text
http://localhost:8000
```

FastAPI Swagger documentation:

```text
http://localhost:8000/docs
```

---

# 🔌 API

The FastAPI layer provides a service interface for submitting research jobs.

A typical request can contain:

```json
{
  "topic": "Impact of Agentic AI on enterprise software development"
}
```

The API manages:

```text
Request
  │
  ▼
Rate Limit
  │
  ▼
Concurrency Check
  │
  ▼
Research Job
  │
  ▼
CrewAI
  │
  ▼
Verified Report
```

The exact request and response schema is defined by the FastAPI/Pydantic models in the `app/` package.

---

# 🚦 Rate Limiting & Backpressure

The platform implements **three independent protection layers**.

This is important for production environments where multiple research jobs may execute simultaneously.

---

## 1️⃣ LLM Rate Limiting

CrewAI agent and crew configurations use:

```text
max_rpm
```

The default configuration is:

```text
max_rpm = 10
```

This limits LLM requests per crew run.

For example:

```text
MAX_CONCURRENT_JOBS = 2

max_rpm = 10
```

The theoretical worst-case aggregate request rate can therefore approach:

```text
2 × 10 = 20 RPM
```

Therefore, the configured `max_rpm` should account for the number of concurrent jobs and the provider's actual rate limit.

A useful rule is:

```text
max_rpm ≈ provider_limit / concurrent_jobs
```

---

# 2️⃣ API Rate Limiting

The FastAPI service uses **SlowAPI** to limit requests per client IP.

Configuration:

```env
SUBMIT_RATE_LIMIT=...
```

When a client exceeds the configured limit:

```text
HTTP 429 Too Many Requests
```

is returned.

This protects the API from excessive request submission.

---

# 3️⃣ Backpressure

The service also limits how many jobs can execute and wait at the same time.

Configuration includes:

```env
MAX_CONCURRENT_JOBS=...
MAX_PENDING_JOBS=...
```

Conceptually:

```text
                Incoming Requests
                       │
                       ▼
                ┌──────────────┐
                │ Rate Limiter │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │ Pending Jobs │
                │    Queue     │
                └──────┬───────┘
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
        Worker 1             Worker 2
             │                   │
             └─────────┬─────────┘
                       │
                       ▼
                    CrewAI
```

When capacity is exhausted:

```text
HTTP 429 Too Many Requests
```

is returned with a `Retry-After` header.

This prevents uncontrolled queue growth and protects system resources.

---

# 📊 Langfuse Observability

The platform supports **Langfuse** for end-to-end observability.

Configure:

```env
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_SECRET_KEY=your_secret_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

When configured, each research request can be represented as a:

```text
research-job
```

trace.

The trace can contain nested execution information for:

```text
research-job
│
├── 🔎 Researcher
│   ├── LLM Call
│   └── Search Tool
│
├── 📝 Summarizer
│   └── LLM Call
│
├── ✍️ Writer
│   └── LLM Call
│
├── 🔍 Verifier
│   └── LLM Call
│
└── 🔄 Retry
    ├── Researcher
    ├── Summarizer
    ├── Writer
    └── Verifier
```

This makes it possible to investigate:

- 🔍 Research quality
- ⏱️ Latency
- 💰 LLM usage
- 🤖 Agent execution
- 🔎 Search behavior
- 🔄 Retry behavior
- ❌ Verification failures
- 📈 Production performance

### Graceful Degradation

Langfuse tracing is designed to **silently disable itself** when the required packages or configuration keys are missing.

This means observability should not prevent the research application from running.

---

# 🧠 Why Verification Matters

A traditional LLM research workflow might look like:

```text
Topic
  │
  ▼
LLM
  │
  ▼
Final Report
```

The problem is that an LLM can produce information that sounds correct but is not actually supported by the underlying sources.

This platform introduces:

```text
Research
   │
   ▼
Summarize
   │
   ▼
Write
   │
   ▼
Verify
   │
   ▼
Validated Report
```

The Verifier acts as an independent quality gate.

---

# 🛡️ Key Design Decisions

## 1. 🔎 Source-Grounded Research

The system separates:

```text
Research
```

from:

```text
Writing
```

This allows the Writer to generate content from gathered research rather than relying solely on its own internal knowledge.

---

## 2. 🔍 Independent Verification

The Verifier has a specific responsibility:

> **Do not trust the generated report blindly.**

It checks whether the claims are actually supported by the research material.

This creates a quality-control boundary between:

```text
Generation
```

and:

```text
Validation
```

---

# 3. 🔄 Bounded Verify → Retry

A failed verification does not necessarily terminate the job.

Instead:

```text
Verifier
   │
   ├── PASS → Final Report
   │
   └── FAIL → Retry Research
```

The retry count is bounded to prevent:

```text
Infinite Agent Loop ❌
```

and provide:

```text
Controlled Recovery ✅
```

---

# 4. 🧩 Specialized Agents

Each agent has a focused responsibility:

| Agent | Responsibility |
|---|---|
| 🔎 Researcher | Discover information |
| 📝 Summarizer | Synthesize research |
| ✍️ Writer | Generate report |
| 🔍 Verifier | Validate claims |

This is preferable to using one large agent responsible for the entire workflow because each stage can have a clear prompt, objective, and quality boundary.

---

# 5. 🚦 Production Backpressure

LLM workloads can be expensive and slow.

The API therefore protects itself using:

```text
API Rate Limit
      +
Concurrency Limit
      +
Pending Job Limit
      +
LLM RPM Limit
```

This prevents a traffic spike from turning into uncontrolled LLM calls.

---

# 🏭 Production Considerations

The current architecture provides a strong foundation for production deployment.

Potential improvements include:

- 🗄️ Persistent job storage using PostgreSQL
- 📮 Redis-backed distributed job queues
- ☁️ Distributed worker execution
- 🔐 Authentication and authorization
- 🚦 Distributed API rate limiting
- 📊 Advanced Langfuse dashboards
- 🧪 Automated research-quality evaluation
- 📈 Research quality metrics
- 🔎 Source credibility scoring
- 🧠 Semantic deduplication of sources
- 🗃️ Persistent research-result storage
- 🔄 Scheduled research jobs
- 🐳 Containerized deployment
- ☸️ Kubernetes deployment
- 📡 Production monitoring and alerting
- 🛡️ More sophisticated verifier policies

---

# 🐳 Docker

The application is designed to be containerized.

A production deployment can follow:

```text
                    ┌──────────────┐
                    │ Load Balancer│
                    └───────┬──────┘
                            │
                            ▼
                    ┌──────────────┐
                    │   FastAPI    │
                    │   Container  │
                    └───────┬──────┘
                            │
                            ▼
                    ┌──────────────┐
                    │ CrewAI Worker│
                    └───────┬──────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
          Search           LLM          Langfuse
```

---

# ⚡ Performance & Reliability

The architecture intentionally considers the operational characteristics of LLM applications.

### Rate Control

```text
LLM max_rpm
```

controls LLM request frequency.

### API Protection

```text
SUBMIT_RATE_LIMIT
```

protects the public API.

### Concurrency Control

```text
MAX_CONCURRENT_JOBS
```

controls active research jobs.

### Queue Protection

```text
MAX_PENDING_JOBS
```

prevents unlimited job accumulation.

### Retry Control

```text
MAX_RETRIES
```

prevents infinite verification loops.

Together:

```text
LLM Rate Limit
      +
API Rate Limit
      +
Concurrency
      +
Backpressure
      +
Bounded Retry
      │
      ▼
Controlled Agentic AI System
```

---

# 🧠 Architecture Summary

The platform combines:

```text
                  Agentic AI
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
       Search      Reasoning    Tools
          │           │           │
          └───────────┼───────────┘
                      ▼
                  CrewAI
                      │
                      ▼
             Multi-Agent Workflow
                      │
                      ▼
             Verify → Retry Loop
                      │
                      ▼
                FastAPI Service
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      Rate Limit  Backpressure  Workers
                      │
                      ▼
                  Langfuse
                      │
                      ▼
                Observability
```

The result is a **production-structured Agentic AI research platform** rather than a simple LLM wrapper.

---

# 👨‍💻 Author

**Sunil Kumar**

Software Engineering | Node.js | Python | GenAI | RAG | Agentic AI

Interested in building scalable applications using modern:

**AI • LLM • RAG • Agentic AI • Multi-Agent Systems**

---

## 📜 License

This project is available under the license specified in the repository.