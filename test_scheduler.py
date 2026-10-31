import json
from pathlib import Path
import pytest
from scheduler import solve, validate

def example():
    return json.loads(Path(__file__).with_name('example.json').read_text())

def test_valid():
    d = example()
    r = solve(d)
    assert r['status'] == 'feasible'
    validate(d, r['assignments'])

def test_impossible():
    d = example()
    d['jobs'][0]['skill'] = 'unavailable'
    assert solve(d)['status'] == 'infeasible'

def test_validator_rejects_overlap():
    with pytest.raises(ValueError):
        validate(example(), [{'job':'pack','worker':'alex','slot':1}, {'job':'deliver','worker':'alex','slot':1}])
