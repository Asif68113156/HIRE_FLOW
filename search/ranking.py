from search.parser import parse_query
from search.filters import apply_filters
from search.fuzzy import fuzzy_match
from services.candidate_service import get_candidate_stage_duration

def perform_search(query_string):
    parsed = parse_query(query_string)
    
    if not parsed['is_understood'] and parsed['text'] == '':
        return {
            'results': [],
            'explanation': [],
            'understood': False
        }
        
    filtered_db_candidates = apply_filters(parsed)
    
    has_structured_filter = any([
        parsed['stage'],
        parsed['min_days'],
        parsed['moved_since'],
        parsed['exclude_rejected'],
        parsed['reached_offer_not_hired']
    ])
    
    if parsed['text']:
        ranked = fuzzy_match(parsed['text'], filtered_db_candidates)
        ranked.sort(key=lambda x: x[1], reverse=True)
        final_candidates = [item[0] for item in ranked]
    else:
        final_candidates = filtered_db_candidates
        
    results_out = []
    for c in final_candidates:
        c_dict = c.to_dict()
        c_dict['duration'] = get_candidate_stage_duration(c.id)
        results_out.append(c_dict)
        
    understood = True
    if not has_structured_filter and len(results_out) == 0:
        understood = False

    return {
        'results': results_out,
        'explanation': parsed['explanation'] if understood else [],
        'understood': understood
    }
