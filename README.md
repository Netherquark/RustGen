# RustGen

This is a proof of concept implementation of a multiagent Rust coder.

**Prompt refinement agent:** llama3:8b

**Code generation agent:** granite-code:8b

**Code refinement agent:** llama3:8b

**Backend:** Ollama

**Rust:** rustc (not cargo)

## Getting Started

Follow these steps before running main.py:

1. Any Linux setup (preferably with CUDA & 8+GB RAM)
2. Install Ollama from [here](https://ollama.com/download).
3. `ollama pull llama3`
4. `ollama pull granite-code:8b`
5. Install `rustc` (apt/dnf/etc)
