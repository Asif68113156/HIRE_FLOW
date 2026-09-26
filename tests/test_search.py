import pytest
from search.parser import parse_query

def test_parse_name_fuzzy():
    res = parse_query("sharam")
    assert res['text'] == "sharam"
    assert res['stage'] is None
    assert res['is_understood'] is True

def test_parse_stage():
    res = parse_query("Interview candidates")
    assert res['stage'] == "Interview"
    assert res['is_understood'] is True
    assert res['text'] == ''

def test_parse_time_in_stage():
    res = parse_query("Screening > 7 days")
    assert res['min_days'] == 7
    assert res['is_understood'] is True

def test_parse_moved_since():
    res = parse_query("Moved to Interview since Monday")
    assert res['stage'] is None
    assert res['moved_to'] == "Interview"
    assert res['moved_since'] == "monday"
    
def test_parse_offer_not_hired():
    res = parse_query("Who reached offer but didn't get hired")
    assert res['reached_offer_not_hired'] is True

def test_exclude_rejected():
    res = parse_query("Everyone except rejected candidates")
    assert res['exclude_rejected'] is True

def test_combined_search():
    res = parse_query("Interview candidates since Monday")
    assert res['stage'] == "Interview"
    assert res['moved_since'] == "monday"
