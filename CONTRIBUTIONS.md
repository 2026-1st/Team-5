# Contribution Record

This repository contains a **team project**. The project, analysis, documentation, and results should not be presented as the work of a single contributor.

This document records major merged contributions that are directly visible in the repository history. It is intended to make authorship clearer for reviewers, portfolios, and future maintainers without replacing the full commit and pull-request history.

## 박기준 (`gijun1521-hub`)

Major merged contributions include:

- proposed the sleep, noise-exposure, hearing, and mental-health analysis direction
- refined the target from PHQ-9 to a PHQ8-based screening target by excluding the sleep item to reduce conceptual overlap with sleep-duration inputs
- organized a stratified train/validation/test workflow to separate model fitting, threshold selection, and final evaluation
- implemented and documented validation-only threshold selection
- evaluated class-imbalance behavior using Recall, F2-score, PR-AUC, false negatives, and confusion matrices rather than Accuracy alone
- compared baseline and resampling-based models under a consistent split
- added Random Forest feature interpretation and SHAP-based exploratory analysis
- clarified that the work is an exploratory screening analysis rather than a diagnostic or causal model
- improved reproducibility through requirements, output tables, figures, data-handling notes, and result documentation

Related merged pull requests:

- [#1 — Initial project direction](https://github.com/2026-1st/Team-5/pull/1)
- [#3 — Early branch integration](https://github.com/2026-1st/Team-5/pull/3)
- [#5 — CM analysis notebook update](https://github.com/2026-1st/Team-5/pull/5)
- [#6 — PHQ8 screening pipeline and validation-based evaluation](https://github.com/2026-1st/Team-5/pull/6)

## Other contributors

Additional team members contributed to data exploration, notebook development, discussion, presentation preparation, review, and project integration. Their exact contributions should be added here by the relevant contributors or maintainers, using the commit and pull-request history as the primary evidence.

Recommended format:

```markdown
## Name (`github-id`)

- contribution 1
- contribution 2
- contribution 3

Related commits or pull requests:

- [PR or commit link]
```

## Attribution guidance

When referencing this project in a CV, LinkedIn profile, presentation, or portfolio:

- identify it as a team project
- describe only the work personally performed or directly led
- link to the canonical team repository
- avoid copying the repository into a personal account and presenting it as an independent project
- distinguish exploratory screening results from clinical diagnosis or causal claims

Git history remains the authoritative record when this summary and the repository history differ.
