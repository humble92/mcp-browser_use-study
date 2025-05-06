# MCP Browser Use Study

A project demonstrating different ways to run local language models using various frameworks via LangChain, including web automation tasks with `browser_use.Agent`.

## Features

*   Run local LLMs using different backends:
    *   **Use Case 1 (uc1):** Hugging Face Transformers (`hf`), CTransformers (`ctransformers`), LlamaCpp (`llama_cpp`). (Note: `browser_use.Agent` not yet integrated).
    *   **Use Case 2 (uc2):** GPT4All with `browser_use.Agent`. (Currently experiencing issues, see Known Issues).
    *   **Use Case 3 (uc3):** Ollama with `browser_use.Agent` for web automation tasks. (Working)
*   Command-line interface to select the desired use case and backend (for uc1).

## Prerequisites

*   Python >= 3.12
*   [uv](https://github.com/astral-sh/uv) (recommended for faster dependency management) or pip.
*   `browser_use` library and its dependencies (including Playwright browsers: run `playwright install` after installing Python packages).

*   **For Use Case 1 (`hf` runner):** Requires `torch` (included in `pyproject.toml`).
*   **For Use Case 1 (`ctransformers` runner):** Requires `ctransformers` (included). GGUF model file will be automatically downloaded.
*   **For Use Case 1 (`llama_cpp` runner):**
    *   Requires `llama-cpp-python` (included). May require C++ build tools during installation.
    *   The specific GGUF model file must already exist at the path specified in `src/uc1_local_hf/run_llama_cpp.py`.

*   **For Use Case 2 (GPT4All with Agent):**
    *   Requires `gpt4all` (included).
    *   A suitable GGUF model file must be correctly specified in `src/uc2_gpt4all/uc2.py`.
    *   *Note: `browser_use.Agent` integration currently has issues with common GPT4All models for complex tasks (see Known Issues).*

*   **For Use Case 3 (Ollama with Agent):**
    *   Requires `langchain-ollama` and `browser_use` (included).
    *   Ollama server must be running locally.
    *   A capable model (e.g., `qwen2.5-coder`) must be pulled via `ollama pull <model_name>`.

## Known Issues

*   **UC2 (GPT4All with Agent):** The `browser_use.Agent` currently fails to complete tasks with the tested GPT4All models. This is likely due to the model's limitations.

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
        source .venv/bin/activate  # Linux/macOS / Git Bash on Windows
        # .venv\Scripts\activate  # Windows Command Prompt
        # . .venv\Scripts\activate.ps1 # Windows PowerShell
        ```
    *   Using standard `venv`:
        ```bash
        python -m venv .venv
        source .venv/bin/activate  # Linux/macOS / Git Bash on Windows
        # .venv\Scripts\activate  # Windows Command Prompt
        ```

3.  **Install dependencies:**
    ```bash
    uv pip install -e .
    # or for pip:
    # pip install -e .
    ```

4.  **Install Playwright browser drivers (required for `browser_use.Agent`):**
    ```bash
    playwright install
    ```
    *Note: Installing `torch` and `llama-cpp-python` (done by `uv pip install -e .`) might have specific OS/hardware requirements. Refer to their official documentation if issues arise during the editable install.*

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

# Run Use Case 2 (GPT4All with Agent - currently has issues)
uv run main.py uc2

# Run Use Case 3 (Ollama with Agent)
uv run main.py uc3
```

*   For `uc1`, you need to specify the runner (`hf`, `ctransformers`, or `llama_cpp`) after `uc1`.
*   Ensure prerequisites for the chosen use case/runner are met (e.g., Ollama server running for `uc3`).
