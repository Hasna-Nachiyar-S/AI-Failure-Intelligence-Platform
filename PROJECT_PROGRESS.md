FAILURE ANALYTICS AND DECISION SUPPORT SYSTEM USING MACHINE LEARNING TECHNIQUES

PROJECT PROGRESS / CONTINUATION DOCUMENT

============================================================

PROJECT TITLE

Failure Analytics and Decision Support System Using Machine Learning Techniques

PROJECT TYPE

AI-based Failure Analysis, Prediction and Preventive

Decision Support System

RESEARCH DIRECTION

Domain-Constrained Failure Intelligence and

Counterfactual Decision Support

============================================================

1. PROJECT OBJECTIVE

============================================================

The objective of the project is to build an AI-powered platform

that analyzes historical failures across multiple domains,

predicts possible failure outcomes, identifies failure patterns,

provides recommendations, generates counterfactual prevention

scenarios, and allows interactive What-If simulation.

The system is designed as:

"Failure Intelligence and Preventive Decision Support Platform"

rather than only a failure prediction model.

The research direction extends the system from:

"Predict whether failure will happen"

towards:

"Understand failure patterns, predict possible outcomes,

identify feasible intervention opportunities, and evaluate

model-based changes that may reduce predicted failure risk."

Important:

Counterfactual and What-If results are model-based scenario

analyses.

They must NOT be described as causal evidence.

Correct wording:

"According to the trained ML model, changing a selected feature

changes the predicted outcome or predicted failure risk."

============================================================

2. SUPPORTED DOMAINS

============================================================

The platform supports four domains:

1. Student

2. Software

3. Jobs

4. Projects

============================================================

3. FINAL SYSTEM CONCEPT

============================================================

The platform combines:

1. Domain-specific failure prediction

2. Failure pattern identification

3. Failure clustering

4. Historical failure analysis

5. Recommendation generation

6. Counterfactual intervention analysis

7. What-If simulation

8. Preventive decision support

The research-oriented extension is:

Historical Failure Data

↓

Domain-Specific Preprocessing

↓

Failure Prediction

↓

Failure Pattern / Profile Identification

↓

Risk and Prediction Analysis

↓

Domain Constraint Engine

↓

Actionable Counterfactual Generation

↓

What-If Simulation

↓

Predicted Risk Reduction

↓

Preventive Decision Support

============================================================

4. CURRENT SYSTEM ARCHITECTURE

============================================================

Historical Failure Data

↓

Data Collection

↓

Data Standardization

↓

Domain-Specific Preprocessing

↓

Domain-Specific ML Models

↓

Domain Model Manager

↓

FastAPI Backend

↓

React Dashboard

↓

Prediction

↓

Failure Analytics / Clustering

↓

Recommendation

↓

Counterfactual Prevention

↓

What-If Simulation

↓

Preventive Decision Support

============================================================

5. CURRENT ML ARCHITECTURE

============================================================

The architecture was changed from the original single common

model approach to domain-specific ML models.

Current architecture:

React Dashboard

↓

FastAPI

↓

DomainModelManager

↓

┌────────────────┬────────────────┬────────────────┬────────────────┐

│ Student │ Software │ Jobs │ Projects │

│ RF Model │ RF Model │ RF Model │ RF Model │

└────────────────┴────────────────┴────────────────┴────────────────┘

↓

Domain-Specific Prediction

↓

Recommendation / Counterfactual / What-If

This change was necessary because the original common input

fields did not represent the actual important features of

each domain.

The current research experiments also maintain domain-specific

models rather than forcing all domains into one common feature

space.

============================================================

6. ACTUAL DATASET FEATURES

============================================================

6.1 STUDENT

Actual important features include:

- absences

- studytime

- failures

- G1

- G2

- G3

Target:

Exam Failure if G3 < 10

Passed if G3 >= 10

Current ML features:

- absences

- studytime

- failures

- G1

- G2

Target:

Derived from G3.

Important research consideration:

G3 is used to derive the target and is not used as an input

feature.

---

6.2 SOFTWARE

Actual features include:

- bugID

- ct

- sd

- dt

- cl

- pd

- co

- rp

- os

- bs

- rs

- pr

- bsr

- re

- at

Target:

rs

Important:

rs is the target and must not be used as an input feature.

bugID is an identifier and should not be treated as a meaningful

bug-count feature.

at contains values such as usernames in the available data and

must not automatically be described as Test Coverage.

Current ML features:

- pr

- cl

- pd

- co

- rp

- os

- bs

- bsr

- re

- at

Target:

rs

---

6.3 JOBS

Actual features:

- years_experience

- skills_match_score

- education_level

- project_count

- resume_length

- github_activity

- shortlisted

Target:

Selected if shortlisted = Yes

Rejected if shortlisted = No

Current ML features:

- years_experience

- skills_match_score

- education_level

- project_count

- resume_length

- github_activity

Target:

shortlisted

---

6.4 PROJECTS

Actual features include:

- Project Name

- Project Description

- Project Type

- Project Manager

- Region

- Department

- Project Cost

- Project Benefit

- Complexity

- Status

- Completion%

- Phase

- Year

- Month

- Start Date

- End Date

Target:

Status

Current ML features:

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

Important preprocessing:

Project Cost and Project Benefit are cleaned from

comma-formatted strings into numeric values.

Completion% is cleaned from percentage strings into numeric

values.

============================================================

7. DATA COLLECTION

============================================================

STATUS: COMPLETED

Historical datasets are available for:

- Student failures

- Software failures

- Job/recruitment outcomes

- Project outcomes

Data directories:

data/

├── student/

│ └── student-mat.csv

│

├── software/

│ └── Mozilla.csv

│

├── jobs/

│ └── ai_resume_screening.csv

│

└── projects/

└── Project Management Dataset.csv

============================================================

8. DATA STANDARDIZATION

============================================================

STATUS: COMPLETED

The original project defined a common conceptual schema:

- Domain

- Failure_Type

- Severity

- Score

- Description

However, the final ML prediction system uses domain-specific

features from the actual datasets.

This prevents the frontend inputs from becoming only cosmetic

fields.

The common conceptual schema can still be useful for higher-level

failure analytics and dashboard presentation, but prediction

models use the actual domain-specific feature sets.

============================================================

9. DATA PREPROCESSING

============================================================

STATUS: COMPLETED

The project includes:

- Data cleaning

- Missing value handling

- Numerical preprocessing

- Categorical preprocessing

- Feature transformation

- Model-specific input preparation

The domain-specific trainer uses:

- Median imputation for numeric features

- Most-frequent imputation for categorical features

- OneHotEncoder with handle_unknown="ignore"

- Random Forest classification

The preprocessing is implemented through a

ColumnTransformer/Pipeline-based architecture.

============================================================

10. DOMAIN-SPECIFIC MODEL TRAINING

============================================================

File:

backend/ml/domain_trainer.py

Purpose:

Train one ML model for each supported domain using actual

domain-specific features.

Current production models:

models/student_model.pkl

models/software_model.pkl

models/jobs_model.pkl

models/projects_model.pkl

Original production Random Forest results:

Student:

Accuracy = 0.8861

Software:

Accuracy = 0.7685 in the latest controlled experiment

Jobs:

Accuracy = 0.8983

Projects:

Accuracy = 0.6000

Training status:

SUCCESSFUL

IMPORTANT:

The older PROJECT_PROGRESS version contained a Software accuracy

of 0.8079. The latest controlled three-way experiment produced

0.7685 for the Original RF after explicit target cleaning.

For research reporting, use the latest controlled experiment

results rather than mixing results from different experimental

versions.

