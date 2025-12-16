# Skyscope Sentinel Intelligence
### Autonomous Geopolitical Swarm Collective

**Skyscope** is a self-contained, high-fidelity AI swarm designed for autonomous deep research, critical analysis, and multimedia intelligence reporting.

![Status](https://img.shields.io/badge/Status-Operational-green) ![Python](https://img.shields.io/badge/Python-3.10+-blue) ![License](https://img.shields.io/badge/License-Proprietary-red)

---

## 🚀 Key Capabilities

*   **Autonomous Research**: Active scraping of news sites (e.g., RT.com via `trafilatura`) and extraction of YouTube video transcripts (`youtube-transcript-api`) for real-time intel.
*   **Hierarchical Swarm**: Orchestrator → Researcher → Analyst → Simulator agent chain.
*   **Embedded & Fail-Proof**:
    *   **Logic**: `Qwen2.5-0.5B` (Local fallback).
    *   **Voice**: `Kokoro-82M` (Near-human local TTS).
    *   **Vision**: `Moondream2`.
*   **Multimedia Artifacts**: Auto-generates Watermarked PDF Trajectory Reports and Video Briefings.
*   **Resilience**: Intelligent fallback (OpenRouter \u2192 LocalAI \u2192 Embedded).

---

## 🛠️ Installation

1.  **Clone & Environment**:
    ```bash
    git clone https://github.com/skyscope-sentinel-intelligence.git
    cd skyscope-sentinel-intelligence
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Initialize Embedded Models**:
    Downloads Qwen, Kokoro, and Vision models (~1GB total) to `./models`.
    ```bash
    python3 -m skyscope.utils.model_loader
    ```

3.  **Local Stack (Optional)**:
    For RAG and Memory features:
    ```bash
    docker-compose up -d
    ```

## ⚙️ Configuration

Set your API keys (optional for embedded mode) in `.env` or system environment:

```bash
OPENROUTER_API_KEY=sk-or-v1-...
ELEVENLABS_API_KEY=xi-...
```

---

## 🖥️ Usage

### 1. Interactive Swarm Dashboard (Recommended)
Simply run the command with no arguments to enter the **Live Dashboard REPL**.
```bash
python3 main.py
```
*Enter natural language directives like:*
> "Research the impact of new trade sanctions on the Eurozone"
> "Generate a report based on the latest headlines from https://www.rt.com/news/"

### 2. Quick Command
One-shot execution for automation pipelines.
```bash
python3 main.py "Analyze the geopolitical stability of the South China Sea"
```

---

## 📂 Output Artifacts

All intelligence products are generated in the root directory (configurable):
*   **PDF Reports**: `skyscope_report_[TIMESTAMP].pdf` (Watermarked)
*   **Video Briefings**: `skyscope_briefing_[TIMESTAMP].mp4` (Watermarked)

---

## 🛡️ Architecture & Watermarking

**Skyscope Sentinel** enforces strict provenance.
*   All PDF pages contain a top-right watermark: `Skyscope Sentinel Intelligence - Intelligence Report - [DATE] - [GMT]`.
*   All Video briefings include a persistent visual watermark overlay.

---

## ⚠️ Troubleshooting

*   **TTS Issues**: If `Kokoro` fails or `soundfile` errors, ensure `libsndfile` is installed (`brew install libsndsfile` on Mac).
*   **Scraping**: `trafilatura` and `youtube-transcript-api` require internet access. If offline, the **Researcher Agent** will fallback to LocalRecall memory or simulation.

---

**Skyscope Sentinel Intelligence**
*Classified Development Branch*