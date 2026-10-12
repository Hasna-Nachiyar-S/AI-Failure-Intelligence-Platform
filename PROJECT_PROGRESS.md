**\*\*# AI-Failure-Intelligence-Platform\*\***

**\*\*## Project Progress and Research Status\*\***

\\\***\*\*\\\*Project:\\\*\\\*\*\*** AI-Failure-Intelligence-Platform

\\\***\*\*\\\*Working Research Title:\\\*\\\*\*\*** Failure Analytics and Decision Support System Using Machine Learning Techniques

\\\***\*\*\\\*Current System Status:\\\*\\\*\*\*** CODING COMPLETE / READY FOR RESEARCH

\\\***\*\*\\\*Current Coding Baseline:\\\*\\\*\*\*** \`AI-Failure-Intelligence-Platform-coding-complete-v1.zip\`

**\*\*---\*\***

**\*\*# 1. Project Goal\*\***

The project is a multi-domain AI failure intelligence and decision-support platform.

The system currently supports four domains:

1\. Student

2\. Software

3\. Jobs

4\. Projects

The system is designed to:

\- Predict failure/outcome classes.

\- Provide class probabilities.

\- Identify historical failure profiles.

\- Explain risk using failure-profile information.

\- Generate domain-constrained counterfactual scenarios.

\- Identify feasible changes that reduce model-predicted risk.

\- Detect successful prediction transitions.

\- Support What-If simulation.

\- Provide recommendations and improvement actions.

\- Provide an integrated decision-support interface.

The current working research direction is:

\\\***\*\*\\\*Domain-Constrained Failure Intelligence System (DC-FIS)\\\*\\\*\*\***

This is a working research name only. No novelty claim should be made until the literature review is completed.

**\*\*---\*\***

**\*\*# 2. Overall System Architecture\*\***

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

\- React frontend

\- FastAPI backend

\- Domain-specific Random Forest models

\- Failure-profile analytics using K-Means

\- Domain constraint engine

\- Counterfactual candidate sampler

\- Profile-guided counterfactual engine

\- Recommendation system

\- What-If simulation

\- Automated four-domain smoke test

**\*\*---\*\***

**\*\*# 3. Domains\*\***

**\*\*## 3.1 Student\*\***

Dataset:

\`data/student/student-mat.csv\`

Dataset size:

\- 395 records

Main prediction features:

\- absences

\- studytime

\- failures

\- G1

\- G2

Target:

\- \`G3 < 10\` → Exam Failure

\- otherwise → Passed

Class distribution:

\- Passed: 265

\- Exam Failure: 130

Important research consideration:

G1 and G2 are previous academic grades and therefore the prediction time point must be clearly defined in the research methodology.

Current actionable features:

\- absences

\- studytime

Current immutable features:

\- failures

\- G1

\- G2

Desired counterfactual outcome:

\- Passed

**\*\*---\*\***

**\*\*## 3.2 Software\*\***

Dataset:

\`data/software/Mozilla.csv\`

Original dataset size:

\- 4165 records

After target cleaning:

\- 3451 records

Target:

\`rs\`

Standardized target:

\`Failure_Type\`

Current classes include:

\- FIXED

\- DUPLICATE

\- INCOMPLETE

\- INVALID

\- WORKSFORME

\- WONTFIX

\- INACTIVE

\- MOVED

Important data issues:

\- 714 records were removed because of missing/blank/NaN-like target values.

\- Strong class imbalance exists.

\- Minority classes are very small.

\- Missing/Unknown semantics need further investigation.

\- Weighted metrics alone are not sufficient.

Cleaned Software model removes:

\- \`re\`

\- \`at\`

These were treated as username/identity-like metadata.

Preliminary actionable features:

\- pr

\- cl

\- rp

\- os

\- bs

\- bsr

Immutable features include:

\- pd

\- co

Desired counterfactual outcome:

\- FIXED

The exact actionability rules must be justified during the research phase.

**\*\*---\*\***

**\*\*## 3.3 Jobs\*\***

Dataset:

\`data/jobs/ai_resume_screening.csv\`

Dataset size:

\- 30,000 records

Main features:

\- years_experience

\- skills_match_score

\- education_level

\- project_count

\- resume_length

\- github_activity

Target:

Shortlisted

Mapped to:

\- Selected

\- Rejected

Class distribution:

\- Selected: 20,966

\- Rejected: 9,034

Preliminary actionable features:

\- skills_match_score

\- project_count

\- resume_length

\- github_activity

Immutable features:

\- years_experience

\- education_level

Desired counterfactual outcome:

\- Selected

**\*\*---\*\***

**\*\*## 3.4 Projects\*\***

Dataset:

\`data/projects/Project Management Dataset.csv\`

Dataset size:

\- 99 records

Main features:

\- Complexity

\- Project Type

\- Region

\- Department

\- Project Cost

\- Project Benefit

\- Completion%

\- Phase

\- Year

\- Month

Target classes:

\- Completed

\- Cancelled

\- In-Progress

\- On-Hold

Class distribution:

\- Completed: 30

\- Cancelled: 27

\- In-Progress: 25

\- On-Hold: 17

Preliminary actionable features:

\- Complexity

\- Project Cost

\- Project Benefit

\- Completion%

\- Phase

Preliminary immutable features:

\- Project Type

\- Region

\- Department

\- Year

\- Month

Desired counterfactual outcome:

\- Completed

Important research issues:

\- Dataset is very small.

\- Completion% may create temporal leakage depending on prediction time.

\- Project Cost and Project Benefit require semantic/ablation analysis.

\- Stronger or repeated cross-validation should be considered.

\- Actionability of Phase and Completion% must be justified.

**\*\*---\*\***

**\*\*# 4. Prediction Models\*\***

The current production architecture uses domain-specific training pipelines.

General preprocessing:

\- Numeric median imputation

\- Categorical most-frequent imputation

\- One-hot encoding for categorical variables

\- \`handle_unknown="ignore"\`

Original Random Forest baseline:

\- \`n_estimators=200\`

\- \`random_state=42\`

\- \`n_jobs=-1\`

Train/test split:

\- 80/20

\- stratified where applicable

\- \`random_state=42\`

**\*\*---\*\***

**\*\*# 5. Three-Way Random Forest Experiment\*\***

The following experiment has already been completed.

Models:

1\. Original Random Forest

2\. Optimized Random Forest

3\. Cleaned Random Forest

Optimization:

\- RandomizedSearchCV

\- 30 random configurations

\- 5-fold StratifiedKFold

\- shuffle=True

\- random_state=42

\- weighted F1 used as optimization scoring

Parameters included:

\- n_estimators

\- max_depth

\- min_samples_split

\- min_samples_leaf

\- max_features

\- class_weight

Saved comparison:

\`backend/ml/model_comparison_results.csv\`

Saved models:

\- student_original_rf.pkl

\- student_optimized_rf.pkl

\- student_cleaned_rf.pkl

\- software_original_rf.pkl

\- software_optimized_rf.pkl

\- software_cleaned_rf.pkl

\- jobs_original_rf.pkl

\- jobs_optimized_rf.pkl

\- jobs_cleaned_rf.pkl

\- projects_original_rf.pkl

\- projects_optimized_rf.pkl

\- projects_cleaned_rf.pkl

**\*\*---\*\***

**\*\*# 6. Completed Model Results\*\***

**\*\*## Student\*\***

**\*\*### Original RF\*\***

\- Accuracy: 0.8861

\- Precision: 0.8917

\- Recall: 0.8861

\- Weighted F1: 0.8875

\- Balanced Accuracy: 0.8857

**\*\*### Optimized RF\*\***

\- Accuracy: 0.8861

\- Precision: 0.8977

\- Recall: 0.8861

\- Weighted F1: 0.8883

\- Balanced Accuracy: 0.8955

\- CV weighted F1: 0.9310

**\*\*### Cleaned RF\*\***

\- Same as Original for the current feature-cleaning setup.

**\*\*---\*\***

**\*\*## Software\*\***

**\*\*### Original RF\*\***

\- Accuracy: 0.7685

\- Precision: 0.7423

\- Recall: 0.7685

\- Weighted F1: 0.7498

\- Balanced Accuracy: 0.4107

**\*\*### Optimized RF\*\***

\- Accuracy: 0.7410

\- Precision: 0.7527

\- Recall: 0.7410

\- Weighted F1: 0.7430

\- Balanced Accuracy: 0.4949

\- CV weighted F1: 0.7264

**\*\*### Cleaned RF\*\***

\- Accuracy: 0.7178

\- Precision: 0.6756

\- Recall: 0.7178

\- Weighted F1: 0.6821

\- Balanced Accuracy: 0.3815

Important:

Software requires class-wise and macro-level analysis because of strong class imbalance.

**\*\*---\*\***

**\*\*## Jobs\*\***

**\*\*### Original RF\*\***

\- Accuracy: 0.8983

\- Precision: 0.8975

\- Recall: 0.8983

\- Weighted F1: 0.8978

\- Balanced Accuracy: 0.8737

**\*\*### Optimized RF\*\***

\- Accuracy: 0.9032

\- Precision: 0.9023

\- Recall: 0.9032

\- Weighted F1: 0.9025

\- Balanced Accuracy: 0.8788

\- CV weighted F1: 0.9064

**\*\*### Cleaned RF\*\***

\- Same as Original for the current cleaning setup.

**\*\*---\*\***

**\*\*## Projects\*\***

**\*\*### Original RF\*\***

\- Accuracy: 0.6000

\- Precision: 0.5750

\- Recall: 0.6000

\- Weighted F1: 0.5825

\- Balanced Accuracy: 0.5167

**\*\*### Optimized RF\*\***

\- Accuracy: 0.6000

\- Precision: 0.6381

\- Recall: 0.6000

\- Weighted F1: 0.6096

\- Balanced Accuracy: 0.5167

\- CV weighted F1: 0.5440

**\*\*### Cleaned RF\*\***

\- Same as Original for the current cleaning setup.

**\*\*---\*\***

**\*\*# 7. Interpretation of the Three-Way Experiment\*\***

The optimized model should be treated as a model-selection/baseline optimization experiment.

It must NOT be presented as a novel machine-learning algorithm.

Current best weighted-F1 models:

\- Student → Optimized RF

\- Software → Original RF

\- Jobs → Optimized RF

\- Projects → Optimized RF

However, model selection should not rely only on weighted F1.

The research evaluation should additionally consider:

\- Macro F1

\- Balanced Accuracy

\- Per-class precision

\- Per-class recall

\- Per-class F1

\- Failure-focused recall/F1

\- ROC-AUC where appropriate

\- PR-AUC where appropriate

\- Cross-validation stability

**\*\*---\*\***

**\*\*# 8. Failure Profile Analysis\*\***

Failure profiles are generated using K-Means clustering.

The profile system identifies historical groups with similar feature characteristics.

Profile information can include:

\- profile ID

\- sample count

\- feature means

\- feature medians

\- failure count

\- non-failure count

\- failure rate

\- failure rate percentage

Profile guidance compares the current case with its assigned historical profile.

Features can be prioritized based on their difference from the assigned profile.

Important interpretation:

Profile guidance is used for model-based scenario analysis.

It does NOT establish:

\- causality

\- intervention effectiveness in the real world

\- guaranteed failure prevention

**\*\*---\*\***

**\*\*# 9. Profile-Guided Counterfactual System\*\***

The current production counterfactual system supports:

\- desired outcome specification

\- domain-specific actionable features

\- immutable features

\- training-data-derived candidate values

\- numeric candidate sampling

\- categorical candidate sampling

\- domain feasibility constraints

\- profile-guided feature prioritization

\- risk-reduction calculation

\- prediction transition detection

\- successful counterfactual detection

\- risk-reduction-only scenarios

\- already-desired outcome handling

Production implementation:

\`backend/counterfactual/generator.py\`

Supporting components:

\`backend/counterfactual/candidate_sampler.py\`

\`backend/counterfactual/constraint_engine.py\`

\`backend/analytics/profile_guidance.py\`

\`backend/analytics/failure_profiles.py\`

**\*\*---\*\***

**\*\*# 10. Counterfactual Interpretation\*\***

Counterfactual results are model-based scenarios.

For a failure case:

Risk reduction is calculated from the model's predicted probability for the original failure class.

A positive risk reduction means:

The tested input change reduced the model's predicted failure risk.

A successful counterfactual means:

The tested input change caused the trained model's predicted class to change to the desired class.

This does NOT mean:

\- the change is causally responsible for success;

\- the change will definitely work in reality;

\- the model has discovered a causal relationship.

These limitations must be explicitly stated in the research.

**\*\*---\*\***

**\*\*# 11. Production Smoke Test\*\***

Automated test:

\`scripts/system_smoke_test.py\`

Latest successful result:

\`\`\`text

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

\`\`\`

This confirms that the integrated backend pipeline is functioning across

all four domains.

**---**

**# 12. Frontend Verification**

The frontend was manually tested through the React interface.

**## Student**

Test record:

absences = 30

studytime = 1

failures = 3

G1 = 5

G2 = 5

Observed:

Prediction: Exam Failure

Profile identified

Profile-guided features:

  - absences

  - studytime

Risk-reduction scenario generated

No prediction transition in this test case

Status:

PASS

**---**

**## Jobs**

Test record:

years_experience = 1

skills_match_score = 35

education_level = Bachelor

project_count = 1

resume_length = 250

github_activity = 5

Observed:

Prediction: Rejected

Probability approximately 99.61%

Profile identified

Prioritized features:

  - github_activity

  - resume_length

Recommended change:

  - resume_length → 709

Model-predicted risk reduction:

  - approximately 6.11 percentage points

Status:

PASS

**---**

30\. Product Development Update --- 2026-09-25

Today's work temporarily moved the project from research mode back into

product-development mode so that the platform could support real

multi-user usage.

30.1 Authentication and User Accounts

Completed:

User signup

User login

User logout

Password hashing using PBKDF2-SHA256

Server-side session management

HTTP-only authentication cookie

Session expiration

Authenticated-user dependency for protected API endpoints

Duplicate-email protection

Basic password validation

New backend file:

backend/auth.py

30.2 Personalized User Data

Added:

Per-user dashboard

Per-user analysis history

Per-user analysis statistics

User-specific domain breakdown

User isolation between accounts

SQLite persistence

Database:

backend/data/app.db

Runtime tables:

users

sessions

analyses

The database is generated locally at runtime and should not be committed

to source control.

30.3 Backend API Changes

backend/api.py was updated with:

POST /auth/signup

POST /auth/login

POST /auth/logout

GET /auth/me

GET /dashboard

GET /history

Prediction, counterfactual, What-If, and recommendation operations are

protected by authentication.

Successful analysis results are associated with the authenticated user.

30.4 Frontend Changes

frontend/src/App.jsx and frontend/src/App.css were substantially

updated.

The frontend now provides:

Login screen

Signup screen

Authenticated application shell

Personalized dashboard

User identity display

Logout

Analysis history

New-analysis workflow

Existing Student / Software / Jobs / Projects forms

Prediction results

Recommendations

Improvement actions

Counterfactual prevention

What-If simulation

Responsive layout

30.5 Authentication/Frontend Integration Fix

During testing, the frontend initially called:

http\://127.0.0.1:8000

while the browser frontend was running on:

http\://localhost:5173

This caused the session cookie not to be sent correctly and produced

401 Unauthorized responses.

The frontend API base was corrected to use:

http\://localhost:8000

After re-authentication, /auth/me and protected analysis requests

worked correctly.

30.6 Manual Functional Verification

The following user flows were tested successfully:

Signup

Login

Logout

Duplicate signup rejection

Wrong-password rejection

Personalized dashboard

User-specific analysis history

User isolation

Student prediction

Recommendations

Counterfactual functionality

What-If functionality

A Student test case using:

Absences = 10

Study Time = 3

Previous Failures = 0

G1 = 12

G2 = 12

returned a valid prediction after the authentication integration was

corrected.

30.7 Current Non-Blocking Warning

Browser developer tools currently show:

Deprecated: escaping deep link whitespace with \\\_ is unsupported and will be removed in a future 5.x release. Use %20 instead.

This is being treated as a dependency/tooling deprecation warning

because the application functionality is working correctly.

It is not currently considered a project failure.

30.8 Files Added or Updated in This Product Phase

New:

backend/auth.py

Updated:

backend/api.py

frontend/src/App.jsx

frontend/src/App.css

README.md

.gitignore

PROJECT_PROGRESS.md

Generated at runtime:

backend/data/app.db

Updated distributable baseline:

AI-Failure-Intelligence-Platform-user-dashboard-v1.zip

The distributable excludes the runtime SQLite database, frontend

dependency directory, and Python cache files.

31\. Current Project State After Product Update

Product Development

Multi-domain ML platform

Four domain models

FastAPI backend

React frontend

Recommendations

What-If simulation

Failure profiles

Profile-guided feature prioritization

Domain constraints

Counterfactual generation

Risk-reduction evaluation

Four-domain backend smoke test

Four-domain frontend verification

Authentication

User accounts

Personalized dashboard

User-specific history

User isolation

SQLite persistence

Product-level manual verification

Current Status

System Development: FUNCTIONALLY COMPLETE FOR CURRENT SCOPE

Authentication: COMPLETE

Personalized Dashboard: COMPLETE

User History: COMPLETE

Multi-User Isolation: VERIFIED

AI Prediction: WORKING

Counterfactual / What-If: WORKING

Frontend: WORKING

Research Experiments: NOT YET STARTED

Literature Review: PAUSED

Research Phase: PAUSED UNTIL USER RESUMES IT

The project is intentionally stopping here for today's session.

32\. When to Continue the Research

When the user says to continue the research, resume from the

research phase rather than restarting product development.

The research continuation order is:

Literature review

Research gap identification

Research questions

Research objectives

Experimental protocol

Predictive evaluation

Failure-profile evaluation

Counterfactual ablation

Intervention evaluation

Statistical analysis

Results

Discussion

Thesis/paper writing

The first research task when resuming should be a comprehensive

literature review covering:

failure prediction

student failure prediction

software failure/defect prediction

job/resume prediction

project failure prediction

failure profiling

clustering-based profiling

explainable AI

counterfactual explanations

actionable counterfactuals

constrained counterfactual explanations

intervention recommendation

decision-support systems

risk reduction

profile-guided intervention

The literature review must determine whether the combination of:

failure profiles + domain constraints + profile-guided counterfactual

intervention + quantitative risk reduction

constitutes a genuine research gap.

Do not assume novelty before the literature review establishes it.

Research Resume Instruction

When the user says something such as:

"continue the research"

"resume the research"

"let's continue our research"

"start the literature review"

"continue from where we stopped"

use this project-progress document as the starting context.

Do not restart the project from the beginning and do not immediately

start coding.

Resume at:

Literature Review → Research Gap → Research Questions/Objectives →

Experimental Methodology → Reproducible Experiments → Statistical

Analysis → Results → Thesis/Paper

The current product implementation should be treated as the working

software baseline unless a genuine correctness, reproducibility, or

research-methodology issue requires a change.

33\. Session Stop Point --- 2026-09-25

Today's session is intentionally closed after successful product

verification.

Next time, the user can choose either:

A. Continue product development

or

B. Continue the research

If the user chooses research, start with the literature review and

research-gap investigation described in Section 32.

If the user chooses product development, use the current user-dashboard

## version as the starting software baseline.

# 34. Product Development Stop Point — 2026-09-28

The product-development phase was continued after the previous 2026-09-25
baseline and is now intentionally paused again.

## 34.1 Backend Stabilization

During frontend/backend startup verification, two import issues were found
and corrected.

First, the backend must be started from the project root using:

`uvicorn backend.api:app --reload --host 127.0.0.1 --port 8000`

rather than importing `api` directly from the `backend` directory.

Second, `backend/api.py` referenced `get_analysis()` for individual history
records while `backend/auth.py` did not yet contain that function.

The missing function was added with user-ownership filtering:

`WHERE id = ? AND user_id = ?`

This preserves per-user history isolation.

The backend was then successfully started and reached:

`Application startup complete.`

## 34.2 Frontend Verification

The React frontend was successfully started with the Vite development
server.

The authenticated product flow was tested through the browser.

The Student analysis interface exposed two UI issues:

1. The analysis result layout had an alignment problem caused by the
   placement of the What-If section.
2. Student What-If was incorrectly limited to G2.

The Student domain configuration defines:

Actionable:

- absences
- studytime

Immutable:

- failures
- G1
- G2

Therefore G2 must not be presented as an intervention variable.

The What-If design was corrected so that the user selects an actionable
feature rather than being forced to change G2.

The intended What-If behavior across domains is:

Student:

- absences
- studytime

Jobs:

- skills_match_score
- project_count
- resume_length
- github_activity

Software:

- domain-approved actionable software features

Projects:

- domain-approved actionable project features

The backend constraint system remains the authoritative validation layer;
frontend controls must not be treated as the only protection against
immutable-feature changes.

## 34.3 User Analytics and Visualization

The product-development direction was extended to provide richer user-facing
analytics.

The dashboard/history interface is intended to include visual summaries
such as:

- domain distribution pie/donut chart
- analyses-by-domain bar chart
- recent probability/risk trend
- class-probability visualizations
- analysis history visual summaries

The visualization layer should remain descriptive and should not imply that
model probabilities are causal effects or real-world outcome guarantees.

## 34.4 Current Product Baseline

The current product baseline contains:

- Four-domain ML prediction
- Random Forest models
- Failure profiles
- Profile-guided feature prioritization
- Domain constraints
- Counterfactual generation
- Risk-reduction evaluation
- Prediction-transition detection
- Recommendations
- What-If simulation
- FastAPI backend
- React frontend
- Authentication
- User accounts
- Session management
- Personalized dashboard
- User-specific history
- User isolation
- SQLite persistence
- Individual history retrieval
- Responsive frontend
- User-facing analytical visualizations

Current backend startup status:

PASS

Current frontend startup status:

PASS

Current product-development status:

PAUSED AFTER CURRENT SCOPE VERIFICATION

No further product-development work should be started automatically when
the user says to continue the research.

---

# 35. Research Continuation — Starting Point for the Next Research Phase

The next phase is research, not additional feature development.

The product implementation above should be treated as the working software
baseline for experiments.

The research must begin with evidence gathering rather than with a novelty
claim.

## 35.1 Research Continuation Order

The research workflow is:

1. Comprehensive literature review
2. Research-gap identification
3. Research questions
4. Research objectives
5. Formal problem definition
6. Experimental protocol
7. Dataset and preprocessing justification
8. Predictive-model evaluation
9. Failure-profile evaluation
10. Counterfactual ablation study
11. Constraint-ablation study
12. Profile-guidance evaluation
13. Intervention/risk-reduction evaluation
14. Cross-domain comparison
15. Statistical analysis
16. Threats to validity and limitations
17. Results
18. Discussion
19. Thesis/paper methodology
20. Thesis/paper results and discussion
21. Final contribution statement

## 35.2 First Task When Research Resumes

The first task must be a comprehensive literature review.

The review should cover at least:

### Failure and outcome prediction

- student academic failure prediction
- software defect/failure prediction
- employee/job/resume outcome prediction
- project failure/outcome prediction
- heterogeneous-domain predictive decision support

### Failure profiling

- failure pattern mining
- risk profiling
- clustering for failure analysis
- subgroup/risk-profile identification
- profile-based decision support

### Explainable AI

- feature importance
- local explanations
- interpretable risk explanations
- example-based explanations

### Counterfactual explanations

- counterfactual explanations
- actionable counterfactuals
- feasible counterfactuals
- constrained counterfactual explanations
- recourse
- algorithmic recourse
- cost-aware recourse
- feasibility-aware recourse

### Intervention and decision support

- intervention recommendation
- risk-reduction recommendations
- decision-support systems
- human-centered predictive analytics
- profile-guided intervention
- what-if analysis

### Evaluation methodology

- counterfactual quality metrics
- validity
- proximity
- sparsity
- diversity
- feasibility
- actionability
- stability
- risk reduction
- prediction transition
- calibration
- subgroup performance
- cross-domain robustness

## 35.3 Research-Gap Question

The literature review must determine whether the following combination is
actually underexplored:

Failure profiles

- domain constraints
- profile-guided actionable counterfactual intervention
- quantitative model-predicted risk reduction
- multi-domain decision support

This combination must be investigated against existing literature.

Do not describe the system as novel merely because the individual
components are combined.

The research contribution must be based on what the literature establishes.

## 35.4 Research Questions to Develop

Candidate research questions should be refined only after the literature
review.

Potential directions include:

RQ1:
How effectively can machine-learning models predict failure/outcome classes
across heterogeneous domains?

RQ2:
Can historical failure profiles provide useful information for prioritizing
actionable features in failure cases?

RQ3:
Does profile-guided feature prioritization improve the quality or efficiency
of constrained counterfactual generation compared with non-profile-guided
counterfactual generation?

RQ4:
How do domain constraints affect counterfactual feasibility, sparsity,
risk reduction, and prediction-transition rates?

RQ5:
Can the proposed decision-support pipeline produce measurable reductions in
model-predicted failure risk while respecting domain-specific actionability
constraints?

RQ6:
How consistent is the proposed approach across Student, Software, Jobs,
and Projects domains?

These are candidate research questions only. They must be revised after the
literature review and formal problem definition.

## 35.5 Experimental Plan

The eventual research experiments should include at least:

### Experiment A — Predictive baseline

Compare:

- baseline Random Forest
- optimized Random Forest
- cleaned/feature-restricted Random Forest where applicable

Report:

- accuracy
- macro F1
- weighted F1
- balanced accuracy
- per-class precision
- per-class recall
- per-class F1
- failure-focused metrics
- ROC-AUC where appropriate
- PR-AUC where appropriate
- cross-validation stability

### Experiment B — Failure-profile analysis

Measure:

- cluster composition
- profile size
- failure rate
- profile separation
- feature distributions
- stability across repeated clustering runs where appropriate

### Experiment C — Counterfactual ablation

Compare at minimum:

1. Unconstrained/non-profile-guided candidate generation
2. Constraint-aware candidate generation
3. Profile-guided candidate generation
4. Profile-guided + constraint-aware generation

Evaluate:

- validity
- feasibility
- sparsity
- proximity
- diversity where applicable
- risk reduction
- successful prediction transition
- number of candidates evaluated
- computational cost

### Experiment D — Intervention evaluation

Measure:

- percentage of cases with feasible interventions
- average risk reduction
- median risk reduction
- successful transition rate
- risk-reduction-only rate
- no-feasible-intervention rate

Results must distinguish model-predicted risk reduction from real-world
causal intervention effectiveness.

### Experiment E — Cross-domain evaluation

Compare behavior across:

- Student
- Software
- Jobs
- Projects

The comparison should describe differences rather than assume that one
domain is representative of all domains.

## 35.6 Important Research Validity Issues

Before final experiments, explicitly investigate:

- target leakage
- prediction-time definition
- temporal leakage
- train/test contamination
- small-sample effects
- class imbalance
- calibration
- feature actionability assumptions
- immutable-feature assumptions
- dataset-specific semantics
- counterfactual distribution shift
- causal interpretation
- model dependence
- random-seed sensitivity
- clustering stability
- repeated evaluation bias

Specific concerns already identified:

Student:

- G1/G2 require a clearly defined prediction time point.

Software:

- severe class imbalance requires macro/per-class evaluation.
- target cleaning and feature semantics need justification.

Projects:

- only 99 records.
- Completion% may introduce temporal leakage.
- Project Cost and Project Benefit require semantic/ablation analysis.
- Phase and Completion% actionability must be justified.

## 35.7 Research Reproducibility Requirements

When research resumes, record:

- dataset versions
- preprocessing rules
- train/test split seeds
- cross-validation strategy
- hyperparameter search space
- selected model
- clustering parameters
- counterfactual candidate-generation parameters
- constraint definitions
- evaluation metrics
- random seeds
- software/package versions
- experiment outputs
- statistical tests
- confidence intervals where appropriate

All major research experiments should be reproducible from scripts rather
than relying only on manual frontend testing.

## 35.8 Interpretation Boundary

The system provides model-based decision support.

The research must clearly distinguish:

Model prediction
from
model explanation
from
counterfactual scenario
from
model-predicted risk reduction
from
real-world causal intervention.

A successful counterfactual transition means that the trained model changes
its predicted class for the modified input.

It does not establish that the proposed intervention would cause the real
person, software issue, job applicant, or project to achieve that outcome.

## 35.9 Research Resume Instruction

When the user says:

- "continue the research"
- "resume the research"
- "let's continue our research"
- "start the literature review"
- "continue from where we stopped"

resume from this section.

Do not restart product development.

Do not immediately modify the application unless the research methodology
requires a documented software change.

The first action should be:

Literature Review
→ Research Gap
→ Research Questions/Objectives
→ Experimental Methodology
→ Reproducible Experiments
→ Statistical Analysis
→ Results
→ Thesis/Paper

---

# 36. Final Session Stop Point — 2026-09-28

The current session is intentionally closed after product-development
verification and UI refinement.

The next session should begin from one of two explicit choices:

A. Continue product development

or

B. Continue the research

If the user chooses research, start with Section 35.1 and perform the
literature review before making any novelty or contribution claim.

If the user chooses product development, use the current authenticated
user-dashboard implementation as the software baseline and do not restart
the project from the original coding stage.

# 37. Next Product Development Phase — Comprehensive Code Reusability Audit

## 37.1 Current Status

The current project has completed its core multi-domain ML functionality, authentication, personalized dashboard, analysis history, counterfactual generation, What-If simulation, recommendations, and frontend/backend integration.

A preliminary code-reusability refactor has also been completed.

The preliminary refactor introduced shared frontend form components, centralized API utilities, shared domain configuration, reusable test inputs, and cleanup of empty or unused files.

However, the preliminary refactor is not considered a complete code-reusability audit. Additional opportunities may exist across the backend, frontend, ML pipelines, analytics, counterfactual generation, recommendation system, testing, and configuration.

The current working software baseline must be preserved before beginning further refactoring.

## 37.2 Objective

Conduct a comprehensive source-code audit to identify and safely reduce:

- Duplicated functions and repeated business logic.
- Repeated data-loading and preprocessing operations.
- Similar ML training, prediction, and evaluation implementations.
- Duplicated counterfactual and recommendation logic.
- Repeated analytics calculations.
- Repeated API validation and response-handling code.
- Duplicate frontend components and UI logic.
- Redundant tests and test fixtures.
- Unused imports, dead code, obsolete scripts, and unnecessary files.
- Scattered configuration values and duplicated domain definitions.
- Unnecessary dependencies and inconsistent package versions.

The objective is to improve maintainability, consistency, testability, and extensibility without sacrificing readability or domain-specific correctness.

## 37.3 Recommended Implementation Order

### Step 1 — Complete Source-Code Audit

Inspect the entire project, including:

- Backend API and authentication.
- ML model management and prediction pipelines.
- Data-loading and preprocessing modules.
- Failure-profile analytics.
- Counterfactual generation and constraint validation.
- Recommendations and What-If simulation.
- React components, pages, hooks, and utilities.
- Training, evaluation, and testing scripts.
- Configuration files, dependencies, and documentation.

Identify duplicate logic, similar implementations, unused code, dependency issues, circular imports, and opportunities for shared utilities.

For each proposed change, record the affected files, the duplication being addressed, the intended reusable component, and the potential behavioral risks.

Do not assume two functions are redundant solely because their code looks similar. Verify their inputs, outputs, constraints, and domain-specific behavior.

### Step 2 — Establish a Baseline

Before changing implementation code:

- Record the current project version and source-control state.
- Run existing backend tests and four-domain smoke tests.
- Run frontend build and lint checks where dependencies permit.
- Record representative predictions and output structures.
- Record existing API response formats and authentication behavior.
- Record current counterfactual, recommendation, and What-If behavior.
- Identify existing failures separately from regressions introduced by refactoring.

Preserve the original project and keep the working baseline recoverable.

### Step 3 — Refactor Shared Data-Loading and Preprocessing Logic

Identify repeated CSV loading, schema validation, missing-value handling, categorical processing, numeric preprocessing, and feature validation.

Introduce reusable utilities where appropriate while preserving domain-specific dataset schemas, target definitions, preprocessing rules, and leakage protections.

Avoid changing training data or model behavior merely to make implementations look uniform.

### Step 4 — Refactor ML Training, Prediction, and Evaluation

Investigate opportunities to share:

- Model loading and lifecycle management.
- Prediction and probability calculation.
- Reusable preprocessing pipelines.
- Training and evaluation helpers.
- Classification metrics and per-class reports.
- Model configuration and artifact-path resolution.

Keep domain-specific model parameters, target classes, feature definitions, and evaluation decisions configurable.

Do not replace existing model artifacts or retrain models unless required and explicitly documented.

### Step 5 — Refactor Failure Analytics

Identify repeated implementations for:

- Class and failure distributions.
- Risk summaries.
- Profile statistics.
- Aggregate metrics.
- Feature summaries.
- Analysis-history statistics.

Consolidate genuinely common calculations into reusable functions while retaining the semantics required by each domain.

### Step 6 — Refactor Counterfactual and Constraint Logic

Inspect the candidate sampler, constraint engine, profile guidance, counterfactual generator, and supporting analytics.

Investigate shared implementations for:

- Candidate generation and ranking.
- Actionable and immutable feature validation.
- Feasibility checks.
- Risk-reduction calculation.
- Prediction-transition detection.
- Counterfactual quality metrics.
- Result formatting.

Preserve domain-specific actionability rules, allowed value ranges, target classes, and feasibility constraints.

Do not present model-predicted risk reduction as proof of real-world causal effectiveness.

### Step 7 — Refactor Recommendations and What-If Simulation

Identify duplicated logic for actionable-feature selection, scenario evaluation, recommendation ranking, and result formatting.

Reuse common algorithms where their semantics match. Keep domain-specific recommendation policies and constraints separate where necessary.

Verify that What-If operations cannot bypass backend constraint validation or modify immutable features.

### Step 8 — Refactor API and Authentication Utilities

Review request validation, response formatting, exception handling, shared dependencies, and database access.

Reduce duplication without changing:

- Authentication requirements.
- Session management.
- User-specific data filtering.
- User isolation.
- Existing API routes and response contracts, unless a documented change is necessary.

Preserve ownership checks for analysis-history retrieval and other user-specific records.

### Step 9 — Refactor Frontend Components

Investigate reusable components for:

- Domain forms and field controls.
- Loading and error states.
- Prediction summaries.
- Class-probability displays.
- Recommendations and improvement actions.
- Counterfactual results.
- What-If controls.
- Analytics charts.
- History tables and dashboard summaries.

Reuse components where behavior and presentation are sufficiently similar. Keep domain-specific labels, validation, and allowed intervention features configuration-driven.

Avoid introducing unnecessary abstractions that make the React application harder to maintain.

### Step 10 — Consolidate Tests and Fixtures

Review the existing test suite and create reusable test fixtures and parameterized tests where appropriate.

Ensure that shared tests cover all four domains:

- Student.
- Software.
- Jobs.
- Projects.

Retain dedicated tests for domain-specific constraints, edge cases, authentication, user isolation, API validation, and counterfactual behavior.

Do not delete a test merely because it overlaps with another test. Confirm that its coverage is preserved before removing it.

### Step 11 — Review Configuration and Dependencies

Centralize duplicated configuration where appropriate, including domain definitions, model paths, API settings, and shared constants.

Inspect dependencies for actual usage, version compatibility, and unnecessary duplication.

Do not combine frontend and backend dependencies into one environment when separate dependency management is more appropriate.

Keep sensitive credentials and runtime databases out of distributable source archives.

### Step 12 — Regression Testing and Final Verification

After refactoring:

- Run Python compilation checks.
- Run the complete available backend test suite.
- Run the four-domain system smoke test.
- Run API and authentication tests.
- Run counterfactual and recommendation tests.
- Run frontend lint and production build checks.
- Verify dashboard, history, and user-isolation behavior.
- Compare representative predictions and response structures against the baseline.
- Document intentional differences and any tests that could not be executed.

Investigate any unexplained regression before declaring the refactor complete.

### Step 13 — Package the Complete Project

Create a complete distributable ZIP containing the updated source code, required datasets, model artifacts, configuration templates, scripts, and documentation.

Exclude generated caches, installed dependency directories, local runtime databases, and secrets where appropriate.

Include a refactoring report containing:

- Modified files.
- Added files.
- Removed files.
- Reusable components introduced.
- Duplicated logic consolidated.
- Tests executed and their results.
- Known warnings and unresolved issues.
- Instructions for installation and execution.

Verify ZIP integrity and confirm that the archive contains the complete required project.

## 37.4 Acceptance Criteria

The code-reusability phase is complete only when:

1. The full source tree has been inspected.
2. Identified duplication has been reviewed and addressed where beneficial.
3. Shared components have clear responsibilities and interfaces.
4. Domain-specific rules and constraints remain correct.
5. Authentication and user isolation continue to work.
6. Existing prediction and response behavior is preserved unless changes are documented.
7. Available backend and frontend verification checks have been run.
8. Unavailable checks and unresolved issues are explicitly recorded.
9. The complete project ZIP has been packaged and validated.
10. A file-by-file change report and refactoring summary have been produced.

The goal is not to eliminate every repeated line at any cost. The goal is to remove unnecessary duplication while keeping the platform understandable, reliable, and extensible.

## 37.5 Current Next Action

**Next task: Step 1 — Complete Source-Code Audit.**

Start by inspecting the current complete project baseline and generating a file-by-file inventory of duplication and reusability opportunities.

Do not immediately rewrite the entire application. First establish what can safely be shared, what must remain domain-specific, and which tests are needed to protect existing behavior.

After the audit, implement the refactoring incrementally in the order defined above.

**Current status:** Comprehensive reusability audit and second-stage refactoring — NOT YET STARTED.

**Completion status:** Pending source-code audit, implementation, regression testing, and packaging.

**Baseline rule:** Preserve the current authenticated four-domain platform as the starting point. Do not restart from the original coding stage or replace the existing application with a new implementation.