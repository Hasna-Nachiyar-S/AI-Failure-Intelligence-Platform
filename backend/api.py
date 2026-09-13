from typing import Optional, Any

from fastapi import (
    FastAPI,
    HTTPException
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)

from backend.ml.domain_model_manager import (
    DomainModelManager
)

from backend.recommendation.recommender import (
    Recommender
)

from backend.counterfactual.generator import (
    CounterfactualGenerator
)

from backend.what_if.simulator import (
    WhatIfSimulator
)


app = FastAPI(
    title="AI Failure Intelligence Platform",
    version="1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


manager = DomainModelManager()

recommender = Recommender()

counterfactual = CounterfactualGenerator()

what_if = WhatIfSimulator()


class FailureInput(BaseModel):

    model_config = ConfigDict(
        extra="allow"
    )

    Domain: str

    Severity: Optional[float] = None
    Score: Optional[float] = None
    Description: Optional[str] = None

    # Student

    absences: Optional[float] = None
    studytime: Optional[float] = None
    failures: Optional[float] = None
    G1: Optional[float] = None
    G2: Optional[float] = None

    # Software

    pr: Optional[Any] = None
    cl: Optional[Any] = None
    pd: Optional[Any] = None
    co: Optional[Any] = None
    rp: Optional[Any] = None
    os: Optional[Any] = None
    bs: Optional[Any] = None
    bsr: Optional[Any] = None
    re: Optional[Any] = None
    at: Optional[Any] = None

    # Jobs

    years_experience: Optional[float] = None

    skills_match_score: Optional[float] = None

    education_level: Optional[Any] = None

    project_count: Optional[float] = None

    resume_length: Optional[float] = None

    github_activity: Optional[float] = None

    # Projects

    Complexity: Optional[Any] = None

    Project_Type: Optional[Any] = None

    Region: Optional[Any] = None

    Department: Optional[Any] = None

    Project_Cost: Optional[float] = None

    Project_Benefit: Optional[float] = None

    Completion: Optional[float] = None

    Phase: Optional[Any] = None

    Year: Optional[float] = None

    Month: Optional[float] = None


class WhatIfInput(FailureInput):

    changes: dict = Field(
        default_factory=dict
    )


@app.get("/health")
def health():

    return {
        "status": "ok",
        "message":
            "AI Failure Intelligence API is running"
    }


@app.post("/predict")
def predict(data: FailureInput):

    payload = data.model_dump()

    try:

        return manager.predict(
            data.Domain,
            payload
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.post("/recommend")
def recommend(data: FailureInput):

    payload = data.model_dump()

    try:

        return recommender.recommend(
            payload
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.post("/counterfactual")
def generate_counterfactual(
    data: FailureInput
):

    payload = data.model_dump()

    try:

        return counterfactual.generate(
            payload
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.post("/what-if")
def simulate_what_if(
    data: WhatIfInput
):

    payload = data.model_dump()

    changes = payload.pop(
        "changes",
        {}
    )

    try:

        return what_if.simulate(
            payload,
            changes
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )