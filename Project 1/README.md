# URL Credibility Checker AI Chatbot

An **intelligent Streamlit chatbot** that analyzes URL credibility using machine learning, domain reputation analysis, and conversational AI. Now with natural language understanding, multi-URL comparison, and educational capabilities!

## 🆕 New Features

- 💬 **Natural Conversations**: Chat naturally with greetings, questions, and follow-ups
- 📊 **Multi-URL Comparison**: Analyze and compare multiple sources side-by-side
- 🎓 **Educational Mode**: Learn about credibility, fact-checking, and information literacy
- 🧠 **Context Memory**: Remembers your session history and previous analyses
- 📈 **Session Statistics**: Track your analysis history and credibility rates
- 🤖 **Intent Detection**: Automatically understands what you're asking for

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

`streamlit run app.py`

The app will open in your browser at `http://localhost:8501`

***Task Kill***
`Get-NetTCPConnection -LocalPort 8501 | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force}`

### Example Interactions

**Analyze a single URL:**
```
User: Check https://www.nature.com
Bot: [Analyzes and shows credibility score]
```

**Compare multiple URLs:**
```
User: Compare cdc.gov vs example.com
Bot: [Shows side-by-side comparison with rankings]
```

**Ask educational questions:**
```
User: How do you score URLs?
Bot: [Explains methodology in detail]

User: What makes a source credible?
Bot: [Provides educational content]
```

**Natural conversation:**
```
User: Hello!
Bot: [Friendly greeting with instructions]

User: Thanks!
Bot: [Acknowledgment]
```

**Follow-up questions:**
```
User: Why did that site get a low score?
Bot: [Explains the previous analysis in detail]
```

### Running CLI Version

```powershell
python deliverable1-3.py
```

## Project Structure

```
Project 1/
├── app.py                    # Enhanced Streamlit chatbot with conversational AI
├── conversational_ai.py      # Intent detection and conversational responses
├── deliverable1_3.py         # Optimized credibility analysis module
├── deliverable1.py           # Original implementation (DO NOT MODIFY)
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## How It Works

### Conversational AI Layer

The bot uses **rule-based intent detection** (100% free, no API keys) to understand:
- **Analyze**: URLs to check for credibility
- **Compare**: Multiple URLs to rank by credibility  
- **Educate**: Questions about methodology and credibility
- **Chat**: Greetings, thanks, and general conversation
- **Follow-up**: Questions about previous analyses

### Credibility Analysis

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
