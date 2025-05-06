from langchain_community.llms.ctransformers import CTransformers
from langchain.prompts import PromptTemplate

def main():
    prompt = PromptTemplate.from_template("A {word} is a")

    # Note: You might need to specify the model_type explicitly if auto-detection fails.
    # Common types include 'llama', 'gptq', etc. depending on the model architecture.
    # Check ctransformers documentation for supported types.
    llm = CTransformers(
        model="TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
        model_type='llama',  # Explicitly set model type: 'llama', 'gpt2', 'falcon', 'mistral', 'gptj', 'gptq', 'bert', 'starchat'
        # config={'max_new_tokens': 150} # Example configuration
    )

    chain = prompt | llm

    result = chain.invoke({"word": "tomato"})
    print(result) # Print the result to see the output

if __name__ == "__main__":
    main()

