# PRISMA-RAG

Repository for running a fully local Retrieval-Augmented Generation system using Ollama for language models and embeddings.
This setup simplifies installation and runs entirely offline.

---

## Requirements

Before starting, install:

* [Git](https://git-scm.com/download/win)
* [Python 3.11](https://www.python.org/downloads/release/python-3119/)
* [Ollama](https://ollama.ai) (required to run models locally)
* [Visual Studio Build Tools](https://visualstudio.microsoft.com/pt-br/visual-cpp-build-tools/) (optional but recommended on Windows to avoid compilation issues)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/antonio-vmoura/prisma_rag.git
cd prisma_rag
```

---

### 2. Install Poetry

```bash
python3 scripts/poetry_install.py
```

<!-- UnB server:

```bash
python3.11 scripts/poetry_install.py
``` -->

To uninstall:

```bash
py scripts/poetry_install.py --uninstall
```

<!-- Alternative installation:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

UnB server:

```bash
curl -sSL https://install.python-poetry.org | python3.11 -
``` -->

---

### 3. Add Poetry to your PATH

Windows (PowerShell):

```bash
$env:PATH += ";C:\Users\<USER>\AppData\Roaming\Python\Scripts"
```

Linux / WSL:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

<!-- UnB server:

```bash
export PATH="/home/antoniovinicius/.local/bin:$PATH"
``` -->

---

### 4. Install dependencies

```bash
poetry install --extras "ui llms-ollama embeddings-ollama vector-stores-qdrant"
```

---

## Models in Ollama

PRISMA-RAG uses two main models:

* LLM (text generation): `llama3.1:8b`
* Embeddings: `nomic-embed-text`

Download them with:

```bash
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

> You may replace them with any available Ollama model (for example `mistral` or `deepseek-r1`).

---

## Running the System

### 1. Install Ollama (Linux/macOS)

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

---

### 2. Start the Ollama server

```bash
ollama serve
```

---

### 3. Launch PRISMA-RAG

```bash
PGPT_PROFILES=ollama poetry run python -m private_gpt
```

---

## Web Interface

The interface will be available at:

```
http://localhost:8001
```

---

## Troubleshooting

**ConnectionRefusedError when using Ollama**

Ensure Ollama is running:

```bash
ollama serve
```

**ModuleNotFoundError - Gradio**

Reinstall Poetry and dependencies:

```bash
py scripts/poetry_install.py --uninstall
py scripts/poetry_install.py
poetry install --extras "ui llms-ollama embeddings-ollama vector-stores-qdrant"
```

---

## Remote Access (SSH Tunnel)

```bash
ssh -L 8001:localhost:8001 -p 13508 antoniovinicius@164.41.75.221
```

Run inside a screen session:

```bash
screen -S prisma_rag
PGPT_PROFILES=ollama poetry run python -m private_gpt
```

---

## CSV Processing Script (Remote Execution)

```bash
ssh -L 8001:localhost:8001 -p 13508 antoniovinicius@164.41.75.221

screen -S prisma_rag_script

python3.11 create_csv.py llama3370b_2 \
  --path "$(pwd)" \
  --api_url "http://localhost:8001/"
```