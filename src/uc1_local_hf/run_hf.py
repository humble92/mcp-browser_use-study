from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.prompts import PromptTemplate

def main():
    prompt = PromptTemplate.from_template("A {word} is a")

    llm = HuggingFacePipeline.from_model_id(
        # model_id="google/gemma-3-1b-it",
        model_id="distilbert/distilgpt2",
        task="text-generation",
        # device=-1,
        # pipeline_kwargs={"max_new_tokens": 150},
    )

    chain = prompt | llm

    result = chain.invoke({"word": "tomato"})
    print(result)

if __name__ == "__main__":
    main()

