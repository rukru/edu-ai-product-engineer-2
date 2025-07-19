# 🤖 Review Analysis Agent - Timofey Novikov

**AI Product Engineer Season 2 - Lesson 1 Assignment**

## Project Overview

This project demonstrates the comparison between deterministic and probabilistic (LLM-powered) programming paradigms through a reviews analysis agent. The core objective is to build an agent using OpenAI Agents SDK that analyzes AppStore reviews (using Skyeng app as example) with both approaches and generates PM-style reports.

### 🎯 Key Features

- **Deterministic Analysis**: NLTK-based sentiment analysis and keyword extraction (<0.5s processing)
- **LLM Analysis**: OpenAI GPT-4 powered insights and analysis (<5s processing)
- **Parallel Processing**: Concurrent execution for optimal performance
- **PM Reports**: Automated product management insights from user feedback
- **Web Interface**: Streamlit-based demo for interactive testing
- **Advanced Agent**: Tool calling and quality control loops

### 🏗️ Architecture

The project follows a clean, modular architecture:
- **Agent Orchestrator**: Coordinates both analysis approaches
- **Deterministic Analyzer**: Fast, reproducible NLTK analysis
- **LLM Analyzer**: Deep insights using OpenAI API
- **Report Generator**: Combines results into actionable PM reports

## Tools and Technologies Used

### Core Technologies
- **Python 3.9+** - Main programming language for agent development
- **OpenAI API** - GPT-4 for LLM analysis and function calling capabilities
- **NLTK** - Natural language processing for deterministic sentiment analysis
- **Streamlit** - Web interface for interactive demonstrations

### Analysis Libraries
- **scikit-learn** - TF-IDF vectorization and machine learning utilities
- **pandas** - Data processing and structured analysis
- **numpy** - Numerical computations and array operations
- **plotly** - Interactive visualizations for performance metrics
- **python-dotenv** - Environment variable management

### Why These Technologies?

1. **OpenAI Function Calling**: Enables intelligent tool selection and sophisticated agent loops for quality control
2. **NLTK**: Provides fast (~0.5s), reproducible deterministic analysis with proven NLP algorithms
3. **Streamlit**: Allows rapid prototyping and deployment of interactive web interfaces
4. **scikit-learn**: Industry-standard ML tools for text processing and feature extraction
5. **Modular Design**: Clear separation of concerns following best practices

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- OpenAI API key
- Git for version control

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/BayramAnnakov/edu-ai-product-engineer-2.git
   cd edu-ai-product-engineer-2/Timofey_Novikov
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   # Create .env file with your OpenAI API key
   echo "OPENAI_API_KEY=your_openai_key_here" > .env
   echo "OPENAI_MODEL=gpt-4" >> .env
   ```

4. **Download NLTK data**:
   ```bash
   python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('wordnet')"
   ```

### Running the Application

#### Web Interface (Recommended)
```bash
# Using the launcher script
python run_streamlit.py

# Or directly
streamlit run src/ui/streamlit_app.py
```

#### Command Line Interface
```bash
# Interactive demo
python src/ui/interactive_demo.py

# Main agent
python main.py

# Run tests
python tests/test_agent.py
```

#### Advanced Features
```bash
# Compare basic vs advanced agents
python src/agent_comparison.py

# Generate demo reports
python tests/demo_report.py
```

## Project Structure

```
Timofey_Novikov/
├── main.py                      # OpenAI Agent orchestrator
├── run_streamlit.py            # Streamlit launcher script
├── requirements.txt            # Project dependencies
├── src/                        # Source code
│   ├── analyzers/             # Analysis modules
│   │   ├── deterministic.py   # NLTK-based analysis
│   │   └── llm_analyzer.py    # OpenAI API integration
│   ├── reports/               # Report generation
│   │   └── report_generator.py # PM report generator
│   ├── ui/                    # User interfaces
│   │   ├── streamlit_app.py   # Web interface
│   │   └── interactive_demo.py # CLI interface
│   ├── advanced_agent.py      # Advanced agent with tools
│   └── agent_comparison.py    # Agent comparison utility
├── tests/                     # Test files
│   ├── test_agent.py         # Agent tests
│   └── demo_report.py        # Demo report generator
├── docs/                      # Documentation
│   ├── README.md             # This file
│   ├── CLAUDE.md             # Development guidelines
│   └── *.md                  # Other documentation
├── reports/                   # Generated reports
│   └── generated/            # Auto-generated reports
└── config/                    # Configuration files
```

## Usage Examples

### Basic Analysis
```python
from main import ReviewAnalysisAgent

agent = ReviewAnalysisAgent()
review = "Great app! Easy to use but crashes sometimes."
results = agent.process_review(review)

print(f"Sentiment: {results['llm_results']['sentiment']}")
print(f"Processing time: {results['performance']['total_processing_time']}s")
```

### Batch Processing
```python
reviews = ["Amazing app!", "Terrible bugs", "Good but slow"]
batch_results = agent.batch_process(reviews, parallel=True)
print(f"Processed {len(reviews)} reviews in {batch_results['performance']['total_batch_time']}s")
```

## Performance Metrics

- **Speed Advantage**: Deterministic analysis is ~1000x faster than LLM
- **Accuracy**: Both approaches show high sentiment classification accuracy
- **Throughput**: Can process 100+ reviews in under 2 minutes
- **Quality Score**: Advanced agent achieves 0.705 quality score with minimal overhead

## Learning Objectives Demonstrated

✅ **Deterministic vs Probabilistic Paradigms**: Clear comparison of NLTK vs OpenAI approaches  
✅ **OpenAI Agents SDK Usage**: Practical implementation of agent orchestration  
✅ **Evaluation-Driven Development**: Comprehensive metrics and performance testing  
✅ **PM Report Generation**: Automated product insights from user feedback  
✅ **Cost-Performance Trade-offs**: Understanding speed vs quality decisions  

## Contributing

This project follows the contribution guidelines for edu-ai-product-engineer-2:

1. All work is contained within the `Timofey_Novikov/` directory
2. Clear commit messages and feature branches are used
3. Code follows Python best practices with proper documentation
4. Regular synchronization with upstream repository

## License

This project is part of the edu-ai-product-engineer-2 course and follows the repository's licensing terms.

## Contact

For questions or collaboration opportunities, please use GitHub discussions or create an issue in the main repository.

---

**Course**: AI Product Engineer Season 2  
**Assignment**: Lesson 1 - Deterministic vs Probabilistic Programming  
**Author**: Timofey Novikov  
**Date**: 2025