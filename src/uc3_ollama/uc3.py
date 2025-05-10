import json
import pathlib
import os
import platform  # For OS detection
import subprocess
import time
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from browser_use import Agent, Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig

MAX_STEPS = 20
COOKIES_FILE_PATH = pathlib.Path("cookies.json").resolve()

# --- OS-dependent Chrome Path Configuration --- #
current_os = platform.system()

# Try to get paths from environment variables first, then OS defaults, then None
CHROME_EXECUTABLE_PATH = os.environ.get("CHROME_EXECUTABLE_PATH")

if not CHROME_EXECUTABLE_PATH:
    if current_os == "Windows":
        # Common paths for Chrome on Windows
        possible_paths = [
            pathlib.Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
            pathlib.Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
            pathlib.Path(os.path.expanduser("~/AppData/Local/Google/Chrome/Application/chrome.exe"))
        ]
        for path in possible_paths:
            if path.exists():
                CHROME_EXECUTABLE_PATH = str(path)
                break
    elif current_os == "Darwin": # macOS
        CHROME_EXECUTABLE_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    elif current_os == "Linux":
        # Common paths for Chrome on Linux (Debian/Ubuntu based)
        possible_paths = [
            pathlib.Path("/usr/bin/google-chrome-stable"),
            pathlib.Path("/usr/bin/google-chrome"),
            pathlib.Path("/opt/google/chrome/chrome"),
        ]
        for path in possible_paths:
            if path.exists():
                CHROME_EXECUTABLE_PATH = str(path)
                break

print(f"Detected OS: {current_os}")
if CHROME_EXECUTABLE_PATH:
    print(f"Using Chrome executable: {CHROME_EXECUTABLE_PATH}")
else:
    print("Warning: Chrome executable path not found or set.")
# --- End OS-dependent Chrome Path Configuration --- #

async def uc3(argv=None):
    print("Running Use Case 3 (Ollama with Agent)...")

    # Specify the Ollama model name which supports tool-calling
    # Make sure this model is pulled (e.g., 'ollama pull qwen3')
    # model_name = "qwen3"
    # model_name = "llama3.2"
    model_name = "mistral"
    print(f"Attempting to connect to Ollama with model: {model_name}")

    # Define the task for the Agent
    task_template = "Search a picture of {word} and save it to the file {filename}"
    input_variables = {"word": "a beautiful cat", "filename": "cat_ollama.png"}
    formatted_task = task_template.format(**input_variables)
    # formatted_task = "filter and show emails in gmail containing Otter.ai"
    print(f"Formatted task for Agent: {formatted_task}")

    # load context cookies (Fallback)
    context_config = BrowserContextConfig()
    if COOKIES_FILE_PATH.exists():
        try:
            with open(COOKIES_FILE_PATH, "r") as f:
                context_config.cookies = json.load(f)
            print(f"Loaded cookies from {COOKIES_FILE_PATH}")
        except Exception as e:
            print(f"Warning: Failed to load cookies.json: {e}")

    try:
        # Ollama model w/ tool-calling
        llm = ChatOllama(
            model=model_name,
            num_ctx=32000, # Max context window
            num_gpu=40,    # Layers to offload to GPU (adjust based on model & VRAM)
                           # For RTX 3090 with 24GB, many models can offload all/most layers.
                           # Try values like 35, 40, 50 or even higher (e.g., 99 for all possible).
            num_thread=8,  # CPU threads for parallel processing (adjust to your CPU core count)
            num_batch=1024, # Batch size for prompt processing (default 512)
            repeat_penalty=1.1, # Uncomment to penalize repetition
            # f16_kv=True,   # Use FP16 for KV cache to save VRAM
            # temperature=0.7, # Uncomment and set for generation creativity
            # top_k=40,        # Uncomment for top-k sampling
            # top_p=0.9,       # Uncomment for nucleus sampling
            # repeat_penalty=1.1, # Uncomment to penalize repetition
            # verbose=True, # For more detailed Ollama logs if needed
        )

        # Remote API LLM model
        # llm = ChatOpenAI(model="gpt-4o")

        # Chrome in debug mode
        temp_profile = pathlib.Path("./.tmp_chrome_debug_uc3").resolve()
        temp_profile.mkdir(exist_ok=True)
        debug_cmd = [
            CHROME_EXECUTABLE_PATH,
            "--remote-debugging-port=9222",
            f"--user-data-dir={str(temp_profile)}"
        ]
        print(f"Launching Chrome in debug mode:\n  {' '.join(debug_cmd)}")
        chrome_proc = subprocess.Popen(debug_cmd)
        time.sleep(3)

        # BrowserConfig & Browser
        browser_cfg = BrowserConfig(
            headless=False,
            cdp_url="http://127.0.0.1:9222",
            new_context_config=context_config,
        )
        browser = Browser(config=browser_cfg)

        # Agent
        agent = Agent(
            task=formatted_task,
            llm=llm,
            browser=browser,
        )

        print(f"Invoking agent with task using Ollama ({model_name})...")
        result = await agent.run(max_steps=MAX_STEPS)
        print("\nResult:")
        print(result)

    except ImportError as ie:
        print(f"ImportError: {ie}")
    except Exception as e:
        print(f"Error initializing or running Ollama/Agent: {e}")
    finally:
        if 'browser' in locals():
            await browser.close()
        if 'chrome_proc' in locals():
            chrome_proc.terminate()
