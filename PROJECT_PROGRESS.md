AI FAILURE INTELLIGENCE PLATFORM
PROJECT PROGRESS / CONTINUATION DOCUMENT

============================================================

1. # PROJECT TITLE

AI Failure Intelligence Platform

Project Type:
AI-based Failure Analysis, Prediction and Preventive Decision Support System

# ============================================================ 2. PROJECT OBJECTIVE

The objective of the project is to build an AI-powered platform that
analyzes historical failures across multiple domains, predicts possible
failure outcomes, identifies similar historical cases, provides
recommendations, and determines what changes could reduce or prevent
failure risk.

The system is designed as a:

"Failure Intelligence and Preventive Decision Support Platform"

rather than only a failure prediction model.

# ============================================================ 3. SUPPORTED DOMAINS

The platform currently works with four domains:

1. Student
2. Software
3. Jobs
4. Projects

# ============================================================ 4. OVERALL SYSTEM ARCHITECTURE

Historical Failure Data
↓
Data Collection
↓
Data Standardization
↓
Data Preprocessing
↓
Classification + Clustering
↓
Failure Analytics
↓
Recommendation Engine
↓
Counterfactual Failure Prevention
↓
What-If Simulation
↓
FastAPI Backend
↓
React Dashboard
↓
Preventive Decision Support

# ============================================================ 5. STANDARD DATA SCHEMA

All four datasets were converted into a common schema:

Domain
Failure_Type
Severity
Score
Description

---

## 5.1 STUDENT DATASET

Domain:
Student

Failure_Type:
Exam Failure if G3 < 10
Passed if G3 >= 10

Severity:
Failures

Score:
G3

Description:
Absences + Study Time

---

## 5.2 SOFTWARE DATASET

Domain:
Software

Failure_Type:
rs

Severity:
Priority mapping:

P1 = 5
P2 = 4
P3 = 3
P4 = 2
P5 = 1
-- = 0

Score:
0.0

Description:
sd

---

## 5.3 JOBS DATASET

Domain:
Jobs

Failure_Type:
Selected if shortlisted = Yes
Rejected if shortlisted = No

Severity:
skills_match_score

Score:
skills_match_score

Description:
Experience + years

---

## 5.4 PROJECT DATASET

Domain:
Projects

Failure_Type:
Status

Severity:
Completion%

Score:
Completion%

Description:
Project Name

# ============================================================ 6. CURRENT PROJECT STRUCTURE

AI-Failure-Intelligence-Platform/

backend/
│
├── ml/
│ ├── classifier.py
│ ├── clustering.py
│ ├── evaluator.py
│ └── trainer.py
│
├── services/
│ └── preprocessing.py
│
├── recommendation/
│ ├── **init**.py
│ ├── templates.py
│ ├── rules.py
│ └── recommender.py
│
├── counterfactual/
│ ├── **init**.py
│ └── generator.py
│
├── what_if/
│ ├── **init**.py
│ └── simulator.py
│
└── api.py

models/
├── best_classifier.pkl
├── kmeans.pkl
├── scaler.pkl
└── encoders.pkl

scripts/
├── test_recommendation.py
├── test_counterfactual.py
└── test_what_if.py

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

# ============================================================ 7. DATA COLLECTION

STATUS: COMPLETED

Historical datasets have been collected for:

- Student failures
- Software failures
- Job/recruitment outcomes
- Project outcomes

# ============================================================ 8. DATA STANDARDIZATION

STATUS: COMPLETED

All four datasets were transformed into the common schema:

Domain
Failure_Type
Severity
Score
Description

This allows the different failure domains to be processed by a
common machine learning pipeline.

# ============================================================ 9. DATA PREPROCESSING

STATUS: COMPLETED

The preprocessing pipeline includes:

- Data cleaning
- Missing value handling
- Numerical preprocessing
- Categorical encoding
- Feature scaling

Missing values:

- Numerical columns use median values.
- Categorical columns use "Unknown".

Categorical values are encoded using LabelEncoder.

The preprocessing system saves:

scaler.pkl
encoders.pkl

