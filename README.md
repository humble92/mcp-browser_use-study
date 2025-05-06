# MCP Browser Use Study

A project demonstrating different ways to run local language models using various frameworks via LangChain.

## Features

*   Run local LLMs using different backends:
    *   **Use Case 1 (uc1):** Hugging Face Transformers (`hf`), CTransformers (`ctransformers`), LlamaCpp (`llama_cpp`).
    *   **Use Case 2 (uc2):** GPT4All.
    *   **Use Case 3 (uc3):** Ollama.
*   Command-line interface to select the desired use case and backend (for uc1).

## Prerequisites

*   Python >= 3.12
*   [uv](https://github.com/astral-sh/uv) (recommended for faster dependency management) or pip.
*   **For Use Case 1 (`hf` runner):** PyTorch or TensorFlow installed. (`uv pip install torch`)
*   **For Use Case 1 (`ctransformers` runner):** GGUF model file will be automatically downloaded on the first run.
*   **For Use Case 1 (`llama_cpp` runner):**
    *   `llama-cpp-python` installed (potentially requires C++ build tools). (`uv pip install llama-cpp-python`)
    *   The specific GGUF model file must already exist at the path specified in `src/uc1_local_hf/run_llama_cpp.py`. This file might be downloaded initially by running the `ctransformers` runner or manually placed.
*   **For Use Case 2 (GPT4All):**
    *   `gpt4all` library installed (`uv pip install gpt4all`).
    *   Model file will be automatically downloaded by the `gpt4all` library to its default cache directory (`~/.cache/gpt4all/`) OR you need to specify the path to an existing model file in `src/uc2_gpt4all/uc2.py`.
*   **For Use Case 3 (Ollama):**
    *   Ollama server must be running locally (e.g., run `ollama serve` in a separate terminal or use the Ollama desktop app).
    *   The desired model (e.g., `hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF:latest`) must be pulled using `ollama pull <model_name>`.
    *   `langchain-ollama` installed (`uv pip install langchain-ollama`).

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd mcp-browser-use-study
    ```

2.  **Create and activate a virtual environment:**
    *   Using `uv`:
        ```bash
        uv venv
        source .venv/bin/activate  # Linux/macOS
        # or
        .venv\Scripts\activate  # Windows (Command Prompt/PowerShell)
        # or
        . .venv/Scripts/activate.ps1 # Windows (PowerShell Core)
        ```
    *   Using standard `venv`:
        ```bash
        python -m venv .venv
        source .venv/bin/activate  # Linux/macOS
        # or
        .venv\Scripts\activate  # Windows (Command Prompt/PowerShell)
        ```

3.  **Install dependencies:**
    *   Using `uv`:
        ```bash
        uv pip install -e .
        # Install necessary backend libraries based on the prerequisites above, e.g.:
        # uv pip install torch llama-cpp-python gpt4all langchain-ollama
        ```
    *   Using `pip`:
        ```bash
        pip install -e .
        # Install necessary backend libraries based on the prerequisites above, e.g.:
        # pip install torch llama-cpp-python gpt4all langchain-ollama
        ```
    *Note: Installing `torch` and `llama-cpp-python` might require specific steps depending on your OS and hardware (especially GPU support for `llama-cpp-python`). Refer to their official documentation.*

## Usage

Run the use cases via the `main.py` script from the **project root directory**.

```bash
# Show help message
uv run main.py

# Run Use Case 1 (Local Hugging Face Transformers)
uv run main.py uc1 hf

# Run Use Case 1 (CTransformers with GGUF)
uv run main.py uc1 ctransformers

# Run Use Case 1 (LlamaCpp with GGUF)
uv run main.py uc1 llama_cpp

# Run Use Case 2 (GPT4All)
uv run main.py uc2

# Run Use Case 3 (Ollama)
uv run main.py uc3
```

*   For `uc1`, you need to specify the runner (`hf`, `ctransformers`, or `llama_cpp`) after `uc1`.
*   Ensure prerequisites for the chosen use case/runner are met (e.g., Ollama server running for `uc3`).
