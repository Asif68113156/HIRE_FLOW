from rapidfuzz import process, fuzz

def fuzzy_match(query, candidates, threshold=60):
    if not query:
        return [(c, 100) for c in candidates]
        
    results = []
    candidate_map = {str(i): c for i, c in enumerate(candidates)}
    choices = {str(i): c.name for i, c in enumerate(candidates)}
    
    matches = process.extract(query, choices, scorer=fuzz.WRatio, limit=len(candidates))
    
    for match in matches:
        score = match[1]
        if score >= threshold:
            key = match[2]
            results.append((candidate_map[key], score))
            
    return results