The encoder file contains:

Domain encoder
Failure_Type encoder
Description encoder

Important:

The existing preprocessing and ML pipeline should NOT be unnecessarily
rewritten or refactored at this stage.

# ============================================================ 10. CLASSIFICATION

STATUS: COMPLETED

Classification models were trained and evaluated.

Models include:

- Logistic Regression
- Decision Tree
- Random Forest

The best classifier is selected based on accuracy.

The selected model is saved as:

models/best_classifier.pkl

The classifier currently uses:

Domain
Severity
Score
Description

to predict:

Failure_Type

# ============================================================ 11. MODEL EVALUATION

STATUS: COMPLETED

The classification models were evaluated using performance metrics,
including accuracy.

The best-performing classifier was selected and saved for use by the
application.

# ============================================================ 12. K-MEANS CLUSTERING

STATUS: COMPLETED

K-Means clustering was implemented to identify groups of similar
failure cases.

Different values of K were evaluated using silhouette score.

The best K value was selected and the clustering model was saved as:

models/kmeans.pkl

# ============================================================ 13. FAILURE ANALYTICS

STATUS: COMPLETED

Failure analytics has been integrated into the recommendation workflow.

The system can analyze:

- Predicted failure type
- Failure probability
- Failure cluster
- Historical failure patterns
- Similar historical failures
- Domain information

# ============================================================ 14. RECOMMENDATION ENGINE

STATUS: COMPLETED AND TESTED

Files:

backend/recommendation/
├── **init**.py
├── templates.py
├── rules.py
└── recommender.py

The recommendation engine provides:

- Failure prediction
- Probability
- Cluster information
- Historical analysis
- Similar failure cases
- Recommendations
- Improvement actions

Example Student Input:

{
"Domain": "Student",
"Severity": 4,
"Score": 8,
"Description": "Absences + Study Time"
}

Example Prediction:

Failure Type:
Exam Failure

Cluster:
2

Example recommendations include:

- Increase the final academic score before the next examination.
- Previous failures are present; focus on subjects/areas where
  difficulties occurred.
- Improve academic performance before next exam.
- Increase study time and follow consistent schedule.
- Reduce avoidable absences and attend regularly.
- Review previous weak areas and focus on targeted improvement.

Example improvement actions:

- Improve academic score
- Reduce previous failures
- Increase study time
- Reduce avoidable absences

Test Status:

SUCCESSFUL

# ============================================================ 15. COUNTERFACTUAL FAILURE PREVENTION

STATUS: COMPLETED AND TESTED

File:

backend/counterfactual/generator.py

Purpose:

The counterfactual module answers:

"What changes could cause the predicted failure outcome to change?"

The system generates alternative scenarios by changing:

- Score
- Severity

It then checks whether the prediction changes.

The system identifies:

1. Original prediction
2. Counterfactual scenarios
3. Minimum effective change
4. Highest-confidence scenario
5. Recommended changes

Example input:

{
"Domain": "Student",
"Severity": 4,
"Score": 8,
"Description": "Absences + Study Time"
}

Original prediction:

Exam Failure

Probability:

0.48898141677472046

Counterfactual examples:

Score 9
→ Passed
→ Probability: 0.506483515291659

Score 10
→ Passed
→ Probability: 0.5580322221043557

Score 9 + Severity 3
→ Passed
→ Probability: 0.5246562983356684

Severity 2
→ Passed
→ Probability: 0.4910010874868412

Score 11
→ Passed
→ Probability: 0.6082647864741663

Minimum effective change:

Score 8 → Score 9

Prediction:

Passed

Probability:

0.506483515291659

Highest-confidence scenario:

Score 18 + Severity 1

Prediction:

Passed

Probability:

0.888672052892537

Recommended change:

Increase score from 8 toward 9.

Important:

The counterfactual module is positioned as a preventive decision-support
component. It should not be described as an entirely new invention of
counterfactual explanations. The project novelty comes from integrating
multi-domain failure analysis, prediction, clustering, historical
analytics, recommendations, counterfactual prevention, and interactive
what-if simulation into one platform.

