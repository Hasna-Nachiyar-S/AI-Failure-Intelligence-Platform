import { useEffect, useState } from "react";
import DomainFields from "./components/DomainFields";
import { DOMAINS, WHAT_IF_OPTIONS } from "./config/domains";
import { api } from "./lib/api";

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
  const [domainData, setDomainData] = useState({
    Student: { absences: 10, studytime: 3, failures: 0, G1: 12, G2: 12 },
    Software: {
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
    },
    Jobs: {
      years_experience: 2,
      skills_match_score: 70,
      education_level: "Bachelor",
      project_count: 3,
      resume_length: 500,
      github_activity: 10,
    },
    Projects: {
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
    },
  });
  const [results, setResults] = useState(emptyResults());
  const [whatIfFeature, setWhatIfFeature] = useState("absences");
  const [whatIfValue, setWhatIfValue] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

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

  const getData = () => ({ Domain: domain, ...domainData[domain] });

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

  const getCurrentDomainValue = (key, selectedDomain = domain) =>
    domainData[selectedDomain]?.[key];

  const whatIfOptions = WHAT_IF_OPTIONS[domain] || [];
  const whatIfConfig =
    whatIfOptions.find((option) => option.key === whatIfFeature) ||
    whatIfOptions[0];

  const updateAuthField = (field, value) =>
    setAuthForm((old) => ({ ...old, [field]: value }));

  const resetWhatIf = (nextDomain = domain) => {
    const nextFeature = (WHAT_IF_OPTIONS[nextDomain] || [])[0]?.key;
    setWhatIfFeature(nextFeature || "");
    setWhatIfValue(
      String(getCurrentDomainValue(nextFeature, nextDomain) ?? ""),
    );
  };

  const runWhatIf = async () => {
    const config = whatIfConfig;
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

  const domainValues = domainData[domain];
  const updateDomainField = (key, value) =>
    setDomainData((old) => ({
      ...old,
      [domain]: { ...old[domain], [key]: value },
    }));

  if (screen === "loading") {
    return <div className="loading-screen">Loading your workspace…</div>;
  }

  if (screen === "auth") {
    return (
      <div className="auth-page">
        <div className="auth-brand">
          <span className="brand-mark">AI</span>
          <span>
            <strong>Failure Intelligence</strong>
            <small>Decision support</small>
          </span>
        </div>
        <section className="auth-card">
          <div className="auth-copy">
            <p className="eyebrow">AI FAILURE INTELLIGENCE PLATFORM</p>
            <h1>
              {authMode === "login" ? "Welcome back" : "Create your account"}
            </h1>
            <p>Sign in to access your personal analysis workspace.</p>
          </div>
          {authError && <div className="error">{authError}</div>}
          <form onSubmit={loginOrSignup}>
            {authMode === "signup" && (
              <Field label="Full name">
                <input
                  autoComplete="name"
                  value={authForm.full_name}
                  onChange={(e) => updateAuthField("full_name", e.target.value)}
                  required
                  minLength={2}
                />
              </Field>
            )}
            <Field label="Email">
              <input
                type="email"
                autoComplete="email"
                value={authForm.email}
                onChange={(e) => updateAuthField("email", e.target.value)}
                required
              />
            </Field>
            <Field label="Password">
              <input
                type="password"
                autoComplete={
                  authMode === "login" ? "current-password" : "new-password"
                }
                value={authForm.password}
                onChange={(e) => updateAuthField("password", e.target.value)}
                required
                minLength={8}
              />
            </Field>
            <button className="primary-btn" type="submit">
              {authMode === "login" ? "Sign in" : "Create account"}
            </button>
          </form>
          <p className="auth-foot">
            {authMode === "login"
              ? "New to the platform?"
              : "Already have an account?"}{" "}
            <button
              className="text-btn"
              type="button"
              onClick={() => {
                setAuthMode(authMode === "login" ? "signup" : "login");
                setAuthError("");
              }}
            >
              {authMode === "login" ? "Create an account" : "Sign in"}
            </button>
          </p>
        </section>
      </div>
    );
  }

  if (screen === "dashboard") {
    const breakdown = DOMAINS.map((name) => ({
      domain: name,
      count:
        dashboard?.domain_breakdown?.find((item) => item.domain === name)
          ?.count || 0,
    }));
    const trend = [...(dashboard?.recent_analyses || [])]
      .reverse()
      .map((item) => ({
        label: new Date(item.created_at).toLocaleDateString(),
        probability: Number(item.probability || 0),
      }));
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
        {error && <div className="error global-error">{error}</div>}
        <main className="dashboard">
          <div className="welcome">
            <div>
              <p className="eyebrow">PERSONAL WORKSPACE</p>
              <h1>Welcome, {user?.full_name}</h1>
              <p>
                Monitor your analyses and explore failure patterns across all
                four domains.
              </p>
            </div>
            <button
              className="primary-btn compact"
              onClick={() => setScreen("analyze")}
            >
              New analysis
            </button>
          </div>
          <div className="stat-grid">
            <Stat
              title="Total analyses"
              value={dashboard?.total_analyses ?? 0}
              detail="Saved to your account"
            />
            <Stat
              title="Domains explored"
              value={breakdown.filter((item) => item.count > 0).length}
              detail="Out of four domains"
            />
            <Stat
              title="Average probability"
              value={
                dashboard?.average_probability == null
                  ? "—"
                  : `${(dashboard.average_probability * 100).toFixed(1)}%`
              }
              detail="Across saved predictions"
            />
            <Stat
              title="Recent records"
              value={dashboard?.recent_analyses?.length ?? 0}
              detail="Latest 10 analyses"
            />
          </div>
          <div className="dashboard-grid">
            <ChartPanel
              eyebrow="DOMAIN DISTRIBUTION"
              title="Analyses by domain"
            >
              <DonutChart data={breakdown} labelKey="domain" valueKey="count" />
            </ChartPanel>
            <ChartPanel
              eyebrow="RECENT ACTIVITY"
              title="Predicted probability trend"
              description="Model probability for the predicted class in your latest analyses."
            >
              <LineChart
                data={trend}
                labelKey="label"
                valueKey="probability"
                percent
              />
            </ChartPanel>
            <ChartPanel
              eyebrow="DOMAIN COMPARISON"
              title="Analysis volume comparison"
            >
              <BarChart data={breakdown} labelKey="domain" valueKey="count" />
            </ChartPanel>
            <section className="panel history-panel">
              <div className="panel-head">
                <div>
                  <p className="eyebrow">LATEST RECORDS</p>
                  <h2>Recent analyses</h2>
                </div>
                <button
                  className="text-btn"
                  onClick={() => setScreen("history")}
                >
                  View history
                </button>
              </div>
              {(dashboard?.recent_analyses || []).length ? (
                dashboard.recent_analyses
                  .slice(0, 5)
                  .map((item) => (
                    <HistoryRow
                      key={item.id}
                      item={item}
                      onOpen={openAnalysis}
                    />
                  ))
              ) : (
                <Empty text="No analyses have been saved yet." />
              )}
            </section>
          </div>
        </main>
        {selectedAnalysis && (
          <AnalysisDetail
            analysis={selectedAnalysis}
            onClose={() => setSelectedAnalysis(null)}
          />
        )}
      </div>
    );
  }

  if (screen === "history") {
    const filteredHistory =
      historyFilter === "All"
        ? history
        : history.filter((item) => item.domain === historyFilter);
    const ordered = [...history].reverse();
    const trend = ordered.map((item) => ({
      label: new Date(item.created_at).toLocaleDateString(),
      probability: Number(item.probability || 0),
    }));
    const comparison = DOMAINS.map((name) => {
      const rows = history.filter(
        (item) => item.domain === name && item.probability != null,
      );
      return {
        domain: name,
        average: rows.length
          ? rows.reduce((sum, item) => sum + Number(item.probability), 0) /
            rows.length
          : 0,
      };
    });
    const domainMix = DOMAINS.map((name) => ({
      domain: name,
      count: history.filter((item) => item.domain === name).length,
    }));
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
        {error && <div className="error global-error">{error}</div>}
        <main className="dashboard">
          <div className="welcome">
            <div>
              <p className="eyebrow">SAVED WORK</p>
              <h1>Analysis history</h1>
              <p>
                Review previous predictions and compare activity across domains.
              </p>
            </div>
          </div>
          <div className="dashboard-grid">
            <ChartPanel
              eyebrow="HISTORICAL ANALYTICS"
              title="Predicted probability over time"
            >
              <LineChart
                data={trend}
                labelKey="label"
                valueKey="probability"
                percent
              />
            </ChartPanel>
            <ChartPanel
              eyebrow="DOMAIN MIX"
              title="Historical domain distribution"
            >
              <DonutChart data={domainMix} labelKey="domain" valueKey="count" />
            </ChartPanel>
            <ChartPanel
              eyebrow="FAILURE COMPARISON"
              title="Average predicted probability by domain"
              description="Descriptive averages from saved predictions; not a model-performance score."
            >
              <BarChart
                data={comparison}
                labelKey="domain"
                valueKey="average"
              />
            </ChartPanel>
          </div>
          <div className="history-toolbar">
            <label className="filter-label">
              <span>Filter by domain</span>
              <select
                value={historyFilter}
                onChange={(e) => setHistoryFilter(e.target.value)}
              >
                <option>All</option>
                {DOMAINS.map((name) => (
                  <option key={name}>{name}</option>
                ))}
              </select>
            </label>
            <span className="muted">{filteredHistory.length} records</span>
          </div>
          <section className="panel history-panel">
            {filteredHistory.length ? (
              filteredHistory.map((item) => (
                <HistoryRow
                  key={item.id}
                  item={item}
                  detailed
                  onOpen={openAnalysis}
                />
              ))
            ) : (
              <Empty text="No saved analyses match this filter." />
            )}
          </section>
          {historyLoading && (
            <p className="loading-note">Loading analysis details…</p>
          )}
        </main>
        {selectedAnalysis && (
          <AnalysisDetail
            analysis={selectedAnalysis}
            onClose={() => setSelectedAnalysis(null)}
          />
        )}
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
              {DOMAINS.map((name) => (
                <option key={name}>{name}</option>
              ))}
            </select>
            <div className="form-grid">
              <DomainFields
                domain={domain}
                values={domainValues}
                onChange={updateDomainField}
              />
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
                {whatIfOptions.map((option) => (
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
    const savedInput = analysis.input ?? analysis.input_json;
    input =
      typeof savedInput === "string"
        ? JSON.parse(savedInput)
        : savedInput || {};
  } catch {
    input = {};
  }
  try {
    const savedResult = analysis.result ?? analysis.result_json;
    result =
      typeof savedResult === "string"
        ? JSON.parse(savedResult)
        : savedResult || {};
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
        {Object.keys(prediction.class_probabilities || result.probability || {})
          .length > 0 && (
          <div className="prob-chart">
            <h3>Saved class probabilities</h3>
            <HorizontalProbabilities
              probabilities={
                prediction.class_probabilities || result.probability || {}
              }
            />
          </div>
        )}
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
