# 🏥 ER Agentic Twin - Healthcare Surge Management

An AI-powered multi-agent system for Emergency Room surge prediction, built with Google ADK and Gemini 3.5 Flash.

## Features

- **Multi-Agent Architecture**: Orchestrator, Triage, Resource, and World Model agents
- **Memory-Augmented Predictions**: Learns from historical patterns
- **Real-time Simulation**: Streamlit dashboard with "what-if" scenarios
- **HIPAA-Ready Design**: Walled garden architecture

## Quick Start

```bash
# Clone and setup
git clone https://github.com/yourusername/er-agentic-twin.git
cd er-agentic-twin

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run dashboard/app.py
