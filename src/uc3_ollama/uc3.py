from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate

# Function signature updated for consistency, though argv is not used currently
def uc3(argv=None):
    print("Running Use Case 3 (Ollama)...")

    # --- LangChain Ollama Integration --- 

    # Specify the model name served by your local Ollama instance
    # Make sure this model is pulled (e.g., 'ollama run ...')
    # Use the exact name as shown in 'ollama list'
    model_name = "hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF:latest"
    print(f"Attempting to connect to Ollama with model: {model_name}")

    prompt = PromptTemplate.from_template("A {word} is a")

    try:
        # Initialize Ollama using the new class name
        # Assumes Ollama server is running on http://localhost:11434
        # You can specify base_url if it's different
        llm = OllamaLLM(
            model=model_name,
            # Optional: Add parameters like temperature, top_p, etc.
            # temperature=0.7
        )

        chain = prompt | llm

        print(f"Invoking chain with word 'tomato' using Ollama ({model_name})...")
        result = chain.invoke({"word": "tomato"})
        print("\nResult:")
        print(result)

    except Exception as e:
        print(f"Error initializing or running Ollama: {e}")
        print(f"Please ensure the Ollama server is running and the model '{model_name}' is available.  (e.g., run 'ollama serve' if needed)")
