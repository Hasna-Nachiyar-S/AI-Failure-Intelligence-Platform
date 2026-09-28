AI Failure Intelligence Platform - Dashboard Charts Update

Replace these two files in your project:

1. frontend/src/App.jsx
2. frontend/src/App.css

No new npm packages are required. Charts are implemented with React + CSS + inline SVG.

After replacing the files:

1. Save both files.
2. Restart Vite if needed: npm run dev
3. Refresh http://localhost:5173

Features added:

- Dashboard domain-share donut chart
- Dashboard analyses-by-domain bar chart
- Dashboard recent predicted-probability line chart
- History probability trend chart
- History domain-mix donut chart
- Class-probability bars on analysis results
- Correct parsing of saved input/result JSON in History detail
- Existing What-If actionable-feature behavior is preserved
