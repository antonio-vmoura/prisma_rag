# **PRISMA-RAG**

Repositório para execução local de um sistema de RAG.

---

## 📋 Pré-requisitos

Antes de começar, instale:

* [Git](https://git-scm.com/download/win)
* [Python 3.11](https://www.python.org/downloads/release/python-3119/)
* [Visual Studio Build Tools](https://visualstudio.microsoft.com/pt-br/visual-cpp-build-tools/) (opcional, mas recomendado para evitar erros de compilação)

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

Alternativamente:

```sh
curl -sSL https://install.python-poetry.org | python3 -
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

### 3. Instale as dependências

```sh
poetry install --extras "ui llms-llama-cpp embeddings-huggingface vector-stores-qdrant"
```

### 4. Baixe o modelo

1. Crie uma conta no [Hugging Face](https://huggingface.co/)

2. Instale e faça login no CLI:

   ```sh
   poetry run python -m pip install huggingface_hub
   poetry run huggingface-cli login
   ```

3. Baixe o modelo recomendado (**Mistral-7B-Instruct-v0.2**):

   ```sh
   poetry run python scripts/setup
   ```

---

## ▶️ Execução

Para rodar localmente:

```sh
export PGPT_PROFILES=local
poetry run python -m private_gpt
```

---

## ⚡ Execução com GPU (WSL2 + CUDA)

### 1. Instale dependências do sistema

```sh
sudo apt-get install git gcc make openssl libssl-dev libbz2-dev \
libreadline-dev libsqlite3-dev zlib1g-dev libncursesw5-dev \
libgdbm-dev libc6-dev tk-dev libffi-dev
```

### 2. Instale o CUDA Toolkit

```sh
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-8
```

Configure variáveis de ambiente:

```sh
export PATH="/usr/local/cuda-12.8/bin:$PATH"
export LD_LIBRARY_PATH="/usr/local/cuda-12.8/lib64:$LD_LIBRARY_PATH"
export CUDACXX=/usr/local/cuda/bin/nvcc
```


<!-- 
export PATH="/usr/local/cuda-12.8/bin:$PATH"
export LD_LIBRARY_PATH="/usr/local/cuda-12.8/lib64:$LD_LIBRARY_PATH"
export CUDACXX=/usr/local/cuda/bin/nvcc
-->

Verifique a instalação:

```sh
nvcc --version
nvidia-smi
```

### 3. Instale o **llama-cpp-python** com suporte CUDA

```sh
CMAKE_ARGS='-DGGML_CUDA=on' poetry run pip install --force-reinstall --no-cache-dir \
llama-cpp-python==0.2.90 numpy==1.26.4 markupsafe==2.1.5
```

### 4. Reconfigure e rode (Verifique se BLAS = 1)

```sh
poetry run python scripts/setup
poetry run python -m private_gpt
```

---

## 🔧 Instalação e execução com Shell Script

Edite os **paths** em `install_and_run.sh` e rode:

```sh
./install_and_run.sh
```

---

## ❗ Solução de Problemas

* **Erro `ModuleNotFoundError: gradio`**
  Certifique-se de que o Visual C++ Build Tools está instalado e atualizado.
  Em seguida, desinstale e reinstale o Poetry:

  ```sh
  py scripts/poetry_install.py --uninstall
  py scripts/poetry_install.py
  ```

  sudo find . -name "*.Identifier" -type f -delete