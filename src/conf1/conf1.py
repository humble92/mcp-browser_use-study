import asyncio, json
import pathlib # Import pathlib
from browser_use import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig

async def dump_cookies():
    # Configuration for the browser context
    context_config = BrowserContextConfig()

    # Configuration for the browser itself (defaults to headless=False)
    browser_config = BrowserConfig()

    browser = Browser(config=browser_config)
    active_context = None  # Initialize active_context to None
    
    try:
        # Create an explicit context for this operation
        active_context = BrowserContext(browser=browser, config=context_config)

        # This will open the browser page and prepare it for interaction
        # and returns the session object
        session = await active_context.get_session()

        # Construct the absolute path to the HTML file
        # Assuming conf1.py and conf1_instructions.html are in the same directory (src/conf1)
        html_file_path = pathlib.Path(__file__).parent / "conf1_instructions.html"
        await session.current_page.goto(f"file:///{html_file_path.resolve()}")

        print(f"→ Browser opened with instructions. Please follow them, then press Enter here to continue.")
        input()

        # Get cookies from the Playwright context within the session
        cookies = await session.context.cookies()
        with open("cookies.json", "w") as f:
            json.dump(cookies, f, indent=2)
        # Alternatively, if you want to dump the entire storage_state:
        # state = await session.context.storage_state()
        # with open("storage_state.json","w") as f: json.dump(state, f, indent=2)

        print("✅ cookies.json created successfully.")
    finally:
        if active_context:
            await active_context.close() # Explicitly close the context
        await browser.close() 