============================================================
AI FAILURE INTELLIGENCE PLATFORM
PROJECT PROGRESS / CONTINUATION DOCUMENT
============================================================

PROJECT TITLE
AI Failure Intelligence Platform

PROJECT TYPE
AI-based Failure Analysis, Prediction and Preventive
Decision Support System

============================================================

1. # PROJECT OBJECTIVE

The objective of the project is to build an AI-powered platform
that analyzes historical failures across multiple domains,
predicts possible failure outcomes, provides recommendations,
generates counterfactual prevention scenarios, and allows
interactive What-If simulation.

The system is designed as:

"Failure Intelligence and Preventive Decision Support Platform"

rather than only a failure prediction model.

============================================================ 2. SUPPORTED DOMAINS
============================================================

The platform supports four domains:

1. Student
2. Software
3. Jobs
4. Projects

============================================================ 3. FINAL SYSTEM CONCEPT
============================================================

The platform moves from:

"Predict whether failure will happen"

towards:

"Understand the predicted outcome, provide recommendations,
explore possible interventions, and test how changes in
inputs affect the model prediction."

Important technical wording:

Counterfactual and What-If results are model-based scenario
analyses. They should NOT be described as proof of causation.

Correct wording:

"According to the trained ML model, changing a selected
feature changes the predicted outcome."

============================================================ 4. CURRENT SYSTEM ARCHITECTURE
============================================================

Historical Failure Data
↓
Data Collection
↓
Data Standardization
↓
Data Preprocessing
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
Recommendation
↓
Counterfactual Prevention
↓
What-If Simulation
↓
Preventive Decision Support

============================================================ 5. CURRENT ML ARCHITECTURE
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
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Student │ Software │ Jobs │ Projects │
│ model.pkl │ model.pkl │ model.pkl │ model.pkl │
└──────────────┴──────────────┴──────────────┴──────────────┘
↓
Domain-Specific Prediction
↓
Recommendation / Counterfactual / What-If

This change was necessary because the original common input
fields did not represent the actual important features of
each domain.

============================================================ 6. ACTUAL DATASET FEATURES
============================================================

6.1 STUDENT

Important actual features include:

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

---

6.2 SOFTWARE

Important actual features include:

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

rs is used as the target and must not be used as an input
feature.

Also:

bugID is an ID and should not be treated as a bug count.

at contains values such as usernames in the available data
and must not automatically be described as Test Coverage.

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

============================================================ 7. DATA COLLECTION
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

============================================================ 8. DATA STANDARDIZATION
============================================================

STATUS: COMPLETED

The original project defined a common conceptual schema:

- Domain
- Failure_Type
- Severity
- Score
- Description

However, the final ML prediction system now uses
domain-specific features from the actual datasets.

This prevents the frontend inputs from becoming only cosmetic
fields.

============================================================ 9. DATA PREPROCESSING
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

============================================================ 10. DOMAIN-SPECIFIC MODEL TRAINING
============================================================

File:

backend/ml/domain_trainer.py

Purpose:

Train one ML model for each supported domain using actual
domain-specific features.

Models generated:

models/student_model.pkl
models/software_model.pkl
models/jobs_model.pkl
models/projects_model.pkl

Training results:

Student accuracy:
0.8861

Software accuracy:
0.8079

Jobs accuracy:
0.8983

Projects accuracy:
0.6000

Training status:

SUCCESSFUL

============================================================ 11. DOMAIN MODEL MANAGER
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

============================================================ 12. STUDENT MODEL TESTING
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

Probability:

95.5%

Class probabilities:

Exam Failure = 95.5%
Passed = 4.5%

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

Probability:

99.5%

Class probabilities:

Exam Failure = 0.5%
Passed = 99.5%

This confirmed that actual domain-specific inputs affect
the ML prediction.

============================================================ 13. FASTAPI BACKEND
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

============================================================ 14. CURRENT API ENDPOINTS
============================================================

GET /health

POST /predict

POST /recommend

POST /counterfactual

POST /what-if

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

- domain
- failure_type
- probability
- class_probabilities

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

Generates alternative input scenarios and determines whether
the model prediction changes.

Returns:

- original_input
- original_prediction
- desired_prediction
- counterfactuals
- minimum_effective_change
- highest_confidence_scenario
- recommended_changes

Status:

SUCCESSFUL

---

14.5 POST /what-if

Purpose:

Allows the user to manually change an input feature and run
the model again.

Returns:

- original_input
- changes
- new_input
- original_prediction
- new_prediction
- original_probability
- new_probability
- probability_change
- class_probabilities_before
- class_probabilities_after
- prediction_changed

Status:

SUCCESSFUL

============================================================ 15. RECOMMENDATION ENGINE
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

This should be improved later if required.

============================================================ 16. COUNTERFACTUAL FAILURE PREVENTION
============================================================

File:

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

99.50%

Target prediction:

Exam Failure

Minimum effective change:

G2

Change:

G2 = 5

New prediction:

Exam Failure

Probability:

78.40%

Highest-confidence scenario:

G1 + G2 + absences

Change:

G1 = 5
G2 = 5
absences = 20

Prediction:

Exam Failure

Probability:

98.50%

Status:

SUCCESSFUL

Important:

This is model-based counterfactual analysis, not a causal
claim.

============================================================ 17. WHAT-IF SIMULATION
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

============================================================ 18. REACT FRONTEND
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

============================================================ 19. FRONTEND DOMAIN INPUTS
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

============================================================ 20. FRONTEND WHAT-IF CONTROLS
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

============================================================ 21. CURRENT FRONTEND STATUS
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

============================================================ 22. CURRENT PROJECT STRUCTURE
============================================================

AI-Failure-Intelligence-Platform/

├── .github/
│
├── .venv/
│
├── app/
│
├── backend/
│ │
│ ├── ml/
│ │ ├── classifier.py
│ │ ├── clustering.py
│ │ ├── evaluator.py
│ │ ├── trainer.py
│ │ ├── domain_trainer.py
│ │ └── domain_model_manager.py
│ │
│ ├── services/
│ │ └── preprocessing.py
│ │
│ ├── recommendation/
│ │ ├── **init**.py
│ │ ├── templates.py
│ │ ├── rules.py
│ │ └── recommender.py
│ │
│ ├── counterfactual/
│ │ ├── **init**.py
│ │ ├── generator.py
│ │ └── generator_backup.py
│ │
│ ├── what_if/
│ │ ├── **init**.py
│ │ └── simulator.py
│ │
│ ├── api.py
│ └── api_backup.py
│
├── data/
│ ├── student/
│ ├── software/
│ ├── jobs/
│ └── projects/
│
├── docs/
│
├── frontend/
│ ├── src/
│ │ ├── App.jsx
│ │ ├── App.css
│ │ └── main.jsx
│ └── ...
│
├── models/
│ ├── student_model.pkl
│ ├── software_model.pkl
│ ├── jobs_model.pkl
│ ├── projects_model.pkl
│ │
│ ├── best_classifier.pkl
│ ├── kmeans.pkl
│ ├── scaler.pkl
│ ├── encoders.pkl
│ │
│ └── backup/
│
├── notebooks/
│
├── scripts/
│
├── tests/
│
├── PROJECT_PROGRESS.md
├── README.md
└── requirements.txt

============================================================ 23. BACKUP FILES
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

============================================================ 24. IMPORTANT ARCHITECTURE CLEANUP NOTE
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

The next cleanup task should be:

1. Identify all Python files.
2. Check imports and references.
3. Identify files still used by the current API.
4. Identify obsolete model files.
5. Identify obsolete scripts.
6. Identify duplicate backup files.
7. Remove only files confirmed to be unnecessary.
8. Run backend tests again.
9. Run frontend tests again.
10. Confirm the application still works.

============================================================ 25. OLD MODEL FILES
============================================================

The following files belong to the older architecture:

models/best_classifier.pkl
models/kmeans.pkl
models/scaler.pkl
models/encoders.pkl

They should NOT be deleted immediately.

The current domain-specific models are:

models/student_model.pkl
models/software_model.pkl
models/jobs_model.pkl
models/projects_model.pkl

The old models should first be checked for remaining usage.

============================================================ 26. IMPORTANT DEVELOPMENT RULES
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

============================================================ 27. CURRENT DEVELOPMENT COMMANDS
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

Node version confirmed:

v24.14.1

npm version confirmed:

11.11.0

============================================================ 28. CURRENT TESTING STATUS
============================================================

Backend:

[✓] FastAPI starts
[✓] CORS configured
[✓] /health
[✓] /predict
[✓] /recommend
[✓] /counterfactual
[✓] /what-if

ML:

[✓] Student model
[✓] Software model
[✓] Jobs model
[✓] Projects model

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

============================================================ 29. CURRENT PROJECT STATUS
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

FULL FOUR-DOMAIN TESTING:

PENDING

ARCHITECTURE CLEANUP:

