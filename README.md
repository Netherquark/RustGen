# RustGen

LLM Enhanced Rust Code Generation

**Prompt refinement:** llama3:8b

**Code generation:** granite-code:8b

**Code refinement using logs:** llama3:8b

**Backend:** Ollama

**Rust:** rustc (not ollama)

## Getting Started

Follow these steps before running main.py:

1. Any Linux setup (preferably with CUDA & 8+GB RAM)
2. Install Ollama from [here](https://ollama.com/download).
3. `ollama pull llama3`
4. `ollama pull granite-code:8b`
5. Install `rustc` (apt/dnf/etc)
