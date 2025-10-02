from typing import Optional, Tuple
from urllib.parse import urlparse
import requests
import re
from bs4 import BeautifulSoup
from typing import Dict, Union
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def prompt_for_url(prompt: str = "Enter a URL (scheme optional, e.g. example.com or https://example.com; blank to cancel): ") -> Optional[str]:
    """
    Prompt the user for a URL, accept host-only inputs (like "www.example.com") and normalize
    them by prepending "https://". Returns a validated URL string or None if the user cancels.
    """
    while True:
        s = input(prompt).strip()
        if not s:
            return None

        # Quick syntactic parse
        parsed = urlparse(s)

        # If user included a scheme and a host, accept as-is
        if parsed.scheme.lower() in ("http", "https") and parsed.netloc:
            return s

        # If input looks like a host (e.g. "www.example.com" or "example.com"),
        # normalize by assuming https and return the normalized URL.
        # Heuristic: contains at least one dot and no spaces, and not starting with '/'
        if ('.' in s) and (' ' not in s) and (not s.startswith('/')):
            normalized = 'https://' + s
            parsed2 = urlparse(normalized)
            if parsed2.netloc:
                print(f"No scheme provided; assuming https:// and using {normalized}")
                return normalized

        print("Invalid URL — enter a host (example.com) or a full URL including http:// or https://, or press Enter to cancel.")

def validate_url(url: str, timeout: int = 10) -> Tuple[bool, str]:
    """
    Validate a URL by:
      1) Ensuring it has http/https scheme and a host.
      2) Attempting a quick HTTP GET with the given timeout (seconds).
         We use stream=True to avoid downloading the whole body.

    Returns:
      (True, "") on success
      (False, "reason") on failure

    Notes:
      - This will raise no exceptions to the caller; all network errors are converted to False + message.
      - timeout is the maximum number of seconds to wait for the connection + response.
    """
    # Basic syntactic check
    parsed = urlparse(url)
    if parsed.scheme.lower() not in ("http", "https") or not parsed.netloc:
        return False, "Invalid URL format: must include http:// or https:// and a host"

    try:
        # Prefer HEAD to be light; fallback to GET if HEAD not allowed/returns 405.
        try:
            resp = requests.head(url, timeout=timeout, allow_redirects=True)
            # Some servers respond 405 Method Not Allowed to HEAD; treat as fallback
            if resp.status_code == 405:
                raise RuntimeError("HEAD not allowed, falling back to GET")
        except (requests.exceptions.RequestException, RuntimeError):
            # Fallback to GET (streamed) to avoid downloading full body
            resp = requests.get(url, timeout=timeout, stream=True, allow_redirects=True)

        # Consider successful if we got any 2xx or 3xx response
        if 200 <= resp.status_code < 400:
            return True, ""

        # Treat 403 as "reachable but blocked" (many commercial sites block programmatic clients)
        if resp.status_code == 403:
            return True, f"Reachable but blocked (HTTP {resp.status_code})"

        # Other non-success status codes are treated as failures
        return False, f"Server returned HTTP {resp.status_code}"
    except requests.exceptions.Timeout:
        return False, f"Request timed out after {timeout} seconds"
    except requests.exceptions.SSLError as e:
        return False, f"SSL error: {e}"
    except requests.exceptions.ConnectionError as e:
        return False, f"Connection error: {e}"
    except Exception as e:
        return False, f"Unexpected error: {e}"

def evaluate_reference_credibility(url: str) -> Dict[str, Union[float, str]]:
    """
    Simple credibility evaluator.

    Fetches the HTML at a given URL, extracts visible text, and runs a tiny
    BERT fake-news classifier (mrm8488/bert-tiny-finetuned-fake-news-detection)
    on the content (max 512 tokens). Returns a dictionary with a probability
    credibility_score and an explanation string.

    Returns
    -------
    Dict[str, Union[float, str]]
    """
        
    try:
        
        tokenizer = AutoTokenizer.from_pretrained("mrm8488/bert-tiny-finetuned-fake-news-detection")
        model = AutoModelForSequenceClassification.from_pretrained("mrm8488/bert-tiny-finetuned-fake-news-detection")
        model.eval()
    except Exception as e:
        return {"credibility_score": 0.0, "explanation": f"Init error: {e}"}

    # fetch
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        text = " ".join(BeautifulSoup(r.text, "html.parser").stripped_strings)
        if not text:
            return {"credibility_score": 0.0, "explanation": "No text extracted"}
    except Exception as e:
        return {"credibility_score": 0.0, "explanation": f"Failed to fetch URL content: {e}"}

    # infer
    try:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            logits = model(**inputs).logits
            probs = torch.softmax(logits, dim=-1).squeeze(0)

        id2label = {int(k): v.upper() for k, v in model.config.id2label.items()}

        # Prefer explicit REAL/TRUE labels
        real_ids = [i for i, lbl in id2label.items() if ("REAL" in lbl) or ("TRUE" in lbl)]
        if real_ids:
            rid = real_ids[0]
        else:
            # Fallback for common schema {LABEL_0, LABEL_1}: treat class 1 as positive
            if set(id2label.values()) == {"LABEL_0", "LABEL_1"} and 1 in id2label:
                rid = 1
            else:
                return {"credibility_score": 0.0, "explanation": f"No REAL-like label in model: {id2label}"}

        credibility_score = float(probs[rid])
        return {"credibility_score": credibility_score, "explanation": f"ML model confidence: {credibility_score:.2f}"}

    except Exception as e:
        return {"credibility_score": 0.0, "explanation": f"Model eval failed: {e}"}

