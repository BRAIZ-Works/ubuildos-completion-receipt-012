# Day 11 Carousel - Prospect Qualification Pipeline

1. **The problem** - Qualification often disappears into a score nobody can inspect.
2. **The model** - Fit + need + timing + next step. Four explicit fields; no hidden score.
3. **How it works** - Supported evidence can qualify. Explicit non-fit/no-need/out-of-window timing disqualifies with a reason. Missing/invalid/contradictory evidence goes to REVIEW.
4. **Proof** - Synthetic cases cover QUALIFIED, DISQUALIFIED, and REVIEW paths; reasons remain visible; CSV export preserves status and reason.
5. **Boundary** - Demo only. Synthetic data. No CRM, enrichment, predictive scoring, revenue claim, or regulated-data claim.
6. **Inspect it** - Compare the explicit workflow with your own qualification process. Day 11/30.
