from langchain_ollama import ChatOllama
from browser_use import Agent


# Function signature updated for consistency and async
async def uc3(argv=None):
    print("Running Use Case 3 (Ollama with Agent)...")

    # Specify the Ollama model name which supports tool-calling
    # Make sure this model is pulled (e.g., 'ollama pull qwen2.5-coder')
    # model_name = "qwen2.5-coder"
    model_name = "hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF:latest"
    print(f"Attempting to connect to Ollama with model: {model_name}")

    # Define the task for the Agent, assuming it can be a template string
    task_template = "Search a picture of {word} and save it to the file {filename}" 
    input_variables = {"word": "tomato", "filename": "tomato.png"}
    
    # Format the task string with the input variables
    formatted_task = task_template.format(**input_variables)
    print(f"Formatted task for Agent: {formatted_task}") # Log the formatted task

    try:
        # Initialize the ChatOllama model
        llm = ChatOllama(
            model=model_name,
            num_ctx=32000
            # Optional: Add other parameters like temperature, top_p, etc.
            # temperature=0.7
        )

        # Create agent with the fully formatted task string
        agent = Agent(
            task=formatted_task, # Pass the formatted task
            llm=llm
        )

        print(f"Invoking agent with pre-formatted task using Ollama ({model_name})...")
        # Call agent.run() without the input dictionary, 
        # as inputs are now part of the formatted_task.
        # max_steps will default to 100 unless specified.
        result = await agent.run()
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