============================================================

11. DOMAIN MODEL MANAGER

============================================================

File:

backend/ml/domain_model_manager.py

Purpose:

- Load domain-specific models

- Normalize domain names

- Retrieve model features

- Prepare frontend input

- Run predictions

- Return class probabilities

Supported domains:

Student

Software

Jobs

Projects

The manager correctly loads:

student_model.pkl

software_model.pkl

jobs_model.pkl

projects_model.pkl

Testing confirmed that the correct feature lists are loaded

for all four domains.

============================================================

12. STUDENT MODEL TESTING

============================================================

Student model was tested using domain-specific inputs.

Weak Student Example:

Domain = Student

absences = 30

studytime = 1

failures = 3

G1 = 7

G2 = 6

Prediction:

Exam Failure

Earlier API probability:

Approximately 95.5%

Latest research-engine probability:

Exam Failure = 95.73%

Passed = approximately 4.27%

The slight difference reflects the use of the optimized research

model in the new counterfactual experiment.

---

Strong Student Example:

Domain = Student

absences = 2

studytime = 4

failures = 0

G1 = 18

G2 = 18

Prediction:

Passed

Earlier API probability:

Approximately 99.5%

The production prediction pipeline has been confirmed to respond

correctly to domain-specific student inputs.

============================================================

13. FASTAPI BACKEND

============================================================

STATUS: COMPLETED AND WORKING

File:

backend/api.py

Application:

AI Failure Intelligence Platform

Version:

1.0

CORS configured for:

http://localhost:5173

http://127.0.0.1:5173

============================================================

14. CURRENT API ENDPOINTS

CURRENT API ENDPOINTS

============================================================

GET /health

POST /predict

POST /recommend

POST /counterfactual

POST /what-if

GET /constraints/{domain}

GET /profiles/{domain}

POST /profiles/{domain}/identify

---

14.1 GET /health

Purpose:

Checks whether the API is running.

Status:

SUCCESSFUL

---

14.2 POST /predict

Purpose:

Runs the correct domain-specific ML model.

Returns:

domain

failure_type

probability

class_probabilities

Status:

SUCCESSFUL

---

14.3 POST /recommend

Purpose:

Generates recommendations and improvement actions.

Status:

SUCCESSFUL

---

14.4 POST /counterfactual

Purpose:

Generates alternative input scenarios using actionable features,
domain constraints, and model-based risk evaluation.

Current implementation returns:

original_input

original_prediction

desired_prediction

candidate_count

feasible_candidate_count

rejected_candidate_count

analysis_status

counterfactuals

successful_counterfactuals

risk_reduction_only

best_intervention

recommended_changes

interpretation

Important:

The counterfactual engine distinguishes between a reduction in
model-predicted failure risk and an actual prediction-class
transition.

Status:

SUCCESSFUL

---

14.5 POST /what-if

Purpose:

Allows the user to manually change an input feature and run
the model again.

Returns:

original_input

changes

new_input

original_prediction

new_prediction

original_probability

new_probability

probability_change

class_probabilities_before

class_probabilities_after

prediction_changed

Status:

SUCCESSFUL

---

14.6 GET /constraints/{domain}

Purpose:

Returns the domain-specific actionable and non-actionable feature
configuration used by the domain constraint engine.

Status:

SUCCESSFUL

---

14.7 GET /profiles/{domain}

Purpose:

Runs K-Means failure-profile analysis for a domain and returns
cluster-level descriptive statistics.

Current output includes:

profile_id

sample_count

feature_means

feature_medians

failure_count where target mapping is available

non_failure_count where target mapping is available

failure_rate where target mapping is available

failure_rate_percentage where target mapping is available

Status:

SUCCESSFUL

---

14.8 POST /profiles/{domain}/identify

Purpose:

Assigns a new input case to the closest K-Means failure profile.

Returns:

domain

profile_id

distance_to_profile

profile description

Status:

SUCCESSFUL

15. RECOMMENDATION ENGINE

============================================================

Files:

backend/recommendation/recommender.py

backend/recommendation/rules.py

backend/recommendation/templates.py

The recommendation system has been adapted to work with the

new domain-specific ML architecture.

Current recommendation output includes:

- domain

- prediction

- probability

- class probabilities

- cluster information

- historical analysis

- similar failures

- recommendations

- improvement actions

Important current limitation:

The latest recommender is a compatibility implementation for

the new domain-specific model architecture.

The cluster and historical-analysis fields are currently

placeholder/compatibility outputs rather than a complete

reimplementation of the original clustering and historical

analytics pipeline.

This should be improved after the research ML pipeline is stable.

============================================================

16. COUNTERFACTUAL FAILURE PREVENTION

============================================================

Current API file:

backend/counterfactual/generator.py

Class:

CounterfactualGenerator

Purpose:

Find input changes that can make the trained model predict a

different outcome.

The system evaluates:

1. Original prediction

2. Alternative scenarios

3. Minimum effective change

4. Highest-confidence scenario

5. Recommended changes

---

CURRENT STUDENT COUNTERFACTUAL TEST

Original input:

Domain = Student

absences = 2

studytime = 4

failures = 0

G1 = 18

G2 = 18

Original prediction:

Passed

Original probability:

Approximately 99.50%

Target prediction:

Exam Failure

Minimum effective change:

G2

Change:

G2 = 5

New prediction:

Exam Failure

Earlier recorded probability:

Approximately 78.40%

Highest-confidence scenario:

G1 + G2 + absences

Change:

G1 = 5

G2 = 5

absences = 20

Prediction:

Exam Failure

Earlier recorded probability:

Approximately 98.50%

Status:

SUCCESSFUL

Important:

This demonstrates that the counterfactual generator can identify

feature changes that alter the model prediction.

It does NOT demonstrate that changing G2 causes failure.

============================================================

17. WHAT-IF SIMULATION

============================================================

File:

backend/what_if/simulator.py

Class:

WhatIfSimulator

Purpose:

Allow the user to manually modify a domain feature and

observe the model's new prediction.

The simulator:

1. Takes original input.

2. Generates original prediction.

3. Applies user-selected changes.

4. Generates new prediction.

5. Compares probabilities.

6. Determines whether the predicted class changed.

---

CURRENT STUDENT WHAT-IF TEST

Original:

G2 = 18

What-If:

G2 = 5

Frontend console confirmed:

What-If data:

Domain = Student

G1 = 18

G2 = 18

absences = 2

failures = 0

studytime = 4

What-If changes:

G2 = 5

The request is correctly reaching the backend.

The What-If pipeline is therefore WORKING CORRECTLY.

Important:

The frontend and backend are successfully communicating the

selected What-If value.

============================================================

18. REACT FRONTEND

============================================================

STATUS: WORKING

Frontend location:

frontend/

Vite React application.

Frontend server:

http://localhost:5173/

The React dashboard currently provides domain-specific inputs

and communicates with the FastAPI backend.

The frontend has been updated so that the domain-specific

inputs actually affect ML predictions.

============================================================

19. FRONTEND DOMAIN INPUTS

============================================================

Student:

- absences

- studytime

- failures

- G1

- G2

Software:

- pr

- cl

- pd

- co

- rp

- os

- bs

- bsr

- re

- at

Jobs:

- years_experience

- skills_match_score

- education_level

- project_count

- resume_length

- github_activity

Projects:

- Complexity

- Project Type

- Region

- Department

- Project Cost

- Project Benefit

- Completion

- Phase

- Year

- Month

============================================================

20. FRONTEND WHAT-IF CONTROLS

============================================================

Current What-If behavior:

Student:

Change G2

Jobs:

Change skills_match_score

