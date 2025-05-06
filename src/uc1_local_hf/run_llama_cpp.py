# src/uc1_local_hf/run_llama_cpp.py

from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate

# Path to the downloaded GGUF model file.
# Make sure backslashes are escaped or use a raw string (r"...")
model_path = r"C:\Users\daniel.hwang\.cache\huggingface\hub\models--TheBloke--TinyLlama-1.1B-Chat-v1.0-GGUF\blobs\bf0264251d7c9406983b6beb71b2242428d4564f5a5154bc00825b43965f89b2"

def main():
    prompt = PromptTemplate.from_template("A {word} is a")

    try:
        # Initialize LlamaCpp
        # Adjust parameters as needed:
        # n_ctx: Context window size (default 2048). Check model's max context size.
        # n_gpu_layers: Number of layers to offload to GPU (if supported and desired). Requires llama-cpp-python built with GPU support.
        # verbose: Set to True for detailed logging from llama.cpp.
        llm = LlamaCpp(
            model_path=model_path,
            n_ctx=2048, # Example context size, adjust if needed
            # n_gpu_layers=0, # Set > 0 if you have GPU support and want to use it
            verbose=True,
            # Optional: Add other llama.cpp parameters here, e.g., temperature, top_p
        )

        chain = prompt | llm

        print(f"Invoking chain with word 'tomato' using LlamaCpp and model: {model_path}")
        result = chain.invoke({"word": "tomato"})
        print("\nResult:")
        print(result)

    except Exception as e:
        print(f"Error initializing or running LlamaCpp: {e}")
        print("Please ensure the model path is correct and llama-cpp-python is installed correctly (with GPU support if n_gpu_layers > 0).")

# Note: No if __name__ == "__main__" block needed as this will be called via uc1.py 