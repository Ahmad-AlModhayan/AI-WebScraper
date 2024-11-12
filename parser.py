# parser.py
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Define Ollama model
model = OllamaLLM(model="llama3.2")

# Define a prompt template for parsing content
template = (
    "Extract information based on the following prompt: {parse_description} "
    "from the content provided: {dom_content}. Only return the relevant details."
)

def ai_parse_content(content, parse_description):
    # Create a template and pass in description and content
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    
    # Invoke the model on the given content
    response = chain.invoke({"dom_content": content, "parse_description": parse_description})
    return response.strip() if response else "No response."