Projects:

Change Completion

Software:

Change cl

The frontend creates a domain-specific changes object.

Example Student:

{

"G2": 5

}

The backend receives:

{

...original_data,

"changes": {

"G2": 5

}

}

============================================================

21. CURRENT FRONTEND STATUS

============================================================

React dashboard:

WORKING

Frontend/API integration:

WORKING

Prediction:

WORKING

Counterfactual:

WORKING

What-If:

WORKING

Buttons:

WORKING

Browser console confirmed that What-If data and changes are

being sent correctly.

============================================================

22. CURRENT PROJECT STRUCTURE

CURRENT PROJECT STRUCTURE

============================================================

AI-Failure-Intelligence-Platform/

├── .github/
├── .venv/
├── app/
├── backend/
│ ├── ml/
│ │ ├── classifier.py
│ │ ├── clustering.py
│ │ ├── evaluator.py
│ │ ├── trainer.py
│ │ ├── domain_trainer.py
│ │ ├── domain_model_manager.py
│ │ ├── counterfactual_engine.py
│ │ └── test_counterfactual.py
│ ├── analytics/
│ │ └── failure_profiles.py
│ ├── services/
│ │ └── preprocessing.py
│ ├── recommendation/
│ │ ├── init.py
│ │ ├── templates.py
│ │ ├── rules.py
│ │ └── recommender.py
│ ├── counterfactual/
│ │ ├── init.py
│ │ ├── generator.py
│ │ ├── generator_backup.py
│ │ ├── constraint_engine.py
│ │ └── candidate_sampler.py
│ ├── what_if/
│ │ ├── init.py
│ │ └── simulator.py
│ ├── api.py
│ └── api_backup.py
├── data/
│ ├── student/
│ ├── software/
│ ├── jobs/
│ └── projects/
├── docs/
├── frontend/
│ ├── src/
│ │ ├── App.jsx
│ │ ├── App.css
│ │ └── main.jsx
│ └── ...
├── models/
│ ├── student_model.pkl
│ ├── software_model.pkl
│ ├── jobs_model.pkl
│ ├── projects_model.pkl
│ ├── best_classifier.pkl
│ ├── kmeans.pkl
│ ├── scaler.pkl
│ ├── encoders.pkl
│ └── backup/
├── notebooks/
├── scripts/
├── tests/
├── PROJECT_PROGRESS.md
├── README.md
└── requirements.txt

Additional research model files:

backend/ml/models/

├── student_cleaned_rf.pkl
├── student_optimized_rf.pkl
├── student_original_rf.pkl
└── other controlled experimental models

Research experiment output:

backend/ml/model_comparison_results.csv

Recent research-support modules:

backend/counterfactual/constraint_engine.py

Domain-aware actionable/non-actionable feature constraints.

backend/counterfactual/candidate_sampler.py

Training-data-derived candidate value sampling.

backend/analytics/failure_profiles.py

K-Means failure-profile generation.

Profile identification for new cases.

Profile-level failure statistics where target definitions are available.

23. BACKUP FILES

============================================================

Backups were intentionally created before major architecture

changes.

Current backups:

backend/counterfactual/generator_backup.py

backend/recommendation/recommender_backup.py

backend/api_backup.py

models/backup/

IMPORTANT:

DO NOT DELETE THESE YET.

The architecture was changed recently and the project should

first undergo a dependency/architecture audit.

After confirming which files are still required, unnecessary

backup or obsolete files can be removed safely.

============================================================

24. IMPORTANT ARCHITECTURE CLEANUP NOTE

============================================================

The project previously used a common model architecture based

on:

- Domain

- Severity

- Score

- Description

The current architecture uses domain-specific features and

separate models.

Therefore, some older files may now be unused or partially

obsolete.

DO NOT DELETE FILES RANDOMLY.

The next cleanup task is:

1. Identify all Python files.

2. Check imports and references.

3. Identify files still used by the current API.

4. Identify files used indirectly.

5. Identify obsolete model files.

6. Identify obsolete scripts.

7. Identify duplicate backup files.

8. Remove only files confirmed to be unnecessary.

9. Run backend tests again.

10. Run frontend tests again.

11. Confirm the application still works.

============================================================

25. OLD MODEL FILES

============================================================

The following files belong to the older architecture:

models/best_classifier.pkl

models/kmeans.pkl

models/scaler.pkl

models/encoders.pkl

They should NOT be deleted immediately.

The current production domain-specific models are:

models/student_model.pkl

models/software_model.pkl

models/jobs_model.pkl

models/projects_model.pkl

The old models should first be checked for remaining usage.

============================================================

26. THREE-WAY RANDOM FOREST EXPERIMENT

============================================================

STATUS:

COMPLETED

File:

backend/ml/domain_trainer.py

Experiment output:

backend/ml/model_comparison_results.csv

Three experiments were performed:

1. Original Random Forest

2. Optimized Random Forest

3. Cleaned Random Forest

The purpose was to determine whether Random Forest

hyperparameter optimization or feature cleaning produced

meaningful improvements.

IMPORTANT:

This experiment is a baseline/model-selection study.

It is NOT the novel research contribution.

RandomizedSearchCV tuning itself should NOT be claimed as a

novel algorithm.

---

26.1 STUDENT RESULTS

Original RF:

Accuracy = 0.8861

Precision = 0.8917

Recall = 0.8861

F1 = 0.8875

Balanced Accuracy = 0.8857

Optimized RF:

Accuracy = 0.8861

Precision = 0.8977

Recall = 0.8861

F1 = 0.8883

Balanced Accuracy = 0.8955

CV Weighted F1:

0.9310

Best parameters:

n_estimators = 200

min_samples_split = 5

min_samples_leaf = 4

max_features = sqrt

max_depth = 5

class_weight = None

Cleaned RF:

Accuracy = 0.8861

Precision = 0.8917

Recall = 0.8861

F1 = 0.8875

Balanced Accuracy = 0.8857

Interpretation:

Optimization produced only a very small weighted-F1

improvement, but balanced accuracy improved.

Therefore:

Student → Optimized RF can be used as the stronger baseline.

---

26.2 SOFTWARE RESULTS

Original RF:

Accuracy = 0.7685

Precision = 0.7423

Recall = 0.7685

F1 = 0.7498

Balanced Accuracy = 0.4107

Optimized RF:

Accuracy = 0.7410

Precision = 0.7527

Recall = 0.7410

F1 = 0.7430

Balanced Accuracy = 0.4949

CV Weighted F1:

0.7264

Best parameters:

n_estimators = 300

min_samples_split = 5

min_samples_leaf = 1

max_features = sqrt

max_depth = 20

class_weight = balanced_subsample

Cleaned RF:

Accuracy = 0.7178

Precision = 0.6756

Recall = 0.7178

F1 = 0.6821

Balanced Accuracy = 0.3815

Interpretation:

The Original RF has the best weighted F1.

The Optimized RF has lower accuracy and weighted F1 but better

balanced accuracy.

The Software dataset is strongly imbalanced.

Minority classes are poorly predicted, and weighted metrics can

hide this issue.

Therefore:

Software → Original RF is currently the stronger baseline.

Further research should examine macro F1, per-class recall,

confusion matrix, and class imbalance rather than relying on

accuracy alone.

---

26.3 JOBS RESULTS

Original RF:

Accuracy = 0.8983

Precision = 0.8975

Recall = 0.8983

F1 = 0.8978

Balanced Accuracy = 0.8737

Optimized RF:

Accuracy = 0.9032

Precision = 0.9023

Recall = 0.9032

F1 = 0.9025

Balanced Accuracy = 0.8788

