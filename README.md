# RustGen

This is a proof of concept implementation of a multiagent Rust coder.

![unnamed](https://github.com/user-attachments/assets/d13c0d2a-7c18-4d68-aa8d-92f40a805782)

**Prompt refinement agent:** llama3:8b

**Code generation agent:** granite-code:8b

**Code refinement agent:** llama3:8b

**Backend:** Ollama

**Rust:** rustc (not cargo)

![Picture1](https://github.com/user-attachments/assets/47d4234c-0bb5-4ad0-be1c-b18359e17580)



## Getting Started

Follow these steps before running main.py:

1. Any Linux setup (preferably with CUDA & 8+GB RAM)
2. Install Ollama from [here](https://ollama.com/download).
3. `ollama pull llama3`
4. `ollama pull granite-code:8b`
5. Install `rustc` (apt/dnf/etc)
