Absolutely. Below is the **complete `PROJECT_PROGRESS.md` content in one copy-paste block**, including a clear **“What to Continue Next”** section at the end.

Replace the entire contents of your existing `PROJECT_PROGRESS.md` with this.

````markdown
# AI-Failure-Intelligence-Platform

## Project Progress and Research Status

**Project:** AI-Failure-Intelligence-Platform

**Working Research Title:** Failure Analytics and Decision Support System Using Machine Learning Techniques

**Current System Status:** CODING COMPLETE / READY FOR RESEARCH

**Current Coding Baseline:** `AI-Failure-Intelligence-Platform-coding-complete-v1.zip`

---

# 1. Project Goal

The project is a multi-domain AI failure intelligence and decision-support platform.

The system currently supports four domains:

1. Student
2. Software
3. Jobs
4. Projects

The system is designed to:

- Predict failure/outcome classes.
- Provide class probabilities.
- Identify historical failure profiles.
- Explain risk using failure-profile information.
- Generate domain-constrained counterfactual scenarios.
- Identify feasible changes that reduce model-predicted risk.
- Detect successful prediction transitions.
- Support What-If simulation.
- Provide recommendations and improvement actions.
- Provide an integrated decision-support interface.

The current working research direction is:

**Domain-Constrained Failure Intelligence System (DC-FIS)**

This is a working research name only. No novelty claim should be made until the literature review is completed.

---

# 2. Overall System Architecture

Current pipeline:

Heterogeneous Failure Data
↓
Data Preprocessing
↓
Domain-Specific Feature Processing
↓
Random Forest Prediction
↓
Failure Risk / Class Probability
↓
Failure Profile Identification
↓
Profile-Guided Feature Prioritization
↓
Domain Constraint Engine
↓
Counterfactual Candidate Generation
↓
Feasibility Filtering
↓
Risk Reduction Evaluation
↓
Prediction Transition Detection
↓
Recommendations / What-If / Decision Support

Main components:

- React frontend
- FastAPI backend
- Domain-specific Random Forest models
- Failure-profile analytics using K-Means
- Domain constraint engine
- Counterfactual candidate sampler
- Profile-guided counterfactual engine
- Recommendation system
- What-If simulation
- Automated four-domain smoke test

---

# 3. Domains

## 3.1 Student

Dataset:

`data/student/student-mat.csv`

Dataset size:

- 395 records

Main prediction features:

- absences
- studytime
- failures
- G1
- G2

Target:

- `G3 < 10` → Exam Failure
- otherwise → Passed

Class distribution:

- Passed: 265
- Exam Failure: 130

Important research consideration:

G1 and G2 are previous academic grades and therefore the prediction time point must be clearly defined in the research methodology.

Current actionable features:

- absences
- studytime

Current immutable features:

- failures
- G1
- G2

Desired counterfactual outcome:

- Passed

---

## 3.2 Software

Dataset:

`data/software/Mozilla.csv`

Original dataset size:

- 4165 records

After target cleaning:

- 3451 records

Target:

`rs`

Standardized target:

`Failure_Type`

Current classes include:

- FIXED
- DUPLICATE
- INCOMPLETE
- INVALID
- WORKSFORME
- WONTFIX
- INACTIVE
- MOVED

Important data issues:

- 714 records were removed because of missing/blank/NaN-like target values.
- Strong class imbalance exists.
- Minority classes are very small.
- Missing/Unknown semantics need further investigation.
- Weighted metrics alone are not sufficient.

Cleaned Software model removes:

- `re`
- `at`

These were treated as username/identity-like metadata.

Preliminary actionable features:

- pr
- cl
- rp
- os
- bs
- bsr

Immutable features include:

- pd
- co

Desired counterfactual outcome:

- FIXED

The exact actionability rules must be justified during the research phase.

---

## 3.3 Jobs

Dataset:

`data/jobs/ai_resume_screening.csv`

Dataset size:

- 30,000 records

Main features:

- years_experience
- skills_match_score
- education_level
- project_count
- resume_length
- github_activity

Target:

Shortlisted

Mapped to:

- Selected
- Rejected

Class distribution:

- Selected: 20,966
- Rejected: 9,034

Preliminary actionable features:

- skills_match_score
- project_count
- resume_length
- github_activity

