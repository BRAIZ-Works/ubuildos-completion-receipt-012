# Recovery — Day 11 Public Projection

The frozen product subject is preserved by exact SHA-256 and is not modified by public-projection preparation.

If publication preparation or deployment fails:
- preserve the frozen subject unchanged;
- preserve the last known-good public projection and repository HEAD;
- classify the external action as completed, partial, not completed, or ambiguous before retry;
- repair only the public projection or deployment layer unless evidence proves a frozen-product defect.
