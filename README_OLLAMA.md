# **PRISMA-RAG**

Repositório para execução local de um sistema de utilizando **Ollama** para LLMs e embeddings.
Este setup simplifica a instalação e roda totalmente **offline**.

---

## 📋 Pré-requisitos

Antes de começar, instale:

* [Git](https://git-scm.com/download/win)
* [Python 3.11](https://www.python.org/downloads/release/python-3119/)
* [Ollama](https://ollama.ai) (necessário para rodar os modelos)
* [Visual Studio Build Tools](https://visualstudio.microsoft.com/pt-br/visual-cpp-build-tools/) (opcional, mas recomendado no Windows para evitar erros de compilação)

---

## ⚙️ Instalação

### 1. Clone o repositório

```sh
git clone https://github.com/antonio-vmoura/prisma_rag.git && cd prisma_rag
```

### 2. Instale o Poetry

```sh
python3 scripts/poetry_install.py
```
UnB server:

```sh
/usr/bin/python3.8 scripts/poetry_install.py
```

Para desinstalar:

```sh
    py scripts/poetry_install.py --uninstall
```

Alternativamente:

```sh
curl -sSL https://install.python-poetry.org | python3 -
```
UnB server:

```sh
curl -sSL https://install.python-poetry.org | /usr/bin/python3.8 -
```

Adicione o Poetry ao seu **PATH**:

* **Windows (PowerShell)**:

  ```sh
  export PATH="C:\Users\<USUARIO>\AppData\Roaming\Python\Scripts"
  ```
* **Linux / WSL**:

  ```sh
  export PATH="$HOME/.local/bin:$PATH"
  ```

  UnB server:

  ```sh
  export PATH="/home/antoniovinicius/.local/bin:$PATH"
  ```

### 3. Instale as dependências

```sh
poetry install --extras "ui llms-ollama embeddings-ollama vector-stores-qdrant"
```

---

## 📥 Modelos no Ollama

O PRISMA-RAG usa dois modelos principais:

* **LLM (texto)**: `llama3.1:8b`
* **Embeddings**: `nomic-embed-text`

Baixe-os com:

```sh
ollama pull llama3:8b
ollama pull nomic-embed-text
```

> ⚡ Você pode trocar por qualquer outro modelo disponível no Ollama (ex.: `mistral`, `deepseek-r1`, etc.).

---

## ▶️ Execução

### 1. Inicie o Ollama

```sh
ollama serve
```

### 2. Rode o PRISMA-RAG

```sh
PGPT_PROFILES=ollama poetry run python -m private_gpt
```

---

## 🌐 Interface Web

A interface estará disponível em:

👉 [http://localhost:8001](http://localhost:8001)


## ❗ Solução de Problemas

* **Erro `ConnectionRefusedError` ao rodar com Ollama**
  Verifique se o Ollama está rodando:

  ```sh
  ollama serve
  ```

* **Erro `ModuleNotFoundError: gradio`**
  Reinstale o Poetry e dependências:

  ```sh
  py scripts/poetry_install.py --uninstall
  py scripts/poetry_install.py
  poetry install --extras "ui llms-ollama embeddings-ollama vector-stores-qdrant"
  ```
