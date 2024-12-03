import os
from typing import List, Dict, Optional, Union, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain_community.document_loaders import DataFrameLoader
from langchain.docstore.document import Document
import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import logging
import ollama

class ContentParser:
    def __init__(self, model_name: str = "llama3.2"):
        """Initialize the ContentParser with specified model and embeddings."""
        self.model_name = model_name
        self.llm = Ollama(model=model_name)
        self.embeddings = HuggingFaceEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
    def _create_vectorstore(self, texts: List[str]) -> Chroma:
        """Create a vector store from the provided texts."""
        docs = self.text_splitter.create_documents(texts)
        return Chroma.from_documents(docs, self.embeddings)
    
    def _create_chain(self, template: str) -> LLMChain:
        """Create a LangChain chain with the specified template."""
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=template
        )
        return LLMChain(llm=self.llm, prompt=prompt)

    def analyze_content(self, data: Union[str, List[str]], task: str = "analyze", 
                       options: Optional[str] = None) -> str:
        """
        Analyze content using LangChain and vector store for better context handling.
        """
        # Convert input to list if string
        texts = [data] if isinstance(data, str) else data
        
        # Create vector store
        vectorstore = self._create_vectorstore(texts)
        
        # Generate task-specific template
        template = self._get_task_template(task)
        
        # Create chain
        chain = self._create_chain(template)
        
        # Get relevant context
        context = self._get_relevant_context(vectorstore, task, options)
        
        try:
            # Run chain
            response = chain.run(context=context, question=options if options else task)
            return response
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")
            return "Error occurred during analysis."

    def _get_task_template(self, task: str) -> str:
        """Get task-specific prompt template."""
        templates = {
            "analyze": """
            You are analyzing web content. Use the following context to provide insights:
            
            Context: {context}
            
            Question: {question}
            
            Provide a detailed analysis focusing on key patterns and insights.
            """,
            
            "summarize": """
            Summarize the following content concisely:
            
            Context: {context}
            
            Question: {question}
            
            Provide a clear and concise summary.
            """,
            
            "identify selectors": """
            Analyze the following HTML to identify CSS selectors:
            
            Context: {context}
            
            Requirements: {question}
            
            Identify and explain the most relevant CSS selectors.
            """,
            
            "extract": """
            Extract specific information from the following content:
            
            Context: {context}
            
            Requirements: {question}
            
            Provide the extracted information in a structured format.
            """
        }
        
        return templates.get(task, templates["analyze"])

    def _get_relevant_context(self, vectorstore: Chroma, task: str, 
                            options: Optional[str] = None) -> str:
        """Get relevant context from vector store based on task and options."""
        query = options if options else task
        docs = vectorstore.similarity_search(query, k=3)
        return "\n\n".join(doc.page_content for doc in docs)

    def extract_structured_data(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract structured data from content using LangChain.
        """
        template = """
        Extract structured information from the following content:
        
        Content: {context}
        
        Extract the following information:
        - Main topic or title
        - Key points or facts
        - Dates and numbers
        - Named entities (people, organizations, locations)
        - Any relevant metadata
        
        Format the output as a structured summary.
        """
        
        chain = self._create_chain(template)
        
        try:
            # Convert content dict to string
            content_str = "\n".join(f"{k}: {v}" for k, v in content.items())
            
            # Get structured analysis
            result = chain.run(context=content_str, question="")
            
            # Parse the result into a structured format
            # This is a simple implementation - you might want to add more sophisticated parsing
            structured_data = {
                "content": content,
                "analysis": result,
                "metadata": {
                    "model": self.model_name,
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            return structured_data
            
        except Exception as e:
            st.error(f"Error extracting structured data: {str(e)}")
            return {"error": str(e)}

class DataAnalyzer:
    def __init__(
        self, 
        model: str = 'llama3.2', 
        embedding_model: str = 'sentence-transformers/all-mpnet-base-v2'
    ):
        """
        Initialize DataAnalyzer with AI model and embedding configuration
        
        :param model: AI model for analysis
        :param embedding_model: Embedding model for vector representation
        """
        self.logger = logging.getLogger(__name__)
        self.model = model
        self.embedding_model = HuggingFaceEmbeddings(model_name=embedding_model)
        
        # Configure text splitting
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
    
    def _prepare_documents(self, data: Union[pd.DataFrame, str]) -> list:
        """
        Prepare documents for vector store
        
        :param data: Input data to be processed
        :return: List of prepared documents
        """
        if isinstance(data, pd.DataFrame):
            # Combine all text columns
            text = ' '.join(data.apply(lambda row: ' '.join(row.astype(str)), axis=1))
        elif isinstance(data, str):
            text = data
        else:
            raise ValueError("Unsupported data type. Use DataFrame or string.")
        
        # Split text into chunks
        return self.text_splitter.split_text(text)
    
    def analyze_dataset(
        self, 
        data: Union[pd.DataFrame, str], 
        analysis_type: str = 'summary', 
        custom_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze dataset using AI
        
        :param data: Dataset to analyze
        :param analysis_type: Type of analysis (summary, technical, custom)
        :param custom_prompt: Optional custom analysis prompt
        :return: Analysis results
        """
        try:
            # Prepare documents
            documents = self._prepare_documents(data)
            
            # Create vector store
            vectorstore = Chroma.from_texts(
                documents, 
                embedding=self.embedding_model
            )
            
            # Select prompt based on analysis type
            prompts = {
                'summary': "Provide a concise summary of the key insights from this text.",
                'technical': "Perform a detailed technical analysis of the content, highlighting key technical aspects.",
                'custom': custom_prompt or "Analyze the text comprehensively."
            }
            
            prompt = prompts.get(analysis_type.lower(), prompts['summary'])
            
            # Generate AI analysis
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'system', 
                        'content': 'You are an expert data analyst and AI assistant.'
                    },
                    {
                        'role': 'user', 
                        'content': f"{prompt}\n\nContext:\n{' '.join(documents[:5])}"
                    }
                ]
            )
            
            return {
                'analysis_type': analysis_type,
                'summary': response['message']['content'],
                'document_count': len(documents),
                'vector_store_size': len(vectorstore._collection.get())
            }
        
        except Exception as e:
            self.logger.error(f"Analysis error: {e}")
            raise

    def export_data(self, data: Union[pd.DataFrame, List[Dict]], 
                   format_type: str,
                   filename: str) -> str:
        """Export data in various formats."""
        try:
            df = pd.DataFrame(data) if isinstance(data, list) else data
            
            if format_type == "csv":
                df.to_csv(filename, index=False)
            elif format_type == "excel":
                df.to_excel(filename, index=False)
            elif format_type == "json":
                df.to_json(filename, orient="records", indent=2)
            elif format_type == "sql":
                # Generate SQL create and insert statements
                table_name = os.path.splitext(os.path.basename(filename))[0]
                sql_statements = []
                
                # Create table statement
                columns = []
                for col, dtype in df.dtypes.items():
                    sql_type = "TEXT"  # Default type
                    if np.issubdtype(dtype, np.number):
                        sql_type = "NUMERIC"
                    elif np.issubdtype(dtype, np.datetime64):
                        sql_type = "DATETIME"
                    columns.append(f"{col} {sql_type}")
                
                create_stmt = f"CREATE TABLE {table_name} (\n  "
                create_stmt += ",\n  ".join(columns)
                create_stmt += "\n);"
                sql_statements.append(create_stmt)
                
                # Insert statements
                for _, row in df.iterrows():
                    values = []
                    for val in row:
                        if pd.isna(val):
                            values.append("NULL")
                        elif isinstance(val, (int, float)):
                            values.append(str(val))
                        else:
                            values.append(f"'{str(val)}'")
                    
                    insert_stmt = f"INSERT INTO {table_name} VALUES ({', '.join(values)});"
                    sql_statements.append(insert_stmt)
                
                with open(filename, 'w') as f:
                    f.write("\n".join(sql_statements))
            else:
                raise ValueError(f"Unsupported export format: {format_type}")
            
            return filename
        except Exception as e:
            logging.error(f"Error exporting data: {e}")
            raise

# For backward compatibility
def ai_parse_content(data, task="analyze", options=None):
    """Legacy function for backward compatibility."""
    parser = ContentParser()
    return parser.analyze_content(data, task, options)
