# Install Poetry
python scripts/poetry_install.py

# Alternatively, use curl to install Poetry
# Uncomment the line below if you prefer this method
# curl -sSL https://install.python-poetry.org | python -

# Add Poetry to PATH - Change the path according to the machine
export PATH="C:\Users\sas\AppData\Roaming\Python\Scripts:$PATH"
# Append to shell configuration file for persistence 
echo 'export PATH="C:\Users\sas\AppData\Roaming\Python\Scripts:$PATH"' >> ~/.bashrc

# Install dependencies
poetry install --extras "ui llms-llama-cpp embeddings-huggingface vector-stores-qdrant"

# Install additional requirements
poetry run python -m pip install injector llama_index --upgrade llama-index-embeddings-huggingface

# Install huggingface_hub and login
poetry run python -m pip install huggingface_hub
# RUN THIS COOMAND ONCE TO SET HUGGINGFACE_HUB LOGIN
# poetry run huggingface-cli login

# Download the model
poetry run python scripts/setup

# Execute the prisma_rag
export PGPT_PROFILES=local
poetry run python -m private_gpt