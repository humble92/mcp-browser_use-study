import json
import pathlib
from langchain_ollama import ChatOllama
from browser_use import Agent, Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig

MAX_STEPS=15
COOKIES_FILE_PATH = pathlib.Path("cookies.json").resolve()

# Function signature updated for consistency and async
async def uc3(argv=None):
    print("Running Use Case 3 (Ollama with Agent using saved cookies)...")

    # Specify the Ollama model name which supports tool-calling
    # Make sure this model is pulled (e.g., 'ollama pull qwen2.5-coder')
    # model_name = "qwen3"
    # model_name = "llama3.2"
    model_name = "mistral"
    print(f"Attempting to connect to Ollama with model: {model_name}")

    # Define the task for the Agent
    task_template = "Search a picture of {word} and save it to the file {filename}" 
    input_variables = {"word": "a beautiful cat", "filename": "cat_ollama.png"}
    formatted_task = task_template.format(**input_variables)
    print(f"Formatted task for Agent: {formatted_task}")

    # --- BrowserContextConfig with cookies --- 
    context_config = BrowserContextConfig()
    if COOKIES_FILE_PATH.exists() and COOKIES_FILE_PATH.is_file():
        try:
            with open(COOKIES_FILE_PATH, 'r') as f:
                cookies = json.load(f)
            context_config.cookies = cookies # Set cookies
            print(f"Successfully loaded cookies from {COOKIES_FILE_PATH}")
        except Exception as e:
            print(f"Warning: Could not load or parse cookies from {COOKIES_FILE_PATH}. Proceeding without saved cookies. Error: {e}")
    else:
        print(f"Warning: Cookies file not found at {COOKIES_FILE_PATH}. Proceeding without saved cookies. You might need to run 'conf1' first.")
    # --- End BrowserContextConfig --- 

    try:
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

        # Pass the context_config to BrowserConfig, then to Browser
        browser_config = BrowserConfig(
            # headless=False, # Keep browser visible for debugging if needed
            # disable_security=True,
            new_context_config=context_config # Pass context_config here
        )
        browser = Browser(config=browser_config)

        # Controller for manual input is no longer needed if cookies are used
        # sensitive_data is also not needed

        agent = Agent(
            task=formatted_task,
            llm=llm,
            browser=browser,
            # controller is removed as we are using cookies
        )

        print(f"Invoking agent with task using Ollama ({model_name}) and potentially saved session...")
        result = await agent.run(max_steps=MAX_STEPS)
        print("\nResult:")
        print(result)

    except ImportError as ie:
        if "browser_use" in str(ie):
            print(f"Error: Could not import Agent from browser_use. Please ensure browser_use.py exists and is in the PYTHONPATH. Details: {ie}")
        else:
            print(f"ImportError: {ie}")            
    except Exception as e:
        print(f"Error initializing or running Ollama/Agent: {e}")
        print(f"Please ensure the Ollama server is running, the model '{model_name}' is available, and the Agent class is correctly defined and imported.")
    finally:
        if 'browser' in locals() and browser:
             await browser.close() # Ensure browser is closed in finally block
