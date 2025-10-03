# Credibility Scoring: Technical Report (Brief)

## Overview
Using a hybrid approach. This scrip was a rebuild on the first pracital data science project. Improvments were implementing a user prompt for URL and a checker to validate website and incorporating a qualitative tranche and json type output as required by project instructions. 
* `evaluate_citations()` is mostly unchanged and just adds to hybrid model.   
* `evaluate_fact_check` was updated to include not just medical sites, but a more expansive list to cover a more generic URL credibility vs just a medical focused list.
* `evaluate_reference_credibility` Rebuilt cleaner, more robust, and correctly interprets model outputs. Comparison to V1 below:

## Differences

- Error handling:  
  - V1: One generic try/except.  
  - V2: Separate handling for init, fetch, and inference errors.

- Text extraction:  
  - V1: Uses `soup.get_text()` (messy, often includes junk).  
  - V2: Uses `stripped_strings` (clean, visible text only).

- HTTP requests:  
  - V1: No headers, short timeout.  
  - V2: Custom `User-Agent`, longer timeout — avoids blocks and timeouts.

- Model label handling:  
  - V1: Assumes class `1` is “reliable”.  
  - V2: Searches for `"REAL"` or `"TRUE"` in labels — works across different model configs.

- Scoring logic:  
  - V1: Arbitrary mix of base score + model output.  
  - V2: Returns actual model softmax probability.

- Output meaning:  
  - V1: Rough heuristic, partially hardcoded.  
  - V2: True confidence probability from the classifier.


## Algorithm & Rationale
- Combines ML (BERT-based fake news classifier) and rule-based heuristics.
- Features: domain authority, citation count, fact-check sources, content quality.
- Scoring: Weighted sum of component scores (credibility, fact check, citations).
- Decision thresholds: Scores mapped to tranches (Poor–Excellent).
- Complexity: Fast enough for real-time use; scalable to large datasets.

## Literature Review (Summary)
- ML models (BERT, RoBERTa) outperform simple heuristics for credibility detection.
- Rule-based systems offer transparency but miss subtle patterns.
- Hybrid approaches (ML + rules) balance accuracy and interpretability.

## Methodology Justification
- ML used for nuanced content analysis; rules for domain/citation checks.
- Hybrid model improves accuracy over either alone.
- Trade-offs: ML is less interpretable, rules are less flexible.

## Parameters (Documentation)
- Input: URL (string)
- Output: JSON with scores and explanations
- Parameters: model weights, thresholds, feature toggles
- Future: Add more features, retrain ML, tune weights, improve error handling

## Maintenance Guidelines
- Update authoritative source lists and retrain ML model as new data emerges.
- Document changes and scoring logic for reproducibility.
