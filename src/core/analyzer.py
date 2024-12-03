import os
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any

import torch
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
import ollama

from src.utils.config import config
from src.utils.logging import logger

class AIAnalyzer:
    def __init__(self, 
                 language: Optional[str] = None, 
                 model: Optional[str] = None):
        """
        Initialize AI Analyzer with multilingual support
        
        Args:
            language (Optional[str]): Language context for analysis
            model (Optional[str]): Specific AI model to use
        """
        # Language configuration
        self.language = language or config.get('app.languages.default', 'ar')
        
        # Model configuration
        self.model_name = model or config.get('analyzer.model', 'llama3.2')
        self.embedding_model_name = config.get('analyzer.embedding_model', 'sentence-transformers/all-mpnet-base-v2')
        
        # Chunk configuration
        self.chunk_size = config.get('analyzer.chunk_size', 2000)
        self.chunk_overlap = config.get('analyzer.chunk_overlap', 400)
        
        # Load models
        self._load_models()

    def _load_models(self):
        """
        Load AI models with multilingual support
        """
        try:
            # Embedding model
            self.embedding_model = SentenceTransformer(self.embedding_model_name)
            
            # Ensure Ollama model is available
            try:
                ollama.pull(self.model_name)
            except Exception as e:
                logger.warning(f"Could not pull Ollama model: {e}")
        
        except Exception as e:
            logger.error(f"Model loading error: {e} | خطأ في تحميل النماذج: {e}")
            raise

    def _chunk_text(self, text: str) -> List[str]:
        """
        Split text into manageable chunks
        
        Args:
            text (str): Input text to chunk
        
        Returns:
            List[str]: List of text chunks
        """
        # Multilingual chunk splitting
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0

        for word in words:
            current_chunk.append(word)
            current_length += len(word)

            if current_length >= self.chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = current_chunk[-int(self.chunk_overlap/2):]
                current_length = len(' '.join(current_chunk))

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks

    def _get_prompt(self, prompt_type: str) -> str:
        """
        Get localized prompt based on language and type
        
        Args:
            prompt_type (str): Type of prompt (summary, technical, custom)
        
        Returns:
            str: Localized prompt template
        """
        return config.get(f'analyzer.prompts.{self.language}.{prompt_type}', 
                          config.get(f'analyzer.prompts.en.{prompt_type}'))

    def summarize(self, file_or_text: Union[str, pd.DataFrame, pd.Series]) -> Dict[str, Any]:
        """
        Generate a summary of the input content
        
        Args:
            file_or_text (Union[str, pd.DataFrame, pd.Series]): Content to summarize
        
        Returns:
            Dict[str, Any]: Summary results
        """
        try:
            # Prepare text
            if isinstance(file_or_text, (pd.DataFrame, pd.Series)):
                text = ' '.join(file_or_text.astype(str))
            elif isinstance(file_or_text, str):
                text = file_or_text
            else:
                raise ValueError("Unsupported input type")

            # Chunk text
            chunks = self._chunk_text(text)

            # Prepare prompt
            prompt = self._get_prompt('summary')

            # Analyze using Ollama
            summaries = []
            for chunk in chunks:
                response = ollama.chat(model=self.model_name, messages=[
                    {'role': 'system', 'content': prompt},
                    {'role': 'user', 'content': chunk}
                ])
                summaries.append(response['message']['content'])

            # Combine summaries
            final_summary = ' '.join(summaries)

            return {
                'language': self.language,
                'summary_length': len(final_summary),
                'summary': final_summary
            }

        except Exception as e:
            logger.error(f"Summarization error: {e} | خطأ في التلخيص: {e}")
            raise

    def technical_analysis(self, file_or_text: Union[str, pd.DataFrame, pd.Series]) -> Dict[str, Any]:
        """
        Perform technical analysis of the content
        
        Args:
            file_or_text (Union[str, pd.DataFrame, pd.Series]): Content to analyze
        
        Returns:
            Dict[str, Any]: Technical analysis results
        """
        try:
            # Prepare text
            if isinstance(file_or_text, (pd.DataFrame, pd.Series)):
                text = ' '.join(file_or_text.astype(str))
            elif isinstance(file_or_text, str):
                text = file_or_text
            else:
                raise ValueError("Unsupported input type")

            # Chunk text
            chunks = self._chunk_text(text)

            # Prepare prompt
            prompt = self._get_prompt('technical')

            # Analyze using Ollama
            technical_insights = []
            for chunk in chunks:
                response = ollama.chat(model=self.model_name, messages=[
                    {'role': 'system', 'content': prompt},
                    {'role': 'user', 'content': chunk}
                ])
                technical_insights.append(response['message']['content'])

            # Combine insights
            final_insights = ' '.join(technical_insights)

            # Compute embeddings for key insights
            embeddings = self.embedding_model.encode(final_insights.split('.'))

            return {
                'language': self.language,
                'insights_length': len(final_insights),
                'technical_insights': final_insights,
                'embedding_dimensions': embeddings.shape[1]
            }

        except Exception as e:
            logger.error(f"Technical analysis error: {e} | خطأ في التحليل التقني: {e}")
            raise

    def custom_analysis(self, 
                        file_or_text: Union[str, pd.DataFrame, pd.Series], 
                        custom_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform custom analysis with user-provided prompt
        
        Args:
            file_or_text (Union[str, pd.DataFrame, pd.Series]): Content to analyze
            custom_prompt (Optional[str]): User-defined analysis prompt
        
        Returns:
            Dict[str, Any]: Custom analysis results
        """
        try:
            # Prepare text
            if isinstance(file_or_text, (pd.DataFrame, pd.Series)):
                text = ' '.join(file_or_text.astype(str))
            elif isinstance(file_or_text, str):
                text = file_or_text
            else:
                raise ValueError("Unsupported input type")

            # Use default prompt if not provided
            if not custom_prompt:
                custom_prompt = self._get_prompt('custom')

            # Chunk text
            chunks = self._chunk_text(text)

            # Analyze using Ollama
            custom_insights = []
            for chunk in chunks:
                response = ollama.chat(model=self.model_name, messages=[
                    {'role': 'system', 'content': custom_prompt},
                    {'role': 'user', 'content': chunk}
                ])
                custom_insights.append(response['message']['content'])

            # Combine insights
            final_insights = ' '.join(custom_insights)

            return {
                'language': self.language,
                'prompt': custom_prompt,
                'insights_length': len(final_insights),
                'custom_insights': final_insights
            }

        except Exception as e:
            logger.error(f"Custom analysis error: {e} | خطأ في التحليل المخصص: {e}")
            raise

    def export_results(self, 
                       results: Dict[str, Any], 
                       format: str = 'json') -> str:
        """
        Export analysis results in various formats
        
        Args:
            results (Dict[str, Any]): Analysis results
            format (str): Export format (json, csv, txt)
        
        Returns:
            str: Path to exported file
        """
        # Ensure export directory exists
        export_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'exports')
        os.makedirs(export_dir, exist_ok=True)
        
        # Generate filename
        timestamp = pd.Timestamp.now().strftime("%Y%m%d-%H%M%S")
        base_filename = f'analysis_results_{timestamp}'
        
        # Export based on format
        if format == 'json':
            filepath = os.path.join(export_dir, f'{base_filename}.json')
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
        elif format == 'csv':
            filepath = os.path.join(export_dir, f'{base_filename}.csv')
            df = pd.DataFrame.from_dict(results, orient='index').transpose()
            df.to_csv(filepath, index=False, encoding='utf-8')
        elif format == 'txt':
            filepath = os.path.join(export_dir, f'{base_filename}.txt')
            with open(filepath, 'w', encoding='utf-8') as f:
                for key, value in results.items():
                    f.write(f"{key}: {value}\n")
        else:
            raise ValueError(f"Unsupported export format: {format}")
        
        return filepath

def DataAnalyzer(*args, **kwargs):
    """
    Backward compatibility function for DataAnalyzer
    Redirects to AIAnalyzer with a deprecation warning
    """
    import warnings
    warnings.warn(
        "DataAnalyzer is deprecated. Use AIAnalyzer instead.", 
        DeprecationWarning, 
        stacklevel=2
    )
    return AIAnalyzer(*args, **kwargs)