CV Weighted F1:

0.9064

Best parameters:

n_estimators = 200

min_samples_split = 5

min_samples_leaf = 4

max_features = log2

max_depth = None

class_weight = None

Cleaned RF:

Accuracy = 0.8983

Precision = 0.8975

Recall = 0.8983

F1 = 0.8978

Balanced Accuracy = 0.8737

Interpretation:

Optimization produced a modest but consistent improvement.

Therefore:

Jobs → Optimized RF is currently the stronger baseline.

---

26.4 PROJECTS RESULTS

Original RF:

Accuracy = 0.6000

Precision = 0.5750

Recall = 0.6000

F1 = 0.5825

Balanced Accuracy = 0.5167

Optimized RF:

Accuracy = 0.6000

Precision = 0.6381

Recall = 0.6000

F1 = 0.6096

Balanced Accuracy = 0.5167

CV Weighted F1:

0.5440

Best parameters:

n_estimators = 300

min_samples_split = 2

min_samples_leaf = 2

max_features = log2

max_depth = 5

class_weight = balanced_subsample

Cleaned RF:

Accuracy = 0.6000

Precision = 0.5750

Recall = 0.6000

F1 = 0.5825

Balanced Accuracy = 0.5167

Interpretation:

The test F1 improved slightly, but cross-validation performance

is weak.

The dataset contains only approximately 99 usable rows.

Therefore, Project results are unstable and should not be

over-interpreted.

A larger dataset or repeated cross-validation should be

considered before making strong claims.

============================================================

27. FINAL THREE-WAY COMPARISON

============================================================

Domain | Experiment | Accuracy | Precision | Recall | F1 | Balanced Accuracy | CV Weighted F1

Student | Original RF | 0.8861 | 0.8917 | 0.8861 | 0.8875 | 0.8857 | -

Student | Optimized RF | 0.8861 | 0.8977 | 0.8861 | 0.8883 | 0.8955 | 0.9310

Student | Cleaned RF | 0.8861 | 0.8917 | 0.8861 | 0.8875 | 0.8857 | -

Software | Original RF | 0.7685 | 0.7423 | 0.7685 | 0.7498 | 0.4107 | -

Software | Optimized RF | 0.7410 | 0.7527 | 0.7410 | 0.7430 | 0.4949 | 0.7264

Software | Cleaned RF | 0.7178 | 0.6756 | 0.7178 | 0.6821 | 0.3815 | -

Jobs | Original RF | 0.8983 | 0.8975 | 0.8983 | 0.8978 | 0.8737 | -

Jobs | Optimized RF | 0.9032 | 0.9023 | 0.9032 | 0.9025 | 0.8788 | 0.9064

Jobs | Cleaned RF | 0.8983 | 0.8975 | 0.8983 | 0.8978 | 0.8737 | -

Projects | Original RF | 0.6000 | 0.5750 | 0.6000 | 0.5825 | 0.5167 | -

Projects | Optimized RF | 0.6000 | 0.6381 | 0.6000 | 0.6096 | 0.5167 | 0.5440

Projects | Cleaned RF | 0.6000 | 0.5750 | 0.6000 | 0.5825 | 0.5167 | -

============================================================

28. CURRENT BASELINE MODEL SELECTION

============================================================

Current domain-specific baseline selection:

Student:

Optimized RF

F1 = 0.8883

Software:

Original RF

F1 = 0.7498

Jobs:

Optimized RF

F1 = 0.9025

Projects:

Optimized RF

F1 = 0.6096

Important:

There is currently no single "best algorithm" that clearly wins

across all four domains.

This supports maintaining domain-specific modeling.

The three-way experiment should therefore be treated as the

baseline/model-selection stage before the proposed research

method.

============================================================

29. RESEARCH INTERPRETATION OF THE THREE-WAY EXPERIMENT

============================================================

The experiment shows:

1. Hyperparameter optimization can provide modest improvements

   in some domains.

2. Optimization does not consistently improve all domains.

3. Feature cleaning can sometimes reduce predictive performance.

4. Software contains strong class imbalance.

5. Projects has insufficient data for strong conclusions.

6. Domain-specific behavior is important.

7. Random Forest tuning alone is not sufficient as a research

   contribution.

Therefore, the research should move beyond:

"Which Random Forest parameters give the highest accuracy?"

towards:

"How can failure prediction be connected to actionable,

domain-constrained intervention recommendations?"

============================================================

30. RESEARCH GAP / PROPOSED RESEARCH DIRECTION

============================================================

The current project already contains:

- Prediction

- Clustering

- Recommendation

- Counterfactual generation

- What-If simulation

However, these components are not yet connected into a rigorous

research methodology.

The proposed research direction is to build a unified framework

that connects:

Failure Prediction

-

Failure Profiles

-

Domain Constraints

-

Actionable Counterfactual Intervention

-

Quantitative Risk-Reduction Evaluation

This is currently the strongest candidate for the research

contribution.

Working name:

Domain-Constrained Failure Intelligence System

Alternative:

Domain-Constrained Counterfactual Failure Intelligence

Short form:

DC-FIS

or

DC-CFI

============================================================

31. IMPORTANT NOVELTY POSITION

============================================================

A framework can be the main contribution of the research paper.

However:

"Building a framework" alone is NOT automatically novel.

Counterfactual explanations already exist in the research

literature.

Actionable recourse and feasibility constraints also already

exist.

Therefore, the project must NOT claim:

"Counterfactual explanations are novel."

or:

"Domain constraints are novel."

The potential research contribution is the integration and

evaluation of these components in a heterogeneous failure

intelligence setting.

Potential contribution:

A unified multi-domain failure intelligence framework in which

failure patterns are used to guide feasible, domain-specific

counterfactual interventions and the effectiveness of those

interventions is quantitatively evaluated using predicted risk

reduction and actionability constraints.

This is a POTENTIAL novelty claim.

A systematic literature review must be completed before making

a final novelty claim in the paper.

============================================================

32. PROPOSED RESEARCH FRAMEWORK

============================================================

Heterogeneous Failure Data

↓

Data Preprocessing

↓

Domain-Specific Prediction

↓

Failure Pattern Mining

(K-Means / Failure Profiles)

↓

Failure Profile Identification

↓

Risk / Prediction Explanation

↓

Domain Constraint Engine

↓

Actionable Feature Selection

↓

Candidate Counterfactual Generation

↓

Feasibility Filtering

↓

Profile-Guided Intervention Ranking

↓

What-If Simulation

↓

Predicted Risk Reduction

↓

Preventive Decision Support

============================================================

33. DOMAIN-CONSTRAINED COUNTERFACTUAL IDEA

============================================================

The proposed method should distinguish between:

ACTIONABLE FEATURES

and

NON-ACTIONABLE / IMMUTABLE FEATURES

Example:

Student

Potentially actionable:

- absences

- studytime

Potentially immutable at a chosen prediction time:

- failures

- G1

- G2

Important:

The exact actionability definition must be tied to the prediction

timepoint.

---

Jobs

Potentially actionable:

- skills_match_score

- project_count

- resume_length

- github_activity

Potentially less actionable in the short term:

- years_experience

- education_level

---

Software

Preliminary potentially actionable features:

- pr

- cl

- rp

- os

- bs

- bsr

Potentially immutable/historical features:

- pd

- co

These mappings require domain validation before final research

publication.

---

Projects

Preliminary potentially actionable features:

- Complexity

- Project Cost

- Project Benefit

- Completion%

- Phase

Potentially immutable/historical features:

- Project Type

- Region

- Department

- Year

- Month

These mappings also require domain validation.

============================================================

