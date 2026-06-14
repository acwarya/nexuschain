# NexusChain — Agentic Supply Chain Broker

### 🚀 Track 1: Agents & Agentic Workflows for Industry Transformation

**NexusChain** is a production-ready prototype demonstrating how intelligent, multi-agent workflows can transform industrial supply chains without sacrificing operational safety.

Most enterprise workflows fail when moving from a demo to production because LLMs are inherently probabilistic and chaotic. NexusChain solves this by wrapping specialized agents inside a **deterministic finite state machine**. The agents handle complex semantic matching and asset discovery, but strict business logic and a **Human-in-the-Loop (HITL) gateway** ensure no financial payload is transmitted to legacy databases without authorization.

---

## 🏗️ System Architecture & Workflow State

Unlike loose agent chains that suffer from "agent drift" or infinite loops, NexusChain enforces a strict, linear state progression:

```
[State: IDLE]
      │
      ▼
[State: PROCESSING] ──► 1. Inventory Agent (Reads Legacy ERP)
      │             ──► 2. Sourcing Agent (Evaluates Vendors)
      │             ──► 3. Contract Agent (Synthesizes Data Structures)
      ▼
[State: GATEWAY]    ──► Requires Human Sign-off (Slack / UI Dashboard)
   ├── (Approve) ──► [State: COMPLETE] ──► Injects transaction to ERP
   └── (Reject)  ──► [State: REJECTED] ──► Halts & Logs Termination

```

---

## ✨ Key Features & Technical Solutions

### 1. Deterministic Execution Layer

Instead of letting an LLM blindly decide what step to take next, the application state machine dictates the flow. If a constraint is broken, the system gracefully self-terminates into an **Escalated State** rather than executing a bad transaction.

### 2. Semantic Data Normalization (Legacy ERP Integration)

The system simulates interaction with legacy, rigid enterprise structures (like SAP or Oracle DBs). The agents read unformatted inventory anomalies, cross-reference them against modern supplier matrices, and output perfectly structured JSON telemetry.

### 3. Real-Time Trace Log Observability

Transparency is vital in industrial AI. The Middle Pane exposes a live tracking interface that explicitly logs the exact timestamp, agent identity, and mathematical logic behind every decision made by the sub-agents.

### 4. Human-in-the-Loop Guardrail

The contract agent drafts a cryptographically uniform, proposed JSON Purchase Order payload. The application blocks any automated script from executing database updates until a manager interacts with the Secure Gateway.

---

## 🛠️ Local Installation & Testing Guide

Want to run this prototype locally on your machine? Follow these quick steps:

### Prerequisites

Make sure you have **Python 3.8 or higher** installed.

### 1. Clone or Download the Files

Create a local directory containing the codebase:

```bash
mkdir nexus-chain-prototype
cd nexus-chain-prototype

```

Save the application script as `app.py` and your dependency file as `requirements.txt`.

### 2. Setup a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Boot Up the Interface

```bash
streamlit run app.py

```

Your terminal will output a local network address (usually `http://localhost:8501`). Open this URL in any web browser to interact with the demo.

---

## 🎯 How to Demo & Pressure-Test the Application

To show off the robustness of this system to judges, perform these three testing scenarios live:

### Scenario A: The Optimal Path (Happy Path)

1. Leave the **Max Allowed Budget** at `$500` and **Max Allowed Lead Time** at `5 Days`.
2. Click **Trigger Agent Workflow**.
3. *Result:* The sourcing agent will find `Alpha Components` (which fits under budget and takes 4 days). The contract agent passes validation, and the JSON payload populates the Secure Gateway instantly.

### Scenario B: The Time-Crunch Escalation

1. Lower the **Max Allowed Lead Time** slider down to `2 Days` (keeping the budget at `$500`).
2. Click **Trigger Agent Workflow**.
3. *Result:* `Beta Electronics` can deliver in 1 day, but their high unit price brings the total order to `$572.00`. The Contract Agent will catch that this violates your `$500` maximum budget. The system will throw a **Constraint Breach** and lock down into the **Escalated** screen to prevent an over-budget purchase.

### Scenario C: The Budget-Lock Escalation

1. Change the **Max Allowed Lead Time** to `10 Days` but lower the **Max Allowed Budget** to `$300`.
2. Click **Trigger Agent Workflow**.
3. *Result:* Even though `Gamma Tech` is incredibly cheap ($3.80/unit), the pure volume of missing parts required brings the total to `$334.40`. The workflow halts, demonstrating that the agent cannot be tricked or pushed past operational boundaries.
