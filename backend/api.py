from fastapi import FastAPI
from pydantic import BaseModel

from backend.what_if.simulator import WhatIfSimulator
from backend.recommendation.recommender import Recommender
from backend.counterfactual.generator import CounterfactualGenerator


app = FastAPI(
    title="AI Failure Intelligence Platform",
    version="1.0"
)


class FailureInput(BaseModel):
    Domain: str
    Severity: float
    Score: float
    Description: str


class CounterfactualInput(FailureInput):
    desired_prediction: str | None = None

class WhatIfInput(FailureInput):
    changes: dict

counterfactual = CounterfactualGenerator()
recommendation = Recommender()
what_if = WhatIfSimulator()

@app.get("/health")
def health():
    return {
        "status": "ok",
        "message": "AI Failure Intelligence API is running"
    }


@app.post("/predict")
def predict(data: FailureInput):

    result = counterfactual.predict(
        data.model_dump()
    )

    return result

@app.post("/recommend")
def recommend(data: FailureInput):

    result = recommendation.recommend(
        data.model_dump()
    )

    return result

@app.post("/counterfactual")
def counterfactual_analysis(data: CounterfactualInput):

    return counterfactual.generate(
        data.model_dump(
            exclude={"desired_prediction"}
        ),
        data.desired_prediction
    )

@app.post("/what-if")
def what_if_analysis(data: WhatIfInput):

    original = data.model_dump(
        exclude={"changes"}
    )

    return what_if.simulate(
        original,
        data.changes
    )