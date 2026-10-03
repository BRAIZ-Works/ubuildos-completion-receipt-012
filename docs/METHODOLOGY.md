# Methodology

Day 11 demonstrates a bounded prospect-qualification workflow using explicit evidence rather than hidden scoring.

## Decision logic
1. If required evidence is missing or invalid, route to `REVIEW`.
2. If explicit fit evidence is `no`, route to `DISQUALIFIED` and show the reason.
3. If explicit need evidence is `no`, route to `DISQUALIFIED` and show the reason.
4. If timing is `later`, route to `DISQUALIFIED` for the active qualification window and preserve the timing reason.
5. If fit and need are `yes`, timing is `now` or `soon`, and a next step exists, route to `QUALIFIED`.
6. Contradictory explicit disqualification notes route to `REVIEW` instead of being silently resolved.

This is deterministic workflow logic. It is not an AI probability score and does not infer facts not present in the record.
