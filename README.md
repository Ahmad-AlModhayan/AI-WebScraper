# AI Web Scraper Pro 🌐

## Overview
AI Web Scraper Pro is an advanced web scraping and data analysis tool powered by AI technologies. It provides intelligent web content extraction, analysis, and insights generation.

## 🚀 Features
- 🔍 Advanced Web Scraping
- 📊 AI-Powered Data Analysis
- 🤖 Llama 3.2 Model Integration
- 📈 Flexible Configuration
- 🔒 Secure and Robust

## 🛠 Technologies
- Python 3.10+
- Streamlit
- Selenium
- LangChain
- Ollama
- ChromaDB
- Sentence Transformers

## 📦 Prerequisites
- Docker
- Docker Compose
- Ollama (optional, but recommended)

## 🚀 Quick Start

### Local Development
1. Clone the repository
```bash
git clone https://github.com/yourusername/ai-web-scraper-pro.git
cd ai-web-scraper-pro
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
streamlit run src/app.py
```

### Docker Deployment
1. Build and run with Docker Compose
```bash
docker-compose up --build
```

2. Access the application
- URL: `http://localhost:8501`

## 🔧 Configuration
Customize your deployment using configuration files:
- `config/development.yml`
- `config/production.yml`

## 🔬 Environment Variables
- `ENV`: Set environment (`development`/`production`)
- `OLLAMA_MODEL`: Specify AI model

## 📋 Project Structure
```
ai-web-scraper-pro/
│
├── src/
│   ├── core/          # Scraping and analysis logic
│   ├── ui/            # User interface components
│   └── utils/         # Configuration and logging
│
├── config/            # Environment configurations
├── data/              # Data storage
├── docs/              # Documentation
└── tests/             # Testing infrastructure
```

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License
MIT License

## 🌟 Support
Star the project, open issues, or submit pull requests!