PENDING

UI POLISH:

PENDING

DEPLOYMENT:

PENDING

FINAL DOCUMENTATION:

PENDING

FINAL PROJECT DEMONSTRATION:

PENDING

============================================================ 30. NEXT DEVELOPMENT PHASE
============================================================

NEXT TASK:

SAFE ARCHITECTURE AUDIT AND CLEANUP

Do NOT immediately delete files.

First:

1. Inspect current project structure.
2. Identify imports.
3. Identify obsolete code.
4. Identify old model dependencies.
5. Identify duplicate files.
6. Confirm which files are actually required.
7. Remove unnecessary files only after verification.

---

AFTER CLEANUP:

Test all four domains.

Student:

- Prediction
- Recommendation
- Counterfactual
- What-If

Software:

- Prediction
- Recommendation
- Counterfactual
- What-If

Jobs:

- Prediction
- Recommendation
- Counterfactual
- What-If

Projects:

- Prediction
- Recommendation
- Counterfactual
- What-If

---

THEN:

- UI improvements
- Error handling improvements
- Loading indicators
- Better result visualization
- Validation of domain inputs
- Final integration testing
- End-to-end testing
- Documentation
- Project demonstration
- Deployment

============================================================ 31. PROJECT NOVELTY / CONTRIBUTION
============================================================

The project is not positioned as merely another classification
model.

The main contribution is the integration of:

- Multi-domain failure analysis
- Domain-specific failure prediction
- Failure clustering
- Historical failure analytics
- Similar-case analysis
- Recommendation generation
- Improvement actions
- Counterfactual failure prevention
- Minimum effective intervention identification
- Interactive What-If simulation
- REST API
- React preventive decision-support dashboard

The system therefore moves from:

"Predict whether failure will happen"

towards:

"Understand the predicted outcome, provide recommendations,
explore possible interventions, and interactively test how
changes affect the model prediction."

============================================================ 32. CURRENT CONFIRMED WORKING EXAMPLE
============================================================

STUDENT DOMAIN

Original:

absences = 2
studytime = 4
failures = 0
G1 = 18
G2 = 18

Prediction:

Passed

Probability:

99.50%

Counterfactual:

G2 = 5

Prediction:

Exam Failure

Probability:

78.40%

What-If:

G2 = 5

Frontend console confirmed:

What-If data correctly received.

What-If changes correctly created:

{
"G2": 5
}

What-If request correctly sent to backend.

STATUS:

WORKING CORRECTLY ✓

============================================================ 33. IMPORTANT CURRENT POSITION
============================================================

The project has successfully moved from the original
single-model/common-feature architecture to a domain-specific
ML architecture.

The most important functionality is now working:

DOMAIN INPUT
↓
DOMAIN-SPECIFIC ML MODEL
↓
PREDICTION
↓
RECOMMENDATION
↓
COUNTERFACTUAL
↓
WHAT-IF

The next step is NOT to rebuild the system.

The next step is to:

AUDIT → CLEAN → TEST → POLISH → DOCUMENT → DEMONSTRATE

============================================================ 34. TOMORROW'S STARTING POINT
============================================================

When continuing this project, start here:

"Continue the AI Failure Intelligence Platform from the latest
progress.

The domain-specific ML architecture is working.

Student prediction is tested.

Counterfactual Prevention is working.

What-If Simulation is working.

The React frontend is connected to FastAPI.

The latest confirmed What-If test successfully sent:

G2 = 5

for a Student input where:

G2 = 18

The next task is a SAFE ARCHITECTURE AUDIT AND CLEANUP.

Do not delete files blindly.

First inspect imports, dependencies, old models, duplicate
files, and obsolete code.

Then test all four domains end-to-end:

Student
Software
Jobs
Projects

After that, continue with UI polishing, final integration
testing, documentation, deployment, and project demonstration."

============================================================ 35. FINAL PROJECT GOAL
============================================================

The final platform should allow a user to:

1. Select a failure domain.
2. Enter domain-specific information.
3. Predict the likely outcome.
4. View prediction probability.
5. Receive recommendations.
6. View improvement actions.
7. Explore counterfactual prevention scenarios.
8. Identify minimum effective model-based changes.
9. Perform What-If simulations.
10. Understand how changing inputs affects the trained model's
    predicted outcome.
11. Use the system as a preventive decision-support platform.

FINAL SYSTEM NAME:

AI Failure Intelligence and Preventive Decision Support Platform

============================================================
END OF PROJECT PROGRESS
============================================================
