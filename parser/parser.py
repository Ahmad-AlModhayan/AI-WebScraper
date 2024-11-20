from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
import os

def ai_parse_content(content: str, parse_description: str) -> str:
    """
    Parses HTML content using AI to extract specific information.

    Args:
        content (str): A chunk of HTML content to parse.
        parse_description (str): Description of the parsing task.

    Returns:
        str: Parsed result from AI.
    """
    model_name = os.getenv("OLLAMA_MODEL", "llama3.2")

    try:
        llm = OllamaLLM(model=model_name)
        prompt = ChatPromptTemplate.from_template(
            "Extract information as described:\n"
            "Content: {dom_content}\n"
            "Task: {parse_description}\n"
            "Output the result in plain text format only."
        )
        response = llm.invoke(
            prompt.format(dom_content=content, parse_description=parse_description)
        )
        return response.strip() if response else "No meaningful response from AI."
    except Exception as e:
        return f"Error in AI Parsing: {str(e)}"