# ============================================================ 16. WHAT-IF SIMULATOR

STATUS: COMPLETED AND TESTED

Files:

backend/what_if/
├── **init**.py
└── simulator.py

Purpose:

The What-If Simulator allows the user to manually change input values
and immediately see how the prediction changes.

Example:

Original:

Score = 8

What-If:

Score = 9

Result:

Original prediction:
Exam Failure

Original probability:
48.90%

New prediction:
Passed

New probability:
50.65%

Probability change:

+1.75 percentage points

Prediction changed:

True

This allows users to interactively test possible interventions.

# ============================================================ 17. FASTAPI BACKEND

STATUS: COMPLETED AND TESTED

FastAPI has been installed and configured.

Swagger documentation is available through:

/docs

Current backend file:

backend/api.py

Application title:

AI Failure Intelligence Platform

Version:

1.0

# ============================================================ 18. CURRENT API ENDPOINTS

The backend currently provides:

GET /health

POST /predict

POST /recommend

POST /counterfactual

POST /what-if

---

## 18.1 HEALTH ENDPOINT

Endpoint:

GET /health

Purpose:

Checks whether the API is running.

Successful response:

{
"status": "ok",
"message": "AI Failure Intelligence API is running"
}

---

## 18.2 PREDICT ENDPOINT

Endpoint:

POST /predict

Purpose:

Predicts the failure type and probability.

Example input:

{
"Domain": "Student",
"Severity": 4,
"Score": 8,
"Description": "Absences + Study Time"
}

Example result:

Failure Type:
Exam Failure

Probability:
0.48898141677472046

The endpoint also returns class probabilities for all learned
failure classes.

---

## 18.3 RECOMMEND ENDPOINT

Endpoint:

POST /recommend

Purpose:

Provides:

- Prediction
- Probability
- Cluster
- Historical analysis
- Similar failures
- Recommendations
- Improvement actions

STATUS:

SUCCESSFUL

---

## 18.4 COUNTERFACTUAL ENDPOINT

Endpoint:

POST /counterfactual

Purpose:

Determines what changes could potentially change the predicted outcome.

Supports optional:

desired_prediction

STATUS:

SUCCESSFUL

---

## 18.5 WHAT-IF ENDPOINT

Endpoint:

POST /what-if

Purpose:

Allows manual simulation of changes to the input.

Example:

{
"Domain": "Student",
"Severity": 4,
"Score": 8,
"Description": "Absences + Study Time",
"changes": {
"Score": 9
}
}

STATUS:

SUCCESSFUL

# ============================================================ 19. FASTAPI TESTING STATUS

All current backend endpoints have been tested through Swagger.

Tested:

[✓] GET /health
[✓] POST /predict
[✓] POST /recommend
[✓] POST /counterfactual
[✓] POST /what-if

Backend status:

WORKING

# ============================================================ 20. CURRENT WORKING SYSTEM

At this point, the project has progressed beyond a simple ML model.

The current working backend can:

1. Accept failure-related input.
2. Predict a failure outcome.
3. Calculate prediction probabilities.
4. Identify a failure cluster.
5. Analyze historical failure information.
6. Find similar failure cases.
7. Generate recommendations.
8. Suggest improvement actions.
9. Generate counterfactual scenarios.
10. Identify minimum effective changes.
11. Run interactive what-if simulations.
12. Expose all major functionality through REST APIs.

# ============================================================ 21. CURRENT ARCHITECTURE STATUS

COMPLETED:

[✓] Data Collection
[✓] Data Standardization
[✓] Data Preprocessing
[✓] Classification
[✓] Model Evaluation
[✓] K-Means Clustering
[✓] Failure Analytics
[✓] Recommendation Engine
[✓] Counterfactual Failure Prevention
[✓] What-If Simulator
[✓] FastAPI Backend
[✓] Swagger API Testing

PENDING:

[ ] React Dashboard
[ ] Frontend/API Integration
[ ] Full Integration Testing
[ ] End-to-End Testing
[ ] UI Improvements
[ ] Deployment
[ ] Final Documentation
[ ] Final Project Demonstration

