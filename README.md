# AI Web Scraper 🌐🤖

## Overview
AI Web Scraper is an advanced, multilingual web scraping tool powered by AI, designed to extract and analyze web content with intelligent capabilities.

## 🌟 Features
- Multilingual Support (Arabic & English)
- AI-Powered Content Analysis
- Dynamic Web Scraping
- Configurable Extraction Strategies
- Advanced Error Handling
- Secure and Scalable Architecture

## 🛠 Technology Stack
- Python 3.10+
- Streamlit
- Ollama
- Sentence Transformers
- LangChain
- Docker

## 📦 Prerequisites
- Docker
- Docker Compose
- Python 3.10+

## 🚀 Quick Start

### Local Development
```bash
# Clone the repository
git clone https://github.com/Ahmad-AlModhayan/AI-WebScraper.git
cd AI-WebScraper

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run src/app.py
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build

# Access the application
# Open http://localhost:8501 in your browser
```

## 🔧 Configuration
- `config/production.yml`: Production settings
- `config/development.yml`: Development environment configurations
- Supports dynamic language switching
- Configurable AI models and scraping parameters

## 📊 Project Structure
```
AI-WebScraper/
│
├── config/                 # Configuration files
├── data/                   # Data storage
├── docs/                   # Documentation
├── logs/                   # Application logs
├── scripts/                # Utility scripts
├── src/                    # Source code
│   ├── core/               # Core scraping logic
│   ├── ui/                 # User interface
│   ├── utils/              # Utility modules
│   └── app.py              # Main application
├── tests/                  # Unit and integration tests
├── dockerfile              # Docker configuration
├── docker-compose.yml      # Multi-container orchestration
└── requirements.txt        # Python dependencies
```

## 🌐 Multilingual Support
- Default Language: Arabic
- Supported Languages: Arabic, English
- RTL/LTR Layout Adaptation
- Dynamic Font Selection

## 🔒 Security Features
- Proxy Support
- User Agent Rotation
- Configurable Timeouts
- Secure Configuration Management

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📜 License
MIT License

## 🙏 Acknowledgements
- Ollama AI
- Streamlit
- LangChain Community
