import { useEffect, useMemo, useState } from "react";

const API = "http://localhost:8000";

const emptyResults = () => ({
  prediction: null,
  recommendation: null,
  counterfactual: null,
  whatIf: null,
});

function App() {
  const [screen, setScreen] = useState("loading");
  const [authMode, setAuthMode] = useState("login");
  const [user, setUser] = useState(null);
  const [authForm, setAuthForm] = useState({
    full_name: "",
    email: "",
    password: "",
  });
  const [authError, setAuthError] = useState("");
  const [dashboard, setDashboard] = useState(null);
  const [history, setHistory] = useState([]);
  const [domain, setDomain] = useState("Student");
  const [student, setStudent] = useState({
    absences: 10,
    studytime: 3,
    failures: 0,
    G1: 12,
    G2: 12,
  });
  const [software, setSoftware] = useState({
    pr: "P3",
    cl: "5",
    pd: "5",
    co: "5",
    rp: "5",
    os: "windows",
    bs: "5",
    bsr: "5",
    re: "user",
    at: "user",
  });
  const [jobs, setJobs] = useState({
    years_experience: 2,
    skills_match_score: 70,
    education_level: "Bachelor",
    project_count: 3,
    resume_length: 500,
    github_activity: 10,
  });
  const [projects, setProjects] = useState({
    Complexity: "Medium",
    Project_Type: "Software",
    Region: "Asia",
    Department: "IT",
    Project_Cost: 100000,
    Project_Benefit: 150000,
    Completion: 60,
    Phase: "Execution",
    Year: 2024,
    Month: 6,
  });
  const [results, setResults] = useState(emptyResults());
  const [whatIfValue, setWhatIfValue] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const api = async (path, options = {}) => {
    const response = await fetch(`${API}${path}`, {
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
      ...options,
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || "Request failed.");
    return data;
  };

  const loadDashboard = async () => {
    const data = await api("/dashboard");
    setDashboard(data);
    setUser(data.user);
    setHistory(await api("/history"));
  };

  useEffect(() => {
    api("/auth/me")
      .then(async (me) => {
        setUser(me);
        setScreen("dashboard");
        await loadDashboard();
      })
      .catch(() => setScreen("auth"));
  }, []);

  const update = (setter, key, value) =>
    setter((old) => ({ ...old, [key]: value }));

  const getData = () => {
    if (domain === "Student") return { Domain: domain, ...student };
    if (domain === "Software") return { Domain: domain, ...software };
    if (domain === "Jobs") return { Domain: domain, ...jobs };
    return { Domain: domain, ...projects };
  };

  const resetResults = () => {
    setResults(emptyResults());
    setError("");
  };

  const analyze = async () => {
    setLoading(true);
    resetResults();
    try {
      const result = await api("/recommend", {
        method: "POST",
        body: JSON.stringify(getData()),
      });
      setResults({
        prediction: result.prediction,
        recommendation: result,
        counterfactual: null,
        whatIf: null,
      });
      await loadDashboard();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const generateCounterfactual = async () => {
    setLoading(true);
    setError("");
    try {
      const result = await api("/counterfactual", {
        method: "POST",
        body: JSON.stringify(getData()),
      });
      setResults((old) => ({ ...old, counterfactual: result }));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const runWhatIf = async () => {
    if (whatIfValue === "" || !Number.isFinite(Number(whatIfValue))) {
      setError("Please enter a valid number.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const changes =
        domain === "Student"
          ? { G2: Number(whatIfValue) }
          : domain === "Jobs"
            ? { skills_match_score: Number(whatIfValue) }
            : domain === "Projects"
              ? { Completion: Number(whatIfValue) }
              : { cl: String(Number(whatIfValue)) };

      const result = await api("/what-if", {
        method: "POST",
        body: JSON.stringify({ ...getData(), changes }),
      });
      setResults((old) => ({ ...old, whatIf: result }));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const loginOrSignup = async (event) => {
    event.preventDefault();
    setAuthError("");
    try {
      const path = authMode === "login" ? "/auth/login" : "/auth/signup";
      const body =
        authMode === "login"
          ? { email: authForm.email, password: authForm.password }
          : authForm;
      const me = await api(path, {
        method: "POST",
        body: JSON.stringify(body),
      });
      setUser(me);
      setScreen("dashboard");
      await loadDashboard();
    } catch (err) {
      setAuthError(err.message);
    }
  };

  const logout = async () => {
    await api("/auth/logout", { method: "POST" }).catch(() => {});
    setUser(null);
    setDashboard(null);
    setHistory([]);
    setScreen("auth");
    setAuthForm({ full_name: "", email: "", password: "" });
  };

  const goDashboard = async () => {
    setError("");
    await loadDashboard();
    setScreen("dashboard");
  };

  const probability = results.prediction
    ? Number(results.prediction.probability || 0) * 100
    : null;

  const domainCount = useMemo(
    () =>
      dashboard?.domain_breakdown?.reduce((sum, item) => sum + item.count, 0) ||
      0,
    [dashboard],
  );

  const getWhatIfLabel = () =>
    domain === "Student"
      ? "New G2"
      : domain === "Jobs"
        ? "New Skills Match Score"
        : domain === "Projects"
          ? "New Completion %"
          : "New Complexity (numeric)";

  const renderStudent = () => (
    <>
      <Field label="Absences">
        <input
          type="number"
          value={student.absences}
          onChange={(e) =>
            update(setStudent, "absences", Number(e.target.value))
          }
        />
      </Field>
      <Field label="Study Time">
        <input
          type="number"
          min="1"
          max="4"
          value={student.studytime}
          onChange={(e) =>
            update(setStudent, "studytime", Number(e.target.value))
          }
        />
      </Field>
      <Field label="Previous Failures">
        <input
          type="number"
          min="0"
          value={student.failures}
          onChange={(e) =>
            update(setStudent, "failures", Number(e.target.value))
          }
        />
      </Field>
      <Field label="G1">
        <input
          type="number"
          min="0"
          max="20"
          value={student.G1}
          onChange={(e) => update(setStudent, "G1", Number(e.target.value))}
        />
      </Field>
      <Field label="G2">
        <input
          type="number"
          min="0"
          max="20"
          value={student.G2}
          onChange={(e) => update(setStudent, "G2", Number(e.target.value))}
        />
      </Field>
    </>
  );

  const renderSoftware = () => (
    <>
      {[
        ["Priority", "pr"],
        ["Complexity", "cl"],
        ["Dependencies", "pd"],
        ["Coupling", "co"],
        ["Risk", "rp"],
        ["Operating System", "os"],
        ["Bug Size", "bs"],
        ["Bug Severity", "bsr"],
        ["Reporter", "re"],
        ["Assigned To", "at"],
      ].map(([label, key]) => (
        <Field label={label} key={key}>
          <input
            value={software[key]}
            onChange={(e) => update(setSoftware, key, e.target.value)}
          />
        </Field>
      ))}
    </>
  );

  const renderJobs = () => (
    <>
      <Field label="Years Experience">
        <input
          type="number"
          value={jobs.years_experience}
          onChange={(e) =>
            update(setJobs, "years_experience", Number(e.target.value))
          }
        />
      </Field>
      <Field label="Skills Match Score">
        <input
          type="number"
          min="0"
          max="100"
          value={jobs.skills_match_score}
          onChange={(e) =>
            update(setJobs, "skills_match_score", Number(e.target.value))
          }
        />
      </Field>
      <Field label="Education Level">
        <input
          value={jobs.education_level}
          onChange={(e) => update(setJobs, "education_level", e.target.value)}
        />
      </Field>
      <Field label="Project Count">
        <input
          type="number"
          value={jobs.project_count}
          onChange={(e) =>
            update(setJobs, "project_count", Number(e.target.value))
          }
        />
      </Field>
      <Field label="Resume Length">
        <input
          type="number"
          value={jobs.resume_length}
          onChange={(e) =>
            update(setJobs, "resume_length", Number(e.target.value))
          }
        />
      </Field>
      <Field label="GitHub Activity">
        <input
          type="number"
          value={jobs.github_activity}
          onChange={(e) =>
            update(setJobs, "github_activity", Number(e.target.value))
          }
        />
      </Field>
    </>
  );

  const renderProjects = () => (
    <>
      {[
        ["Complexity", "Complexity"],
        ["Project Type", "Project_Type"],
        ["Region", "Region"],
        ["Department", "Department"],
        ["Project Cost", "Project_Cost"],
        ["Project Benefit", "Project_Benefit"],
        ["Completion %", "Completion"],
        ["Phase", "Phase"],
        ["Year", "Year"],
        ["Month", "Month"],
      ].map(([label, key]) => (
        <Field label={label} key={key}>
          <input
            type={
              [
                "Project_Cost",
                "Project_Benefit",
                "Completion",
                "Year",
                "Month",
              ].includes(key)
                ? "number"
                : "text"
            }
            value={projects[key]}
            onChange={(e) =>
              update(
                setProjects,
                key,
                [
                  "Project_Cost",
                  "Project_Benefit",
                  "Completion",
                  "Year",
                  "Month",
                ].includes(key)
                  ? Number(e.target.value)
                  : e.target.value,
              )
            }
          />
        </Field>
      ))}
    </>
  );

  if (screen === "loading")
    return <div className="loading-screen">Loading your workspace…</div>;

  if (screen === "auth") {
    return (
      <div className="auth-page">
        <div className="auth-brand">
          <span className="brand-mark">AI</span>
          <div>
            <strong>Failure Intelligence</strong>
            <small>Predict • Understand • Improve</small>
          </div>
        </div>
        <div className="auth-card">
          <div className="auth-copy">
            <p className="eyebrow">PERSONAL DECISION SUPPORT</p>
            <h1>
              {authMode === "login"
                ? "Welcome back."
                : "Create your workspace."}
            </h1>
            <p>
              {authMode === "login"
                ? "Sign in to continue your failure analysis history."
                : "Create an account to keep your analyses, insights and progress in one place."}
            </p>
          </div>
          {authError && <div className="error">{authError}</div>}
          <form onSubmit={loginOrSignup}>
            {authMode === "signup" && (
              <Field label="Full name">
                <input
                  autoFocus
                  value={authForm.full_name}
                  onChange={(e) =>
                    setAuthForm({ ...authForm, full_name: e.target.value })
                  }
                  placeholder="Your name"
                />
              </Field>
            )}
            <Field label="Email">
              <input
                type="email"
                required
                value={authForm.email}
                onChange={(e) =>
                  setAuthForm({ ...authForm, email: e.target.value })
                }
                placeholder="you@example.com"
              />
            </Field>
            <Field label="Password">
              <input
                type="password"
                required
                minLength="8"
                value={authForm.password}
                onChange={(e) =>
                  setAuthForm({ ...authForm, password: e.target.value })
                }
                placeholder="At least 8 characters"
              />
            </Field>
            <button className="primary-btn" type="submit">
              {authMode === "login" ? "Sign in" : "Create account"}
            </button>
          </form>
          <button
            className="link-btn"
            onClick={() => {
              setAuthMode(authMode === "login" ? "signup" : "login");
              setAuthError("");
            }}
          >
            {authMode === "login"
              ? "New here? Create an account"
              : "Already have an account? Sign in"}
          </button>
        </div>
        <p className="auth-foot">
          Your analysis history is stored with your account on this application.
        </p>
      </div>
    );
  }

  if (screen === "dashboard") {
    return (
      <div className="shell">
        <Topbar
          user={user}
          onDashboard={goDashboard}
          onAnalyze={() => setScreen("analyze")}
          onHistory={() => setScreen("history")}
          onLogout={logout}
          active="dashboard"
        />
        <main className="dashboard">
          <div className="welcome">
            <div>
              <p className="eyebrow">YOUR WORKSPACE</p>
              <h1>
                Good to see you, {user?.full_name?.split(" ")[0] || "there"}.
              </h1>
              <p>
                Track your failure analyses and jump back into a domain whenever
                you're ready.
              </p>
            </div>
            <button
              className="primary-btn compact"
              onClick={() => setScreen("analyze")}
            >
              + New analysis
            </button>
          </div>
          <div className="stat-grid">
            <Stat
              title="Total analyses"
              value={dashboard?.total_analyses || 0}
              detail="Across all domains"
            />
            <Stat
              title="Domains explored"
              value={dashboard?.domain_breakdown?.length || 0}
              detail="Student, Software, Jobs, Projects"
            />
            <Stat
              title="Avg. predicted probability"
              value={
                dashboard?.average_probability == null
                  ? "—"
                  : `${(dashboard.average_probability * 100).toFixed(1)}%`
              }
              detail="Across recorded predictions"
            />
            <Stat
              title="This workspace"
              value={domainCount}
              detail="Saved analysis records"
            />
          </div>
          <div className="dashboard-grid">
            <section className="panel">
              <div className="panel-head">
                <div>
                  <p className="eyebrow">ACTIVITY</p>
                  <h2>Recent analyses</h2>
                </div>
                <button
                  className="text-btn"
                  onClick={() => setScreen("history")}
                >
                  View all
                </button>
              </div>
              {dashboard?.recent_analyses?.length ? (
                dashboard.recent_analyses
                  .slice(0, 6)
                  .map((item) => <HistoryRow key={item.id} item={item} />)
              ) : (
                <Empty text="No analyses yet. Run your first analysis to build your personal history." />
              )}
            </section>
            <section className="panel">
              <div className="panel-head">
                <div>
                  <p className="eyebrow">YOUR DOMAINS</p>
                  <h2>Analysis breakdown</h2>
                </div>
              </div>
              {dashboard?.domain_breakdown?.length ? (
                dashboard.domain_breakdown.map((item) => {
                  const pct = dashboard.total_analyses
                    ? (item.count / dashboard.total_analyses) * 100
                    : 0;
                  return (
                    <div className="domain-row" key={item.domain}>
                      <div>
                        <strong>{item.domain}</strong>
                        <span>
                          {item.count} analysis{item.count !== 1 ? "es" : ""}
                        </span>
                      </div>
                      <div className="bar">
                        <i style={{ width: `${pct}%` }} />
                      </div>
                    </div>
                  );
                })
              ) : (
                <Empty text="Your domain activity will appear here." />
              )}
            </section>
          </div>
        </main>
      </div>
    );
  }

  if (screen === "history") {
    return (
      <div className="shell">
        <Topbar
          user={user}
          onDashboard={goDashboard}
          onAnalyze={() => setScreen("analyze")}
          onHistory={() => setScreen("history")}
          onLogout={logout}
          active="history"
        />
        <main className="dashboard">
          <div className="page-heading">
            <p className="eyebrow">PERSONAL HISTORY</p>
            <h1>Your analyses</h1>
            <p>
              Every completed analysis is associated with your account so you
              can review your work later.
            </p>
          </div>
          <section className="panel history-panel">
            {history.length ? (
              history.map((item) => (
                <HistoryRow key={item.id} item={item} detailed />
              ))
            ) : (
              <Empty text="No saved analyses yet." />
            )}
          </section>
        </main>
      </div>
    );
  }

  return (
    <div className="shell">
      <Topbar
        user={user}
        onDashboard={goDashboard}
        onAnalyze={() => setScreen("analyze")}
        onHistory={() => setScreen("history")}
        onLogout={logout}
        active="analyze"
      />
      {error && <div className="error global-error">{error}</div>}
      <main className="analysis-page">
        <div className="page-heading">
          <div>
            <p className="eyebrow">NEW ANALYSIS</p>
            <h1>Failure analysis</h1>
            <p>
              Choose a domain, enter the case details, and explore model-based
              risk and intervention scenarios.
            </p>
          </div>
          <span className="user-chip">{user?.full_name}</span>
        </div>
        <div className="analysis-layout">
          <section className="panel form-panel">
            <div className="panel-head">
              <div>
                <p className="eyebrow">CASE INPUT</p>
                <h2>Failure domain</h2>
              </div>
            </div>
            <select
              value={domain}
              onChange={(e) => {
                setDomain(e.target.value);
                resetResults();
              }}
            >
              <option>Student</option>
              <option>Software</option>
              <option>Jobs</option>
              <option>Projects</option>
            </select>
            <div className="form-grid">
              {domain === "Student"
                ? renderStudent()
                : domain === "Software"
                  ? renderSoftware()
                  : domain === "Jobs"
                    ? renderJobs()
                    : renderProjects()}
            </div>
            <button
              className="primary-btn"
              onClick={analyze}
              disabled={loading}
            >
              {loading ? "Analyzing…" : "Analyze failure"}
            </button>
          </section>

          <section className="panel result-panel">
            <div className="panel-head">
              <div>
                <p className="eyebrow">MODEL OUTPUT</p>
                <h2>Prediction</h2>
              </div>
            </div>
            {!results.prediction ? (
              <Empty text="Your prediction and class probabilities will appear here after analysis." />
            ) : (
              <>
                <div className="prediction-hero">
                  <span>Predicted outcome</span>
                  <strong>{results.prediction.failure_type}</strong>
                  <b>{(probability || 0).toFixed(2)}%</b>
                  <small>model probability</small>
                </div>
                <div className="prob-list">
                  {Object.entries(
                    results.prediction.class_probabilities || {},
                  ).map(([label, value]) => (
                    <div className="probability" key={label}>
                      <span>{label}</span>
                      <strong>{(Number(value) * 100).toFixed(2)}%</strong>
                    </div>
                  ))}
                </div>
                <div className="result-section">
                  <h3>Recommendations</h3>
                  <ul>
                    {(results.recommendation?.recommendations || []).map(
                      (x, i) => (
                        <li key={i}>{x}</li>
                      ),
                    )}
                  </ul>
                </div>
                <div className="result-section">
                  <h3>Improvement actions</h3>
                  <ul>
                    {(results.recommendation?.improvement_actions || []).map(
                      (x, i) => (
                        <li key={i}>{x}</li>
                      ),
                    )}
                  </ul>
                </div>
              </>
            )}
          </section>

          <section className="panel">
            <div className="panel-head">
              <div>
                <p className="eyebrow">INTERVENTION</p>
                <h2>Counterfactual prevention</h2>
              </div>
            </div>
            <p>
              Test feasible, domain-constrained changes that may reduce the
              model-predicted risk or change the predicted outcome.
            </p>
            <button
              className="secondary-btn"
              onClick={generateCounterfactual}
              disabled={!results.prediction || loading}
            >
              Generate scenarios
            </button>
            {!results.prediction && (
              <p className="muted">Run Failure Analysis first.</p>
            )}
            {results.counterfactual && (
              <div className="results">
                <div className="callout">
                  <strong>{results.counterfactual.analysis_message}</strong>
                </div>
                <h3>Target prediction</h3>
                <p>
                  {results.counterfactual.desired_prediction ||
                    "Alternative outcome"}
                </p>
                <h3>Profile guidance</h3>
                <p>
                  Profile:{" "}
                  {results.counterfactual.profile_analysis?.profile_id ?? "N/A"}
                </p>
                <p>
                  Prioritized features:{" "}
                  {(
                    results.counterfactual.prioritized_features_used || []
                  ).join(", ") || "None"}
                </p>
                <h3>Recommended change</h3>
                {results.counterfactual.recommended_changes &&
                Object.keys(results.counterfactual.recommended_changes)
                  .length ? (
                  <div className="result-box">
                    <code>
                      {JSON.stringify(
                        results.counterfactual.recommended_changes,
                      )}
                    </code>
                    {(results.counterfactual.best_successful_counterfactual ||
                      results.counterfactual.best_risk_reduction_only) && (
                      <p>
                        Risk reduction:{" "}
                        {(
                          Number(
                            (
                              results.counterfactual
                                .best_successful_counterfactual ||
                              results.counterfactual.best_risk_reduction_only
                            ).risk_reduction || 0,
                          ) * 100
                        ).toFixed(2)}{" "}
                        percentage points
                      </p>
                    )}
                  </div>
                ) : (
                  <p>No beneficial feasible intervention found.</p>
                )}
                <div className="mini-stats">
                  <span>
                    <b>
                      {results.counterfactual.feasible_candidate_count || 0}
                    </b>{" "}
                    feasible candidates
                  </span>
                  <span>
                    <b>
                      {results.counterfactual.successful_counterfactual_count ||
                        0}
                    </b>{" "}
                    successful transitions
                  </span>
                </div>
              </div>
            )}
          </section>

          <section className="panel">
            <div className="panel-head">
              <div>
                <p className="eyebrow">SCENARIO TESTING</p>
                <h2>What-if simulation</h2>
              </div>
            </div>
            <p>
              Change one important numeric feature and test the model again.
            </p>
            <Field label={getWhatIfLabel()}>
              <input
                type="number"
                value={whatIfValue}
                onChange={(e) => setWhatIfValue(e.target.value)}
                placeholder="Enter new value"
              />
            </Field>
            <button
              className="secondary-btn"
              onClick={runWhatIf}
              disabled={loading}
            >
              Run what-if
            </button>
            {results.whatIf && (
              <div className="results">
                <div className="compare">
                  <div>
                    <span>Original</span>
                    <strong>
                      {results.whatIf.original_prediction?.failure_type}
                    </strong>
                    <small>
                      {(
                        Number(
                          results.whatIf.original_prediction?.probability || 0,
                        ) * 100
                      ).toFixed(2)}
                      %
                    </small>
                  </div>
                  <div className="arrow">→</div>
                  <div>
                    <span>New</span>
                    <strong>
                      {results.whatIf.new_prediction?.failure_type}
                    </strong>
                    <small>
                      {(
                        Number(
                          results.whatIf.new_prediction?.probability || 0,
                        ) * 100
                      ).toFixed(2)}
                      %
                    </small>
                  </div>
                </div>
                <p>
                  Probability change:{" "}
                  <strong>
                    {(
                      Number(results.whatIf.probability_change || 0) * 100
                    ).toFixed(2)}
                    %
                  </strong>
                </p>
                <p>
                  Prediction changed:{" "}
                  <strong>
                    {results.whatIf.prediction_changed ? "Yes" : "No"}
                  </strong>
                </p>
              </div>
            )}
          </section>
        </div>
      </main>
    </div>
  );
}

function Field({ label, children }) {
  return (
    <label className="field">
      <span>{label}</span>
      {children}
    </label>
  );
}

function Topbar({ user, onDashboard, onAnalyze, onHistory, onLogout, active }) {
  return (
    <header className="topbar">
      <button className="brand-btn" onClick={onDashboard}>
        <span className="brand-mark small">AI</span>
        <span>
          <strong>Failure Intelligence</strong>
          <small>Decision support</small>
        </span>
      </button>
      <nav>
        <button
          className={active === "dashboard" ? "active" : ""}
          onClick={onDashboard}
        >
          Dashboard
        </button>
        <button
          className={active === "analyze" ? "active" : ""}
          onClick={onAnalyze}
        >
          New analysis
        </button>
        <button
          className={active === "history" ? "active" : ""}
          onClick={onHistory}
        >
          History
        </button>
      </nav>
      <div className="account">
        <span>{user?.full_name}</span>
        <button onClick={onLogout}>Log out</button>
      </div>
    </header>
  );
}

function Stat({ title, value, detail }) {
  return (
    <div className="stat-card">
      <span>{title}</span>
      <strong>{value}</strong>
      <small>{detail}</small>
    </div>
  );
}

function HistoryRow({ item, detailed = false }) {
  return (
    <div className={`history-row ${detailed ? "detailed" : ""}`}>
      <div className="history-icon">{item.domain.slice(0, 1)}</div>
      <div className="history-main">
        <strong>{item.domain}</strong>
        <span>{item.prediction || "Analysis completed"}</span>
        {detailed && (
          <small>{new Date(item.created_at).toLocaleString()}</small>
        )}
      </div>
      <div className="history-risk">
        <strong>
          {item.probability == null
            ? "—"
            : `${(item.probability * 100).toFixed(1)}%`}
        </strong>
        <small>
          {detailed
            ? new Date(item.created_at).toLocaleDateString()
            : "predicted probability"}
        </small>
      </div>
    </div>
  );
}

function Empty({ text }) {
  return (
    <div className="empty">
      <span>◎</span>
      <p>{text}</p>
    </div>
  );
}

export default App;