# ============================================================ 22. NEXT DEVELOPMENT PHASE

NEXT PHASE:

REACT DASHBOARD

Planned implementation order:

1. Check Node.js and npm installation.

Commands:

node --version
npm --version

2. Create the React frontend.

3. Verify that the React application runs successfully.

4. Connect React frontend to:

POST /predict

5. Display prediction results.

6. Connect and display:

POST /recommend

7. Add recommendation and improvement-action sections.

8. Connect and display:

POST /counterfactual

9. Add counterfactual scenario visualization.

10. Connect:

POST /what-if

11. Add interactive What-If controls.

12. Improve dashboard UI.

13. Perform complete frontend-backend integration testing.

14. Perform end-to-end testing.

15. Prepare deployment.

16. Complete final documentation.

17. Prepare project demonstration.

# ============================================================ 23. IMPORTANT DEVELOPMENT RULES

Do NOT unnecessarily rewrite the existing ML pipeline.

Use the existing trained model files:

models/best_classifier.pkl
models/kmeans.pkl
models/scaler.pkl
models/encoders.pkl

The current ML pipeline is already working.

Future development should focus on:

- Frontend
- API integration
- User experience
- Testing
- Deployment
- Documentation

Each development step should be tested before moving to the next step.

# ============================================================ 24. CURRENT DEVELOPMENT COMMANDS

Backend:

uvicorn backend.api:app --reload

Swagger:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/health

The FastAPI server should remain running while the React frontend is
developed in a separate terminal.

# ============================================================ 25. PROJECT NOVELTY / CONTRIBUTION

The project is not positioned as merely another classification model.

The main contribution is the integration of:

- Multi-domain failure analysis
- Failure prediction
- Failure clustering
- Historical failure analytics
- Similar-case analysis
- Recommendation generation
- Counterfactual failure prevention
- Minimum effective intervention identification
- Interactive What-If simulation
- REST API
- Preventive decision support dashboard

The system therefore moves from:

"Predict whether failure will happen"

towards:

"Understand why failure is likely, learn from historical failures,
recommend improvements, and explore what changes could reduce the
failure risk."

# ============================================================ 26. CURRENT PROJECT STATUS

PROJECT STATUS:

BACKEND + AI CORE = COMPLETED

The AI and backend portion of the platform is currently working and
has been tested successfully.

The next major task is:

REACT FRONTEND DEVELOPMENT

# ============================================================ 27. IMMEDIATE NEXT STEP

Open a second PowerShell terminal while keeping FastAPI running.

Navigate to:

C:\Users\ELCOT\AI-Failure-Intelligence-Platform

Activate the virtual environment if required.

Then check:

node --version
npm --version

After confirming Node.js and npm are available, create the React
frontend and test that it runs successfully before connecting it to
the FastAPI backend.

# ============================================================ 28. FINAL PROJECT GOAL

The final platform should allow a user to:

1. Select a failure domain.
2. Enter failure-related information.
3. Predict the likely outcome.
4. View prediction probability.
5. Understand historical failure patterns.
6. View similar failures.
7. Receive recommendations.
8. View improvement actions.
9. Explore counterfactual prevention scenarios.
10. Identify the minimum effective intervention.
11. Perform What-If simulations.
12. Understand how changing inputs can affect the predicted outcome.

Final system:

AI Failure Intelligence and Preventive Decision Support Platform

============================================================
CURRENT POSITION IN PROJECT
============================================================

DATA + ML:
COMPLETED ✓

ANALYTICS:
COMPLETED ✓

RECOMMENDATION:
COMPLETED ✓

COUNTERFACTUAL:
COMPLETED ✓

WHAT-IF:
COMPLETED ✓

FASTAPI:
COMPLETED ✓

REACT DASHBOARD:
NEXT STEP →

INTEGRATION TESTING:
PENDING

DEPLOYMENT:
PENDING

FINAL DOCUMENTATION:
PENDING

PROJECT DEMONSTRATION:
PENDING
