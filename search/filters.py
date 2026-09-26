from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU
from models import db, Candidate, StageHistory

def apply_filters(parsed_query):
    query = Candidate.query
    
    if parsed_query['exclude_rejected']:
        query = query.filter(Candidate.current_stage != 'Rejected')
        
    if parsed_query['stage']:
        query = query.filter(Candidate.current_stage == parsed_query['stage'])
        
    if parsed_query['reached_offer_not_hired']:
        query = query.join(StageHistory).filter(StageHistory.to_stage == 'Offer').filter(Candidate.current_stage != 'Hired')
        
    candidates = query.all()
    filtered_candidates = []
    
    now = datetime.now(timezone.utc)
    
    for c in candidates:
        keep = True
        
        if parsed_query['min_days']:
            history = StageHistory.query.filter_by(candidate_id=c.id).order_by(StageHistory.timestamp.desc()).first()
            if history:
                ts = history.timestamp
                if ts.tzinfo is None:
                    ts = ts.replace(tzinfo=timezone.utc)
                if (now - ts).days <= parsed_query['min_days']:
                    keep = False
            else:
                keep = False
                
        if parsed_query['moved_since'] and keep:
            day_map = {
                'monday': MO, 'tuesday': TU, 'wednesday': WE,
                'thursday': TH, 'friday': FR, 'saturday': SA, 'sunday': SU
            }
            target_weekday = day_map.get(parsed_query['moved_since'])
            if target_weekday:
                last_day = now + relativedelta(weekday=target_weekday(-1))
                last_day = last_day.replace(hour=0, minute=0, second=0, microsecond=0)
                
                histories = StageHistory.query.filter_by(candidate_id=c.id).filter(StageHistory.timestamp >= last_day).all()
                if not histories:
                    keep = False
                elif parsed_query['moved_to']:
                    moved_to_target = False
                    for h in histories:
                        if h.to_stage == parsed_query['moved_to']:
                            moved_to_target = True
                            break
                    if not moved_to_target:
                        keep = False
                    
        if keep:
            filtered_candidates.append(c)
            
    return filtered_candidates