def evaluate_fact_check(url: str) -> Dict[str, Union[float, str]]:
    """
    Basic fact-checking evaluation based on known fact-checking sources and scientific journals.
    
    Args:
        url (str): The URL to evaluate
        
    Returns:
        dict: Contains 'fact_check_score' (float) and 'explanation' (str)
    """
    try:
        # Parse the URL
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        
        # Remove 'www.' if present
        if domain.startswith('www.'):
            domain = domain[4:]
            
        # Define authoritative sources and their scores
        authoritative_sources = {
            # Government Health & Science Organizations
            'ncbi.nlm.nih.gov': 0.95,
            'nih.gov': 0.9,
            'cdc.gov': 0.7,
            'fda.gov': 0.85,
            'who.int': 0.8,
            'hhs.gov': 0.8,
            'health.gov': 0.8,
            'europa.eu': 0.8,
            'canada.ca': 0.8,
            'gov.uk': 0.8,

            # Academic & Research Institutions
            'mayoclinic.org': 0.9,
            'hopkinsmedicine.org': 0.9,
            'medlineplus.gov': 0.9,
            'clevelandclinic.org': 0.9,
            'stanfordhealthcare.org': 0.9,
            'mskcc.org': 0.9,
            'massgeneral.org': 0.9,
            'uchicagomedicine.org': 0.9,
            'ucl.ac.uk': 0.9,
            'ox.ac.uk': 0.9,
            'harvard.edu': 0.9,
            'mit.edu': 0.9,
            'caltech.edu': 0.9,

            # Scientific Journals & Publishers
            'nature.com': 0.9,
            'science.org': 0.9,
            'thelancet.com': 0.9,
            'nejm.org': 0.9,
            'jamanetwork.com': 0.9,
            'bmj.com': 0.9,
            'cell.com': 0.9,
            'plos.org': 0.9,
            'springer.com': 0.9,
            'sciencedirect.com': 0.85,

            # Medical & Research Databases
            'cochrane.org': 0.9,
            'clinicaltrials.gov': 0.9,
            'scopus.com': 0.85,
            'pubmed.ncbi.nlm.nih.gov': 0.95,
            'researchgate.net': 0.8,
            'semanticscholar.org': 0.8,

            # Technological Journals & Engineering Sources
            'ieee.org': 0.9,
            'acm.org': 0.9,
            'computingreviews.com': 0.85,
            'techscience.com': 0.85,
            'arxiv.org': 0.85,
            'engineering.com': 0.8,
            'spectrum.ieee.org': 0.85,
            'nasa.gov': 0.9,
            'esa.int': 0.85,
            'nist.gov': 0.9,
            'usenix.org': 0.85,
            'siggraph.org': 0.85,

            # Finance & Economics
            'imf.org': 0.9,
            'worldbank.org': 0.9,
            'bis.org': 0.9,
            'oecd.org': 0.9,
            'treasury.gov': 0.9,
            'sec.gov': 0.9,
            'federalreserve.gov': 0.9,
            'bea.gov': 0.9,
            'bls.gov': 0.9,
            'edgar.sec.gov': 0.9,
            'morningstar.com': 0.8,
            'statista.com': 0.8,

            # Law, Government & Policy
            'supremecourt.gov': 0.9,
            'gao.gov': 0.9,
            'cbo.gov': 0.9,
            'crsreports.congress.gov': 0.9,
            'congress.gov': 0.9,
            'justice.gov': 0.9,
            'law.cornell.edu': 0.9,
            'uscourts.gov': 0.9,

            # Standards & Industry Bodies
            'iso.org': 0.9,
            'w3.org': 0.9,
            'ietf.org': 0.9,
            'icann.org': 0.85,
            'etsi.org': 0.85,
            'ansi.org': 0.85,

            # General Reference & Encyclopedias
            'britannica.com': 0.85,
            'stanford.edu/entries': 0.85,
            'internetencyclopediaofphilosophy.org': 0.85,

            # Business & Market Intelligence
            'forrester.com': 0.85,
            'gartner.com': 0.85,
            'pitchbook.com': 0.85,
            'cbinsights.com': 0.85,
            'crunchbase.com': 0.8
        }        
        # Basic scoring logic
        score = 0.5  # Default score
        explanation = []
        
        # Check if it's a known authoritative source
        for source, source_score in authoritative_sources.items():
            if domain == source or domain.endswith('.' + source):
                score = source_score
                explanation.append(f"Recognized authoritative source ({source})")
                break
                
        # Additional score for .gov domains not in our list
        if domain.endswith('.gov') and score == 0.5:
            score = 0.8
            explanation.append("Government domain")
            
        # Additional score for academic institutions
        if domain.endswith('.edu'):
            score = max(score, 0.8)
            explanation.append("Academic institution")
            
        # Check for scientific article indicators in URL
        path = parsed_url.path.lower()
        if any(x in path for x in ['/article/', '/research/', '/study/', '/paper/']):
            score = min(score + 0.05, 1.0)
            explanation.append("Scientific article indicators")
            
        return {
            "fact_check_score": score,
            "explanation": " | ".join(explanation) if explanation else "Basic fact-check evaluation"
        }
        
    except Exception as e:
        return {
            "fact_check_score": 0.0,
            "explanation": f"Error evaluating URL: {str(e)}"
        }

