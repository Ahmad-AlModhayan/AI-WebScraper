import os
import yaml
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        # Determine environment
        env = os.getenv('ENV', 'development')
        
        # Load base configuration
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
            'config', 
            f'{env}.yml'
        )
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Override with environment variables
        self._override_with_env_vars()
    
    def _override_with_env_vars(self):
        """Override config with environment variables"""
        for key, value in os.environ.items():
            # Convert nested keys like SCRAPER_TIMEOUT to nested dict
            if '_' in key:
                parts = key.lower().split('_')
                current = self.config
                for part in parts[:-1]:
                    current = current.setdefault(part, {})
                current[parts[-1]] = self._parse_value(value)
    
    def _parse_value(self, value: str) -> Any:
        """Parse string values to appropriate types"""
        if value.lower() in ['true', 'yes', '1']:
            return True
        elif value.lower() in ['false', 'no', '0']:
            return False
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a configuration value"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value

# Singleton instance
config = ConfigManager()