34. PROFILE-GUIDED COUNTERFACTUAL RESEARCH IDEA

============================================================

K-Means clustering should not simply be added for decoration.

The research goal is to use clusters as:

"Failure Profiles"

that describe groups of similar failure cases.

Example conceptual process:

Historical failures

↓

K-Means

↓

Failure Profile 1

Failure Profile 2

Failure Profile 3

...

↓

Profile characteristics

↓

Identify common actionable characteristics

↓

Generate feasible interventions

↓

Evaluate predicted risk reduction

This creates a stronger connection between:

Failure Analytics

and

Failure Prevention.

Important:

Simply assigning clusters and using them to weight ensemble

models should NOT be claimed as novel without literature

evidence.

============================================================

35. PROPOSED COUNTERFACTUAL EVALUATION

============================================================

For each test instance:

Step 1:

Calculate original failure risk.

risk_before

↓

Step 2:

Generate candidate interventions.

↓

Step 3:

Apply domain constraints.

↓

Step 4:

Generate feasible counterfactuals.

↓

Step 5:

Calculate new predicted failure risk.

risk_after

↓

Step 6:

Calculate:

risk_reduction = risk_before - risk_after

Possible evaluation metrics:

1. Average predicted risk reduction

2. Median predicted risk reduction

3. Intervention success rate

4. Prediction transition rate

5. Counterfactual validity

6. Actionability rate

7. Feasibility rate

8. Number of feature changes

9. Magnitude of feature changes

10. Sparsity of interventions

============================================================

36. PROPOSED RESEARCH EXPERIMENT

============================================================

The stronger experiment should compare:

Method A:

Random / unconstrained feature changes

versus

Method B:

Ordinary counterfactual generation

versus

Method C:

Domain-constrained counterfactual generation

versus

Method D:

Profile-guided domain-constrained counterfactual generation

The research question becomes:

"Can feasibility-constrained and failure-profile-guided

counterfactual generation produce more actionable failure

prevention recommendations than unconstrained counterfactual

generation?"

Potential evaluation:

- Validity

- Actionability

- Feasibility

- Sparsity

- Predicted risk reduction

- Prediction transition rate

============================================================

37. RESEARCH COUNTERFACTUAL ENGINE

============================================================

STATUS:

BASELINE IMPLEMENTATION CREATED AND FUNCTIONALLY TESTED

File:

backend/ml/counterfactual_engine.py

Test file:

backend/ml/test_counterfactual.py

Purpose:

Provide a research-oriented baseline for generating

domain-constrained counterfactual interventions.

The baseline engine currently contains:

Intervention:

- feature

- old_value

- new_value

- risk_before

- risk_after

- risk_reduction

- prediction_before

- prediction_after

CounterfactualResult:

- original_prediction

- original_failure_risk

- recommended_interventions

- best_intervention

Domain configuration currently includes:

Student:

Actionable features:

- absences

- studytime

Jobs:

Actionable features:

- skills_match_score

- project_count

- resume_length

- github_activity

Software:

Actionable features:

- pr

- cl

- rp

- os

- bs

- bsr

Projects:

Actionable features:

- Complexity

- Project_Cost

- Project_Benefit

- Completion

- Phase

The baseline engine currently:

1. Accepts a fitted model.

2. Accepts an input feature dictionary.

3. Identifies actionable features.

4. Generates candidate feature values.

5. Predicts candidate outcomes.

6. Calculates model-based failure risk.

7. Calculates predicted risk reduction.

8. Ranks candidate interventions.

9. Returns the highest predicted risk-reduction intervention.

Important:

The saved optimized Random Forest models are stored as model

bundles.

Example:

backend/ml/models/student_optimized_rf.pkl

The bundle contains:

- model

- domain

- experiment

- features

- metrics

- best_params

- random_state

The actual trained model is extracted using:

model_bundle["model"]

The trained object is a scikit-learn Pipeline.

The counterfactual engine therefore converts each feature

dictionary into a pandas DataFrame before prediction.

This was required because the preprocessing pipeline expects

2D tabular input with feature columns.

The baseline engine is now successfully executing.

Important:

This baseline implementation is NOT yet the final proposed

research method.

It currently uses predefined candidate values and does not yet

use training-data-derived quantiles.

It also does not yet implement profile-guided intervention

generation.

============================================================

38. STUDENT COUNTERFACTUAL BASELINE VALIDATION

============================================================

STATUS:

SUCCESSFUL

Test file:

backend/ml/test_counterfactual.py

Execution command:

python -m backend.ml.test_counterfactual

Model used:

backend/ml/models/student_optimized_rf.pkl

Model:

Optimized Random Forest

Experiment:

Optimized Random Forest

Model object:

scikit-learn Pipeline

Test case:

absences = 30

studytime = 1

failures = 3

G1 = 7

G2 = 6

Original prediction:

Exam Failure

Original failure risk:

0.9573

Approximately:

95.73%

Actionable features tested:

- absences

- studytime

Total candidate interventions tested:

7

Best model-based risk-reduction intervention:

Feature:

studytime

Old value:

1

New value:

3

Prediction before:

Exam Failure

Prediction after:

Exam Failure

Risk before:

0.9573

Risk after:

0.9560

Predicted risk reduction:

0.0013

Approximately:

0.13 percentage points

Other tested interventions included negative predicted

risk reductions.

For example:

absences:

30 → 0

Predicted risk reduction:

-0.0153

This means the trained model predicted a higher failure risk

for that counterfactual scenario.

Important interpretation:

The engine does NOT force a successful intervention.

For the tested high-risk Student case, none of the tested

actionable interventions changed the prediction from:

Exam Failure

to:

Passed

Therefore, the baseline experiment correctly reports a small

positive model-predicted risk reduction without claiming that

the intervention successfully prevents failure.

This is an important baseline result.

It demonstrates that the research engine can evaluate

candidate interventions even when no successful class-transition

counterfactual exists.

Important:

The result is model-based.

It does NOT establish that increasing studytime from 1 to 3

would actually prevent exam failure.

============================================================

39. CURRENT RESEARCH COUNTERFACTUAL STATUS

CURRENT RESEARCH COUNTERFACTUAL STATUS

============================================================

COMPLETED:

[✓] Research counterfactual engine file created
[✓] Research counterfactual test file created
[✓] Correct model path identified
[✓] Saved model bundle structure verified
[✓] Actual trained Pipeline extracted from model bundle
[✓] DataFrame-based pipeline input implemented
[✓] Student baseline counterfactual execution completed
[✓] Original predicted failure risk calculated
[✓] Candidate interventions generated
[✓] Risk-before / risk-after calculated
[✓] Predicted risk reduction calculated
[✓] Interventions ranked by predicted risk reduction
[✓] DomainConstraintEngine implemented
[✓] Domain-specific actionable and non-actionable feature configuration added
[✓] Counterfactual generator updated to apply domain constraints
[✓] CandidateSampler implemented using training-dataset-derived values
[✓] Counterfactual results separated into successful transitions,
risk-reduction-only interventions, and non-beneficial interventions
[✓] Model-based interpretation added to counterfactual output
[✓] K-Means failure-profile analyzer implemented
[✓] Profile-level failure statistics added where target definitions are available
[✓] Student failure profiles tested successfully
[✓] Student profile identification tested successfully

PENDING:

[ ] Profile-guided candidate generation
[ ] Multi-feature counterfactual generation
[ ] Stronger domain feasibility constraints
[ ] Systematic Student counterfactual validation
[ ] Four-domain counterfactual evaluation
[ ] Baseline vs proposed intervention comparison
[ ] Intervention evaluation
[ ] Statistical / repeated evaluation