Immutable features:

- years_experience
- education_level

Desired counterfactual outcome:

- Selected

---

## 3.4 Projects

Dataset:

`data/projects/Project Management Dataset.csv`

Dataset size:

- 99 records

Main features:

- Complexity
- Project Type
- Region
- Department
- Project Cost
- Project Benefit
- Completion%
- Phase
- Year
- Month

Target classes:

- Completed
- Cancelled
- In-Progress
- On-Hold

Class distribution:

- Completed: 30
- Cancelled: 27
- In-Progress: 25
- On-Hold: 17

Preliminary actionable features:

- Complexity
- Project Cost
- Project Benefit
- Completion%
- Phase

Preliminary immutable features:

- Project Type
- Region
- Department
- Year
- Month

Desired counterfactual outcome:

- Completed

Important research issues:

- Dataset is very small.
- Completion% may create temporal leakage depending on prediction time.
- Project Cost and Project Benefit require semantic/ablation analysis.
- Stronger or repeated cross-validation should be considered.
- Actionability of Phase and Completion% must be justified.

---

# 4. Prediction Models

The current production architecture uses domain-specific training pipelines.

General preprocessing:

- Numeric median imputation
- Categorical most-frequent imputation
- One-hot encoding for categorical variables
- `handle_unknown="ignore"`

Original Random Forest baseline:

- `n_estimators=200`
- `random_state=42`
- `n_jobs=-1`

Train/test split:

- 80/20
- stratified where applicable
- `random_state=42`

---

# 5. Three-Way Random Forest Experiment

The following experiment has already been completed.

Models:

1. Original Random Forest
2. Optimized Random Forest
3. Cleaned Random Forest

Optimization:

- RandomizedSearchCV
- 30 random configurations
- 5-fold StratifiedKFold
- shuffle=True
- random_state=42
- weighted F1 used as optimization scoring

Parameters included:

- n_estimators
- max_depth
- min_samples_split
- min_samples_leaf
- max_features
- class_weight

Saved comparison:

`backend/ml/model_comparison_results.csv`

Saved models:

- student_original_rf.pkl
- student_optimized_rf.pkl
- student_cleaned_rf.pkl
- software_original_rf.pkl
- software_optimized_rf.pkl
- software_cleaned_rf.pkl
- jobs_original_rf.pkl
- jobs_optimized_rf.pkl
- jobs_cleaned_rf.pkl
- projects_original_rf.pkl
- projects_optimized_rf.pkl
- projects_cleaned_rf.pkl

---

# 6. Completed Model Results

## Student

### Original RF

- Accuracy: 0.8861
- Precision: 0.8917
- Recall: 0.8861
- Weighted F1: 0.8875
- Balanced Accuracy: 0.8857

### Optimized RF

- Accuracy: 0.8861
- Precision: 0.8977
- Recall: 0.8861
- Weighted F1: 0.8883
- Balanced Accuracy: 0.8955
- CV weighted F1: 0.9310

### Cleaned RF

- Same as Original for the current feature-cleaning setup.

---

## Software

### Original RF

- Accuracy: 0.7685
- Precision: 0.7423
- Recall: 0.7685
- Weighted F1: 0.7498
- Balanced Accuracy: 0.4107

### Optimized RF

- Accuracy: 0.7410
- Precision: 0.7527
- Recall: 0.7410
- Weighted F1: 0.7430
- Balanced Accuracy: 0.4949
- CV weighted F1: 0.7264

### Cleaned RF

- Accuracy: 0.7178
- Precision: 0.6756
- Recall: 0.7178
- Weighted F1: 0.6821
- Balanced Accuracy: 0.3815

Important:

Software requires class-wise and macro-level analysis because of strong class imbalance.

---

## Jobs

### Original RF

- Accuracy: 0.8983
- Precision: 0.8975
- Recall: 0.8983
- Weighted F1: 0.8978
- Balanced Accuracy: 0.8737

### Optimized RF

- Accuracy: 0.9032
- Precision: 0.9023
- Recall: 0.9032
- Weighted F1: 0.9025
- Balanced Accuracy: 0.8788
- CV weighted F1: 0.9064

### Cleaned RF

- Same as Original for the current cleaning setup.

---

## Projects

### Original RF

- Accuracy: 0.6000
- Precision: 0.5750
- Recall: 0.6000
- Weighted F1: 0.5825
- Balanced Accuracy: 0.5167

### Optimized RF

- Accuracy: 0.6000
- Precision: 0.6381
- Recall: 0.6000
- Weighted F1: 0.6096
- Balanced Accuracy: 0.5167
- CV weighted F1: 0.5440

### Cleaned RF

- Same as Original for the current cleaning setup.

---

# 7. Interpretation of the Three-Way Experiment

The optimized model should be treated as a model-selection/baseline optimization experiment.

It must NOT be presented as a novel machine-learning algorithm.

Current best weighted-F1 models:

- Student → Optimized RF
- Software → Original RF
- Jobs → Optimized RF
- Projects → Optimized RF

However, model selection should not rely only on weighted F1.

The research evaluation should additionally consider:

- Macro F1
- Balanced Accuracy
- Per-class precision
- Per-class recall
- Per-class F1
- Failure-focused recall/F1
- ROC-AUC where appropriate
- PR-AUC where appropriate
- Cross-validation stability

---

# 8. Failure Profile Analysis

Failure profiles are generated using K-Means clustering.

The profile system identifies historical groups with similar feature characteristics.

Profile information can include:

- profile ID
- sample count
- feature means
- feature medians
- failure count
- non-failure count
- failure rate
- failure rate percentage

Profile guidance compares the current case with its assigned historical profile.

Features can be prioritized based on their difference from the assigned profile.

Important interpretation:

Profile guidance is used for model-based scenario analysis.

It does NOT establish:

- causality
- intervention effectiveness in the real world
- guaranteed failure prevention

---

# 9. Profile-Guided Counterfactual System

The current production counterfactual system supports:

- desired outcome specification
- domain-specific actionable features
- immutable features
- training-data-derived candidate values
- numeric candidate sampling
- categorical candidate sampling
- domain feasibility constraints
- profile-guided feature prioritization
- risk-reduction calculation
- prediction transition detection
- successful counterfactual detection
- risk-reduction-only scenarios
- already-desired outcome handling

Production implementation:

`backend/counterfactual/generator.py`

Supporting components:

`backend/counterfactual/candidate_sampler.py`

`backend/counterfactual/constraint_engine.py`

`backend/analytics/profile_guidance.py`

`backend/analytics/failure_profiles.py`

---

# 10. Counterfactual Interpretation

Counterfactual results are model-based scenarios.

For a failure case:

Risk reduction is calculated from the model's predicted probability for the original failure class.

A positive risk reduction means:

The tested input change reduced the model's predicted failure risk.

A successful counterfactual means:

The tested input change caused the trained model's predicted class to change to the desired class.

This does NOT mean:

- the change is causally responsible for success;
- the change will definitely work in reality;
- the model has discovered a causal relationship.

These limitations must be explicitly stated in the research.

---

# 11. Production Smoke Test

Automated test:

`scripts/system_smoke_test.py`

Latest successful result:

```text
[PASS] Student:
prediction=Exam Failure
probability=0.9613
profile=2
cf_status=risk_reduction_without_transition

[PASS] Software:
prediction=FIXED
probability=0.8350
profile=1
cf_status=already_desired_outcome

[PASS] Jobs:
prediction=Rejected
probability=0.9774
profile=1
cf_status=risk_reduction_without_transition

[PASS] Projects:
prediction=In - Progress
probability=0.3960
profile=0
cf_status=successful_counterfactual_found

All four domains passed the production smoke test.
```
````

This confirms that the integrated backend pipeline is functioning across all four domains.

---

# 12. Frontend Verification

The frontend was manually tested through the React interface.

## Student

Test record:

- absences = 30
- studytime = 1
- failures = 3
- G1 = 5
- G2 = 5

Observed:

- Prediction: Exam Failure
- Profile identified
- Profile-guided features:
  - absences
  - studytime

- Risk-reduction scenario generated
- No prediction transition in this test case

Status:

PASS

---

## Jobs

Test record:

- years_experience = 1
- skills_match_score = 35
- education_level = Bachelor
- project_count = 1
- resume_length = 250
- github_activity = 5

Observed:

- Prediction: Rejected
- Probability approximately 99.61%
- Profile identified
- Prioritized features:
  - github_activity
  - resume_length

- Recommended change:
  - resume_length → 709

- Model-predicted risk reduction:
  - approximately 6.11 percentage points

Status:

PASS

---

## Software

Tested through the frontend.

Observed:

- Prediction: FIXED
- Probability approximately 91%
- Target outcome: FIXED
- System correctly recognized that the model already predicts the desired outcome.
- No unnecessary preventive intervention was required.

Status:

PASS

---

## Projects

Tested through the frontend.

Observed:

- Prediction: Cancelled
- Probability approximately 35.93%
- Target outcome: Completed
- Counterfactual system identified a feasible risk-reduction intervention.
- Prediction did not change in this particular test case.

Status:

PASS

---

# 13. Current Frontend Status

The React interface currently provides:

- Domain selection
- Domain-specific input forms
- Prediction
- Class probabilities
- Recommendations
- Improvement actions
- Counterfactual Prevention
- Profile Guidance
- Risk-reduction information
- What-If Simulation

All four domains have been manually tested through the frontend.

---

# 14. Coding Changes Completed

Modified files:

- `backend/api.py`
- `backend/analytics/failure_profiles.py`
- `backend/analytics/profile_guidance.py`
- `backend/counterfactual/candidate_sampler.py`
- `backend/counterfactual/constraint_engine.py`
- `backend/counterfactual/generator.py`
- `frontend/src/App.jsx`
- `requirements.txt`
- `README.md`
- `PROJECT_PROGRESS.md`

Added file:

- `scripts/system_smoke_test.py`

Generated/cache files were cleaned from the final package.

Existing datasets and trained models were retained.

---

# 15. Current Coding Status

## CODING PHASE: COMPLETE

The production implementation is now considered frozen for research.

Verified:

- [x] Backend starts
- [x] FastAPI API works
- [x] Student prediction
- [x] Software prediction
- [x] Jobs prediction
- [x] Projects prediction
- [x] Probability output
- [x] Recommendations
- [x] What-If interface
- [x] Failure profiles
- [x] Profile-guided feature prioritization
- [x] Domain constraints
- [x] Counterfactual generation
- [x] Risk reduction
- [x] Prediction transition detection
- [x] Already-desired outcome handling
- [x] Four-domain backend smoke test
- [x] Student frontend test
- [x] Software frontend test
- [x] Jobs frontend test
- [x] Projects frontend test
- [x] Project documentation updated

The production code should now be treated as a frozen baseline.

Further code changes should only be made if a genuine reproducibility, correctness, or research-methodology issue is discovered.

---

# 16. Known Environment Warning

During the Windows smoke test, Joblib/Loky produced:

```text
UserWarning: Could not find the number of physical cores
[WinError 2]
```

Joblib then correctly fell back to the number of logical CPU cores.

This warning did not affect the smoke test.

All four domains passed.

It is an environment warning, not a project failure.

---

# 17. Important Research Risks

## 17.1 No causal claims

Counterfactual results are model-based scenarios.

Do not claim that an intervention causes real-world success.

---

## 17.2 No novelty claims yet

Random Forest, K-Means, counterfactual analysis, and feature constraints are established techniques.

Novelty must be established only after a proper literature review.

The possible contribution is the integration of:

- failure profiles
- domain constraints
- actionable counterfactuals
- risk-reduction evaluation
- profile-guided intervention prioritization

This remains a research hypothesis until the literature review confirms the gap.

---

## 17.3 Software class imbalance

Software has strong class imbalance.

Research must report:

- macro F1
- per-class F1
- minority-class recall
- balanced accuracy
- confusion matrix

Weighted F1 alone is insufficient.

---

## 17.4 Projects small dataset

Projects contains only 99 records.

Research should use an evaluation methodology appropriate for a small dataset.

Possible approaches:

- repeated stratified cross-validation
- repeated train/test experiments
- confidence intervals
- stability analysis

The exact methodology must be finalized before the final experiments.

---

## 17.5 Projects temporal leakage

`Completion%` may represent information that is only available later in the project lifecycle.

The prediction time point must therefore be defined.

Research should investigate:

- with Completion%
- without Completion%

and explain the difference.

---

## 17.6 Projects Cost/Benefit Variables

Project Cost and Project Benefit may carry substantial predictive information.

An ablation should investigate their contribution and whether their use is appropriate for the defined prediction time point.

---

## 17.7 Student Prediction Time Point

Because G1 and G2 are used to predict G3, the research must explicitly state:

The prediction is made after G1/G2 are available and before the final G3 outcome.

---

## 17.8 Actionability Rules

Counterfactual actionability rules must be justified.

For every domain, distinguish:

- actionable variables
- immutable variables
- categorical variables
- numerical variables
- domain constraints

These decisions must be documented in the methodology.

---

# 18. Research Phase

The coding phase is now stopped.

The next phase is research.

The research workflow should be:

1. Literature review
2. Research gap identification
3. Research questions
4. Research objectives
5. Experimental protocol
6. Predictive evaluation
7. Failure-profile evaluation
8. Counterfactual ablation
9. Intervention evaluation
10. Statistical analysis
11. Results
12. Discussion
13. Thesis/paper writing

---

# 19. Research Experiment 1 — Predictive Baseline

Compare:

1. Original RF
2. Optimized RF
3. Cleaned RF

Evaluate across all four domains.

Metrics:

- Accuracy
- Macro F1
- Weighted F1
- Balanced Accuracy
- Precision
- Recall
- Per-class F1
- Failure-focused recall/F1
- ROC-AUC where appropriate
- PR-AUC where appropriate

The existing three-way experiment is the starting point, but the final research evaluation should include the additional metrics above.

---

# 20. Research Experiment 2 — Failure Profile Analysis

Run K-Means for each domain.

Analyze:

- number of clusters
- profile characteristics
- failure rates
- feature distributions
- profile separation
- profile stability

Identify whether meaningful failure profiles exist.

Do not assume that a particular number of clusters is correct without an appropriate justification.

---

# 21. Research Experiment 3 — Profile Guidance Ablation

Compare:

1. Prediction only
2. Prediction + failure profiles
3. Ordinary counterfactual
4. Domain-constrained counterfactual
5. Profile-guided + domain-constrained counterfactual

Purpose:

Measure whether profile guidance adds measurable value.

---

# 22. Research Experiment 4 — Counterfactual Evaluation

Compare:

1. Random/unconstrained changes
2. Ordinary counterfactual generation
3. Domain-constrained counterfactual generation
4. Profile-guided domain-constrained counterfactual generation

Measure:

- Mean risk reduction
- Median risk reduction
- Successful transition rate
- Failure → desired transition rate
- Number of changed features
- Intervention sparsity
- Feasibility rate
- Rejected candidate rate
- Diversity of interventions
- Profile alignment

---

# 23. Counterfactual Metrics

For each domain calculate:

## Risk Reduction

Difference between original model-predicted failure risk and post-intervention failure risk.

## Prediction Transition Rate

Percentage of cases where:

Failure → Desired Outcome

## Intervention Success Rate

Percentage of cases with a feasible intervention that reaches the desired predicted class.

## Feasibility Rate

Percentage of generated candidates satisfying domain constraints.

## Sparsity

Number of features changed per intervention.

## Profile Alignment

Degree to which selected intervention features correspond to the features prioritized by the assigned failure profile.

---

# 24. Research Dataset Splitting Principle

Avoid using the test set to design intervention rules.

The following must be considered carefully:

- training data
- validation data
- test data
- profile construction
- candidate sampling
- counterfactual evaluation

Failure profiles and candidate values should not leak test-set information into intervention design.

This must be explicitly addressed in the experimental methodology.

---

# 25. Reproducibility Requirements

All final research experiments should record:

- random seeds
- dataset versions
- feature lists
- preprocessing steps
- model parameters
- optimization parameters
- CV strategy
- evaluation metrics
- profile configuration
- counterfactual constraints
- candidate-generation configuration

Results should be saved as CSV/JSON files where appropriate.

---

# 26. Planned Research Output Structure

```text
research/
├── experiments/
├── results/
├── figures/
├── tables/
├── logs/
└── reports/
```

Potential result files:

```text
model_comparison.csv
profile_analysis.csv
counterfactual_comparison.csv
intervention_metrics.csv
ablation_results.csv
per_class_metrics.csv
```

---

# 27. What to Continue Next

