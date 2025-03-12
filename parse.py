from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


template = (
    "You are an AI assistant tasked with analyzing the following text:\n\n"
    "{dom_content}\n\n"
    "### Instructions:\n"
    "1. **Extract & Expand:** Identify relevant information based on this description: {parse_description}.\n"
    "2. **Provide Context:** Include supporting details where necessary to ensure clarity.\n"
    "3. **Detailed & Complete Answer:** Ensure your response is comprehensive, well-structured, and easy to understand.\n"
)



model = OllamaLLM(model="gemma:2b", max_tokens=1024)

def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    
    parsed_results = [];
    
    for i, chunk in enumerate(dom_chunks, start = 1):
        response = chain.invoke({"dom_content": chunk, "parse_description": parse_description})
        print(f"Parsed batch {i} of {len(dom_chunks)}")
        parsed_results.append(response)
        
    return "\n".join(parsed_results)