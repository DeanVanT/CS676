from deliverable1_3 import analyze_url_credibility

url = "https://www.cancer.gov/about-cancer/causes-prevention/risk/tobacco/cessation-fact-sheet"
result = analyze_url_credibility(url)

print(f"URL: {result['url']}")
print(f"Final Score: {result['final_score']}")
print(f"Tranche: {result['tranche']}")
print(f"\nIndividual Scores:")
print(f"  Credibility: {result['individual_scores']['credibility']}")
print(f"  Fact-Check: {result['individual_scores']['fact_check']}")
print(f"  Citations: {result['individual_scores']['citations']}")

# Verify math
cred = result['individual_scores']['credibility']
fact = result['individual_scores']['fact_check']
cite = result['individual_scores']['citations']
calculated = (cred * 0.35) + (fact * 0.35) + (cite * 0.30)
print(f"\nMath Check:")
print(f"  ({cred} * 0.35) + ({fact} * 0.35) + ({cite} * 0.30) = {calculated:.4f}")
print(f"  Stored final_score: {result['final_score']}")
print(f"  Match: {abs(calculated - result['final_score']) < 0.01}")
