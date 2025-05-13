import json
import pathlib
import os
import platform
# import asyncio

from langchain_ollama import ChatOllama
from browser_use import Agent, Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig

MAX_STEPS = 25
COOKIES_FILE_PATH = pathlib.Path("cookies_uc4.json").resolve()
MODEL_NAME = "qwen3:30b" # Or another capable model

# --- OS-dependent Chrome Path Configuration (Keep for potential Playwright fallback) ---
current_os = platform.system()
CHROME_EXECUTABLE_PATH = os.environ.get("CHROME_EXECUTABLE_PATH")

if not CHROME_EXECUTABLE_PATH:
    if current_os == "Windows":
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
    print(f"Found Chrome executable (might be used by Playwright): {CHROME_EXECUTABLE_PATH}")
else:
    # This might not be strictly necessary if Playwright uses its own downloaded browsers,
    # but keeping the check as a potential fallback or info point.
    print("Warning: System Chrome executable path not found or set. Playwright will use its own browser.")
# --- End OS-dependent Chrome Path Configuration ---

async def uc4(argv=None):
    print("Running Use Case 4 (Google Login with Agent using sensitive_data)...")
    print("This use case will launch its own browser instance.")

    # Get sensitive data from environment variables
    google_id = os.environ.get("GOOGLE_ID")
    google_password = os.environ.get("GOOGLE_PASSWORD")

    if not google_id or not google_password:
        print("Error: GOOGLE_ID and GOOGLE_PASSWORD environment variables must be set.")
        return # Exit the function if credentials are not set

    sensitive_data = {
        "google_login_id": google_id,
        "google_login_password": google_password
    }
    print("Loaded Google credentials from environment variables.")

    # Restrict the browser from accessing other domains
    allowed_domains=[
        "accounts.google.com",
        "mail.google.com",
        "drive.google.com",
        "workspace.google.com"
        "gmail.com",
    ]

    # Specify the Ollama model name
    model_name = MODEL_NAME
    print(f"Attempting to connect to Ollama with model: {model_name}")

    # Initial action: Go to Google Sign-in page
    initial_actions = [
    	{'open_tab': {'url': 'https://mail.google.com'}},
    	# {'open_tab': {'url': 'https://drive.google.com'}},
    ]

    # Define the task for the Agent
    formatted_task = f"Complete the Google login using the provided sensitive data of id({google_id}). After logging in, confirm you see the inbox of gmail."
    formatted_task += f"Then, navigate to google drive and find recent files. Save the file names to a text file."
    print(f"Task for Agent: {formatted_task}")

    # Load context cookies (optional)
    # Initialize BrowserContextConfig with allowed_domains
    context_config = BrowserContextConfig(
        allowed_domains=allowed_domains,
        save_downloads_path=os.path.join(os.path.expanduser('~'), 'downloads'),
    )
    if COOKIES_FILE_PATH.exists():
        try:
            with open(COOKIES_FILE_PATH, "r") as f:
                loaded_cookies = json.load(f)
                # Re-initialize with cookies and allowed_domains
                context_config = BrowserContextConfig(
                    cookies=loaded_cookies,
                    allowed_domains=allowed_domains,
                    save_downloads_path=os.path.join(os.path.expanduser('~'), 'downloads'),
                )
            print(f"Loaded cookies from {COOKIES_FILE_PATH}")
        except Exception as e:
            print(f"Warning: Failed to load {COOKIES_FILE_PATH}: {e}")

    browser = None

    try:
        # Ollama model
        llm = ChatOllama(
            model=model_name,
            num_ctx=8000,
            num_gpu=30,
            num_thread=8,
            verbose=False
        )

        # BrowserConfig & Browser - No cdp_url provided
        # Agent will instruct Playwright to launch a new browser instance.
        print("Configuring browser to be launched by the agent with context restrictions...")
        browser_cfg = BrowserConfig(
            headless=False,
            new_context_config=context_config,
            # chrome_instance_path=CHROME_EXECUTABLE_PATH if CHROME_EXECUTABLE_PATH else None, # Optionally provide path
        )
        # Browser instance will be created when Agent needs it or explicitly started
        browser = Browser(config=browser_cfg)

        # Agent with sensitive data and initial actions
        agent = Agent(
            task=formatted_task,
            llm=llm,
            browser=browser, # Pass the browser instance (not started yet)
            sensitive_data=sensitive_data,
            initial_actions=initial_actions,
            max_actions_per_step=3,
        )

        print(f"Invoking agent for Google Login using Ollama ({model_name})...")
        # The agent will handle browser startup when run is called
        result = await agent.run(max_steps=MAX_STEPS)
        print("Agent Result:")
        print(result)

        # Optional: Save cookies after successful run
        # try:
        #     current_cookies = await browser.context.cookies()
        #     with open(COOKIES_FILE_PATH, "w") as f:
        #         json.dump(current_cookies, f, indent=2)
        #     print(f"Saved cookies to {COOKIES_FILE_PATH}")
        # except Exception as e_cookie:
        #     print(f"Could not save cookies: {e_cookie}")

    except Exception as e:
        print(f"An error occurred during UC4 execution: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Closing browser...")
        if browser:
            try:
                await browser.close() # This should close the browser launched by Playwright
                print("Browser closed.")
            except Exception as e_close:
                print(f"Error closing browser: {e_close}")

# Example of how to run this specific async function if needed for testing
# if __name__ == '__main__':
#     # Set environment variables before running for standalone test
#     # os.environ['GOOGLE_ID'] = 'your_test_id'
#     # os.environ['GOOGLE_PASSWORD'] = 'your_test_password'
#     asyncio.run(uc4())