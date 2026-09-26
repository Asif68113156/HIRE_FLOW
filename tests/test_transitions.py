import pytest
from services.transitions import validate_stage_transition, InvalidTransitionError

def test_valid_transitions():
    assert validate_stage_transition('Applied', 'Screening') == True
    assert validate_stage_transition('Screening', 'Interview') == True
    assert validate_stage_transition('Interview', 'Offer') == True
    assert validate_stage_transition('Offer', 'Hired') == True
    
def test_valid_rejections():
    assert validate_stage_transition('Applied', 'Rejected') == True
    assert validate_stage_transition('Screening', 'Rejected') == True
    assert validate_stage_transition('Interview', 'Rejected') == True
    assert validate_stage_transition('Offer', 'Rejected') == True

def test_invalid_forward_skips():
    with pytest.raises(InvalidTransitionError):
        validate_stage_transition('Applied', 'Interview')
        
    with pytest.raises(InvalidTransitionError):
        validate_stage_transition('Applied', 'Offer')
        
    with pytest.raises(InvalidTransitionError):
        validate_stage_transition('Screening', 'Offer')

def test_invalid_backward_moves():
    with pytest.raises(InvalidTransitionError):
        validate_stage_transition('Interview', 'Applied')
        
    with pytest.raises(InvalidTransitionError):
        validate_stage_transition('Offer', 'Screening')

def test_terminal_states():
    with pytest.raises(InvalidTransitionError):
        validate_stage_transition('Hired', 'Interview')
        
    with pytest.raises(InvalidTransitionError):
        validate_stage_transition('Hired', 'Rejected')
        
    with pytest.raises(InvalidTransitionError):
        validate_stage_transition('Rejected', 'Screening')