40. IMPORTANT BASELINE COUNTERFACTUAL OBSERVATION

============================================================

The first research-oriented counterfactual experiment produced

the following Student result:

Original prediction:

Exam Failure

Original failure risk:

0.9573

Best tested intervention:

studytime:

1 → 3

New prediction:

Exam Failure

New predicted failure risk:

0.9560

Predicted risk reduction:

0.0013

Therefore:

The current baseline engine found a small positive change in

predicted failure risk but did not produce a successful

prediction transition.

This should NOT be treated as a failure of the research idea.

It establishes a useful baseline condition:

A counterfactual method should be able to report when no tested

actionable intervention successfully changes the predicted class.

The future proposed method should be evaluated against this

baseline rather than forcing every case to produce a successful

intervention.

============================================================

41. IMPORTANT METHODOLOGICAL IMPROVEMENTS IDENTIFIED

============================================================

The first baseline test revealed several improvements needed

for the research implementation.

1. Separate risk reduction from class transition.

A candidate may reduce predicted failure risk while still

remaining in the failure class.

Therefore, future evaluation should separately report:

- predicted risk reduction

- prediction transition

2. Distinguish effective and ineffective interventions.

Positive risk reduction:

risk_reduction > 0

Non-positive risk reduction:

risk_reduction <= 0

3. Report when no successful counterfactual exists.

The system should explicitly allow:

"No successful counterfactual found."

4. Use training-data-derived candidate values.

The current baseline uses predefined candidate ranges.

The stronger research implementation should derive realistic

candidate values from the training distribution.

5. Strengthen domain constraints.

Actionability must be defined according to the prediction

timepoint and validated for each domain.

6. Add multi-feature counterfactuals.

The baseline currently evaluates single-feature interventions.

The proposed method should later evaluate sparse combinations

of actionable features.

7. Add failure-profile guidance.

K-Means failure profiles should eventually guide which

interventions are considered or prioritized.

============================================================

42. IMPORTANT RESEARCH CLAIMS TO AVOID

============================================================

DO NOT CLAIM:

"Random Forest optimization is our novel algorithm."

DO NOT CLAIM:

"K-Means + Random Forest is automatically novel."

DO NOT CLAIM:

"Counterfactual explanations are novel."

DO NOT CLAIM:

"Changing the feature will definitely prevent failure."

DO NOT CLAIM:

"The system proves causation."

DO NOT CLAIM:

"The model identifies the true cause of failure."

DO NOT CLAIM:

"High accuracy means the intervention will work in reality."

DO NOT CLAIM:

"A positive predicted risk reduction proves that the real-world

intervention is effective."

Instead use:

"The model predicts..."

"The model estimates..."

"According to the trained model..."

"Predicted failure-risk reduction..."

"Model-based counterfactual..."

"Feasibility-constrained intervention..."

"Model-predicted change..."

============================================================

43. CURRENT RESEARCH STATUS

CURRENT RESEARCH STATUS

============================================================

COMPLETED:

[✓] Dataset collection
[✓] Dataset inspection
[✓] Domain-specific feature identification
[✓] Data preprocessing
[✓] Domain-specific Random Forest models
[✓] Domain model manager
[✓] FastAPI prediction pipeline
[✓] Recommendation system compatibility
[✓] Counterfactual API
[✓] What-If API
[✓] React dashboard
[✓] Frontend/backend integration
[✓] Three-way Random Forest experiment
[✓] Baseline model comparison
[✓] Initial research gap identification
[✓] Initial proposed research framework
[✓] Research counterfactual engine baseline
[✓] Research counterfactual test
[✓] Student counterfactual baseline validation
[✓] Predicted risk-reduction calculation
[✓] Domain Constraint Engine
[✓] Training-data-derived candidate sampling
[✓] Constrained counterfactual generation
[✓] Separation of prediction transition and risk reduction
[✓] K-Means failure profile generation
[✓] Profile-level failure statistics
[✓] Student failure profile endpoint
[✓] Student profile identification endpoint

PENDING:

[ ] Profile-guided intervention generation
[ ] Stronger domain constraint validation
[ ] Full four-domain end-to-end testing
[ ] Four-domain counterfactual evaluation
[ ] Systematic Student counterfactual validation
[ ] Baseline vs proposed intervention comparison
[ ] Intervention evaluation
[ ] Statistical / repeated evaluation
[ ] Research literature review
[ ] Final novelty validation
[ ] UI polishing
[ ] Final integration testing
[ ] Documentation
[ ] Research paper
[ ] Deployment

44. IMPORTANT ARCHITECTURE CLEANUP PLAN

============================================================

NEXT ENGINEERING TASK:

SAFE ARCHITECTURE AUDIT AND CLEANUP

Do NOT immediately delete files.

First:

1. Inspect all Python files.

2. Search for imports and references.

3. Identify which modules are imported by backend/api.py.

4. Identify which modules are imported indirectly.

5. Identify old common-model dependencies.

6. Identify usage of:

   - best_classifier.pkl

   - kmeans.pkl

   - scaler.pkl

   - encoders.pkl

7. Identify duplicate backup files.

8. Identify obsolete scripts.

9. Record findings.

10. Remove only files confirmed to be unnecessary.

11. Run backend tests.

12. Run frontend tests.

13. Re-test prediction, recommendation, counterfactual,

    and What-If.

IMPORTANT:

Do not delete the old files simply because they appear unused.

Confirm their usage first.

============================================================

45. FULL FOUR-DOMAIN TESTING PLAN

============================================================

After architecture audit:

STUDENT

- Prediction

- Recommendation

- Counterfactual

- What-If

SOFTWARE

- Prediction

- Recommendation

- Counterfactual

- What-If

JOBS

- Prediction

- Recommendation

- Counterfactual

- What-If

PROJECTS

- Prediction

- Recommendation

- Counterfactual

- What-If

Testing should include:

- Valid inputs

- Boundary inputs

- Missing values

- Categorical values

- Invalid values

- Unknown categorical values

- Prediction probabilities

- Counterfactual outputs

- What-If outputs

============================================================

46. RESEARCH METRIC IMPROVEMENT

============================================================

The current evaluator focuses strongly on accuracy.

For the research paper, evaluation should be expanded.

Recommended metrics:

- Accuracy

- Precision

- Recall

- Weighted F1

- Macro F1

- Balanced Accuracy

- ROC-AUC where appropriate

- PR-AUC where appropriate

- Per-class recall

- Per-class F1

- Confusion matrix

For imbalanced datasets:

Do not rely only on accuracy.

Software in particular requires careful reporting of minority

class performance.

Projects requires careful uncertainty reporting because of the

very small dataset.

For the counterfactual research component, additionally report:

- Average predicted risk reduction

- Median predicted risk reduction

- Intervention success rate

- Prediction transition rate

- Counterfactual validity

- Actionability rate

- Feasibility rate

- Number of feature changes

- Intervention magnitude

- Sparsity

============================================================

47. IMPORTANT DATASET RISKS

============================================================

Student:

Approximately 395 rows.

Risk:

Moderate dataset size.

---

Software:

Approximately 4,165 rows after loading, with approximately

3,451 rows remaining after removing missing target values.

Target classes are strongly imbalanced.

Risk:

Weighted metrics can hide poor minority-class performance.

---

Jobs:

Approximately 30,000 rows.

Risk:

Large dataset, but target construction should be clearly

documented because shortlisted is used as the outcome.

---

Projects:

Approximately 99 rows.

Risk:

Very small dataset.

The test set contains approximately 20 observations.

Therefore:

Project accuracy and F1 should not be treated as highly stable