## NEXT STEP 1 — Freeze the Coding Version

Do not make unnecessary feature changes.

Use:

`AI-Failure-Intelligence-Platform-coding-complete-v1.zip`

as the current coding baseline.

---

## NEXT STEP 2 — Start Literature Review

Before claiming a research contribution, study existing research on:

- failure prediction
- student failure prediction
- software failure/defect prediction
- job/resume prediction
- project failure prediction
- failure profiling
- clustering-based profiling
- explainable AI
- counterfactual explanations
- actionable counterfactuals
- constrained counterfactual explanations
- intervention recommendation
- decision-support systems
- risk reduction
- profile-guided intervention

The literature review should answer:

1. What has already been done?
2. What methods are commonly used?
3. What are the limitations of existing approaches?
4. Are failure profiles already used for intervention guidance?
5. Are domain-constrained counterfactuals already used in similar systems?
6. Has profile-guided counterfactual intervention already been proposed?
7. What exact research gap remains?

---

## NEXT STEP 3 — Define the Research Problem

After the literature review:

- finalize the research problem
- define the research gap
- define research questions
- define research objectives
- define hypotheses if required
- define the proposed contribution

Do not finalize the claimed contribution before the literature review.

---

## NEXT STEP 4 — Finalize Experimental Methodology

Before running final experiments, decide:

- dataset splits
- cross-validation strategy
- model-selection procedure
- profile-generation procedure
- number-of-clusters selection method
- counterfactual candidate-generation method
- actionability rules
- evaluation metrics
- statistical tests
- leakage controls

---

## NEXT STEP 5 — Run Reproducible Research Experiments

Then implement/run:

1. Predictive model comparison
2. Failure-profile analysis
3. Profile-guidance ablation
4. Counterfactual comparison
5. Intervention evaluation
6. Statistical analysis

All results should be automatically saved.

---

## NEXT STEP 6 — Generate Research Tables and Figures

Create:

- model comparison tables
- per-class metric tables
- confusion matrices
- profile distributions
- cluster/profile visualizations
- risk-reduction comparisons
- intervention success comparisons
- ablation tables
- domain-wise comparison figures

---

## NEXT STEP 7 — Write the Research

Only after the experiments are completed:

- Methodology
- Results
- Discussion
- Limitations
- Conclusion
- Future Work

---

# 28. Current Project State

## Completed

- [x] Multi-domain ML platform
- [x] Four domain models
- [x] Original/Optimized/Cleaned RF comparison
- [x] FastAPI backend
- [x] React frontend
- [x] Recommendations
- [x] What-If simulation
- [x] Failure profiles
- [x] Profile-guided feature prioritization
- [x] Domain constraints
- [x] Counterfactual generation
- [x] Risk-reduction evaluation
- [x] Four-domain smoke test
- [x] Four-domain frontend verification
- [x] Coding documentation
- [x] Coding freeze

## Current Status

**System Development:** COMPLETE

**Backend:** COMPLETE

**Frontend:** COMPLETE

**Four-Domain Integration:** COMPLETE

**Failure Profiles:** COMPLETE

**Profile-Guided Counterfactual:** COMPLETE

**Automated Smoke Test:** PASS

**Frontend Verification:** PASS

**Coding Baseline:** FROZEN

**Research Experiments:** NOT YET STARTED

**Literature Review:** NEXT

**Research Phase:** READY TO BEGIN

---

# 29. Final Current Status

The coding phase of the AI-Failure-Intelligence-Platform is complete and the production implementation has been tested across all four domains.

The current system is ready to serve as the frozen implementation for the research phase.

The next work should focus on:

**Literature Review → Research Gap → Research Questions/Objectives → Experimental Methodology → Reproducible Experiments → Statistical Analysis → Results → Thesis/Paper**

No further major production-code changes should be made unless a genuine correctness or reproducibility problem is discovered.

```

### What we continue with next

When you come back to the project, **do not start coding again**. We should start at:

**Step 1: Literature Review**

And specifically, we should investigate whether the combination of **failure profiles + domain constraints + profile-guided counterfactual intervention + quantitative risk reduction** is actually a research gap.

Only after establishing that gap should we lock the research objectives and experiment design. That will prevent us from building a research story first and trying to justify it afterward.
```
