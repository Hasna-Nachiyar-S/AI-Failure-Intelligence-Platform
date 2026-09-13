import { useState } from "react";

const API = "http://127.0.0.1:8000";

function App() {
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

  const [prediction, setPrediction] = useState(null);

  const [recommendation, setRecommendation] = useState(null);

  const [counterfactual, setCounterfactual] = useState(null);

  const [whatIf, setWhatIf] = useState(null);

  const [whatIfValue, setWhatIfValue] = useState("");

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const updateStudent = (key, value) => {
    setStudent({
      ...student,
      [key]: value,
    });
  };

  const updateSoftware = (key, value) => {
    setSoftware({
      ...software,
      [key]: value,
    });
  };

  const updateJobs = (key, value) => {
    setJobs({
      ...jobs,
      [key]: value,
    });
  };

  const updateProjects = (key, value) => {
    setProjects({
      ...projects,
      [key]: value,
    });
  };

  const getData = () => {
    if (domain === "Student") {
      return {
        Domain: "Student",
        ...student,
      };
    }

    if (domain === "Software") {
      return {
        Domain: "Software",
        ...software,
      };
    }

    if (domain === "Jobs") {
      return {
        Domain: "Jobs",
        ...jobs,
      };
    }

    return {
      Domain: "Projects",
      ...projects,
    };
  };

  const analyze = async () => {
    setLoading(true);
    setError("");

    setPrediction(null);
    setRecommendation(null);
    setCounterfactual(null);
    setWhatIf(null);

    try {
      const data = getData();

      const response = await fetch(`${API}/recommend`, {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify(data),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.detail || "Analysis failed.");
      }

      setPrediction(result.prediction);

      setRecommendation(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const generateCounterfactual = async () => {
    setError("");

    try {
      const data = getData();

      const response = await fetch(`${API}/counterfactual`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.detail || "Counterfactual analysis failed.");
      }

      setCounterfactual(result);
    } catch (err) {
      setError(err.message);
    }
  };

  const runWhatIf = async () => {
    setError("");

    if (whatIfValue === "" || whatIfValue === null) {
      setError("Please enter a value.");

      return;
    }

    const value = Number(whatIfValue);

    if (!Number.isFinite(value)) {
      setError("Please enter a valid number.");

      return;
    }

    try {
      const data = getData();

      let changes = {};

      if (domain === "Student") {
        changes = {
          G2: value,
        };
      } else if (domain === "Jobs") {
        changes = {
          skills_match_score: value,
        };
      } else if (domain === "Projects") {
        changes = {
          Completion: value,
        };
      } else {
        changes = {
          cl: String(value),
        };
      }

      console.log("What-If data:", data);

      console.log("What-If changes:", changes);

      const response = await fetch(`${API}/what-if`, {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          ...data,
          changes: changes,
        }),
      });

      const result = await response.json();

      console.log("What-If result:", result);

      if (!response.ok) {
        throw new Error(result.detail || "What-If simulation failed.");
      }

      setWhatIf(result);
    } catch (err) {
      setError(err.message);
    }
  };

  const probability = prediction
    ? Number(prediction.probability || 0) * 100
    : null;

  const renderStudent = () => (
    <>
      <label>Absences</label>

      <input
        type="number"
        value={student.absences}
        onChange={(e) => updateStudent("absences", Number(e.target.value))}
      />

      <label>Study Time</label>

      <input
        type="number"
        min="1"
        max="4"
        value={student.studytime}
        onChange={(e) => updateStudent("studytime", Number(e.target.value))}
      />

      <label>Previous Failures</label>

      <input
        type="number"
        min="0"
        value={student.failures}
        onChange={(e) => updateStudent("failures", Number(e.target.value))}
      />

      <label>G1</label>

      <input
        type="number"
        min="0"
        max="20"
        value={student.G1}
        onChange={(e) => updateStudent("G1", Number(e.target.value))}
      />

      <label>G2</label>

      <input
        type="number"
        min="0"
        max="20"
        value={student.G2}
        onChange={(e) => updateStudent("G2", Number(e.target.value))}
      />
    </>
  );

  const renderSoftware = () => (
    <>
      <label>Priority</label>

      <input
        value={software.pr}
        onChange={(e) => updateSoftware("pr", e.target.value)}
      />

      <label>Complexity</label>

      <input
        value={software.cl}
        onChange={(e) => updateSoftware("cl", e.target.value)}
      />

      <label>Dependencies</label>

      <input
        value={software.pd}
        onChange={(e) => updateSoftware("pd", e.target.value)}
      />

      <label>Coupling</label>

      <input
        value={software.co}
        onChange={(e) => updateSoftware("co", e.target.value)}
      />

      <label>Risk</label>

      <input
        value={software.rp}
        onChange={(e) => updateSoftware("rp", e.target.value)}
      />

      <label>Operating System</label>

      <input
        value={software.os}
        onChange={(e) => updateSoftware("os", e.target.value)}
      />

      <label>Bug Size</label>

      <input
        value={software.bs}
        onChange={(e) => updateSoftware("bs", e.target.value)}
      />

      <label>Bug Severity</label>

      <input
        value={software.bsr}
        onChange={(e) => updateSoftware("bsr", e.target.value)}
      />

      <label>Reporter</label>

      <input
        value={software.re}
        onChange={(e) => updateSoftware("re", e.target.value)}
      />

      <label>Assigned To</label>

      <input
        value={software.at}
        onChange={(e) => updateSoftware("at", e.target.value)}
      />
    </>
  );

  const renderJobs = () => (
    <>
      <label>Years Experience</label>

      <input
        type="number"
        value={jobs.years_experience}
        onChange={(e) => updateJobs("years_experience", Number(e.target.value))}
      />

      <label>Skills Match Score</label>

      <input
        type="number"
        min="0"
        max="100"
        value={jobs.skills_match_score}
        onChange={(e) =>
          updateJobs("skills_match_score", Number(e.target.value))
        }
      />

      <label>Education Level</label>

      <input
        value={jobs.education_level}
        onChange={(e) => updateJobs("education_level", e.target.value)}
      />

      <label>Project Count</label>

      <input
        type="number"
        value={jobs.project_count}
        onChange={(e) => updateJobs("project_count", Number(e.target.value))}
      />

      <label>Resume Length</label>

      <input
        type="number"
        value={jobs.resume_length}
        onChange={(e) => updateJobs("resume_length", Number(e.target.value))}
      />

      <label>GitHub Activity</label>

      <input
        type="number"
        value={jobs.github_activity}
        onChange={(e) => updateJobs("github_activity", Number(e.target.value))}
      />
    </>
  );

  const renderProjects = () => (
    <>
      <label>Complexity</label>

      <input
        value={projects.Complexity}
        onChange={(e) => updateProjects("Complexity", e.target.value)}
      />

      <label>Project Type</label>

      <input
        value={projects.Project_Type}
        onChange={(e) => updateProjects("Project_Type", e.target.value)}
      />

      <label>Region</label>

      <input
        value={projects.Region}
        onChange={(e) => updateProjects("Region", e.target.value)}
      />

      <label>Department</label>

      <input
        value={projects.Department}
        onChange={(e) => updateProjects("Department", e.target.value)}
      />

      <label>Project Cost</label>

      <input
        type="number"
        value={projects.Project_Cost}
        onChange={(e) => updateProjects("Project_Cost", Number(e.target.value))}
      />

      <label>Project Benefit</label>

      <input
        type="number"
        value={projects.Project_Benefit}
        onChange={(e) =>
          updateProjects("Project_Benefit", Number(e.target.value))
        }
      />

      <label>Completion %</label>

      <input
        type="number"
        min="0"
        max="100"
        value={projects.Completion}
        onChange={(e) => updateProjects("Completion", Number(e.target.value))}
      />

      <label>Phase</label>

      <input
        value={projects.Phase}
        onChange={(e) => updateProjects("Phase", e.target.value)}
      />

      <label>Year</label>

      <input
        type="number"
        value={projects.Year}
        onChange={(e) => updateProjects("Year", Number(e.target.value))}
      />

      <label>Month</label>

      <input
        type="number"
        min="1"
        max="12"
        value={projects.Month}
        onChange={(e) => updateProjects("Month", Number(e.target.value))}
      />
    </>
  );

  const renderInputs = () => {
    if (domain === "Student") {
      return renderStudent();
    }

    if (domain === "Software") {
      return renderSoftware();
    }

    if (domain === "Jobs") {
      return renderJobs();
    }

    return renderProjects();
  };

  const getWhatIfLabel = () => {
    if (domain === "Student") {
      return "New G2";
    }

    if (domain === "Jobs") {
      return "New Skills Match Score";
    }

    if (domain === "Projects") {
      return "New Completion %";
    }

    return "New Complexity";
  };

  return (
    <div className="app">
      <header>
        <h1>AI Failure Intelligence Platform</h1>

        <p>Failure Prediction and Preventive Decision Support</p>
      </header>

      {error && <div className="error">{error}</div>}

      <main>
        {/* INPUT */}

        <section className="card">
          <h2>Failure Analysis</h2>

          <label>Failure Domain</label>

          <select
            value={domain}
            onChange={(e) => {
              setDomain(e.target.value);

              setPrediction(null);
              setRecommendation(null);
              setCounterfactual(null);
              setWhatIf(null);
              setWhatIfValue("");
            }}
          >
            <option>Student</option>

            <option>Software</option>

            <option>Jobs</option>

            <option>Projects</option>
          </select>

          {renderInputs()}

          <button onClick={analyze} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze Failure"}
          </button>
        </section>

        {/* PREDICTION */}

        <section className="card">
          <h2>Prediction</h2>

          {!prediction && (
            <p>Enter the domain inputs and analyze the failure risk.</p>
          )}

          {prediction && (
            <>
              <div className="prediction">
                <h3>{prediction.failure_type}</h3>

                <p>Probability: {(probability || 0).toFixed(2)}%</p>
              </div>

              <h3>Class Probabilities</h3>

              <div>
                {Object.entries(prediction.class_probabilities || {}).map(
                  ([label, value]) => (
                    <div className="probability" key={label}>
                      <span>{label}</span>

                      <span>{(Number(value) * 100).toFixed(2)}%</span>
                    </div>
                  ),
                )}
              </div>

              <h3>Recommendations</h3>

              <ul>
                {(recommendation?.recommendations || []).map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>

              <h3>Improvement Actions</h3>

              <ul>
                {(recommendation?.improvement_actions || []).map(
                  (item, index) => (
                    <li key={index}>{item}</li>
                  ),
                )}
              </ul>
            </>
          )}
        </section>

        {/* COUNTERFACTUAL */}

        <section className="card">
          <h2>Counterfactual Prevention</h2>

          <p>Find input changes that may change the predicted outcome.</p>

          <button onClick={generateCounterfactual}>Generate Scenarios</button>

          {counterfactual && (
            <div className="results">
              <h3>Original Prediction</h3>

              <p>{counterfactual.original_prediction?.failure_type}</p>

              <p>
                Probability:{" "}
                {(
                  Number(counterfactual.original_prediction?.probability || 0) *
                  100
                ).toFixed(2)}
                %
              </p>

              <h3>Target Prediction</h3>

              <p>
                {counterfactual.desired_prediction || "Alternative outcome"}
              </p>

              <h3>Minimum Effective Change</h3>

              {counterfactual.minimum_effective_change ? (
                <div className="result-box">
                  <strong>
                    {counterfactual.minimum_effective_change.feature}
                  </strong>

                  <p>
                    Change:{" "}
                    {JSON.stringify(
                      counterfactual.minimum_effective_change.changes,
                    )}
                  </p>

                  <p>
                    New Prediction:{" "}
                    {counterfactual.minimum_effective_change.prediction}
                  </p>

                  <p>
                    Probability:{" "}
                    {(
                      Number(
                        counterfactual.minimum_effective_change.probability,
                      ) * 100
                    ).toFixed(2)}
                    %
                  </p>
                </div>
              ) : (
                <p>No successful scenario found.</p>
              )}

              <h3>Highest Confidence</h3>

              {counterfactual.highest_confidence_scenario ? (
                <div className="result-box">
                  <strong>
                    {counterfactual.highest_confidence_scenario.feature}
                  </strong>

                  <p>
                    Change:{" "}
                    {JSON.stringify(
                      counterfactual.highest_confidence_scenario.changes,
                    )}
                  </p>

                  <p>
                    Prediction:{" "}
                    {counterfactual.highest_confidence_scenario.prediction}
                  </p>

                  <p>
                    Probability:{" "}
                    {(
                      Number(
                        counterfactual.highest_confidence_scenario.probability,
                      ) * 100
                    ).toFixed(2)}
                    %
                  </p>
                </div>
              ) : (
                <p>No high-confidence scenario.</p>
              )}
            </div>
          )}
        </section>

        {/* WHAT IF */}

        {/* WHAT IF */}

        <section className="card">
          <h2>What-If Simulation</h2>

          <p>Change one important numeric feature and test the model again.</p>

          <label>{getWhatIfLabel()}</label>

          <input
            type="number"
            value={whatIfValue}
            onChange={(e) => setWhatIfValue(e.target.value)}
            placeholder="Enter new value"
          />

          <button onClick={runWhatIf}>Run What-If</button>

          {whatIf && (
            <div className="results">
              <h3>Tested Change</h3>

              <p>{JSON.stringify(whatIf.changes)}</p>

              <h3>Original</h3>

              <p>{whatIf.original_prediction?.failure_type}</p>

              <p>
                Probability:{" "}
                {(
                  Number(whatIf.original_prediction?.probability || 0) * 100
                ).toFixed(2)}
                %
              </p>

              <h3>New</h3>

              <p>{whatIf.new_prediction?.failure_type}</p>

              <p>
                Probability:{" "}
                {(
                  Number(whatIf.new_prediction?.probability || 0) * 100
                ).toFixed(2)}
                %
              </p>

              <h3>Probability Change</h3>

              <p>
                {(Number(whatIf.probability_change || 0) * 100).toFixed(2)}%
              </p>

              <h3>Prediction Changed</h3>

              <p>{whatIf.prediction_changed ? "Yes" : "No"}</p>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
