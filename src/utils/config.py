import os
import yaml
from typing import Any, Dict, Optional

class ConfigManager:
    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_path: Optional[str] = None):
        if not self._config:
            self.load_config(config_path)

    def load_config(self, config_path: Optional[str] = None):
        """
        Load configuration from YAML file
        
        Args:
            config_path (Optional[str]): Path to config file. 
                                         Defaults to production config if not specified.
        """
        if not config_path:
            # Determine environment and select appropriate config
            env = os.environ.get('ENV', 'production').lower()
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                'config', 
                f'{env}.yml'
            )

        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                self._config = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Warning: Config file not found at {config_path}. Using default settings.")
            self._config = {}
        except yaml.YAMLError as e:
            print(f"Error parsing config file: {e}")
            self._config = {}

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by dot-separated key
        
        Args:
            key (str): Dot-separated configuration key
            default (Any, optional): Default value if key not found
        
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, {})
            else:
                return default
        
        return value if value != {} else default

    def get_language_text(self, section: str, key: str, lang: Optional[str] = None) -> str:
        """
        Get localized text for a specific section and key
        
        Args:
            section (str): Section in translations (e.g., 'ui')
            key (str): Specific text key
            lang (Optional[str]): Language code. Defaults to system language.
        
        Returns:
            Localized text string
        """
        # Default to Arabic if not specified
        if not lang:
            lang = self.get('app.languages.default', 'ar')
        
        # Ensure language is supported
        if lang not in self.get('app.languages.available', ['ar', 'en']):
            lang = 'ar'
        
        translations = self.get(f'{section}.translations.{lang}', {})
        return translations.get(key, key)

    def is_rtl(self, lang: Optional[str] = None) -> bool:
        """
        Check if the language is Right-to-Left
        
        Args:
            lang (Optional[str]): Language code
        
        Returns:
            bool: True if language is RTL, False otherwise
        """
        if not lang:
            lang = self.get('app.languages.default', 'ar')
        
        return self.get(f'ui.directions.{lang}', 'rtl') == 'rtl'

    def get_font(self, lang: Optional[str] = None) -> str:
        """
        Get the appropriate font for a language
        
        Args:
            lang (Optional[str]): Language code
        
        Returns:
            str: Font name
        """
        if not lang:
            lang = self.get('app.languages.default', 'ar')
        
        return self.get(f'ui.fonts.{lang}', 'Cairo' if lang == 'ar' else 'Inter')

# Global configuration instance
config = ConfigManager()
