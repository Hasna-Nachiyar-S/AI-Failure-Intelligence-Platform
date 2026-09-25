**# AI-Failure-Intelligence-Platform**

**## Project Progress and Research Status**

\***\*Project:\*\*** AI-Failure-Intelligence-Platform

\***\*Working Research Title:\*\*** Failure Analytics and Decision Support System Using Machine Learning Techniques

\***\*Current System Status:\*\*** CODING COMPLETE / READY FOR RESEARCH

\***\*Current Coding Baseline:\*\*** `AI-Failure-Intelligence-Platform-coding-complete-v1.zip`

**---**

**# 1. Project Goal**

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

\***\*Domain-Constrained Failure Intelligence System (DC-FIS)\*\***

This is a working research name only. No novelty claim should be made until the literature review is completed.

**---**

**# 2. Overall System Architecture**

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

**---**

**# 3. Domains**

**## 3.1 Student**

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

**---**

**## 3.2 Software**

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

**---**

**## 3.3 Jobs**

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

**---**

**## 3.4 Projects**

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

**---**

**# 4. Prediction Models**

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

**---**

**# 5. Three-Way Random Forest Experiment**

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

**---**

**# 6. Completed Model Results**

**## Student**

**### Original RF**

- Accuracy: 0.8861

- Precision: 0.8917

- Recall: 0.8861

- Weighted F1: 0.8875

- Balanced Accuracy: 0.8857

**### Optimized RF**

- Accuracy: 0.8861

- Precision: 0.8977

- Recall: 0.8861

- Weighted F1: 0.8883

- Balanced Accuracy: 0.8955

- CV weighted F1: 0.9310

**### Cleaned RF**

- Same as Original for the current feature-cleaning setup.

**---**

**## Software**

**### Original RF**

- Accuracy: 0.7685

- Precision: 0.7423

- Recall: 0.7685

- Weighted F1: 0.7498

- Balanced Accuracy: 0.4107

**### Optimized RF**

- Accuracy: 0.7410

- Precision: 0.7527

- Recall: 0.7410

- Weighted F1: 0.7430

- Balanced Accuracy: 0.4949

- CV weighted F1: 0.7264

**### Cleaned RF**

- Accuracy: 0.7178

- Precision: 0.6756

- Recall: 0.7178

- Weighted F1: 0.6821

- Balanced Accuracy: 0.3815

Important:

Software requires class-wise and macro-level analysis because of strong class imbalance.

**---**

**## Jobs**

**### Original RF**

- Accuracy: 0.8983

- Precision: 0.8975

- Recall: 0.8983

- Weighted F1: 0.8978

- Balanced Accuracy: 0.8737

**### Optimized RF**

- Accuracy: 0.9032

- Precision: 0.9023

- Recall: 0.9032

- Weighted F1: 0.9025

- Balanced Accuracy: 0.8788

- CV weighted F1: 0.9064

**### Cleaned RF**

- Same as Original for the current cleaning setup.

**---**

**## Projects**

**### Original RF**

- Accuracy: 0.6000

- Precision: 0.5750

- Recall: 0.6000

- Weighted F1: 0.5825

- Balanced Accuracy: 0.5167

**### Optimized RF**

- Accuracy: 0.6000

- Precision: 0.6381

- Recall: 0.6000

- Weighted F1: 0.6096

- Balanced Accuracy: 0.5167

- CV weighted F1: 0.5440

**### Cleaned RF**

- Same as Original for the current cleaning setup.

**---**

**# 7. Interpretation of the Three-Way Experiment**

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

**---**

**# 8. Failure Profile Analysis**

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

**---**

**# 9. Profile-Guided Counterfactual System**

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

**---**

**# 10. Counterfactual Interpretation**

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

**---**

**# 11. Production Smoke Test**

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

This confirms that the integrated backend pipeline is functioning across
all four domains.

---

# 12. Frontend Verification

The frontend was manually tested through the React interface.

## Student

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

---

## Jobs

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

---

30. Product Development Update --- 2026-09-25

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

http://127.0.0.1:8000

while the browser frontend was running on:

http://localhost:5173

This caused the session cookie not to be sent correctly and produced
401 Unauthorized responses.

The frontend API base was corrected to use:

http://localhost:8000

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

Deprecated: escaping deep link whitespace with \_ is unsupported and will be removed in a future 5.x release. Use %20 instead.

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

31. Current Project State After Product Update

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

32. When to Continue the Research

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

33. Session Stop Point --- 2026-09-25

Today's session is intentionally closed after successful product
verification.

Next time, the user can choose either:

A. Continue product development
or
B. Continue the research

If the user chooses research, start with the literature review and
research-gap investigation described in Section 32.

If the user chooses product development, use the current user-dashboard
version as the starting software baseline.
