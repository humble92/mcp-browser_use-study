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
    *   To use your existing Chrome logins/sessions with `uc3`, see the "Using Local Browser Profile with UC3 (Advanced)" section below.

## Using Local Browser Profile with UC3 (Advanced)

To allow `uc3` to use your existing browser sessions (e.g., logged-in Gmail), you need to launch a Chrome instance with a specific remote debugging port and user data directory. The `browser_use` agent will then connect to this pre-launched instance via its CDP (Chrome DevTools Protocol) URL.

**Steps:**

1.  **Close all existing Chrome instances:** This is crucial to avoid conflicts. Ensure no `chrome.exe` (Windows) or `Google Chrome` (macOS/Linux) processes are running.

2.  **Launch Chrome with Remote Debugging:**
    Open your terminal (Command Prompt, PowerShell, Terminal, etc.) and run one of the following commands based on your OS. You might need to adjust the path to `chrome.exe` or `google-chrome` if it's installed in a non-standard location.
    Using a non-standard debug profile directory (e.g., `C:\tmp\chrome_debug` or `~/tmp/chrome_debug`) is mandatory for security reasons since Chrome 136 (see [Changes to remote debugging switches to improve security](https://developer.chrome.com/blog/remote-debugging-port)). If it is set to the default Chrome data directory, it is ignored and the debug port is not allowed to open.

    *   **Windows (Command Prompt/PowerShell):**
        ```cmd
        "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\tmp\chrome_debug_uc3"
        ```
        (Adjust `C:\tmp\chrome_debug_uc3` to your desired temporary profile path. If using your default profile, find its path, e.g., `C:\Users\YourUser\AppData\Local\Google\Chrome\User Data`)

    *   **macOS:**
        ```bash
        /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="$HOME/tmp/chrome_debug_uc3"
        ```
        (Adjust `~/tmp/chrome_debug_uc3` or use your default profile path, e.g., `~/Library/Application\ Support/Google/Chrome`)

    *   **Linux:**
        ```bash
        google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/tmp/chrome_debug_uc3"
        ```
        (Or `google-chrome-stable`. Adjust `~/tmp/chrome_debug_uc3` or use your default profile path, e.g., `~/.config/google-chrome`)

3.  **Log in to Services:** In the newly opened Chrome window (launched by the command above), manually navigate to any websites you need the agent to access (e.g., Gmail, Google) and log in. Perform any necessary 2FA steps.

4.  **Keep this Chrome window open.**

5.  **Configure `uc3`:**
    The `uc3.py` script is configured to attempt to connect to `http://127.0.0.1:9222` by default if local profile usage is detected. If you used a different port, you'll need to modify the `cdp_url` in `src/uc3_ollama/uc3.py`.

    Now, when you run `uv run main.py uc3`, it should connect to this pre-launched, logged-in Chrome session.

    **Fallback to Cookies:** If `uc3` cannot connect via CDP, it will attempt to fall back to using `cookies.json` (if generated by `conf1`).

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
