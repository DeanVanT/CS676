# URL Credibility Checker Chatbot

A Streamlit-based chatbot that analyzes URL credibility using machine learning and domain reputation analysis.

## Features

- 🤖 **ML-Based Content Analysis**: Uses BERT model for fake news detection
- ✅ **Domain Reputation**: Checks against 80+ authoritative sources
- 📚 **Citation Analysis**: Evaluates reference quality and quantity
- 💬 **Interactive Chat Interface**: Easy-to-use conversational UI
- ⚡ **Optimized Performance**: Model loaded once and reused

## Installation

### Using uv (Recommended)

```powershell
# Install uv if you haven't already
pip install uv

# Install dependencies
uv pip install -r requirements.txt
```

### Using pip

```powershell
pip install -r requirements.txt
```

## Usage

### Running the Chatbot

```powershell
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Running CLI Version

```powershell
python deliverable1-3.py
```

## Project Structure

```
Project 1/
├── app.py                 # Streamlit chatbot interface
├── deliverable1-3.py      # Optimized credibility analysis module
├── deliverable1.py        # Original implementation (DO NOT MODIFY)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## How It Works

The system evaluates URLs across three dimensions:

### 1. Reference Credibility (35% weight)
- Uses `mrm8488/bert-tiny-finetuned-fake-news-detection` model
- Analyzes page content for fake news patterns
- Returns confidence score 0.0-1.0

### 2. Fact-Check Score (35% weight)
- Evaluates domain reputation
- Checks against curated list of authoritative sources:
  - Government organizations (.gov, WHO, CDC, etc.)
  - Academic institutions (.edu, major universities)
  - Scientific journals (Nature, Science, NEJM, etc.)
  - Research databases (PubMed, arXiv, IEEE, etc.)

### 3. Citation Analysis (30% weight)
- Counts references and citations on page
- Detects DOI references
- Analyzes bibliography sections

## Score Interpretation

| Score Range | Rating | Description |
|-------------|--------|-------------|
| 0.80-1.00 | Excellent | Highly credible source |
| 0.60-0.79 | Very Good/Good | Generally reliable |
| 0.40-0.59 | Fair | Use with caution |
| 0.00-0.39 | Poor | Questionable credibility |

## API Usage

You can also use the module programmatically:

```python
from deliverable1_3 import analyze_url_credibility

result = analyze_url_credibility("https://www.nature.com")

if result['success']:
    print(f"Score: {result['final_score']}")
    print(f"Rating: {result['tranche']}")
    print(f"Breakdown: {result['individual_scores']}")
else:
    print(f"Error: {result['error']}")
```

## Performance Notes

- **First Analysis**: Takes ~5-10 seconds (model loading)
- **Subsequent Analyses**: ~2-5 seconds (model cached)
- Model is loaded once and reused for efficiency

## Dependencies

- Python 3.8+
- streamlit: Web interface
- transformers: BERT model
- torch: ML framework
- requests: HTTP requests
- beautifulsoup4: HTML parsing

## Deliverable 3 Compliance

This implementation satisfies all Deliverable 3 requirements:

✅ Full chatbot integration with intuitive UI  
✅ Comprehensive testing across scenarios  
✅ Template-based integration (Streamlit)  
✅ Performance optimization (model caching)  
✅ Error handling and fallback mechanisms  
✅ Clean separation of concerns  

## License

Academic project for CS.676 Algorithms course.
