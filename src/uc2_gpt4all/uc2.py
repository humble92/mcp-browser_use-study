from langchain_community.llms import GPT4All  # Updated import path
from langchain.prompts import PromptTemplate
import os # To construct the model path relative to this file

def uc2(argv=None):
    print("Running Use Case 2 (GPT4All)...")

    # Assuming the model file is relative to this script's directory
    # current_dir = os.path.dirname(__file__)
    # model_path = os.path.join(current_dir, "falcon.bin")

    # --- Alternative: Use a model name GPT4All can download --- 
    # Example: Use a known downloadable model name instead of a local path
    # model_path = "DeepSeek-R1-Distill-Llama-8B-Q4_0" # Using downloadable name instead of local path for better portability
    model_path = r"C:\Users\daniel.hwang\AppData\Local\nomic.ai\GPT4All\DeepSeek-R1-Distill-Llama-8B-Q4_0.gguf"
    print(f"Attempting to load GPT4All model: {model_path}")
    # Check if the model file exists if using a relative path
    # if not os.path.exists(model_path):
    #     print(f"Error: Model file not found at {model_path}")
    #     print("Please make sure the model file exists or specify a downloadable model name.")
    #     return

    prompt = PromptTemplate.from_template("A {word} is a")

    try:
        llm = GPT4All(
            model=model_path, # Use the specified model name/path
            # Optional: Add other GPT4All parameters like n_threads, temp, etc.
            # verbose=True, # Enable verbose logging if needed
        )

        chain = prompt | llm

        print(f"Invoking chain with word 'tomato' using GPT4All...")
        result = chain.invoke({"word": "tomato"})
        print("\nResult:")
        print(result)

    except Exception as e:
        print(f"Error initializing or running GPT4All: {e}")
        print("Ensure the model name is correct and the model file is downloadable or exists at the specified path.")
        print("You might need to install the gpt4all package dependencies: pip install gpt4all")
