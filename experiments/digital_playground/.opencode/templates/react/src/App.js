import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>{{PROJECT_NAME}}</h1>
        <p>Built with React and Guardian Framework</p>
        <div className="guardian-info">
          <h2>Guardian Workflow</h2>
          <p>This project uses the Guardian Framework for AI-assisted development:</p>
          <ol>
            <li><strong>Plan:</strong> Architectural planning and requirements</li>
            <li><strong>Build:</strong> Implementation with TDD approach</li>
            <li><strong>Guardian:</strong> Anomaly detection and review</li>
            <li><strong>Ops:</strong> Configuration and model management</li>
          </ol>
        </div>
      </header>
    </div>
  );
}

export default App;