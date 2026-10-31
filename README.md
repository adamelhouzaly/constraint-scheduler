# Constraint Scheduler

AI-assisted portfolio prototype using Python and Z3. Assigns single-slot jobs to qualified, available workers. Returns a feasible schedule, conflicting constraint names, or an explicit unknown result if solving times out. An independent Python validator checks every successful result.

## Run

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scheduler.py example.json
python -m pytest -q
```

Slots are integers. Each job consumes one slot. Worker and job IDs must be unique. Conflict names use zero-based job indexes; an unsatisfiable core is not necessarily the smallest possible explanation.

## Scope and next steps

This is a local prototype, not a deployed service. It does not optimize schedules or support multi-slot durations. Add durations, a greedy baseline, and benchmark cases before making performance claims. Input JSON is intended for trusted local use.

## Attribution

Implementation generated with Codex assistance. Uses the Z3 library; no third-party project was copied. Study the constraints and extend the model before presenting personal engineering contributions.