estimates.

Repeated cross-validation or additional data should be considered.

============================================================

48. CURRENT DEVELOPMENT RULES

============================================================

1. Do not unnecessarily rewrite the working ML pipeline.

2. Do not delete files until their usage has been checked.

3. Keep working backups until the new architecture is stable.

4. Test every major change before moving forward.

5. Use actual dataset features.

6. Do not invent dataset fields that do not exist.

7. Do not treat IDs as meaningful predictive features.

8. Do not use target columns as input features.

9. Do not describe model counterfactuals as causal evidence.

10. Keep frontend and backend field names synchronized.

11. Separate engineering improvements from research novelty.

12. Report both baseline and proposed methods.

13. Use appropriate metrics for class imbalance.

14. Avoid over-interpreting very small datasets.

15. Validate domain constraints before using them in the paper.

16. Do not force counterfactual methods to produce successful

    interventions when the model does not support one.

17. Distinguish predicted risk reduction from prediction

    class transition.

18. Preserve reproducibility by recording model version,

    experiment, candidate generation method, and evaluation

    metrics.

============================================================

49. CURRENT DEVELOPMENT COMMANDS

============================================================

Backend:

uvicorn backend.api:app --reload

Backend:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs

Health:

http://127.0.0.1:8000/health

Frontend:

npm run dev

Frontend:

http://localhost:5173/

Research counterfactual test:

python -m backend.ml.test_counterfactual

Node version confirmed:

v24.14.1

npm version confirmed:

11.11.0

============================================================

50. CURRENT TESTING STATUS

CURRENT TESTING STATUS

============================================================

Backend:

[✓] FastAPI starts
[✓] CORS configured
[✓] /health
[✓] /predict
[✓] /recommend
[✓] /counterfactual
[✓] /what-if
[✓] /constraints/{domain}
[✓] /profiles/{domain}
[✓] /profiles/{domain}/identify

ML:

[✓] Student model
[✓] Software model
[✓] Jobs model
[✓] Projects model
[✓] Three-way RF experiment
[✓] Model comparison CSV generated

Frontend:

[✓] React application starts
[✓] Domain selection
[✓] Domain-specific input fields
[✓] Prediction request
[✓] Prediction display
[✓] Counterfactual request
[✓] Counterfactual display
[✓] What-If input
[✓] What-If request
[✓] What-If backend communication

Research:

[✓] Initial research direction
[✓] Initial research gap
[✓] Baseline comparison
[✓] Research counterfactual engine baseline
[✓] Student counterfactual baseline test
[✓] Predicted risk-reduction calculation
[✓] Domain constraint engine
[✓] Training-data-derived candidate sampling
[✓] Constrained counterfactual generation
[✓] K-Means failure profile analysis
[✓] Student failure profile generation
[✓] Student profile identification
[ ] Profile-guided candidate generation
[ ] Four-domain research counterfactual evaluation
[ ] Intervention evaluation
[ ] Literature validation
[ ] Final novelty validation

51. CURRENT PROJECT STATUS

CURRENT PROJECT STATUS

============================================================

DATA COLLECTION:

COMPLETED ✓

DATA STANDARDIZATION:

COMPLETED ✓

DATA PREPROCESSING:

COMPLETED ✓

DOMAIN-SPECIFIC MODEL TRAINING:

COMPLETED ✓

MODEL EVALUATION:

COMPLETED ✓

THREE-WAY RF COMPARISON:

COMPLETED ✓

DOMAIN MODEL MANAGER:

COMPLETED ✓

FASTAPI BACKEND:

COMPLETED ✓

RECOMMENDATION ENGINE:

WORKING ✓

COUNTERFACTUAL PREVENTION:

WORKING ✓

WHAT-IF SIMULATION:

WORKING ✓

REACT DASHBOARD:

WORKING ✓

FRONTEND/API INTEGRATION:

WORKING ✓

RESEARCH DIRECTION:

DEFINED ✓

BASELINE MODEL:

ESTABLISHED ✓

RESEARCH COUNTERFACTUAL ENGINE:

BASELINE WORKING ✓

STUDENT COUNTERFACTUAL VALIDATION:

BASELINE COMPLETED ✓

PREDICTED RISK REDUCTION:

BASELINE CALCULATION WORKING ✓

DOMAIN CONSTRAINT ENGINE:

IMPLEMENTED ✓

TRAINING-DATA-DERIVED CANDIDATE SAMPLING:

IMPLEMENTED ✓

CONSTRAINED COUNTERFACTUAL GENERATION:

WORKING ✓

K-MEANS FAILURE PROFILES:

IMPLEMENTED AND TESTED ✓

STUDENT PROFILE IDENTIFICATION:

IMPLEMENTED AND TESTED ✓

PROFILE-GUIDED INTERVENTION:

PENDING

FULL FOUR-DOMAIN TESTING:

PENDING

FOUR-DOMAIN COUNTERFACTUAL EVALUATION:

PENDING

INTERVENTION EVALUATION:

PENDING

LITERATURE REVIEW:

PENDING

NOVELTY VALIDATION:

PENDING

UI POLISH:

PENDING

DEPLOYMENT:

PENDING

FINAL DOCUMENTATION:

PENDING

RESEARCH PAPER:

PENDING

FINAL PROJECT DEMONSTRATION:

PENDING

52. NEXT DEVELOPMENT PHASE

NEXT DEVELOPMENT PHASE

============================================================

PHASE 1:

SAFE ARCHITECTURE AUDIT

↓

PHASE 2:

FULL FOUR-DOMAIN END-TO-END TESTING

↓

PHASE 3:

RESEARCH-ORIENTED COUNTERFACTUAL ENGINE REFINEMENT

↓

PHASE 4:

STRENGTHEN DOMAIN CONSTRAINT VALIDATION

↓

PHASE 5:

SYSTEMATIC STUDENT COUNTERFACTUAL VALIDATION

↓

PHASE 6:

MEASURE PREDICTED RISK REDUCTION

↓

PHASE 7:

PROFILE-GUIDED DOMAIN-CONSTRAINED INTERVENTIONS

↓

PHASE 8:

BASELINE VS PROPOSED METHOD EXPERIMENT

↓

PHASE 9:

STATISTICAL / REPEATED EVALUATION

↓

PHASE 10:

LITERATURE REVIEW + NOVELTY VALIDATION

↓

PHASE 11:

UI POLISH

↓

PHASE 12:

FINAL INTEGRATION TESTING

↓

PHASE 13:

DOCUMENTATION

↓

PHASE 14:

RESEARCH PAPER

↓

PHASE 15:

DEPLOYMENT + FINAL DEMONSTRATION

53. TOMORROW'S STARTING POINT

TOMORROW'S STARTING POINT

============================================================

When continuing this project, start from:

"Continue the Failure Analytics and Decision Support System Using
Machine Learning Techniques from the latest progress.

The domain-specific ML architecture is working.

Student prediction is tested.

Counterfactual Prevention is working.

What-If Simulation is working.

The React frontend is connected to FastAPI.

The three-way Random Forest experiment is completed.

The research-oriented counterfactual engine baseline has been
created and tested.

The latest counterfactual implementation includes:

domain-specific actionable feature constraints,

domain constraint validation,

training-data-derived candidate values,

feasible-candidate filtering,

predicted risk-reduction calculation,

separate reporting of successful class transitions and
risk-reduction-only interventions,

explicit reporting when no beneficial intervention is found,

model-based counterfactual interpretation.

The latest Student counterfactual test case is:

absences = 30

studytime = 1

failures = 3

G1 = 7

G2 = 6

Original prediction = Exam Failure