def evaluate_citations(url: str) -> Dict[str, Union[float, str]]:
    """
    Evaluates citation count and reference quality from webpage content.
    
    Args:
        url (str): The URL to evaluate
        
    Returns:
        dict: Contains 'citation_score' (float) and 'explanation' (str)
    """
    try:
        # Fetch the webpage content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Initialize counters and score
        citation_count = 0
        reference_count = 0
        score = 0.5  # Default score
        explanation = []
        
        # Find citations in different formats
        # Look for <cite> tags
        cite_tags = soup.find_all('cite')
        citation_count += len(cite_tags)
        
        # Look for numbered references [1], [2], etc.
        numbered_refs = re.findall(r'\[\d+\]', response.text)
        citation_count += len(numbered_refs)
        
        # Look for reference or bibliography section
        ref_sections = soup.find_all(['div', 'section'], 
                                   class_=re.compile(r'reference|bibliography|citations', re.I))
        
        if ref_sections:
            # Count references in these sections
            for section in ref_sections:
                # Count list items in reference sections
                references = section.find_all('li')
                reference_count += len(references)
        
        # Calculate score based on citations
        total_citations = max(citation_count, reference_count)
        
        if total_citations > 0:
            # Adjust score based on number of citations
            if total_citations >= 50:
                score = 0.9
            elif total_citations >= 30:
                score = 0.8
            elif total_citations >= 15:
                score = 0.7
            elif total_citations >= 5:
                score = 0.6
            
            explanation.append(f"Found {total_citations} citations/references")
            
        # Look for DOI references
        doi_refs = re.findall(r'doi\.org/\d+\.\d+/\S+', response.text)
        if doi_refs:
            score += 0.1
            explanation.append(f"Found {len(doi_refs)} DOI references")
            score = min(score, 1.0)
            
        return {
            "citation_score": score,
            "explanation": " | ".join(explanation) if explanation else "No citations found",
            "citation_count": total_citations
        }
        
    except Exception as e:
        return {
            "citation_score": 0.0,
            "explanation": f"Error analyzing citations: {str(e)}",
            "citation_count": 0
        }

def aggregate_scores(result_credibility, result_fact_check, result_citations):
    """
    Aggregates individual scores into a final weighted score.
    """
    # Define weights for each score component
    weights = {
        'credibility': 0.3,
        'fact_check': 0.35,
        'citations': 0.2
    }
    
    # Extract scores
    scores = {
        'credibility': result_credibility.get('credibility_score', 0),
        'fact_check': result_fact_check.get('fact_check_score', 0),
        'citations': result_citations.get('citation_score', 0)
    }
    
    # Calculate weighted final score
    final_score = sum(scores[key] * weights[key] for key in weights)
    
    return {
        'final_score': round(final_score, 2),
        'individual_scores': scores
    }

def score_tranche(score: float):
    """
    Converts a numeric score into a qualitative tranche.
    
    Args:
        score (float): The numeric score (0.0 to 1.0)
        
    Returns:
        str: The qualitative tranche ("Poor", "Fair", "Good", "Very Good", "Excellent")
    """
    tranche = ""
    if score < 0.2:
        tranche = "Poor"
    elif score < 0.4:
        tranche = "Fair"
    elif score < 0.6:
        tranche = "Good"
    elif score < 0.8:
        tranche = "Very Good"
    else:
        tranche = "Excellent"
    
        final_result = {"score": score, "tranche": tranche}
        return final_result

if __name__ == "__main__":
    url = prompt_for_url()
    if not url:
        print("No URL entered — exiting.")
    else:
        ok, reason = validate_url(url, timeout=10)
        if ok:
            print("URL is valid and reachable. Checking credibility now...")
            result_credibility = evaluate_reference_credibility(url)
            result_fact_check = evaluate_fact_check(url)
            result_citations = evaluate_citations(url)

            results = aggregate_scores(result_credibility, result_fact_check, result_citations)
            print("Final Score:", score_tranche(results.get("final_score")))
            print("Individual Scores:", results.get("individual_scores"))
        else:
            print("URL validation failed:", reason)