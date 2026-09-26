class InvalidTransitionError(ValueError):
    pass

def validate_stage_transition(current_stage, next_stage):
    allowed_transitions = {
        'Applied': ['Screening', 'Rejected'],
        'Screening': ['Interview', 'Rejected'],
        'Interview': ['Offer', 'Rejected'],
        'Offer': ['Hired', 'Rejected'],
        'Hired': [],
        'Rejected': []
    }
    
    if current_stage not in allowed_transitions:
        raise InvalidTransitionError(f"Unknown current stage: {current_stage}")
        
    if next_stage not in allowed_transitions[current_stage]:
        raise InvalidTransitionError("Invalid stage transition. Candidates must move one stage at a time.")
        
    return True