Original failure probability = approximately 95.73%

The tested candidate set contained 6 feasible single-feature
interventions in the current API implementation.

The best current intervention was:

studytime 1 → 4

New predicted failure probability = approximately 95.6633%

Predicted risk reduction = approximately 0.071 percentage points.

The prediction did NOT transition to Passed.

Current status = risk_reduction_without_transition.

This is a model-based result and must not be interpreted causally.

A K-Means failure-profile analyzer has now also been implemented.
It provides cluster-level feature statistics and, where the target
mapping is defined, profile-level failure statistics.

Student profile testing is complete.

For the Student test case above:

Assigned profile = Profile 2

Profile size = 42

Profile failure count = 37

Profile non-failure count = 5

Observed profile failure rate = 88.1%

Distance to profile = 3.413755

The profile-identification endpoint has been successfully tested.

The K-Means profile is descriptive and should not be interpreted as
causal evidence.

The next engineering task should be the SAFE ARCHITECTURE AUDIT AND
CLEANUP. Do not delete files blindly. First inspect imports,
dependencies, old models, duplicate files, and obsolete code.

After cleanup, test all four domains end-to-end.

Then continue with:

Counterfactual Engine Refinement

→ Stronger Domain Constraint Validation

→ Systematic Student Counterfactual Validation

→ Four-Domain Counterfactual Evaluation

→ Profile-Guided Domain-Constrained Intervention

→ Baseline vs Proposed Method

→ Intervention Evaluation

→ Statistical / Repeated Evaluation

→ Literature Review

→ Final Research Framework."

1. Original RF

2. Optimized RF

3. Cleaned RF

The experiment established the current domain-specific

baselines.

A research-oriented counterfactual engine baseline has now been

created and successfully executed on the Student domain.

The research engine currently:

- loads the optimized model bundle,

- extracts the actual trained Pipeline,

- accepts DataFrame-based input,

- generates candidate actionable interventions,

- calculates model-predicted failure risk,

- calculates predicted risk reduction,

- ranks interventions.

The first Student baseline produced:

Original prediction = Exam Failure

Original failure risk = 0.9573

Best tested intervention = studytime 1 → 3

New prediction = Exam Failure

New predicted failure risk = 0.9560

Predicted risk reduction = 0.0013

No tested intervention changed the Student prediction to Passed.

This is a model-based result and must not be interpreted

causally.

Do NOT continue tuning Random Forest without a specific research

reason.

The next engineering task remains:

SAFE ARCHITECTURE AUDIT AND CLEANUP.

Do not delete files blindly.

First inspect imports, dependencies, old models, duplicate files,

and obsolete code.

After cleanup, test all four domains end-to-end.

Then continue with:

Counterfactual Engine Refinement

→ Student Systematic Validation

→ Training-Data-Derived Candidate Values

→ Domain Constraint Validation

→ Predicted Risk Reduction

→ K-Means Failure Profiles

→ Profile-Guided Domain-Constrained Intervention

→ Baseline vs Proposed Method

→ Intervention Evaluation

→ Statistical / Repeated Evaluation

→ Literature Review

→ Final Research Framework."

============================================================

54. EXACT RESEARCH DEVELOPMENT ROADMAP

EXACT RESEARCH DEVELOPMENT ROADMAP

============================================================

CURRENT POSITION:

Three-way RF comparison completed.

Research counterfactual baseline created and tested.

Domain-constrained counterfactual generation implemented.

Training-data-derived candidate sampling implemented.

K-Means failure profiles implemented.

Student profile failure statistics validated.

Student profile identification validated.

CURRENT TESTED STUDENT PROFILE:

Profile 2

Sample count = 42

Failure count = 37

Non-failure count = 5

Failure rate = 88.1%

Distance for current test case = 3.413755

CURRENT TESTED STUDENT COUNTERFACTUAL:

Original prediction = Exam Failure

Original failure risk = approximately 95.73%

Best tested intervention = studytime 1 → 4

New predicted failure risk = approximately 95.6633%

Predicted risk reduction = approximately 0.071 percentage points

Prediction transition = No

CURRENT POSITION:

K-Means failure-profile analysis is implemented and tested.

Profile identification is implemented and tested.

Profile-guided intervention generation has NOT yet been implemented.

↓

NEXT:

Safe architecture audit.

↓

THEN:

Full four-domain end-to-end testing.

↓

THEN:

Strengthen and validate domain constraints.

↓

THEN:

Systematically validate Student counterfactuals.

↓

THEN:

Evaluate four-domain counterfactual behavior.

↓

THEN:

Use failure profiles to guide intervention generation and ranking.

↓

THEN:

Compare:

Unconstrained Counterfactual

vs

Ordinary Counterfactual

vs

Domain-Constrained Counterfactual

vs

Profile-Guided Domain-Constrained Counterfactual

↓

THEN:

Evaluate:

Validity

Actionability

Feasibility

Sparsity

Predicted risk reduction

Prediction transition rate

↓

THEN:

Perform statistical / repeated evaluation.

↓

THEN:

Validate novelty through literature review.

↓

THEN:

Finalize research framework and paper.

55. FINAL PROJECT GOAL

============================================================

The final platform should allow a user to:

1. Select a failure domain.

2. Enter domain-specific information.

3. Predict the likely outcome.

4. View prediction probability.

5. Understand relevant failure patterns.

6. Receive recommendations.

7. View improvement actions.

8. Explore counterfactual prevention scenarios.

9. Identify feasible model-based interventions.

10. Identify minimum effective model-based changes.

11. Perform What-If simulations.

12. Observe how changing inputs affects the trained model's

    predicted outcome.

13. Compare predicted risk before and after an intervention.

14. Use the system as a preventive decision-support platform.

The research system should additionally demonstrate:

FAILURE PREDICTION

FAILURE PROFILE IDENTIFICATION

DOMAIN CONSTRAINTS

ACTIONABLE COUNTERFACTUAL GENERATION

RISK-REDUCTION EVALUATION

PREVENTIVE DECISION SUPPORT

FINAL SYSTEM NAME:

Failure Analytics and Decision Support System Using Machine Learning Techniques

PROPOSED RESEARCH FRAMEWORK:

Domain-Constrained Failure Intelligence System (DC-FIS)

============================================================

LATEST COMPLETED WORK — 20 SEPTEMBER 2026

============================================================

The latest development session completed and verified the following:

Domain-aware counterfactual constraints were implemented in:

backend/counterfactual/constraint_engine.py

Training-data-derived candidate sampling was implemented in:

backend/counterfactual/candidate_sampler.py

The counterfactual generator was updated to use actionable
features, validate feasible changes, calculate predicted risk
reduction, and distinguish class transitions from risk reduction
without transition.

K-Means failure-profile analysis was implemented in:

backend/analytics/failure_profiles.py

New API endpoints were added and tested:

GET /profiles/{domain}

POST /profiles/{domain}/identify

Student profile analysis was successfully verified. The current
test case was assigned to Profile 2, which contains 42 records and
has an observed failure rate of 88.1% (37 failures and 5
non-failures).

The profile-identification response returned a distance of
3.413755 for the current Student test case.

The latest Student counterfactual API test found no successful
class transition to Passed. The best tested intervention reduced
model-predicted failure probability only slightly, from approximately
95.7344% to 95.6633%.

These counterfactual and profile results are model-based and
descriptive. They do not establish causal relationships or guarantee
real-world failure prevention.

The current stopping point is after successful K-Means profile
generation and Student profile identification. Profile-guided
intervention generation is intentionally left for a later phase.

============================================================

============================================================

END OF PROJECT PROGRESS

============================================================
