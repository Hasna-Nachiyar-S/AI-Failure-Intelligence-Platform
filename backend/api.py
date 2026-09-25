from typing import Optional, Any

from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    Response,
    Depends,
    Cookie,
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)

from backend.analytics.failure_profiles import (
    FailureProfileAnalyzer
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
from backend.counterfactual.constraint_engine import DomainConstraintEngine
from backend.auth import (
    SESSION_COOKIE,
    SESSION_MAX_AGE,
    authenticate,
    create_session,
    create_user,
    delete_session,
    get_dashboard,
    get_history,
    get_user_by_session,
    record_analysis,
)
import json


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
constraints = DomainConstraintEngine()

profile_analyzer = FailureProfileAnalyzer(
    n_clusters=3
)

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

    # Counterfactual controls
    profile_guided: Optional[bool] = True
    max_guided_features: Optional[int] = Field(default=2, ge=1, le=10)
    desired_prediction: Optional[str] = None


class WhatIfInput(FailureInput):

    changes: dict = Field(
        default_factory=dict
    )



class AuthSignup(BaseModel):
    full_name: str
    email: str
    password: str


class AuthLogin(BaseModel):
    email: str
    password: str


def current_user(session: Optional[str] = Cookie(default=None, alias=SESSION_COOKIE)):
    user = get_user_by_session(session)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required.")
    return user

DOMAIN_REQUIRED_FIELDS = {
    "Student": ["absences", "studytime", "failures", "G1", "G2"],
    "Software": ["pr", "cl", "pd", "co", "rp", "os", "bs", "bsr", "re", "at"],
    "Jobs": [
        "years_experience", "skills_match_score", "education_level",
        "project_count", "resume_length", "github_activity"
    ],
    "Projects": [
        "Complexity", "Project_Type", "Region", "Department",
        "Project_Cost", "Project_Benefit", "Completion", "Phase", "Year", "Month"
    ],
}


def validate_domain_payload(data: FailureInput, payload: dict) -> None:
    domain = str(data.Domain).strip().lower()
    aliases = {"student": "Student", "software": "Software", "jobs": "Jobs", "projects": "Projects"}
    if domain not in aliases:
        raise HTTPException(status_code=422, detail=f"Unsupported domain: {data.Domain}")

    canonical = aliases[domain]
    missing = [
        field for field in DOMAIN_REQUIRED_FIELDS[canonical]
        if payload.get(field) is None
    ]
    if missing:
        raise HTTPException(
            status_code=422,
            detail={"domain": canonical, "missing_fields": missing},
        )


@app.get("/health")
def health():

    return {
        "status": "ok",
        "message":
            "AI Failure Intelligence API is running"
    }


@app.post("/predict")
def predict(data: FailureInput, user: dict = Depends(current_user)):

    payload = data.model_dump()
    validate_domain_payload(data, payload)

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
def recommend(data: FailureInput, user: dict = Depends(current_user)):

    payload = data.model_dump()
    validate_domain_payload(data, payload)

    try:
        result = recommender.recommend(payload)
        prediction = result.get("prediction") or {}
        probability = prediction.get("probability")
        failure_type = prediction.get("failure_type")
        record_analysis(
            user["id"],
            str(data.Domain),
            failure_type,
            float(probability) if probability is not None else None,
            json.dumps(payload, default=str),
            json.dumps(result, default=str),
        )
        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/auth/me")
def auth_me(user: dict = Depends(current_user)):
    return user


@app.post("/auth/signup")
def auth_signup(data: AuthSignup, response: Response):
    full_name = data.full_name.strip()
    email = data.email.strip().lower()
    if len(full_name) < 2:
        raise HTTPException(status_code=422, detail="Please enter your full name.")
    if "@" not in email or "." not in email.split("@")[-1]:
        raise HTTPException(status_code=422, detail="Please enter a valid email address.")
    if len(data.password) < 8:
        raise HTTPException(status_code=422, detail="Password must be at least 8 characters.")

    try:
        user = create_user(full_name, email, data.password)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    token = create_session(user["id"])
    response.set_cookie(
        SESSION_COOKIE,
        token,
        max_age=SESSION_MAX_AGE,
        httponly=True,
        samesite="lax",
        secure=False,
    )
    return user


@app.post("/auth/login")
def auth_login(data: AuthLogin, response: Response):
    user = authenticate(data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password.")

    token = create_session(user["id"])
    response.set_cookie(
        SESSION_COOKIE,
        token,
        max_age=SESSION_MAX_AGE,
        httponly=True,
        samesite="lax",
        secure=False,
    )
    return {
        "id": user["id"],
        "full_name": user["full_name"],
        "email": user["email"],
        "created_at": user["created_at"],
    }


@app.post("/auth/logout")
def auth_logout(
    response: Response,
    session: Optional[str] = Cookie(default=None, alias=SESSION_COOKIE),
):
    delete_session(session)
    response.delete_cookie(SESSION_COOKIE)
    return {"message": "Logged out."}


@app.get("/dashboard")
def dashboard(user: dict = Depends(current_user)):
    return {
        "user": user,
        **get_dashboard(user["id"]),
    }


@app.get("/history")
def history(user: dict = Depends(current_user)):
    return get_history(user["id"])


@app.get("/constraints/{domain}")
def get_constraints(domain: str):
    try:
        return constraints.describe(domain)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/counterfactual")
def generate_counterfactual(
    data: FailureInput,
    user: dict = Depends(current_user),
):

    payload = data.model_dump()
    validate_domain_payload(data, payload)

    profile_guided = payload.pop("profile_guided", True)
    max_guided_features = payload.pop("max_guided_features", 2)
    desired_prediction = payload.pop("desired_prediction", None)

    try:

        return counterfactual.generate(
            payload,
            desired_prediction=desired_prediction,
            profile_guided=bool(profile_guided),
            max_guided_features=max_guided_features
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.post("/what-if")
def simulate_what_if(
    data: WhatIfInput,
    user: dict = Depends(current_user),
):

    payload = data.model_dump()
    validate_domain_payload(data, payload)

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

@app.get("/profiles/{domain}")
def get_failure_profiles(domain: str):

    try:

        return profile_analyzer.get_profiles(
            domain
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.post("/profiles/{domain}/identify")
def identify_failure_profile(
    domain: str,
    data: dict
):

    try:

        return profile_analyzer.predict_profile(
            domain,
            data
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )