import { useEffect, useMemo, useState } from "react";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

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
  const [historyFilter, setHistoryFilter] = useState("All");
  const [selectedAnalysis, setSelectedAnalysis] = useState(null);
  const [historyLoading, setHistoryLoading] = useState(false);
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
  const [whatIfFeature, setWhatIfFeature] = useState("absences");
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

  const getWhatIfOptions = () => {
    const options = {
      Student: [
        {
          key: "absences",
          label: "Absences",
          type: "number",
          min: 0,
          max: 93,
          step: 1,
        },
        {
          key: "studytime",
          label: "Study Time",
          type: "select",
          values: [1, 2, 3, 4],
        },
      ],
      Software: [
        { key: "pr", label: "Priority", type: "text" },
        { key: "cl", label: "Complexity", type: "text" },
        { key: "rp", label: "Risk", type: "text" },
        { key: "os", label: "Operating System", type: "text" },
        { key: "bs", label: "Bug Size", type: "text" },
        { key: "bsr", label: "Bug Severity", type: "text" },
      ],
      Jobs: [
        {
          key: "skills_match_score",
          label: "Skills Match Score",
          type: "number",
          min: 0,
          max: 100,
          step: 1,
        },
        {
          key: "project_count",
          label: "Project Count",
          type: "number",
          min: 0,
          max: 100,
          step: 1,
        },
        {
          key: "resume_length",
          label: "Resume Length",
          type: "number",
          min: 0,
          max: 10000,
          step: 1,
        },
        {
          key: "github_activity",
          label: "GitHub Activity",
          type: "number",
          min: 0,
          max: 100,
          step: 1,
        },
      ],
      Projects: [
        {
          key: "Project_Cost",
          label: "Project Cost",
          type: "number",
          min: 0,
          step: 1,
        },
        {
          key: "Project_Benefit",
          label: "Project Benefit",
          type: "number",
          min: 0,
          step: 1,
        },
        {
          key: "Completion",
          label: "Completion %",
          type: "number",
          min: 0,
          max: 100,
          step: 1,
        },
        { key: "Complexity", label: "Complexity", type: "text" },
        { key: "Phase", label: "Phase", type: "text" },
      ],
    };
    return options[domain] || [];
  };

  const getCurrentDomainValue = (key, selectedDomain = domain) => {
    if (selectedDomain === "Student") return student[key];
    if (selectedDomain === "Software") return software[key];
    if (selectedDomain === "Jobs") return jobs[key];
    return projects[key];
  };

  const getWhatIfConfig = () =>
    getWhatIfOptions().find((option) => option.key === whatIfFeature) ||
    getWhatIfOptions()[0];

  const resetWhatIf = (nextDomain = domain) => {
    const options = {
      Student: ["absences", "studytime"],
      Software: ["pr", "cl", "rp", "os", "bs", "bsr"],
      Jobs: [
        "skills_match_score",
        "project_count",
        "resume_length",
        "github_activity",
      ],
      Projects: [
        "Project_Cost",
        "Project_Benefit",
        "Completion",
        "Complexity",
        "Phase",
      ],
    };
    const nextFeature = options[nextDomain][0];
    setWhatIfFeature(nextFeature);
    setWhatIfValue(
      String(getCurrentDomainValue(nextFeature, nextDomain) ?? ""),
    );
  };

  const runWhatIf = async () => {
    const config = getWhatIfConfig();
    if (!config || whatIfValue === "") {
      setError("Please enter a value for the selected feature.");
      return;
    }
    let value = whatIfValue;
    if (config.type === "number" || config.type === "select") {
      value = Number(whatIfValue);
      if (!Number.isFinite(value)) {
        setError("Please enter a valid numeric value.");
        return;
      }
    }
    setLoading(true);
    setError("");
    try {
      const result = await api("/what-if", {
        method: "POST",
        body: JSON.stringify({
          ...getData(),
          changes: { [whatIfFeature]: value },
        }),
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
    setSelectedAnalysis(null);
    setScreen("auth");
    setAuthForm({ full_name: "", email: "", password: "" });
  };

  const openAnalysis = async (id) => {
    setHistoryLoading(true);
    setError("");
    try {
      const detail = await api(`/history/${id}`);
      setSelectedAnalysis(detail);
    } catch (err) {
      setError(err.message);
    } finally {
      setHistoryLoading(false);
    }
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

  const whatIfConfig = getWhatIfConfig();

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
          <div className="chart-grid">
            <ChartPanel
              title="Domain share"
              eyebrow="PORTFOLIO"
              description="How your saved analyses are distributed across domains."
            >
              <DonutChart
                data={dashboard?.domain_breakdown || []}
                labelKey="domain"
                valueKey="count"
              />
            </ChartPanel>
            <ChartPanel
              title="Analyses by domain"
              eyebrow="ACTIVITY"
              description="Number of completed analyses in each domain."
            >
              <BarChart
                data={dashboard?.domain_breakdown || []}
                labelKey="domain"
                valueKey="count"
              />
            </ChartPanel>
          </div>
          <div className="chart-grid">
            <ChartPanel
              title="Recent predicted probability"
              eyebrow="RISK TREND"
              description="Model probability recorded for your most recent analyses."
            >
              <LineChart
                data={(dashboard?.recent_analyses || [])
                  .slice()
                  .reverse()
                  .map((item, index) => ({ ...item, label: `#${index + 1}` }))}
                labelKey="label"
                valueKey="probability"
                percent
              />
            </ChartPanel>
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
          <div className="history-toolbar">
            <label className="filter-label">
              <span>Filter by domain</span>
              <select
                value={historyFilter}
                onChange={(e) => setHistoryFilter(e.target.value)}
              >
                <option>All</option>
                <option>Student</option>
                <option>Software</option>
                <option>Jobs</option>
                <option>Projects</option>
              </select>
            </label>
            <span className="muted">
              {
                history.filter(
                  (x) => historyFilter === "All" || x.domain === historyFilter,
                ).length
              }{" "}
              record(s)
            </span>
          </div>
          <div className="chart-grid">
            <ChartPanel
              title="History probability trend"
              eyebrow="HISTORY"
              description="Saved model probabilities for the current filter."
            >
              <LineChart
                data={history
                  .filter(
                    (x) =>
                      historyFilter === "All" || x.domain === historyFilter,
                  )
                  .slice()
                  .reverse()
                  .map((item, index) => ({ ...item, label: `#${index + 1}` }))}
                labelKey="label"
                valueKey="probability"
                percent
              />
            </ChartPanel>
            <ChartPanel
              title="History domain mix"
              eyebrow="COMPOSITION"
              description="Share of saved records in the current filter."
            >
              <DonutChart
                data={countDomains(
                  history.filter(
                    (x) =>
                      historyFilter === "All" || x.domain === historyFilter,
                  ),
                )}
                labelKey="domain"
                valueKey="count"
              />
            </ChartPanel>
          </div>
          <section className="panel history-panel">
            {history.filter(
              (x) => historyFilter === "All" || x.domain === historyFilter,
            ).length ? (
              history
                .filter(
                  (x) => historyFilter === "All" || x.domain === historyFilter,
                )
                .map((item) => (
                  <HistoryRow
                    key={item.id}
                    item={item}
                    detailed
                    onOpen={openAnalysis}
                  />
                ))
            ) : (
              <Empty
                text={
                  history.length
                    ? "No analyses match this filter."
                    : "No saved analyses yet."
                }
              />
            )}
          </section>
          {selectedAnalysis && (
            <AnalysisDetail
              analysis={selectedAnalysis}
              onClose={() => setSelectedAnalysis(null)}
            />
          )}
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
                const nextDomain = e.target.value;
                setDomain(nextDomain);
                resetResults();
                resetWhatIf(nextDomain);
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
                <div className="prob-chart">
                  <h3>Class probabilities</h3>
                  <HorizontalProbabilities
                    probabilities={results.prediction.class_probabilities || {}}
                  />
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
              Change one actionable feature and test the model again. Immutable
              features are intentionally excluded.
            </p>
            <Field label="Feature to change">
              <select
                value={whatIfFeature}
                onChange={(e) => {
                  const nextFeature = e.target.value;
                  setWhatIfFeature(nextFeature);
                  setWhatIfValue(
                    String(getCurrentDomainValue(nextFeature) ?? ""),
                  );
                  setResults((old) => ({ ...old, whatIf: null }));
                }}
              >
                {getWhatIfOptions().map((option) => (
                  <option key={option.key} value={option.key}>
                    {option.label}
                  </option>
                ))}
              </select>
            </Field>
            <Field label={`New ${whatIfConfig?.label || "value"}`}>
              {whatIfConfig?.type === "select" ? (
                <select
                  value={whatIfValue}
                  onChange={(e) => setWhatIfValue(e.target.value)}
                >
                  {whatIfConfig.values.map((value) => (
                    <option key={value} value={value}>
                      {value}
                    </option>
                  ))}
                </select>
              ) : (
                <input
                  type={whatIfConfig?.type === "number" ? "number" : "text"}
                  min={whatIfConfig?.min}
                  max={whatIfConfig?.max}
                  step={whatIfConfig?.step}
                  value={whatIfValue}
                  onChange={(e) => setWhatIfValue(e.target.value)}
                  placeholder={`Enter new ${whatIfConfig?.label?.toLowerCase() || "value"}`}
                />
              )}
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

function HistoryRow({ item, detailed = false, onOpen }) {
  return (
    <button
      className={`history-row history-row-button ${detailed ? "detailed" : ""}`}
      onClick={() => onOpen?.(item.id)}
      type="button"
    >
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
    </button>
  );
}

function AnalysisDetail({ analysis, onClose }) {
  let input = {};
  let result = {};
  try {
    input =
      typeof analysis.input_json === "string"
        ? JSON.parse(analysis.input_json)
        : analysis.input_json || {};
  } catch {
    input = {};
  }
  try {
    result =
      typeof analysis.result_json === "string"
        ? JSON.parse(analysis.result_json)
        : analysis.result_json || {};
  } catch {
    result = {};
  }
  const prediction = result.prediction || {};
  const probability =
    analysis.probability == null ? null : Number(analysis.probability) * 100;
  return (
    <div
      className="detail-overlay"
      role="dialog"
      aria-modal="true"
      aria-label="Analysis details"
    >
      <section className="detail-card">
        <div className="panel-head">
          <div>
            <p className="eyebrow">SAVED ANALYSIS #{analysis.id}</p>
            <h2>{analysis.domain}</h2>
            <p className="muted">
              {new Date(analysis.created_at).toLocaleString()}
            </p>
          </div>
          <button className="account-button" onClick={onClose} type="button">
            Close
          </button>
        </div>
        <div className="detail-summary">
          <div>
            <span>Prediction</span>
            <strong>
              {prediction.failure_type || analysis.prediction || "—"}
            </strong>
          </div>
          <div>
            <span>Probability</span>
            <strong>
              {probability == null ? "—" : `${probability.toFixed(2)}%`}
            </strong>
          </div>
        </div>
        <h3>Recorded inputs</h3>
        <pre className="detail-json">{JSON.stringify(input, null, 2)}</pre>
      </section>
    </div>
  );
}

function ChartPanel({ title, eyebrow, description, children }) {
  return (
    <section className="panel chart-panel">
      <div className="panel-head">
        <div>
          <p className="eyebrow">{eyebrow}</p>
          <h2>{title}</h2>
        </div>
      </div>
      {description && <p className="chart-description">{description}</p>}
      {children}
    </section>
  );
}
function countDomains(items) {
  const counts = {};
  items.forEach((item) => {
    counts[item.domain] = (counts[item.domain] || 0) + 1;
  });
  return Object.entries(counts).map(([domain, count]) => ({ domain, count }));
}
function DonutChart({ data, labelKey, valueKey }) {
  const total = data.reduce(
    (sum, item) => sum + Number(item[valueKey] || 0),
    0,
  );
  if (!total) return <Empty text="No chart data yet." />;
  const colors = [
    "#315efb",
    "#17a673",
    "#f59e0b",
    "#8b5cf6",
    "#ef476f",
    "#0ea5e9",
  ];
  let start = 0;
  const stops = data.map((item, index) => {
    const end = start + (Number(item[valueKey] || 0) / total) * 100;
    const stop = `${colors[index % colors.length]} ${start}% ${end}%`;
    start = end;
    return stop;
  });
  return (
    <div className="donut-wrap">
      <div
        className="donut"
        style={{ background: `conic-gradient(${stops.join(", ")})` }}
      >
        <div className="donut-hole">
          <strong>{total}</strong>
          <span>analyses</span>
        </div>
      </div>
      <div className="chart-legend">
        {data.map((item, index) => (
          <div key={item[labelKey]}>
            <i style={{ background: colors[index % colors.length] }} />
            <span>{item[labelKey]}</span>
            <b>{item[valueKey]}</b>
          </div>
        ))}
      </div>
    </div>
  );
}
function BarChart({ data, labelKey, valueKey }) {
  if (!data.length) return <Empty text="No chart data yet." />;
  const max = Math.max(...data.map((item) => Number(item[valueKey] || 0)), 1);
  return (
    <div className="bar-chart">
      {data.map((item) => (
        <div className="bar-item" key={item[labelKey]}>
          <div className="bar-label">
            <span>{item[labelKey]}</span>
            <b>{item[valueKey]}</b>
          </div>
          <div className="bar-track">
            <i
              style={{ width: `${(Number(item[valueKey] || 0) / max) * 100}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}
function LineChart({ data, labelKey, valueKey, percent = false }) {
  if (!data.length) return <Empty text="No chart data yet." />;
  const values = data.map(
    (item) => Number(item[valueKey] || 0) * (percent ? 100 : 1),
  );
  const max = Math.max(...values, 1),
    min = Math.min(...values, 0),
    width = 600,
    height = 220,
    pad = 28,
    range = max - min || 1;
  const points = values.map((value, index) => ({
    x: pad + (index * (width - pad * 2)) / Math.max(data.length - 1, 1),
    y: height - pad - ((value - min) / range) * (height - pad * 2),
  }));
  return (
    <div className="line-chart">
      <svg
        viewBox={`0 0 ${width} ${height}`}
        role="img"
        aria-label="Probability trend chart"
      >
        <line
          x1={pad}
          y1={height - pad}
          x2={width - pad}
          y2={height - pad}
          className="chart-axis"
        />
        <polyline
          points={points.map((p) => `${p.x},${p.y}`).join(" ")}
          fill="none"
          className="chart-line"
        />
        {points.map((point, index) => (
          <circle
            key={index}
            cx={point.x}
            cy={point.y}
            r="4"
            className="chart-dot"
          />
        ))}
      </svg>
      <div className="line-labels">
        {data.map((item, index) => (
          <span key={index}>{item[labelKey]}</span>
        ))}
      </div>
      <div className="line-range">
        <span>{percent ? `${max.toFixed(0)}%` : max.toFixed(0)}</span>
        <span>{percent ? `${min.toFixed(0)}%` : min.toFixed(0)}</span>
      </div>
    </div>
  );
}
function HorizontalProbabilities({ probabilities }) {
  const entries = Object.entries(probabilities);
  if (!entries.length)
    return <Empty text="No class probabilities available." />;
  const max = Math.max(...entries.map(([, value]) => Number(value)), 1);
  return (
    <div className="horizontal-probs">
      {entries.map(([label, value]) => (
        <div key={label}>
          <div className="prob-head">
            <span>{label}</span>
            <b>{(Number(value) * 100).toFixed(2)}%</b>
          </div>
          <div className="prob-track">
            <i style={{ width: `${(Number(value) / max) * 100}%` }} />
          </div>
        </div>
      ))}
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
