# MCP Browser Use Study

A project demonstrating different ways to run local language models using various frameworks via LangChain, including web automation tasks with `browser_use.Agent`.

## Features

*   Run local LLMs using different backends:
    *   **Use Case 1 (uc1):** Hugging Face Transformers (`hf`), CTransformers (`ctransformers`), LlamaCpp (`llama_cpp`). (Note: `browser_use.Agent` not yet integrated).
    *   **Use Case 2 (uc2):** GPT4All with `browser_use.Agent`. (Currently experiencing issues, see Known Issues).
    *   **Use Case 3 (uc3):** Ollama with `browser_use.Agent` for general web automation tasks. (Working)
    *   **Use Case 4 (uc4):** Ollama with `browser_use.Agent` specifically for attempting Google Login using `sensitive_data` and `initial_actions`. (Experimental)
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
    *   A capable model (e.g., `qwen2:7b-instruct` or `mistral`) must be pulled via `ollama pull <model_name>`.
    *   To use your existing Chrome logins/sessions with `uc3` (or potentially `uc4`), see the "Using a non standard profile" section below.

*   **For Use Case 4 (Google Login with Agent - Experimental):**
    *   Ollama server must be running locally.
    *   A highly capable model (e.g., `qwen2:7b-instruct` or larger) must be pulled via `ollama pull <model_name>`.
    *   **Crucially:** You must set the `GOOGLE_ID` and `GOOGLE_PASSWORD` environment variables with your Google credentials before running `uc4`.
    *   A local Chrome installation path must be detectable or set via the `CHROME_EXECUTABLE_PATH` environment variable.
    *   *Note: Google login flows are complex and change frequently. This use case might require adjustments or fail due to CAPTCHAs, 2FA, or updated UI elements.*

## Using a non standard profile

To allow `uc3` to leverage existing browser sessions or observe the process in a dedicated profile, you can launch Chrome with a specific remote debugging port and a non standard user data directory. The `browser_use` agent will then connect to this pre-launched instance via its CDP (Chrome DevTools Protocol) URL.

**Steps:**

1.  **Close an existing Chrome instances with the same remote debugging port:** This is crucial to avoid conflicts.

2.  **Launch Chrome with Remote Debugging:**
    Open your terminal and run the command appropriate for your OS. You might need to adjust the path to `chrome.exe` or `google-chrome` if it's installed in a non-standard location. Using a non-standard profile directory (e.g., `C:\tmp\chrome_debug` or `~/tmp/chrome_debug`) is essential since Chrome 136. (see [Changes to remote debugging switches to improve security](https://developer.chrome.com/blog/remote-debugging-port)). If it is set to the default Chrome data directory, it is ignored and the debug port is not working. **Do not use your default Chrome profile directory.**

    *   **Windows:**
        ```cmd
        "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 
        --user-data-dir="C:\tmp\chrome_debug_uc3"
        ```
    *   **macOS:**
        ```bash
        /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="$HOME/
        tmp/chrome_debug_uc3"
        ```
    *   **Linux:**
        ```bash
        google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/tmp/chrome_debug_uc3"
        ```

3.  **Log in to Services:** In the newly opened Chrome window (launched by the command above), manually navigate to any websites you need the agent to access (e.g., Gmail, Google) and log in. Perform any necessary 2FA steps.

4.  **Keep this Chrome window open.**

5.  **Run the Use Case:** The script (`uc3.py`) is configured to attempt connection to `http://127.0.0.1:9222` by default (can be overridden by `CHROME_CDP_URL` env var).

    **Fallback to Cookies:** If `uc3` cannot connect via CDP, it will attempt to fall back to using `cookies.json` (if 
    generated by `conf1`).


## Known Issues

*   **UC2 (GPT4All with Agent):** The `browser_use.Agent` currently fails to complete tasks reliably with tested GPT4All models, likely due to model limitations.
*   **UC4 (Google Login):** Google login automation is inherently fragile. Changes in Google's UI, security measures (like CAPTCHAs, device verification), or model limitations can easily cause this to fail. It serves as an experimental demonstration of `sensitive_data` and `initial_actions`.

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
        source .venv/bin/activate  # Linux/macOS / Git Bash
        # .\.venv\Scripts\activate # Windows PowerShell/CMD
        ```
    *   Using standard `venv`:
        ```bash
        python -m venv .venv
        source .venv/bin/activate  # Linux/macOS / Git Bash
        # .venv\Scripts\activate.bat # Windows CMD
        # .\.venv\Scripts\Activate.ps1 # Windows PowerShell
        ```

3.  **Install dependencies:**
    ```bash
    uv pip install -e .
    # or for pip:
    # pip install -e .
    ```

4.  **Install Playwright browser drivers:**
    ```bash
    playwright install
    ```

## Usage

Run the use cases via the `main.py` script from the project root directory.

```bash
# Show help message
uv run main.py --help

# Run Use Case 1 (Local Hugging Face Transformers)
uv run main.py uc1 hf

# Run Use Case 1 (CTransformers with GGUF)
uv run main.py uc1 ctransformers

# Run Use Case 1 (LlamaCpp with GGUF)
uv run main.py uc1 llama_cpp

# Run Use Case 2 (GPT4All with Agent - experimental)
uv run main.py uc2

# Run Use Case 3 (Ollama with Agent)
uv run main.py uc3

# Run Use Case 4 (Ollama Google Login - experimental)
# Ensure GOOGLE_ID and GOOGLE_PASSWORD env vars are set!
uv run main.py uc4
```

*   For `uc1`, you need to specify the runner (`hf`, `ctransformers`, or `llama_cpp`) after `uc1`.
*   Ensure prerequisites for the chosen use cases/runner are met (e.g., Ollama server running for `uc3`/`uc4`, environment variables set for `uc4`).
