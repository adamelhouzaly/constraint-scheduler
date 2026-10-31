"""Discrete assignment solver: jobs require skills and one available time slot."""
import json
import sys
from z3 import Solver, Int, And, Or, sat, unsat


def solve(data):
    workers, jobs = data['workers'], data['jobs']
    if len({w['id'] for w in workers}) != len(workers) or len({j['id'] for j in jobs}) != len(jobs):
        raise ValueError('IDs must be unique')
    s = Solver()
    s.set(timeout=5000)
    assignments = [Int(f'worker_{i}') for i in range(len(jobs))]
    slots = [Int(f'slot_{i}') for i in range(len(jobs))]
    for i, job in enumerate(jobs):
        options = [And(assignments[i] == w, slots[i] == t)
                   for w, worker in enumerate(workers)
                   if job['skill'] in worker['skills']
                   for t in set(worker['slots']) & set(job['slots'])]
        s.assert_and_track(Or(options), f'eligibility_job_{i}')
        for k in range(i):
            s.assert_and_track(Or(assignments[i] != assignments[k], slots[i] != slots[k]), f'no_overlap_{k}_{i}')
    status = s.check()
    if status == unsat:
        return {'status': 'infeasible', 'conflicting_rules': [str(c) for c in s.unsat_core()]}
    if status != sat:
        return {'status': 'unknown', 'reason': s.reason_unknown()}
    m = s.model()
    result = [{'job': j['id'], 'worker': workers[m.eval(assignments[i]).as_long()]['id'],
               'slot': m.eval(slots[i]).as_long()} for i, j in enumerate(jobs)]
    validate(data, result)
    return {'status': 'feasible', 'assignments': result}


def validate(data, assignments):
    workers = {w['id']: w for w in data['workers']}
    jobs = {j['id']: j for j in data['jobs']}
    if len(assignments) != len(jobs) or {a['job'] for a in assignments} != set(jobs):
        raise ValueError('Every job must appear exactly once')
    occupied = set()
    for a in assignments:
        j, w = jobs[a['job']], workers[a['worker']]
        key = (a['worker'], a['slot'])
        if j['skill'] not in w['skills'] or a['slot'] not in w['slots'] or a['slot'] not in j['slots'] or key in occupied:
            raise ValueError('Invalid assignment')
        occupied.add(key)

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        print(json.dumps(solve(json.load(stream)), indent=2))
