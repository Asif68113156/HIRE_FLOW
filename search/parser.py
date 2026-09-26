import re

def parse_query(query_str):
    query = query_str.lower().strip()
    
    filters = {
        'stage': None,
        'min_days': None,
        'moved_since': None,
        'moved_to': None,
        'exclude_rejected': False,
        'reached_offer_not_hired': False,
        'text': '',
        'is_understood': False,
        'explanation': []
    }
    
    if not query:
        return filters
        
    stages = ['applied', 'screening', 'interview', 'offer', 'hired', 'rejected']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    if 'except rejected' in query or 'excluding rejected' in query or 'not rejected' in query:
        filters['exclude_rejected'] = True
        filters['explanation'].append("Excluding rejected candidates")
        filters['is_understood'] = True
        query = re.sub(r'(everyone |all )?(except|excluding|not) rejected( candidates)?', '', query).strip()
        
    if ('reached offer' in query or 'got offer' in query) and ('not hired' in query or "didn't get hired" in query):
        filters['reached_offer_not_hired'] = True
        filters['explanation'].append("Reached Offer stage but currently not Hired")
        filters['is_understood'] = True
        query = re.sub(r'(who )?(reached|got) offer.*(not|didn\'t get) hired', '', query).strip()

    if 'offer but not hired' in query or 'offer not hired' in query:
        filters['reached_offer_not_hired'] = True
        filters['explanation'].append("Reached Offer stage but currently not Hired")
        filters['is_understood'] = True
        query = re.sub(r'offer (but )?not hired', '', query).strip()

    days_match = re.search(r'(more than|>) (\d+) (days|week)', query)
    if days_match:
        val = int(days_match.group(2))
        if days_match.group(3) == 'week':
            filters['min_days'] = val * 7
        else:
            filters['min_days'] = val
        filters['explanation'].append(f"Time in current stage > {filters['min_days']} days")
        filters['is_understood'] = True
        query = re.sub(r'(stuck in |in )?(for )?(more than|>) \d+ (days|week)( old)?', '', query).strip()
        
    day_pattern = r'\b(?:since|from|on)?\s*(' + '|'.join(days) + r')\b'
    since_match = re.search(day_pattern, query)
    if since_match:
        filters['moved_since'] = since_match.group(1)
        filters['explanation'].append(f"Moved since: {since_match.group(1).capitalize()}")
        filters['is_understood'] = True
        
        moved_to_match = re.search(r'moved to (' + '|'.join(stages) + ')', query)
        if moved_to_match:
            filters['moved_to'] = moved_to_match.group(1).capitalize()
            filters['explanation'].append(f"Moved to: {filters['moved_to']}")
            query = re.sub(r'moved to (' + '|'.join(stages) + ')', '', query).strip()

        query = re.sub(day_pattern, '', query).strip()

    for stage in stages:
        if re.search(rf'\b{stage}\b', query) and not filters['moved_to'] and not filters['reached_offer_not_hired'] and not filters['exclude_rejected']:
            filters['stage'] = stage.capitalize()
            filters['explanation'].append(f"Stage: {filters['stage']}")
            filters['is_understood'] = True
            query = re.sub(rf'\b{stage}\b( candidates)?', '', query).strip()
            break
            
    query = re.sub(r"who'?s in |right now|who has been (stuck )?in |who |everyone |all |candidates?|moved|but ", '', query).strip()
    
    remaining = query.strip()
    if remaining:
        filters['text'] = remaining
        filters['explanation'].append(f"Name search: '{remaining}'")
        filters['is_understood'] = True
        
    return filters
