# AI Failure Intelligence Platform

A multi-domain machine-learning decision-support system for failure prediction,
recommendation, What-If simulation, domain-constrained counterfactual analysis,
and historical failure-profile guidance.

## Domains

- **Student** — Exam Failure / Passed
- **Software** — Mozilla issue-resolution classes
- **Jobs** — Selected / Rejected
- **Projects** — Project status classes

## Production architecture

```text
React frontend
      |
      v
FastAPI API
      |
      +--> Domain Model Manager
      |      +--> Student RF
      |      +--> Software RF
      |      +--> Jobs RF
      |      +--> Projects RF
      |
      +--> Recommendation Engine
      +--> What-If Simulator
      +--> Domain-Constrained Counterfactual Engine
      |       +--> Training-data candidate sampler
      |       +--> Constraint engine
      |       +--> Failure-profile guidance
      |
      +--> K-Means Failure Profiles
```

## API

Start the backend from the project root:

```powershell
.\venv\Scripts\activate
uvicorn backend.api:app --reload
```

Swagger UI:

`http://127.0.0.1:8000/docs`

Start the frontend in a second terminal:

```powershell
cd frontend
npm run dev
```

The Vite development server normally runs at:

`http://localhost:5173`

## Main endpoints

- `GET /health`
- `POST /predict`
- `POST /recommend`
- `POST /counterfactual`
- `POST /what-if`
- `GET /constraints/{domain}`
- `GET /profiles/{domain}`
- `POST /profiles/{domain}/identify`

## Counterfactual design

Counterfactuals are **model-based scenario analyses**, not causal estimates.

The production engine:

1. identifies the current prediction;
2. assigns the case to a historical K-Means failure profile;
3. prioritizes actionable features using profile differences/modes;
4. samples candidate values from the corresponding training dataset;
5. applies domain constraints;
6. evaluates every feasible scenario;
7. measures change in the original-class probability;
8. detects transitions to the domain's desired outcome.

Default desired outcomes are:

- Student → `Passed`
- Software → `FIXED`
- Jobs → `Selected`
- Projects → `Completed`

If the model already predicts the desired outcome, the counterfactual engine
reports `already_desired_outcome` rather than incorrectly counting an unchanged
prediction as a successful intervention.

## Production models

The API uses the controlled model artifacts in:

`backend/ml/models/`

Current production selection:

- Student → optimized RF
- Software → original RF
- Jobs → optimized RF
- Projects → optimized RF

The three-way model comparison artifacts remain available for research:

- Original RF
- Optimized RF
- Cleaned RF

See:

`backend/ml/model_comparison_results.csv`

## Validation and testing

Run Python syntax validation:

```powershell
python -m compileall backend scripts
```

Run the production smoke test:

```powershell
python scripts/system_smoke_test.py
```

The smoke test does not retrain models. It verifies all four domains across
prediction, recommendation, profile assignment, constraints, What-If
simulation, and counterfactual generation.

## Important research cautions

- Counterfactual risk reduction is not a causal effect.
- Historical failure profiles are descriptive clusters.
- Student `G1`/`G2` imply a prediction-time definition that must be stated in
  research reporting.
- Software target semantics and excluded records require explicit analysis.
- Projects is a small dataset and requires careful validation.
- Projects `Completion%` must be examined for prediction-time leakage.
- Model selection should not be based on accuracy alone.

## Project structure

```text
backend/
  analytics/
  counterfactual/
  ml/
  recommendation/
  services/
  what_if/
frontend/
data/
scripts/
notebooks/
```
